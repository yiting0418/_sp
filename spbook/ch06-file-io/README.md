# 第 6 章：檔案系統與 I/O

## 章節內容

| 小節 | 檔案 | 說明 |
|------|------|------|
| 6.1 檔案描述符與基本 I/O | [6.1-file-descriptors.md](6.1-file-descriptors.md) | open/read/write/close、檔案描述符 |
| 6.2 檔案系統與 inode | [6.2-file-systems.md](6.2-file-systems.md) | inode 結構、目錄操作、硬連結與軟連結 |

## 學習目標

- 理解檔案描述符（File Descriptor）的概念
- 使用 POSIX 系統呼叫進行檔案讀寫
- 了解 inode 與 VFS 的架構
- 區分硬連結與符號連結的差異
- 實作目錄遍歷

## 範例程式碼

- `filedemo.c` — 檔案讀寫操作
- `lsimple.c` — 簡易目錄列表

### 編譯方式

```bash
gcc -o filedemo filedemo.c && ./filedemo
gcc -o lsimple lsimple.c && ./lsimple
```
