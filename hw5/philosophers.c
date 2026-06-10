/*
 * philosophers.c - 哲學家用餐問題模擬（無死鎖版本）
 *
 * 情境：5 位哲學家圍坐圓桌，每人左右各一支叉子（共 5 支）
 *       哲學家交替進行「思考」與「用餐」
 *       用餐前需同時拿起左右兩支叉子
 *
 * 死鎖預防策略：Tanenbaum 的狀態機解法
 *   - 使用集中式狀態管理（THINKING / HUNGRY / EATING）
 *   - 只有左右鄰居皆非 EATING 狀態，才允許本人進入 EATING
 *   - 避免了「每人只拿一支叉子並互相等待」的循環等待
 *
 * 編譯：gcc -o philosophers philosophers.c -lpthread
 * 執行：./philosophers
 */

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>

#define N        5    /* 哲學家人數（= 叉子數） */
#define ROUNDS   3    /* 每位哲學家用餐次數     */

/* 哲學家狀態 */
#define THINKING 0
#define HUNGRY   1
#define EATING   2

/* 左右鄰居的索引（環狀） */
#define LEFT(i)  (((i) + N - 1) % N)
#define RIGHT(i) (((i) + 1) % N)

/* 哲學家名字 */
const char *names[N] = {
    "亞里斯多德", "蘇格拉底", "柏拉圖", "笛卡兒", "康德"
};

/* ── 共享狀態 ── */
int             state[N];    /* 每位哲學家的目前狀態 */
pthread_mutex_t mutex;       /* 保護 state 陣列的全域鎖 */
pthread_cond_t  cond[N];     /* 每位哲學家專屬的條件變數 */

/* ── 統計 ── */
int meals[N];                /* 各哲學家已用餐次數 */

/* ────────────────────────────────────────
 * 輔助：印出目前桌面狀態
 * ──────────────────────────────────────── */
static void print_table(void)
{
    const char *sym[] = {"💭", "😋", "🍝"};
    printf("  桌面狀態: ");
    for (int i = 0; i < N; i++) {
        printf("[%s %s] ", names[i], sym[state[i]]);
    }
    printf("\n");
}

/* ────────────────────────────────────────
 * 核心函式：嘗試讓哲學家 i 進入 EATING 狀態
 *   條件：i 必須是 HUNGRY，且左右鄰居皆非 EATING
 * ──────────────────────────────────────── */
static void try_eat(int i)
{
    if (state[i] == HUNGRY &&
        state[LEFT(i)]  != EATING &&
        state[RIGHT(i)] != EATING)
    {
        state[i] = EATING;
        pthread_cond_signal(&cond[i]);  /* 通知哲學家 i 可以吃了 */
    }
}

/* ────────────────────────────────────────
 * 拿起叉子（等待直到可以用餐）
 * ──────────────────────────────────────── */
static void take_forks(int i)
{
    pthread_mutex_lock(&mutex);

    state[i] = HUNGRY;
    printf("[%s] 飢餓，嘗試拿叉子...\n", names[i]);
    print_table();

    try_eat(i);  /* 嘗試進入 EATING，若不行則在 cond[i] 上等待 */

    while (state[i] != EATING) {
        pthread_cond_wait(&cond[i], &mutex);
    }

    meals[i]++;
    printf("[%s] ✅ 開始用餐（第 %d 餐）\n", names[i], meals[i]);
    print_table();

    pthread_mutex_unlock(&mutex);
}

/* ────────────────────────────────────────
 * 放下叉子（並嘗試喚醒左右鄰居）
 * ──────────────────────────────────────── */
static void put_forks(int i)
{
    pthread_mutex_lock(&mutex);

    state[i] = THINKING;
    printf("[%s] 放下叉子，繼續思考\n", names[i]);

    /* 通知左右鄰居：叉子空出來了，嘗試讓他們吃 */
    try_eat(LEFT(i));
    try_eat(RIGHT(i));

    pthread_mutex_unlock(&mutex);
}

/* ────────────────────────────────────────
 * 哲學家執行緒
 * ──────────────────────────────────────── */
void *philosopher(void *arg)
{
    int i = *(int *)arg;

    for (int r = 0; r < ROUNDS; r++) {
        /* ── 思考 ── */
        printf("[%s] 💭 正在思考...\n", names[i]);
        usleep((rand() % 4 + 1) * 100000);  /* 思考 100~400ms */

        /* ── 用餐 ── */
        take_forks(i);
        usleep((rand() % 3 + 1) * 100000);  /* 用餐 100~300ms */
        put_forks(i);
    }

    printf("[%s] 🏁 完成所有 %d 餐，離開餐桌\n", names[i], ROUNDS);
    return NULL;
}

/* ────────────────────────────────────────
 * 主程式
 * ──────────────────────────────────────── */
int main(void)
{
    pthread_t threads[N];
    int       ids[N];

    srand((unsigned)time(NULL));

    printf("========================================\n");
    printf("     哲學家用餐問題模擬（無死鎖）\n");
    printf("========================================\n");
    printf("哲學家人數 : %d 位\n", N);
    printf("叉子數量   : %d 支\n", N);
    printf("每人用餐   : %d 次\n", ROUNDS);
    printf("死鎖預防   : Tanenbaum 狀態機法\n");
    printf("----------------------------------------\n\n");

    /* 初始化 */
    pthread_mutex_init(&mutex, NULL);
    for (int i = 0; i < N; i++) {
        state[i] = THINKING;
        meals[i] = 0;
        pthread_cond_init(&cond[i], NULL);
    }

    /* 建立哲學家執行緒 */
    for (int i = 0; i < N; i++) {
        ids[i] = i;
        pthread_create(&threads[i], NULL, philosopher, &ids[i]);
    }

    /* 等待所有哲學家用餐完畢 */
    for (int i = 0; i < N; i++) {
        pthread_join(threads[i], NULL);
    }

    /* 印出統計 */
    printf("\n========================================\n");
    printf("           用餐統計\n");
    printf("========================================\n");
    int ok = 1;
    for (int i = 0; i < N; i++) {
        printf("  %-12s: %d 餐 %s\n",
               names[i], meals[i],
               meals[i] == ROUNDS ? "✓" : "✗ 異常！");
        if (meals[i] != ROUNDS) ok = 0;
    }
    printf("----------------------------------------\n");
    printf("結果 : %s\n",
           ok ? "✓ 所有哲學家都吃飽了，無死鎖！"
              : "✗ 有哲學家未完成用餐，發生錯誤！");

    /* 清理 */
    pthread_mutex_destroy(&mutex);
    for (int i = 0; i < N; i++) {
        pthread_cond_destroy(&cond[i]);
    }
    return 0;
}
