# 安装与配置

## 环境

推荐 CPython 3.12。在项目根目录复制 `.env.example` 为 `.env`，安装项目依赖后使用：

```powershell
python run_app.py
```

可指定端口：`python run_app.py --port 8503`。Windows 也可使用 `run_app.bat`；Linux/macOS 可使用根目录 `run_app.sh`。

## 核心配置

| 变量 | 作用 |
|---|---|
| `LLM_ENABLED` | 是否启用一次 Advice V2 文案增强；默认关闭。 |
| `LLM_API_KEY` / `LLM_BASE_URL` / `LLM_MODEL` | OpenAI-compatible 文案模型；默认硅基流动 `deepseek-ai/DeepSeek-V4-Flash`。 |
| `LLM_THINKING` | 可选：`enabled` / `disabled`；仅直连 `api.deepseek.com` 时生效。 |
| `LLM_CONNECT_TIMEOUT` / `LLM_READ_TIMEOUT` / `LLM_MAX_RETRIES` | 文案调用边界。 |
| `RUN_ARCHIVE_MAX_COUNT` / `RUN_ARCHIVE_MAX_MB` | 运行归档保留上限。 |
| TradingView、Jin10、社交源相关变量 | 行情和外部背景供应商配置。 |

V1 的 `AGENT_MODE=hybrid`、`LLM_STAGE_*`、FAST/STRONG 模型分层已经退役；旧归档中的 hybrid 配置只在兼容读取时映射为当前单次文案模式。

密钥不得提交到 Git、报告或日志。缺少 LLM 密钥不影响确定性建议；外部数据缺失会被明确标记并降级。

## 自检

```powershell
python tests/run.py
python scripts/check_mt5_connection.py
python scripts/inspect_archive.py list
```

MT5 自检只检查连接能力；Advice V2 不下单。
