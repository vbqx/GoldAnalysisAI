"""Smoke-test the optional MT5 connection.

The script reads MT5_* values from .env / environment variables, prints a
non-sensitive account summary, and fetches a few recent bars. It never prints
the password and never sends orders.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data.mt5 import MT5Config, MT5UnavailableError, get_mt5_provider


def main() -> int:
    cfg = MT5Config()
    provider = get_mt5_provider(cfg)
    print(f"provider={provider.name} enabled={cfg.enabled} symbol={cfg.symbol} server={cfg.server or '-'}")

    if not cfg.enabled:
        print("MT5 is disabled. Set MT5_ENABLED=true in .env to test the terminal connection.")
        return 0

    try:
        info = provider.account_info()
        safe_info = {
            "login": info.get("login"),
            "server": info.get("server"),
            "currency": info.get("currency"),
            "balance": info.get("balance"),
            "equity": info.get("equity"),
            "leverage": info.get("leverage"),
        }
        print(f"account={safe_info}")

        bars = provider.fetch_rates("5m", 5)
        latest = bars.iloc[-1]
        print(
            "latest_5m="
            f"time={bars.index[-1].isoformat()} "
            f"open={latest['Open']:.2f} high={latest['High']:.2f} "
            f"low={latest['Low']:.2f} close={latest['Close']:.2f}"
        )
    except (MT5UnavailableError, ValueError) as exc:
        print(f"MT5 check failed: {exc}")
        return 1
    finally:
        provider.shutdown()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
