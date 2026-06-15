# AGENTS.md

## Cursor Cloud specific instructions

GoldAnalysisAI is a single Streamlit app (`app.py`) that renders an XAUUSD analysis dashboard
(Price Action + ICT + SMC) with three navigation pages under `views/`. There is one service.

The update script provisions a `.venv` and installs `requirements.txt` + `requirements-dev.txt`.
Always run Python via the venv (`.venv/bin/python`, `.venv/bin/streamlit`, `.venv/bin/pytest`).

### Environment / `.env`
- The app and tests load `.env` (see `app.py` and `tests/conftest.py` → `load_dotenv()`).
  Copy it from `.env.example` if missing: `cp .env.example .env`.
- Defaults run in `AGENT_MODE=rule` with `LLM_ENABLED=false` (no LLM API key needed).
- Non-obvious test gotcha: the no-network "fast" suite still requires `JIN10_API_TOKEN` to be
  **non-empty** in `.env`. Two tests in `tests/unit/test_external_sources.py`
  (`test_jin10_bundle_flash_articles_calendar`, `test_news_source_external`) mock the network
  fetch functions but the Jin10 bundle short-circuits in `src/data/sources/jin10_feed.py` when the
  token is empty, so they fail without it. Set any placeholder value (e.g.
  `JIN10_API_TOKEN=test-placeholder-token`) — a real token is only needed for live Jin10 data.

### Run
- Dev server: `.venv/bin/streamlit run app.py --server.headless true --server.port 8501`
  (open http://localhost:8501). Click "刷新报告" in the sidebar to (re)generate a report; it is
  cached in session and only regenerates on that button (rule mode ~30s).
- Report price data comes from TradingView (live network). With a placeholder/empty
  `JIN10_API_TOKEN` the dashboard still works fully; it just shows inline "jin10 MCP HTTP 401"
  warnings for the supplementary news/calendar feeds. Set a real token from
  https://mcp.jin10.com/app to remove them. Optional `TV_USERNAME`/`TV_PASSWORD` enable more history.

### Test / lint
- There is no separate linter configured (dev deps are just `pytest`); use the test suite.
- Fast (no network): `.venv/bin/python tests/run.py` (unit + regression).
- Other modes: `--full`, `--integration`, `--external`, `--financial` (see `tests/run.py`).
  `--external` / `--full` / `--integration` hit live network (TradingView, Jin10) and need a real
  `JIN10_API_TOKEN`.
