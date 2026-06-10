# 並發程式設計核心概念

> 深入理解 Thread、Race Condition、Mutex 與 Deadlock，並附三個 C 語言實作範例

---

## 目錄

1. Thread（執行緒）
2. Race Condition（競態條件）
3. Mutex（互斥鎖）
4. Deadlock（死鎖）
5. 概念關係總覽
6. 實作範例一：銀行存提款模擬
7. 實作範例二：生產者消費者問題
8. 實作範例三：哲學家用餐問題
9. 編譯與執行

---

<a id="thread"></a>

## Thread

### 什麼是 Thread？

Thread（執行緒）是作業系統能夠獨立排程的最小執行單元。一個 Process（行程）可以包含多個 Thread，這些 Thread **共享同一塊記憶體空間**，但各自擁有獨立的：

- **Stack（堆疊）**：儲存函式呼叫與區域變數
- **Program Counter**：記錄目前執行到哪一行指令
- **Register**：CPU 暫存器狀態

### Process vs Thread

| 比較項目 | Process | Thread |
|--------|---------|--------|
| 記憶體空間 | 獨立 | 共享（同一 Process） |
| 建立成本 | 較高 | 較低 |
| 通訊方式 | IPC（複雜） | 直接讀寫共享變數（簡單但危險） |
| 崩潰影響 | 不影響其他 Process | 可能拖垮整個 Process |

### 為什麼需要 Thread？

- **提升效能**：在多核 CPU 上平行執行任務
- **提高響應性**：背景執行耗時任務，不阻塞主介面
- **資源共享**：多個任務高效共用同一份資料

---

<a id="race-condition"></a>

## Race Condition

### 什麼是 Race Condition？

Race Condition（競態條件）發生在**兩個以上的 Thread 同時存取共享資源**，且最終結果取決於 Thread 的執行順序。這種不確定性會導致程式出現難以重現的 Bug。

### 問題根源：非原子操作

看似一行的 `balance += amount`，實際上在 CPU 層面是三個步驟：

```
1. READ   → 從記憶體讀取 balance 的值
2. ADD    → 將值加上 amount
3. WRITE  → 將結果寫回記憶體
```

若兩個 Thread 在步驟之間互相交錯，結果就會出錯。

### 時序圖（Race Condition 示意）

```
時間 → → →
Thread A: [READ:1000] ---------> [ADD:900] [WRITE:900]
Thread B:          [READ:1000] [ADD:900] [WRITE:900]

初始餘額 1000，各提取 100，正確結果應為 800
但因為 B 在 A 寫回前就讀取，最終餘額為 900（錯誤！）
```

---

<a id="mutex"></a>

## Mutex

### 什麼是 Mutex？

Mutex（Mutual Exclusion，互斥鎖）是解決 Race Condition 的核心工具。它確保**同一時間只有一個 Thread 能進入臨界區（Critical Section）**，其他 Thread 必須等待鎖被釋放後才能繼續。

### 運作原理

```
Thread A 嘗試取得鎖 → 成功，進入臨界區
Thread B 嘗試取得鎖 → 鎖已被佔用，阻塞等待

Thread A 執行完畢，釋放鎖
Thread B 取得鎖，進入臨界區
Thread B 執行完畢，釋放鎖
```

### 關鍵 API（POSIX pthread）

```c
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

pthread_mutex_lock(&lock);    // 取得鎖（阻塞直到成功）
/* ── 臨界區 ── */
pthread_mutex_unlock(&lock);  // 釋放鎖

pthread_mutex_destroy(&lock); // 釋放資源
```

### Condition Variable（條件變數）

Mutex 只能做「互斥」，無法做「等待某個條件成立」。Condition Variable 搭配 Mutex 使用，讓 Thread 在條件不滿足時釋放鎖並進入睡眠，待條件成立後被喚醒：

```c
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;

// 等待條件（自動釋放 mutex，被喚醒後重新取得）
pthread_cond_wait(&cond, &mutex);

// 喚醒一個等待的 Thread
pthread_cond_signal(&cond);

// 喚醒所有等待的 Thread
pthread_cond_broadcast(&cond);
```

---

<a id="deadlock"></a>

## Deadlock

### 什麼是 Deadlock？

Deadlock（死鎖）發生在**兩個以上的 Thread 互相等待對方釋放資源**，導致所有相關 Thread 永遠無法繼續執行的僵局。

### 死鎖的四個必要條件（Coffman Conditions）

死鎖必須**同時滿足**以下四個條件才會發生：

| 條件 | 說明 |
|------|------|
| **互斥（Mutual Exclusion）** | 資源同一時間只能被一個 Thread 持有 |
| **持有並等待（Hold and Wait）** | Thread 持有資源的同時，等待其他資源 |
| **不可搶奪（No Preemption）** | 資源只能由持有者主動釋放，不能被強奪 |
| **循環等待（Circular Wait）** | Thread 之間形成環狀的等待鏈 |

