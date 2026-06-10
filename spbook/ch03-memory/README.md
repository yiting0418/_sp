# 第 3 章：記憶體管理

## 章節內容

| 小節 | 檔案 | 說明 |
|------|------|------|
| 3.1 程序記憶體佈局 | [3.1-memory-layout.md](3.1-memory-layout.md) | Text/Data/BSS/Heap/Stack 各區段 |
| 3.2 動態記憶體管理 | [3.2-dynamic-memory.md](3.2-dynamic-memory.md) | malloc、calloc、realloc、free |
| 3.3 常見記憶體錯誤 | [3.3-memory-errors.md](3.3-memory-errors.md) | 洩漏、溢位、懸空指標 |

## 學習目標

- 繪製並解釋程序的記憶體佈局
- 理解 Stack 與 Heap 的成長方向與原因
- 安全地使用 `malloc` / `calloc` / `realloc` / `free`
- 辨識並修復常見的記憶體錯誤
- 使用 Valgrind 檢測記憶體洩漏

## 範例程式碼

- `memmap.c` — 觀察各區段記憶體位址
- `malloc_demo.c` — 動態記憶體操作
- `memerr.c` — 記憶體錯誤示範

### 編譯方式

```bash
gcc -o memmap memmap.c && ./memmap
gcc -o malloc_demo malloc_demo.c && ./malloc_demo
gcc -o memerr memerr.c && ./memerr
valgrind --leak-check=full ./memerr
```
