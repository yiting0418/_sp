/*
 * producer_consumer.c - 生產者消費者問題模擬
 *
 * 情境：生產者將商品放入有限緩衝區，消費者從緩衝區取出商品
 *       - 緩衝區滿時，生產者等待
 *       - 緩衝區空時，消費者等待
 *       使用 Mutex + Condition Variable 實作
 *
 * 編譯：gcc -o producer_consumer producer_consumer.c -lpthread
 * 執行：./producer_consumer
 */

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define BUFFER_SIZE    5    /* 緩衝區容量   */
#define PRODUCE_COUNT  20   /* 總生產數量   */
#define NUM_PRODUCERS  2    /* 生產者執行緒數 */
#define NUM_CONSUMERS  3    /* 消費者執行緒數 */

/* ── 環狀緩衝區 ── */
int buffer[BUFFER_SIZE];
int head  = 0;   /* 消費端指標 */
int tail  = 0;   /* 生產端指標 */
int count = 0;   /* 目前緩衝區內物品數 */

/* ── 同步工具 ── */
pthread_mutex_t mutex       = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t  cond_not_full  = PTHREAD_COND_INITIALIZER; /* 緩衝區不滿 */
pthread_cond_t  cond_not_empty = PTHREAD_COND_INITIALIZER; /* 緩衝區不空 */

/* ── 全域計數器（受 mutex 保護） ── */
int total_produced = 0;
int total_consumed = 0;
int next_item      = 1;  /* 下一個要生產的物品編號 */

/* ────────────────────────────────────────
 * 輔助：印出緩衝區狀態
 * ──────────────────────────────────────── */
static void print_buffer(void)
{
    printf("  [緩衝區 ");
    for (int i = 0; i < BUFFER_SIZE; i++) {
        if (i < count) printf("%3d", buffer[(head + i) % BUFFER_SIZE]);
        else           printf("  _");
    }
    printf(" ] (%d/%d)\n", count, BUFFER_SIZE);
}

/* ────────────────────────────────────────
 * 生產者執行緒
 * ──────────────────────────────────────── */
void *producer(void *arg)
{
    int id = *(int *)arg;

    while (1) {
        pthread_mutex_lock(&mutex);

        /* 確認是否還有生產任務 */
        if (total_produced >= PRODUCE_COUNT) {
            pthread_mutex_unlock(&mutex);
            break;
        }

        /* 緩衝區已滿：等待消費者取走商品 */
        while (count == BUFFER_SIZE) {
            printf("[生產者 %d] 緩衝區已滿，進入等待...\n", id);
            pthread_cond_wait(&cond_not_full, &mutex);

            /* 等待後再次確認是否還有任務 */
            if (total_produced >= PRODUCE_COUNT) {
                pthread_mutex_unlock(&mutex);
                return NULL;
            }
        }

        /* 生產物品，放入緩衝區 */
        int item         = next_item++;
        buffer[tail]     = item;
        tail             = (tail + 1) % BUFFER_SIZE;
        count++;
        total_produced++;

        printf("[生產者 %d] ➕ 生產 item-%02d ", id, item);
        print_buffer();

        /* 通知消費者緩衝區有新物品 */
        pthread_cond_signal(&cond_not_empty);
        pthread_mutex_unlock(&mutex);

        usleep(80000 + rand() % 120000);  /* 模擬生產耗時 */
    }
    return NULL;
}

/* ────────────────────────────────────────
 * 消費者執行緒
 * ──────────────────────────────────────── */
void *consumer(void *arg)
{
    int id = *(int *)arg;

    while (1) {
        pthread_mutex_lock(&mutex);

        /* 所有物品已被消費完畢 */
        if (total_consumed >= PRODUCE_COUNT) {
            pthread_mutex_unlock(&mutex);
            break;
        }

        /* 緩衝區為空：等待生產者放入商品 */
        while (count == 0) {
            /* 若生產已全部完成且緩衝區空，退出 */
            if (total_produced >= PRODUCE_COUNT && count == 0) {
                pthread_mutex_unlock(&mutex);
                return NULL;
            }
            printf("[消費者 %d] 緩衝區已空，進入等待...\n", id);
            pthread_cond_wait(&cond_not_empty, &mutex);
        }

        /* 確認還有消費任務 */
        if (total_consumed >= PRODUCE_COUNT) {
            pthread_mutex_unlock(&mutex);
            break;
        }

        /* 從緩衝區取出物品 */
        int item = buffer[head];
        head     = (head + 1) % BUFFER_SIZE;
        count--;
        total_consumed++;

        printf("[消費者 %d] ➖ 消費 item-%02d ", id, item);
        print_buffer();

        /* 通知生產者緩衝區有空位 */
        pthread_cond_signal(&cond_not_full);
        pthread_mutex_unlock(&mutex);

        usleep(150000 + rand() % 100000); /* 模擬消費耗時 */
    }
    return NULL;
}

/* ────────────────────────────────────────
 * 主程式
 * ──────────────────────────────────────── */
int main(void)
{
    pthread_t producers[NUM_PRODUCERS];
    pthread_t consumers[NUM_CONSUMERS];
    int       prod_ids[NUM_PRODUCERS];
    int       cons_ids[NUM_CONSUMERS];

    printf("========================================\n");
    printf("     生產者消費者問題模擬\n");
    printf("========================================\n");
    printf("緩衝區大小 : %d\n", BUFFER_SIZE);
    printf("生產者數量 : %d 個執行緒\n", NUM_PRODUCERS);
    printf("消費者數量 : %d 個執行緒\n", NUM_CONSUMERS);
    printf("總生產數量 : %d 件\n", PRODUCE_COUNT);
    printf("----------------------------------------\n");

    /* 啟動生產者 */
    for (int i = 0; i < NUM_PRODUCERS; i++) {
        prod_ids[i] = i + 1;
        pthread_create(&producers[i], NULL, producer, &prod_ids[i]);
    }

    /* 啟動消費者 */
    for (int i = 0; i < NUM_CONSUMERS; i++) {
        cons_ids[i] = i + 1;
        pthread_create(&consumers[i], NULL, consumer, &cons_ids[i]);
    }

    /* 等待所有執行緒結束 */
    for (int i = 0; i < NUM_PRODUCERS; i++) pthread_join(producers[i], NULL);

    /* 喚醒可能仍在等待的消費者，讓它們檢查結束條件 */
    pthread_cond_broadcast(&cond_not_empty);

    for (int i = 0; i < NUM_CONSUMERS; i++) pthread_join(consumers[i], NULL);

    printf("----------------------------------------\n");
    printf("總計生產 : %d 件\n", total_produced);
    printf("總計消費 : %d 件\n", total_consumed);
    printf("結果     : %s\n",
           (total_produced == PRODUCE_COUNT && total_consumed == PRODUCE_COUNT)
           ? "✓ 生產消費平衡，無資料遺失！"
           : "✗ 數量不一致，有錯誤！");

    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&cond_not_full);
    pthread_cond_destroy(&cond_not_empty);
    return 0;
}
