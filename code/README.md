# 台文程式語言 Tâi-bûn-lang v1.0

> 全球首個以臺灣閩南語台羅拼音為語料庫的程式語言

---

## 語言目標

**台文（Tâi-bûn）** 是以台灣閩南語羅馬字拼音方案（台羅）為語法關鍵字的通用程式語言：

1. **語言保存** — 讓台語成為真正能「跑程式」的語言
2. **教育普及** — 讓母語者以台語思維學習程式設計
3. **完整功能** — 變數、條件、迴圈、函式、陣列全支援
4. **雙執行模式** — 直譯器（即時執行）＋ 編譯器（TaiVM 位元組碼）

---

## 語言設計決策

| 面向 | 選擇 | 說明 |
|------|------|------|
| **型態系統** | 強型態 | 型態在執行期檢查，不隱性轉換數值 |
| **執行方式** | 直譯 + 編譯 | 直譯器直接走訪 AST；編譯器產生 TaiVM 位元組碼 |
| **目標碼架構** | 堆疊機（Stack VM） | 簡單、可攜，無需暫存器分配 |
| **垃圾蒐集** | 引用計數（Reference Counting） | Python 物件天然支援 |
| **作用域** | 靜態（Lexical Scope） | 函式捕捉定義時的環境 |
| **函式** | 一等公民（First-class） | 可存入變數、傳遞引數 |

---

## 資料型態

| 台語名稱 | 說明 | 範例 |
|---------|------|------|
| `tsò-jî` 整數 | 64-bit 有號整數 | `42`, `-7` |
| `sió-siàu` 小數 | 64-bit IEEE 754 | `3.14` |
| `jī-bîn` 字面 | UTF-8 字串 | `"台灣"` |
| `pîng-iōng` 平用 | 布林值 | `si̍t-tsāi`, `bô-si̍t` |
| `bîn-tsōo` 民族 | 動態陣列 | `[1, 2, 3]` |
| `bô` 虛空 | 空值 | `bô` |

---

## 關鍵字對照表

| 台羅關鍵字 | 中文 | 英文 |
|-----------|------|------|
| `nā-sī` | 如果 | `if` |
| `nā-bô` | 否則 | `else` |
| `tng` | 當……時 | `while` |
| `se̍h-lin-long` | 迴圈 | `for` |
| `kè-sio̍k` | 繼續 | `continue` |
| `tn̄g-khì` | 斷開 | `break` |
| `hàm-sò` | 函式 | `function` |
| `tò-tńg` | 回傳 | `return` |
| `tòng-tsò` | 定義變數 | `let` |
| `kóng` | 輸出 | `print` |
| `mn̄g` | 輸入 | `input` |
| `pênn-pênn` | 等於 | `==` |
| `bô-pênn` | 不等於 | `!=` |
| `khah-sè` | 小於 | `<` |
| `khah-tuā` | 大於 | `>` |
| `bô-khah-tuā` | 小於等於 | `<=` |
| `bô-khah-sè` | 大於等於 | `>=` |
| `kah` | 且 | `and` |
| `ia̍h-sī` | 或 | `or` |
| `m̄-sī` | 非 | `not` |
| `si̍t-tsāi` | 真 | `true` |
| `bô-si̍t` | 假 | `false` |

---

## 快速範例

```taibu
// 費波那契（遞迴函式）
hàm-sò fibonacci(n) {
    nā-sī n bô-khah-tuā 1 {
        tò-tńg n ;
    }
    tò-tńg fibonacci(n - 1) + fibonacci(n - 2) ;
}

se̍h-lin-long i = 0 kàu 9 {
    kóng "F(" + i + ") = " + fibonacci(i) ;
}
```

```taibu
// 質數篩選（continue + if/else）
hàm-sò sī-tsit-sòo(n) {
    nā-sī n khah-sè 2 { tò-tńg bô-si̍t ; }
    se̍h-lin-long i = 2 kàu n - 1 {
        nā-sī n % i pênn-pênn 0 { tò-tńg bô-si̍t ; }
    }
    tò-tńg si̍t-tsāi ;
}
```

---

## 安裝與執行

### 需求
- Python 3.9+（無需第三方套件）

### 直譯模式（樹狀走訪直譯器）
```bash
python taibu.py run examples/hello.taibu
```

### 編譯模式（產生 TaiVM 位元組碼）
```bash
python taibu.py compile examples/hello.taibu -o hello.tbc
python taibu.py exec hello.tbc
```

### 反組譯（查看位元組碼）
```bash
python taibu.py dis examples/factorial.taibu
```

### 互動模式（REPL）
```bash
python taibu.py repl
```

---

## 專案結構

```
tailang/
├── README.md           — 本文件
├── grammar.ebnf        — EBNF 語法定義
├── taibu.py            — 主程式入口
├── lexer.py            — 詞法分析器
├── parser.py           — 語法分析器（遞迴下降）
├── ast_nodes.py        — AST 節點定義
├── interpreter.py      — 直譯器（樹狀走訪）
├── compiler.py         — 位元組碼編譯器
├── vm.py               — TaiVM 堆疊虛擬機
├── website/
│   └── index.html      — 官方網站
└── examples/
    ├── hello.taibu
    ├── fibonacci.taibu
    ├── factorial.taibu
    └── control_flow.taibu
```

---

## 版權

MIT License © 2026 Tâi-bûn-lang Project

> 「台語毋是死語，是活跳跳的語言！」