### 如何預防 Deadlock？

只要破壞四個條件之一，死鎖就不會發生：

| 策略 | 破壞哪個條件 | 說明 |
|------|------------|------|
| 固定資源取得順序 | 循環等待 | 所有 Thread 都以相同順序取得鎖 |
| 一次取得所有資源 | 持有並等待 | 失敗則全部放棄，稍後重試 |
| 設定取得鎖的 Timeout | 不可搶奪 | 超時則主動釋放並重試 |
| 集中式狀態管理 | 循環等待 | 由仲裁者決定誰可以取得資源（哲學家問題的解法）|

---

<a id="overview"></a>

## 概念關係總覽

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   多個 Thread 同時存取共享資源                         │
│                ↓                                    │
│         Race Condition（競態條件）                    │
│                ↓  解決方法                           │
│      Mutex + Condition Variable                     │
│                ↓  使用不當                           │
│           Deadlock（死鎖）                           │
│                ↓  預防策略                           │
│      固定順序 / 集中管理 / Timeout                    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

<a id="bank"></a>

## 實作範例一：銀行存提款模擬

**檔案：`bank.c`**

### 情境

同一個帳戶（初始餘額 1,000,000 元），兩個執行緒**同時**各執行 100,000 次操作：

- 存款執行緒：每次存入 100 元，共存入 10,000,000 元
- 提款執行緒：每次提取 100 元，共提取 10,000,000 元

最終餘額應仍為 1,000,000 元。

### 核心問題

若不加鎖，`balance += amount` 不是原子操作，兩個執行緒可能同時讀取舊值再各自寫回，造成更新遺失（Lost Update），最終餘額將是錯誤的隨機值。

### 解決方式

使用 `pthread_mutex_t` 保護 `balance` 的讀寫，確保每次存取都是互斥的：

```c
pthread_mutex_lock(&lock);
balance += AMOUNT;      // 臨界區，一次只有一個執行緒能執行
pthread_mutex_unlock(&lock);
```

### 執行結果

```
========================================
     銀行帳戶並發存提款模擬
========================================
初始餘額  : 1000000 元
存款次數  : 100000 次 × 100 元 = 10000000 元
提款次數  : 100000 次 × 100 元 = 10000000 元
預期餘額  : 1000000 元（淨變動為零）
----------------------------------------
[存款執行緒] 完成 100000 次存款，每次 100 元
[提款執行緒] 完成 100000 次提款，每次 100 元
----------------------------------------
總存款金額 : +10000000 元
總提款金額 : -10000000 元
最終餘額   : 1000000 元
結果       : ✓ 正確！Mutex 成功保護了共享資源
```

---

<a id="producer-consumer"></a>

## 實作範例二：生產者消費者問題

**檔案：`producer_consumer.c`**

### 情境

- **有界緩衝區**：容量為 5 個物品的環狀陣列
- **生產者（2 個執行緒）**：持續生產物品放入緩衝區；緩衝區滿時等待
- **消費者（3 個執行緒）**：持續從緩衝區取出物品；緩衝區空時等待
- 總計生產並消費 20 件物品，最終確認無資料遺失

### 同步工具

| 工具 | 用途 |
|------|------|
| `pthread_mutex_t mutex` | 保護緩衝區的所有讀寫操作 |
| `pthread_cond_t cond_not_full` | 當緩衝區有空位時，喚醒等待中的生產者 |
| `pthread_cond_t cond_not_empty` | 當緩衝區有物品時，喚醒等待中的消費者 |

### 生產者核心邏輯

```c
pthread_mutex_lock(&mutex);

// 緩衝區已滿：釋放鎖並等待消費者取走物品
while (count == BUFFER_SIZE)
    pthread_cond_wait(&cond_not_full, &mutex);

// 放入物品
buffer[tail] = item;
tail = (tail + 1) % BUFFER_SIZE;
count++;

pthread_cond_signal(&cond_not_empty); // 通知消費者
pthread_mutex_unlock(&mutex);
```

### 消費者核心邏輯

```c
pthread_mutex_lock(&mutex);

// 緩衝區為空：釋放鎖並等待生產者放入物品
while (count == 0)
    pthread_cond_wait(&cond_not_empty, &mutex);

// 取出物品
int item = buffer[head];
head = (head + 1) % BUFFER_SIZE;
count--;

pthread_cond_signal(&cond_not_full); // 通知生產者
pthread_mutex_unlock(&mutex);
```

### 執行結果（節錄）

```
[生產者 1] ➕ 生產 item-01   [緩衝區  1  _  _  _  _ ] (1/5)
[生產者 2] ➕ 生產 item-02   [緩衝區  1  2  _  _  _ ] (2/5)
[消費者 1] ➖ 消費 item-01   [緩衝區  2  _  _  _  _ ] (1/5)
...
總計生產 : 20 件
總計消費 : 20 件
結果     : ✓ 生產消費平衡，無資料遺失！
```

