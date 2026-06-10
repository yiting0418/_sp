# 第 7 章：行程間通訊（IPC）

## 章節內容

| 小節 | 檔案 | 說明 |
|------|------|------|
| 7.1 管道（Pipe） | [7.1-pipes.md](7.1-pipes.md) | 匿名管道、命名管道（FIFO） |
| 7.2 共享記憶體與信號量 | [7.2-shared-memory.md](7.2-shared-memory.md) | POSIX shared memory、semaphore 同步 |

## 學習目標

- 理解各種 IPC 機制的優缺點
- 使用 `pipe()` 在父子程序間傳遞資料
- 使用 `mkfifo()` 建立命名管道
- 使用 POSIX 共享記憶體進行高效率資料交換
- 使用信號量（Semaphore）同步共享記憶體存取

## IPC 機制比較

| 機制 | 方向性 | 速度 | 需要同步 | 適用場景 |
|------|--------|------|---------|---------|
| Pipe | 單向 | 快 | 內建阻塞 | 父子程序 |
| FIFO | 單向 | 快 | 內建阻塞 | 無關程序 |
| 共享記憶體 | 雙向 | 最快 | 需要 | 大量資料交換 |
| 信號量 | — | 快 | — | 同步工具 |
| 訊息佇列 | 雙向 | 中 | 內建 | 訊息傳遞 |
| Socket | 雙向 | 中 | 不需要 | 跨機器通訊 |

## 範例程式碼

- `pipe_demo.c` — 父子程序 Pipe 通訊
- `shm_demo.c` — 共享記憶體 + 信號量

### 編譯方式

```bash
gcc -o pipe_demo pipe_demo.c && ./pipe_demo
gcc -pthread -o shm_demo shm_demo.c -lrt && ./shm_demo
```
