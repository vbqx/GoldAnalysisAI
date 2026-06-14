# AGENTS.md

## Cursor Cloud specific instructions

### Product overview

**GoldAnalysisAI** (TradingAgentCN) is a single-process Python MVP: a Streamlit dashboard that fetches XAUUSD OHLCV from TradingView (`OANDA:XAUUSD` via `tvdatafeed-enhanced`), runs ICT/PA analysis and a multi-agent decision pipeline, and renders institutional-style gold analysis reports.

There is no separate API server, database, or Docker stack.

### One-time VM prerequisites

Ubuntu/Debian images may need `python3-venv` before the first `python3 -m venv .venv`:

```bash
sudo apt-get install -y python3.12-venv
```

### Running the app

From repo root (after the update script has run):

```bash
source .venv/bin/activate
streamlit run app.py
```

- **URL:** http://localhost:8501
- **Headless E2E (no browser):** `python scripts/chart_compare_test.py` — runs the full pipeline and writes `_chart_test.html` (gitignored).

### Services

| Service | Required? | Notes |
|---------|-----------|-------|
| Streamlit (`app.py`, port 8501) | Yes | Only runtime service |
| TradingView WebSocket | Yes | Pipeline fails without reachable `tvdatafeed` endpoint |
| unpkg.com CDN | For chart overlays | Lightweight Charts JS in the browser; pipeline still works headlessly without it |

### Environment variables

Copy `.env.example` → `.env` if needed. Defaults work for anonymous TradingView access (`TV_SYMBOL`, `TV_EXCHANGE`). Optional: `TV_USERNAME` / `TV_PASSWORD`, `HTTP_PROXY` / `HTTPS_PROXY` for restricted networks.

### Lint / tests

No pytest, ruff, or flake8 config in the repo. Practical checks:

- **Syntax:** `python -m compileall -q app.py src scripts`
- **Pipeline E2E:** `python scripts/chart_compare_test.py`

### Gotchas

- First Streamlit load triggers a full pipeline run (~2–5s) and caches for 5 minutes (`st.cache_data(ttl=300)`). Use sidebar **刷新报告** to force refresh.
- README mentions Yahoo Finance / demo fallbacks; current code uses **TradingView only** — if the WebSocket is unreachable, the UI shows `数据获取失败`.
- Streamlit logs appear in the terminal; set `LOG_LEVEL=DEBUG` in `.env` for verbose pipeline logging.
