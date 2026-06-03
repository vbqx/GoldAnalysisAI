"""Main analysis pipeline."""

from __future__ import annotations

from src.analysis.ict_pa import analyze_timeframe
from src.analysis.report_engine import build_report
from src.data.fetcher import fetch_multi_timeframe, get_active_source
from src.indicators.technical import enrich


def run_analysis() -> tuple[dict, dict, dict]:
    raw = fetch_multi_timeframe()
    enriched = {tf: enrich(df) for tf, df in raw.items()}

    analyses = {
        "5m": analyze_timeframe(enriched["5m"], "5m"),
        "15m": analyze_timeframe(enriched["15m"], "15m"),
        "1h": analyze_timeframe(enriched["1h"], "1h"),
        "4h": analyze_timeframe(enriched["4h"], "4h"),
    }

    report = build_report(enriched, analyses)
    report["meta"]["data_source"] = get_active_source()
    return report, enriched, analyses
