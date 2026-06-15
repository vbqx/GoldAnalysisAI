"""Macro quotes for gold fundamentals — DXY, US10Y via TradingView."""

from __future__ import annotations

from src.config import TV_DXY_EXCHANGE, TV_DXY_SYMBOL, TV_US10Y_EXCHANGE, TV_US10Y_SYMBOL
from src.core.types import MacroQuote
from src.data.tradingview import fetch_symbol_daily
from src.log import get_logger

log = get_logger(__name__)

_BEARISH_GOLD = "bearish"
_BULLISH_GOLD = "bullish"
_NEUTRAL = "neutral"


def _daily_change(df) -> tuple[float, float, float]:
    latest = float(df["Close"].iloc[-1])
    prev = float(df["Close"].iloc[-2])
    change_pct = ((latest - prev) / prev) * 100 if prev else 0.0
    return latest, prev, change_pct


def _gold_bias_from_change(change_pct: float, *, invert: bool) -> tuple[str, str]:
    """Return (impact text fragment, gold bias). invert=True for DXY (up hurts gold)."""
    if invert:
        if change_pct > 0.25:
            return f"日 {change_pct:+.2f}%", _BEARISH_GOLD
        if change_pct < -0.25:
            return f"日 {change_pct:+.2f}%", _BULLISH_GOLD
        return f"日 {change_pct:+.2f}%", _NEUTRAL
    # US10Y: rising yields typically bearish gold
    if change_pct > 0.15:
        return f"日 {change_pct:+.2f}%", _BEARISH_GOLD
    if change_pct < -0.15:
        return f"日 {change_pct:+.2f}%", _BULLISH_GOLD
    return f"日 {change_pct:+.2f}%", _NEUTRAL


def fetch_dxy_quote() -> MacroQuote | None:
    try:
        df = fetch_symbol_daily(TV_DXY_EXCHANGE, TV_DXY_SYMBOL, n_bars=5, label="DXY")
        if len(df) < 2:
            return None
        close, _, change_pct = _daily_change(df)
        chg_text, bias = _gold_bias_from_change(change_pct, invert=True)
        if bias == _BEARISH_GOLD:
            impact = f"偏强 ({close:.2f}, {chg_text}) → 利空黄金"
        elif bias == _BULLISH_GOLD:
            impact = f"偏弱 ({close:.2f}, {chg_text}) → 利好黄金"
        else:
            impact = f"中性 ({close:.2f}, {chg_text}) → 影响有限"
        return MacroQuote(
            name="DXY",
            symbol=f"{TV_DXY_EXCHANGE}:{TV_DXY_SYMBOL}",
            close=round(close, 2),
            change_pct=round(change_pct, 3),
            impact=impact,
            bias=bias,
            source="tradingview",
        )
    except Exception as exc:
        log.warning("DXY quote failed: %s", exc)
        return None


def fetch_us10y_quote() -> MacroQuote | None:
    try:
        df = fetch_symbol_daily(TV_US10Y_EXCHANGE, TV_US10Y_SYMBOL, n_bars=5, label="US10Y")
        if len(df) < 2:
            return None
        close, _, change_pct = _daily_change(df)
        chg_text, bias = _gold_bias_from_change(change_pct, invert=False)
        if bias == _BEARISH_GOLD:
            impact = f"收益率上行 ({close:.2f}, {chg_text}) → 压制黄金"
        elif bias == _BULLISH_GOLD:
            impact = f"收益率下行 ({close:.2f}, {chg_text}) → 支撑黄金"
        else:
            impact = f"收益率震荡 ({close:.2f}, {chg_text}) → 影响有限"
        return MacroQuote(
            name="US10Y",
            symbol=f"{TV_US10Y_EXCHANGE}:{TV_US10Y_SYMBOL}",
            close=round(close, 2),
            change_pct=round(change_pct, 3),
            impact=impact,
            bias=bias,
            source="tradingview",
        )
    except Exception as exc:
        log.warning("US10Y quote failed: %s", exc)
        return None


def fetch_macro_quotes() -> list[MacroQuote]:
    quotes: list[MacroQuote] = []
    for fn in (fetch_dxy_quote, fetch_us10y_quote):
        q = fn()
        if q:
            quotes.append(q)
    return quotes