---

<a id="philosophers"></a>

## 實作範例三：哲學家用餐問題

**檔案：`philosophers.c`**

### 情境

5 位哲學家圍坐圓桌，桌上有 5 支叉子（每人左右各一支）。哲學家交替進行「思考」與「用餐」，用餐前必須同時持有左右兩支叉子。

### 死鎖的危險

若每位哲學家都先拿左邊的叉子，再嘗試拿右邊的叉子：

```
哲學家 A 拿起左叉，等待右叉
哲學家 B 拿起左叉，等待右叉
...（所有人都拿著一支叉，等待另一支）
→ 循環等待，死鎖！
```

### 解決策略：Tanenbaum 狀態機法

使用集中式狀態管理取代直接搶叉子，每位哲學家有三種狀態：

| 狀態 | 說明 |
|------|------|
| `THINKING` | 正在思考，不持有叉子 |
| `HUNGRY` | 想用餐，嘗試取得叉子 |
| `EATING` | 正在用餐，持有左右兩支叉子 |

**關鍵函式 `try_eat(i)`**：只有當哲學家 `i` 為 `HUNGRY`，且左右鄰居**都不是** `EATING` 時，才讓 `i` 進入 `EATING`：

```c
void try_eat(int i) {
    if (state[i] == HUNGRY &&
        state[LEFT(i)]  != EATING &&
        state[RIGHT(i)] != EATING)
    {
        state[i] = EATING;
        pthread_cond_signal(&cond[i]); // 通知哲學家 i 可以吃了
    }
}
```

**放下叉子時**，順便嘗試讓左右鄰居進入 `EATING`：

```c
void put_forks(int i) {
    pthread_mutex_lock(&mutex);
    state[i] = THINKING;
    try_eat(LEFT(i));   // 我放下叉子，鄰居可能可以吃了
    try_eat(RIGHT(i));
    pthread_mutex_unlock(&mutex);
}
```

### 為何不會死鎖？

此方法破壞了「循環等待」條件。哲學家不直接持有叉子，而是由狀態機集中判斷誰可以用餐。不存在「我拿著一支叉子，等你放下你的叉子」的情況，因為只有在兩支叉子都確認可用時，才會一次性進入 `EATING`。

### 執行結果（節錄）

```
[蘇格拉底] 飢餓，嘗試拿叉子...
[蘇格拉底] ✅ 開始用餐（第 1 餐）
[柏拉圖  ] 飢餓，嘗試拿叉子...  ← 左鄰居在吃，進入等待
[蘇格拉底] 放下叉子，繼續思考
[柏拉圖  ] ✅ 開始用餐（第 1 餐）  ← 鄰居放下後被喚醒
...
========================================
           用餐統計
========================================
  亞里斯多德: 3 餐 ✓
  蘇格拉底  : 3 餐 ✓
  柏拉圖    : 3 餐 ✓
  笛卡兒    : 3 餐 ✓
  康德      : 3 餐 ✓
----------------------------------------
結果 : ✓ 所有哲學家都吃飽了，無死鎖！
```

---

<a id="build"></a>

## 編譯與執行

### 環境需求

- Linux / macOS（或任何支援 POSIX Thread 的系統）
- GCC 編譯器

### 編譯指令

```bash
# 銀行存提款模擬
gcc -o bank bank.c -lpthread

# 生產者消費者問題
gcc -o producer_consumer producer_consumer.c -lpthread

# 哲學家用餐問題
gcc -o philosophers philosophers.c -lpthread
```

### 執行

```bash
./bank
./producer_consumer
./philosophers
```

### 三個程式的同步機制比較

| 程式 | Mutex | Condition Variable | 解決的問題 |
|------|-------|--------------------|-----------|
| `bank.c` | ✅ 一把鎖 | ❌ | Race Condition |
| `producer_consumer.c` | ✅ 一把鎖 | ✅ 兩個（not_full / not_empty） | Race Condition + 緩衝區滿/空的等待 |
| `philosophers.c` | ✅ 一把鎖 | ✅ 五個（每位哲學家一個） | Race Condition + Deadlock 預防 |

---

## 延伸閱讀

- [POSIX Threads Programming - LLNL](https://hpc-tutorials.llnl.gov/posix/)
- *Modern Operating Systems* - Andrew S. Tanenbaum（哲學家問題的出處）
- *The Little Book of Semaphores* - Allen B. Downey（免費線上版）
- [Linux man page: pthread_mutex_lock(3)](https://man7.org/linux/man-pages/man3/pthread_mutex_lock.3p.html)
- [Linux man page: pthread_cond_wait(3)](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html)
