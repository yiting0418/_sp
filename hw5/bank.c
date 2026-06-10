/*
 * bank.c - 銀行存提款執行緒模擬
 *
 * 情境：同一帳戶，兩個執行緒同時進行 100000 次存款與 100000 次提款
 *       使用 Mutex 保護臨界區，確保最終餘額正確
 *
 * 編譯：gcc -o bank bank.c -lpthread
 * 執行：./bank
 */

#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>

#define TIMES        100000   /* 存/提款次數 */
#define AMOUNT       100      /* 每次金額    */
#define INIT_BALANCE 1000000  /* 初始餘額    */

/* ── 共享資料 ── */
long long   balance = INIT_BALANCE;
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

/* ── 統計 ── */
long long total_deposit  = 0;
long long total_withdraw = 0;

/* ────────────────────────────────────────
 * 存款執行緒
 * ──────────────────────────────────────── */
void *deposit(void *arg)
{
    for (int i = 0; i < TIMES; i++) {
        pthread_mutex_lock(&lock);      /* 進入臨界區 */
        balance      += AMOUNT;
        total_deposit += AMOUNT;
        pthread_mutex_unlock(&lock);    /* 離開臨界區 */
    }
    printf("[存款執行緒] 完成 %d 次存款，每次 %d 元\n", TIMES, AMOUNT);
    return NULL;
}

/* ────────────────────────────────────────
 * 提款執行緒
 * ──────────────────────────────────────── */
void *withdraw(void *arg)
{
    for (int i = 0; i < TIMES; i++) {
        pthread_mutex_lock(&lock);
        balance       -= AMOUNT;
        total_withdraw += AMOUNT;
        pthread_mutex_unlock(&lock);
    }
    printf("[提款執行緒] 完成 %d 次提款，每次 %d 元\n", TIMES, AMOUNT);
    return NULL;
}

/* ────────────────────────────────────────
 * 主程式
 * ──────────────────────────────────────── */
int main(void)
{
    pthread_t t_dep, t_wit;

    printf("========================================\n");
    printf("     銀行帳戶並發存提款模擬\n");
    printf("========================================\n");
    printf("初始餘額  : %lld 元\n", balance);
    printf("存款次數  : %d 次 × %d 元 = %d 元\n", TIMES, AMOUNT, TIMES * AMOUNT);
    printf("提款次數  : %d 次 × %d 元 = %d 元\n", TIMES, AMOUNT, TIMES * AMOUNT);
    printf("預期餘額  : %d 元（淨變動為零）\n", INIT_BALANCE);
    printf("----------------------------------------\n");

    /* 建立兩個執行緒，同時執行存款與提款 */
    pthread_create(&t_dep, NULL, deposit,  NULL);
    pthread_create(&t_wit, NULL, withdraw, NULL);

    /* 等待兩個執行緒結束 */
    pthread_join(t_dep, NULL);
    pthread_join(t_wit, NULL);

    printf("----------------------------------------\n");
    printf("總存款金額 : +%lld 元\n", total_deposit);
    printf("總提款金額 : -%lld 元\n", total_withdraw);
    printf("最終餘額   : %lld 元\n", balance);

    if (balance == INIT_BALANCE) {
        printf("結果       : ✓ 正確！Mutex 成功保護了共享資源\n");
    } else {
        printf("結果       : ✗ 錯誤！餘額偏差 %lld 元\n",
               balance - INIT_BALANCE);
    }

    pthread_mutex_destroy(&lock);
    return 0;
}
