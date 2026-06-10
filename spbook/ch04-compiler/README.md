# 第 4 章：編譯器與直譯器

## 章節內容

| 小節 | 檔案 | 說明 |
|------|------|------|
| 4.1 編譯流程概觀 | [4.1-overview.md](4.1-overview.md) | 編譯器 vs 直譯器、GCC 四階段 |
| 4.2 詞法分析器 | [4.2-lexer.md](4.2-lexer.md) | Token 切割、實作簡易 Lexer |
| 4.3 遞迴下降語法分析器 | [4.3-parser.md](4.3-parser.md) | 算術運算式計算器 |

## 學習目標

- 區分編譯器與直譯器的差異與適用場景
- 描述 GCC 的四個編譯階段
- 實作一個簡易的詞法分析器（Lexer）
- 實作一個遞迴下降語法分析器（Parser）
- 理解抽象語法樹（AST）的概念

## 範例程式碼

- `lexer.c` — 簡易 C 語法 Tokenizer
- `parser.c` — 遞迴下降運算式計算器

### 編譯方式

```bash
gcc -o lexer lexer.c && ./lexer
gcc -o parser parser.c && ./parser
```
