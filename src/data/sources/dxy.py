"""DXY (US Dollar Index) snapshot via TradingView."""

from __future__ import annotations

from src.config import TV_DXY_EXCHANGE, TV_DXY_SYMBOL
from src.data.tradingview import fetch_symbol_daily
from src.log import get_logger

log = get_logger(__name__)

_PLACEHOLDER = "偏强 → 利空黄金（占位）"


def fetch_dxy_impact() -> tuple[str, dict]:
    """
    Return (human impact text, refs dict).
    Uses daily DXY change: up → bearish gold, down → bullish gold.
    """
    try:
        df = fetch_symbol_daily(TV_DXY_EXCHANGE, TV_DXY_SYMBOL, n_bars=5, label="DXY")
        if len(df) < 2:
            raise ValueError("insufficient DXY bars")

        latest = float(df["Close"].iloc[-1])
        prev = float(df["Close"].iloc[-2])
        change = latest - prev
        change_pct = (change / prev) * 100 if prev else 0.0

        if change_pct > 0.25:
            impact = f"偏强 ({latest:.2f}, 日 {change_pct:+.2f}%) → 利空黄金"
            bias = "bearish"
        elif change_pct < -0.25:
            impact = f"偏弱 ({latest:.2f}, 日 {change_pct:+.2f}%) → 利好黄金"
            bias = "bullish"
        else:
            impact = f"中性 ({latest:.2f}, 日 {change_pct:+.2f}%) → 影响有限"
            bias = "neutral"

        refs = {
            "source": "tradingview",
            "symbol": f"{TV_DXY_EXCHANGE}:{TV_DXY_SYMBOL}",
            "close": round(latest, 2),
            "change_pct": round(change_pct, 3),
            "bias": bias,
        }
        log.info("DXY snapshot %s change=%+.2f%%", latest, change_pct)
        return impact, refs
    except Exception as exc:
        log.warning("DXY fetch failed, using placeholder: %s", exc)
        return _PLACEHOLDER.replace("（占位）", f"（回退 · {exc}）"), {
            "source": "placeholder",
            "error": str(exc),
        }
