# 系統程式 -- 筆記、習題與專題

---
### 習題 1 — p0：P0 編譯器 + 虛擬機（while 語法）

> [程式碼](https://github.com/yiting0418/_sp/tree/master/p0)

- **關鍵檔案：** `compiler.c`（Lexer + Parser + Code Generator + VM 合一）、
- **核心機制：**
  - 詞法分析 + 遞迴下降語法分析
  - 四元組中介碼（quadruples）：JMP、JMP_F、CALL、RET_VAL 等
  - 堆疊框架（Frame）管理區域變數、返回位址、參數傳遞，支援遞迴函式
  - while 迴圈採用 Backpatching 技術
- **範例程式：** `add.p0`、`fact.p0`、`if.p0`、`prime.p0`、`while.p0`

---
### 習題 2 — code：台文（Tai-bûn）程式語言

> [網站](https://yiting0418.github.io/_sp/code/website/index.html)
> [程式碼](https://github.com/yiting0418/_sp/tree/master/code)

- **關鍵檔案：** `lexer.py` / `parser.py` / `compiler.py` / `vm.py` / `taibu.py`
- **核心機制：**
  - 雙模式：`python taibu.py run <file>`（檔案執行）或 `python taibu.py repl`（REPL 互動）
  - 強型別、一級函式、詞法作用域、參考計數 GC
  - Bytecode 指令：PUSH, LOAD, STORE, ADD, SUB, MUL, DIV, CALL, PRINT, HALT
  - 支援 `taibu.py {run, compile, exec, dis, repl}` 五種子命令
- **額外工具：** VS Code 語法擴充套件（`vscode-taibu/`）、官方網站（`website/index.html`）

---
### 習題 3 — aios_final：AIOS（AI 原生作業系統）

> [原始碼 ZIP](aios_final/aios_enhanced_runtime.zip)

- **核心架構：**
  - L5 Syscall 核心：`agent_spawn`、`mem_store`、`mem_recall`、`tool_call` 等
  - 三層安全機制：ABAC 屬性權限控管、Intent Whitelist、異常偵測 + BehaviorGuard
  - 三級記憶體：Working Memory、Episodic Memory、Semantic Memory
  - 工具註冊與沙箱（Tool Registry / Sandbox）
  - 桌面儀表板（FastAPI / Axum + HTML/CSS/JS）
- **Python 版：** 277 項測試，Pydantic 資料模型
- **Rust 版：** 47 項整合測試，AXUM HTTP 伺服器

---
### 習題 4 — spbook：系統程式教材

> [連結](https://yiting0418.github.io/_sp/spbook/spbook.html)
> [file](https://github.com/yiting0418/_sp/tree/master/spbook)

- **路徑：** 9 章 Markdown，含 `spbook.html` 整書 HTML 渲染
- **章節內容：**

  | 章節 | 主題 |
  |------|------|
  | ch01 | 作業系統基礎 — OS 角色、系統呼叫、中斷 |
  | ch02 | 行程與執行緒 — fork、threads、mutex 同步 |
  | ch03 | 記憶體管理 — 記憶體佈局、動態分配、常見錯誤 |
  | ch04 | 編譯器 — 編譯流程概論、詞法分析、語法分析 |
  | ch05 | Shell — Mini Shell 實作 |
  | ch06 | 檔案 I/O — 檔案描述子、檔案系統 |
  | ch07 | 行程間通訊 — Pipe、共享記憶體 |
  | ch08 | 網路程式設計 — Socket、TCP 伺服器 |
  | ch09 | 結論 |

---
### 習題 5 — hw5：執行緒同步（thread / race condition / mutex / deadlock）

> [GitHub 連結](https://github.com/yiting0418/_sp/tree/master/hw5)

- **關鍵檔案：** `bank.c` / `producer_consumer.c` / `philosophers.c`
- **語言：** C（POSIX pthreads）
- **程式列表：**

  | 程式 | 主題 | 關鍵技術 |
  |------|------|----------|
  | `bank.c` | 銀行交易模擬 | mutex 保護共享變數，對比有/無同步的執行結果 |
  | `producer_consumer.c` | 生產者消費者 | mutex + condition variable，環形緩衝區（size=5） |
  | `philosophers.c` | 哲學家聚餐 | Tanenbaum 集中式狀態機，mutex + 5 個 condition variable |

- **概念涵蓋：** Race condition、Critical Section、Mutex、Deadlock

---
### 習題 6 — hw6：行程與檔案操作（fork / execvp / dup2 / pipe / open / read / write）

> [課程網頁](https://yiting0418.github.io/_sp/hw6.html)

本習題為 Linux 系統程式實作，涵蓋行程管理與檔案 I/O 的核心系統呼叫。

- **語言：** C（POSIX）
- **主題與範例：**

  | 主題 | 說明 |
  |------|------|
  | 檔案描述符（fd） | stdin=0、stdout=1、stderr=2，所有 I/O 統一透過整數 fd 操作 |
  | `open()` / `read()` / `write()` / `close()` | 檔案開啟、讀寫、關閉的基本系統呼叫 |
  | `fork()` | 複製行程，parent 回傳 child PID，child 回傳 0 |
  | `execvp()` | 取代行程映像，執行新程式（自動搜尋 PATH） |
  | `dup2()` | 複製 fd，實作 I/O 重新導向（`>` / `<` 的底層） |
  | `pipe()` | 建立行程間通道，搭配 `dup2()` 實作管線（`\|`） |
  | 迷你 Shell | 綜合運用 fork + execvp + dup2 + open 實作簡易 Shell |

- **範例程式碼位置：** `hw6/` 目錄，含 `fd_demo.c`、`file_rw.c`、`redirect_out.c`、`redirect_in.c`、`pipe_demo.c`、`minishell.c`

## 編譯與執行

```bash
# 習題 1 — p0 (C)
cd p0 && gcc -o compiler compiler.c && ./compiler

# 習題 2 — 台文語言 (Python)
cd code && python taibu.py run examples/hello.taibu  # 檔案模式
cd code && python taibu.py repl                       # REPL 模式

# 習題 3 — AIOS Python 版
cd aios_final/aios_enhanced_runtime && pip install -e . && aios run

# 習題 3 — AIOS Rust 版
cd aios_final/aios-rs && cargo run -- run

# 習題 4 — spbook (文件)
# 使用瀏覽器開啟 spbook/spbook.html

# 習題 5 — hw5 (C, pthread)
cd hw5 && gcc -o bank bank.c -lpthread && ./bank
cd hw5 && gcc -o producer_consumer producer_consumer.c -lpthread && ./producer_consumer
cd hw5 && gcc -o philosophers philosophers.c -lpthread && ./philosophers

# 習題 6 — hw6 (C, POSIX)
cd hw6 && gcc -o fd_demo fd_demo.c && ./fd_demo
cd hw6 && gcc -o file_rw file_rw.c && ./file_rw
cd hw6 && gcc -o redirect_out redirect_out.c && ./redirect_out
cd hw6 && gcc -o redirect_in redirect_in.c && ./redirect_in
cd hw6 && gcc -o pipe_demo pipe_demo.c && ./pipe_demo
cd hw6 && gcc -o minishell minishell.c && ./minishell
```
