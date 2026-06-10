# 第 2 章：程序與執行緒

## 章節內容

| 小節 | 檔案 | 說明 |
|------|------|------|
| 2.1 程序與 fork() | [2.1-fork.md](2.1-fork.md) | 程序概念、fork 建立子程序、wait |
| 2.2 執行緒 | [2.2-threads.md](2.2-threads.md) | pthread、執行緒建立與 join |
| 2.3 競態條件與 Mutex | [2.3-mutex.md](2.3-mutex.md) | Race Condition、mutex 保護臨界區間 |

## 學習目標

- 理解程序與執行緒的本質差異
- 能夠使用 `fork()` 建立子程序並控制執行流程
- 能夠使用 `pthread` 建立多執行緒程式
- 辨識並解決競態條件
- 熟練使用 Mutex 保護共享資源

## 範例程式碼

- `fork_demo.c` — fork 父子程序協作
- `thread_demo.c` — pthread 多執行緒範例
- `mutex_demo.c` — Mutex 保護共享計數器

### 編譯方式

```bash
gcc -o fork_demo fork_demo.c && ./fork_demo
gcc -pthread -o thread_demo thread_demo.c && ./thread_demo
gcc -pthread -o mutex_demo mutex_demo.c && ./mutex_demo
```
