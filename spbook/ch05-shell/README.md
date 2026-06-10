# 第 5 章：綜合實作 — 迷你 Shell

## 章節內容

| 小節 | 檔案 | 說明 |
|------|------|------|
| 5.1 迷你 Shell 實作 | [5.1-minishell.md](5.1-minishell.md) | REPL 主迴圈、fork + exec、內建命令 |

## 學習目標

- 綜合運用 fork、exec、wait、strtok 等系統程式技術
- 理解 Shell 的運作原理（REPL）
- 實作一個簡易但可用的命令列解譯器
- 實作內建命令（cd、exit）
- 為實作 Shell 內建管線（pipe）與重定向打好基礎

## 範例程式碼

- `minishell.c` — 完整迷你 Shell 實作

### 編譯方式

```bash
gcc -o minishell minishell.c && ./minishell
```
