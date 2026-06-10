# 第 8 章：網路程式設計

## 章節內容

| 小節 | 檔案 | 說明 |
|------|------|------|
| 8.1 Socket 基礎 | [8.1-sockets.md](8.1-sockets.md) | Socket 概念、TCP/UDP 區別、位址結構 |
| 8.2 TCP Server/Client | [8.2-tcp-server.md](8.2-tcp-server.md) | 完整 Echo Server 實作、select 模型 |

## 學習目標

- 理解 Socket 抽象與 TCP/UDP 的差異
- 掌握 Socket API：socket、bind、listen、accept、connect
- 實作 TCP 客戶端與伺服器
- 理解 I/O 多工（select/poll/epoll）
- 了解阻塞與非阻塞 I/O 的區別

## Socket API 一覽

| 系統呼叫 | Server | Client | 說明 |
|---------|--------|--------|------|
| `socket()` | ✅ | ✅ | 建立通訊端點 |
| `bind()` | ✅ | ❌（選擇性） | 綁定位址與埠號 |
| `listen()` | ✅ | ❌ | 監聽連線 |
| `accept()` | ✅ | ❌ | 接受連線請求 |
| `connect()` | ❌ | ✅ | 連接到伺服器 |
| `send()`/`recv()` | ✅ | ✅ | 收發資料 |
| `close()` | ✅ | ✅ | 關閉連線 |

## 範例程式碼

- `tcp_server.c` — TCP Echo 伺服器
- `tcp_client.c` — TCP 客戶端

### 編譯方式

```bash
gcc -o tcp_server tcp_server.c && ./tcp_server 8888
gcc -o tcp_client tcp_client.c && ./tcp_client 127.0.0.1 8888
```
