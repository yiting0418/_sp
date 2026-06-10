# 第 1 章：作業系統原理

## 章節內容

| 小節 | 檔案 | 說明 |
|------|------|------|
| 1.1 作業系統的角色 | [1.1-os-role.md](1.1-os-role.md) | OS 作為資源管理者與延伸機器 |
| 1.2 使用者模式與系統呼叫 | [1.2-syscall.md](1.2-syscall.md) | User/Kernel 模式切換、系統呼叫範例 |
| 1.3 中斷處理 | [1.3-interrupts.md](1.3-interrupts.md) | 硬體中斷、信號處理、中斷向量 |

## 學習目標

完成本章後，你應該能夠：

- 說明作業系統的兩個核心角色
- 區分使用者模式與核心模式的差異
- 撰寫使用系統呼叫的 C 程式
- 理解中斷機制與信號處理的關係
- 解釋為什麼系統呼叫比一般函式呼叫慢

## 範例程式碼

本章範例原始檔位於 `code/` 目錄：

- `syscall_demo.c` — 使用 `write()`、`getpid()` 系統呼叫
- `signal_demo.c` — 信號處理（SIGINT 攔截）

### 編譯方式

```bash
gcc -o syscall_demo syscall_demo.c && ./syscall_demo
gcc -o signal_demo signal_demo.c && ./signal_demo
```
