# Instructions for AI Agents & Automation

## Start the Streamlit app (required)

**Do not** run `streamlit run app.py` directly.

Use the **cross-platform** launcher `run_app.py` (loads `.env`, stops stale Streamlit, sets UTF-8):

```bash
python run_app.py
```

| Platform | Optional shortcut |
|----------|-------------------|
| Windows | `.\run_app.bat` (no PowerShell ExecutionPolicy issue) |
| Linux / macOS | `chmod +x run_app.sh && ./run_app.sh` |

Custom port: `python run_app.py --port 8503`

Default URL: `http://localhost:8501`

Legacy wrappers (`run_app.ps1`, `scripts/run_app.sh`) delegate to `run_app.py`.

## Environment

- Copy `.env.example` → `.env` before first run.
- The launcher loads `.env` into the process environment on every start.
- Windows/Linux system environment variables are inherited automatically.

## Other common commands

```bash
python tests/run.py                    # fast unit + regression (no network)
python tests/run.py --full             # includes pipeline integration
python scripts/check_mt5_connection.py # optional MT5 self-check
```

## Key docs

- [docs/operations/setup.md](docs/operations/setup.md) — install & config
- [docs/operations/onboarding.md](docs/operations/onboarding.md) — 15-minute developer onboarding
- [docs/reference/cheat-sheet.md](docs/reference/cheat-sheet.md) — where to change features
