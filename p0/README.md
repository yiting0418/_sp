# p0 編譯器

## while 語法實作

### 設計原理

while 迴圈的語法為：

```
while (condition) {
    statement;
    ...
}
```

編譯器將其轉換為以下四元組（quadruples）模式：

```
        ┌─ condition 的運算碼
        │    ┌─ JMP_F：若條件為假就跳出
        │    │    ┌─ body 的運算碼
        │    │    │    ┌─ JMP：無條件跳回條件檢查
        ▼    ▼    ▼    ▼
L_cond: <cond_code>
        JMP_F cond_result L_exit
L_body: <body_code>
        JMP L_cond
L_exit: ...
```

實作上使用 **回填（Backpatching）** 技術：

1. 解析 condition 前先記錄 `cond_start = quad_count`（作為迴圈跳回目標）
2. 解析 condition 後產生 `JMP_F cond ?`，記下 `jmp_f_idx`
3. 解析 body 後產生 `JMP ?`，記下 `jmp_idx`
4. 回填：`quads[jmp_f_idx].result = quad_count`（跳出目標）
5. 回填：`quads[jmp_idx].result = cond_start`（迴圈起點）

程式碼位於 `statement()` 中的 `TK_WHILE` 分支（compiler.c 第 188~200 行），同時在 VM 中新增了 `JMP` 無條件跳轉指令的處理（compiler.c 第 291~293 行）。

### 新增項目

| 項目 | 說明 |
|------|------|
| `TK_WHILE` | 詞法分析新增 while 關鍵字 |
| while 分支 | 語法分析 `statement()` 中新增 while 處理 |
| `JMP` 指令 | 虛擬機新增無條件跳轉 |

## 函數呼叫機制

p0 的函數呼叫依賴**堆疊幀（Stack Frame）**與**四元組中間碼**協作完成。

### 整體流程

```
原始碼: result = factorial(5);

四元組:
  PARAM t8 - -          ← 1. 參數壓棧
  CALL factorial 1 t9   ← 2. 呼叫函數
  STORE t9 - result     ← 5. 結果存回

虛擬機執行:
  1. PARAM → 把參數值存入 param_stack
  2. CALL  → 建立新 Frame (sp++)，複製參數，PC 跳到函數入口
  3. FORMAL → 將 param 依序賦值給形參
  4. 執行函數體，遇到 RET_VAL 時：
     - 取得回傳值
     - 銷毀當前 Frame (sp--)
     - 將回傳值寫入 Caller 的 ret_var
     - PC 回到 CALL 的下一條指令
```

### Frame 結構

```c
typedef struct {
    char names[100][32];   // 區域變數名稱陣列
    int values[100];       // 區域變數值陣列
    int count;             // 變數數量
    int ret_pc;            // 返回地址 (CALL 下一指令)
    char ret_var[32];      // 結果要寫入 Caller 的哪個變數
    int incoming_args[10]; // 傳入的參數值
    int formal_idx;        // 參數計數器
} Frame;
```

### 遞迴支援原理

遞迴的關鍵是每次 `CALL` 都會**建立全新的 Frame**（`sp++`），因此：

- 每層呼叫有獨立的變數空間，同名變數不會互相干擾
- `RET_VAL` 時銷毀當前 Frame（`sp--`），自然回到上一層的變數環境
- 參數透過 `param_stack` 傳遞，保證 FIFO 順序

以 `factorial(5)` 為例，執行過程的堆疊變化：

```
factorial(5) → 建立 Frame[1], n=5
  factorial(4) → 建立 Frame[2], n=4
    factorial(3) → 建立 Frame[3], n=3
      factorial(2) → 建立 Frame[4], n=2
        factorial(1) → 建立 Frame[5], n=1
          n==0? 否
          factorial(0) → 建立 Frame[6], n=0
            return 1 → Frame[6] 銷毀，回傳 1
          return 1*1=1 → Frame[5] 銷毀，回傳 1
        return 2*1=2 → Frame[4] 銷毀，回傳 2
      return 3*2=6 → Frame[3] 銷毀，回傳 6
    return 4*6=24 → Frame[2] 銷毀，回傳 24
  return 5*24=120 → Frame[1] 銷毀，回傳 120
result = 120
```

### 參數傳遞

參數透過一個全域的 `param_stack` 暫存：

1. `PARAM x` → 將 `x` 的值 push 到 `param_stack`
2. `CALL func n` → 從 `param_stack` 倒序取出 n 個參數（保持順序），存入新 Frame 的 `incoming_args`
3. `FORMAL name` → 依序從 `incoming_args` 取值賦予形參

### VM 指令對照

| 指令 | 作用 |
|------|------|
| `FUNC_BEG name` | 標記函數起點（VM 執行時直接跳過） |
| `FORMAL name` | 接收參數值賦予 name |
| `PARAM val` | 將 val 暫存到參數堆疊 |
| `CALL name n ret` | 呼叫函數，n 個參數，結果存 ret |
| `RET_VAL val` | 回傳 val，銷毀當前 Frame |
| `FUNC_END name` | 標記函數終點 |

### 與 while 的比較

while 使用 `JMP_F`（條件跳轉）和 `JMP`（無條件跳轉）實現流程控制，而函數呼叫使用 `CALL`/`RET_VAL` 搭配 Frame 堆疊實現更複雜的控制流轉移與變數隔離。兩者是編譯器中控制流機制的兩個層次：前者是**區域性跳轉**，後者是**跨區域的環境切換**。
