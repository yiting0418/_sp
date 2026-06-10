# 結語：學習路徑與推薦資源

## 學習回顧

| # | 主題 | 關鍵技能 |
|---|------|---------|
| 1 | 作業系統原理 | 系統呼叫、中斷處理、模式切換 |
| 2 | 程序與執行緒 | fork、pthread、Mutex 同步 |
| 3 | 記憶體管理 | 記憶體佈局、malloc/free、Valgrind |
| 4 | 編譯器與直譯器 | Lexer、Parser、遞迴下降解析 |
| 5 | 綜合實作 | 迷你 Shell（fork + exec） |
| 6 | 檔案系統與 I/O | 檔案描述符、inode、硬/軟連結 |
| 7 | 行程間通訊 | Pipe、共享記憶體、信號量 |
| 8 | 網路程式設計 | Socket、TCP Server/Client |

## 推薦書籍

### 初階

**《Computer Systems: A Programmer's Perspective》**（CS:APP）
- 作者：Bryant & O'Hallaron
- 從程式員視角理解電腦系統，C 語言為基礎
- 系統程式領域最推薦的入門書

### 中階

**《Operating Systems: Three Easy Pieces》**
- 作者：Arpaci-Dusseau（[免費線上版](https://pages.cs.wisc.edu/~remzi/OSTEP/)）
- 生動易懂的 OS 教材，附大量專題實作

**《The Linux Programming Interface》**
- 作者：Michael Kerrisk
- Linux 系統程式設計聖經，1500+ 頁的完整參考

### 進階

**《Compilers: Principles, Techniques, and Tools》**（龍書）
- 作者：Aho, Lam, Sethi, Ullman
- 編譯器領域的經典之作

**《Advanced Programming in the UNIX Environment》**
- 作者：W. Richard Stevens
- Unix 系統程式設計的權威參考書

**《TCP/IP Illustrated, Volume 1》**
- 作者：W. Richard Stevens
- 網路協定的圖解聖經

## 推薦線上資源

| 資源 | 類型 | 說明 |
|------|------|------|
| [Harvard CS61](https://cs61.seas.harvard.edu/) | 課程 | Harvard 系統程式課程 |
| [MIT 6.828 / 6.S081](https://pdos.csail.mit.edu/6.828/) | 課程 | MIT 作業系統課程，實作 xv6 |
| [GNU C Library Manual](https://www.gnu.org/software/libc/manual/) | 文件 | Glibc 官方手冊 |
| [Linux man-pages](https://man7.org/linux/man-pages/) | 文件 | 系統呼叫完整參考 |
| [OSDev Wiki](https://wiki.osdev.org/) | 社群 | 自製作業系統資源 |
| [null program](https://nullprogram.com/) | 部落格 | Chris Wellons 系統程式部落格 |

## 實作專題建議（由淺入深）

1. **Shell 加強版** — 加入管線（`|`）、重定向（`>` `<`）、背景執行（`&`）
2. **自製 HTTP Server** — 用 Socket API 實作支援靜態檔案的 Web Server
3. **記憶體配置器** — 實作自己的 malloc/free，管理 Heap 區塊
4. **簡易核心模組** — 撰寫 Linux Kernel Module，掛載 /proc 檔案系統
5. **簡單的檔案系統** — 在磁碟映像上實作一個 FUSE 檔案系統
6. **自行動手寫 OS** — 從 bootloader 開始，實作一個 x86 玩具核心

> 🎯 系統程式的能力養成靠的是「動手做」。讀完書、看完範例，最重要的是親自寫一遍、改一遍、壞一遍、修一遍。每踩一個坑，你就變強了一點。
