# 金十数据 MCP 接入

流水线（`NewsDataSource` → `jin10_feed.py`）通过 **金十官方 MCP** 拉取快讯、资讯与财经日历。文档索引见 [README.md](../../README.md)。

## 1. 申请 Token

1. 打开 [https://mcp.jin10.com/app](https://mcp.jin10.com/app)
2. 登录金十账号并创建 API Token
3. 写入 `.env`：

```env
JIN10_API_TOKEN=你的token
JIN10_ENABLED=true
JIN10_KEYWORD=黄金
```

## 2. 流水线拉取内容

| MCP 工具 | 用途 | UI 来源标签 |
|----------|------|-------------|
| `list_flash` | 快讯 → 新闻头条 | 金十快讯 |
| `search_news` / `list_news` | 资讯文章 → 新闻头条 | 金十资讯 |
| `list_calendar` | 宏观日历 → 事件风险 | 金十财经日历 |
| `get_quote` | XAUUSD 实时报价 → spot 交叉校验 | — |
| `get_kline` | XAUUSD K 线 → 技术分析师 derived 摘要 | — |

本地验证：

```bash
python scripts/test_live_fetch.py
```

## 3. 数据层结构

```
jin10_mcp_client.py   # JSON-RPC / SSE 传输
jin10_feed.py         # fetch_jin10_bundle() — 快讯 + 资讯 + 日历
news.py               # NewsDataSource → ExternalFactors
```

## 4. Cursor / AI Agent 直接接 MCP

MCP 是 **给 AI 助手用的协议**；Streamlit 报告生成走的是 Python MCP 客户端，两者共用同一个 Token。

在 Cursor 中配置（见 [cursor-mcp.json.example](./cursor-mcp.json.example)）：

```json
{
  "mcpServers": {
    "jin10": {
      "url": "https://mcp.jin10.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_JIN10_API_TOKEN"
      }
    }
  }
}
```

## 5. 环境变量

| 变量 | 默认 | 说明 |
|------|------|------|
| `JIN10_API_TOKEN` | 空 | 必填 |
| `JIN10_MCP_URL` | `https://mcp.jin10.com/mcp` | MCP 端点 |
| `JIN10_MCP_PROTOCOL` | `2025-11-25` | 协议版本 |
| `JIN10_KEYWORD` | `黄金` | 快讯/资讯筛选词（`JIN10_FLASH_KEYWORD` 仍兼容） |
| `JIN10_FLASH_LIMIT` | `8` | 快讯条数上限 |
| `JIN10_ARTICLE_LIMIT` | `6` | 资讯条数上限 |
| `JIN10_NEWS_LIMIT` | `12` | 合并后头条总上限 |
| `JIN10_CACHE_TTL` | `600` | 进程内缓存秒数 |
| `JIN10_MCP_TIMEOUT` | `60` | MCP HTTP 超时秒数 |
| `JIN10_QUOTE_ENABLED` | `true` | 启用 get_quote 交叉校验 |
| `JIN10_QUOTE_CODE` | `XAUUSD` | 报价品种代码 |
| `JIN10_KLINE_ENABLED` | `true` | 启用 get_kline 摘要 |
| `JIN10_KLINE_CODE` | `XAUUSD` | K 线品种代码 |
| `JIN10_KLINE_COUNT` | `20` | K 线条数 |
| `JIN10_KLINE_PERIOD` | 空 | 可选整数周期（不传则用 MCP 默认） |
