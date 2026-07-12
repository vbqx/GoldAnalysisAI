"""Historical replay engine for the existing rule analysis stack."""

from __future__ import annotations

import random
from dataclasses import replace
from typing import Iterable

import pandas as pd

from src.backtest.macro import apply_macro_to_signals, fetch_historical_dxy, macro_state_at, normalize_macro_ohlcv
from src.backtest.metrics import group_trades, summarize_trades
from src.backtest.simulator import simulate_signal
from src.backtest.types import BacktestConfig, BacktestMode, BacktestResult, TradeResult


def normalize_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    rename = {
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
        "datetime": "Datetime",
        "time": "Datetime",
        "timestamp": "Datetime",
    }
    out = out.rename(columns={k: v for k, v in rename.items() if k in out.columns})
    if "Datetime" in out.columns:
        out.index = pd.to_datetime(out.pop("Datetime"), utc=True)
    else:
        out.index = pd.to_datetime(out.index, utc=True)
    for col in ("Open", "High", "Low", "Close"):
        if col not in out.columns:
            raise ValueError(f"OHLCV data missing column: {col}")
    if "Volume" not in out.columns:
        out["Volume"] = 0
    out = out[["Open", "High", "Low", "Close", "Volume"]].astype(float)
    return out.sort_index().dropna(subset=["Open", "High", "Low", "Close"])


def resample_ohlcv(df_5m: pd.DataFrame, rule: str) -> pd.DataFrame:
    out = df_5m.resample(rule).agg(
        {"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"}
    )
    return out.dropna()


def make_multitimeframe(df_5m: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {
        "5m": df_5m,
        "15m": resample_ohlcv(df_5m, "15min"),
        "1h": resample_ohlcv(df_5m, "1h"),
        "4h": resample_ohlcv(df_5m, "4h"),
        "1d": resample_ohlcv(df_5m, "1d"),
    }


def _enough_data(data: dict[str, pd.DataFrame]) -> bool:
    required = {"5m": 80, "15m": 40, "1h": 30, "4h": 10, "1d": 2}
    return all(len(data.get(tf, ())) >= need for tf, need in required.items())


def _selected_signals(
    data_5m: pd.DataFrame,
    *,
    config: BacktestConfig,
    dxy_daily: pd.DataFrame | None = None,
):
    from src.agents.manager import run_manager
    from src.agents.risk import run_risk_team
    from src.agents.trader import run_trader_agent
    from src.analysis.ict_pa import analyze_timeframe, sentiment_score
    from src.analysis.report_engine import compute_trading_signals
    from src.core.types import AgentEvidence, EvidenceItem, ExternalFactors, MarketContext, ResearchDebate
    from src.data.fetcher import daily_metrics
    from src.indicators.technical import enrich

    data = make_multitimeframe(data_5m)
    if not _enough_data(data):
        return [], {"skip_reason": "insufficient_multitimeframe_data"}
    enriched = {tf: enrich(df) for tf, df in data.items()}
    analyses = {tf: analyze_timeframe(enriched[tf], tf) for tf in ("5m", "15m", "1h", "4h", "1d")}
    metrics = daily_metrics(enriched["1d"])
    ctx = MarketContext(
        enriched=enriched,
        analyses=analyses,
        metrics=metrics,
        price=float(metrics["current_price"]),
        external=ExternalFactors(sources=["historical_ohlcv"]),
        source_label="historical replay",
    )
    signals = compute_trading_signals(ctx)
    sentiment = sentiment_score(analyses)
    macro_state = macro_state_at(dxy_daily, data_5m.index[-1]) if config.use_macro else None
    if macro_state is not None:
        signals = apply_macro_to_signals(signals, macro_state, config.macro_weight)
    bull_pct = sentiment.get("bullish", 0.0)
    bear_pct = sentiment.get("bearish", 0.0)
    macro_notes = []
    if macro_state is not None and macro_state.gold_bias != "neutral":
        macro_delta = config.macro_weight * macro_state.confidence
        if macro_state.gold_bias == "bullish":
            bull_pct = min(100.0, bull_pct + macro_delta * 100)
            bear_pct = max(0.0, bear_pct - macro_delta * 50)
        elif macro_state.gold_bias == "bearish":
            bear_pct = min(100.0, bear_pct + macro_delta * 100)
            bull_pct = max(0.0, bull_pct - macro_delta * 50)
        macro_notes.append(
            f"DXY macro: {macro_state.gold_bias} confidence={macro_state.confidence:.2f} dxy_time={macro_state.dxy_time}"
        )
    if bull_pct > bear_pct:
        bias = "bullish"
        strength = bull_pct / 100
    elif bear_pct > bull_pct:
        bias = "bearish"
        strength = bear_pct / 100
    else:
        bias = "neutral"
        strength = 0.5
    evidence = EvidenceItem(
        category="structure",
        summary=f"historical structure vote bull={bull_pct:.1f} bear={bear_pct:.1f}",
        strength=max(bull_pct, bear_pct) / 100,
    )
    bullish = AgentEvidence(
        agent="backtest_structure_bullish",
        direction="bullish",
        items=[evidence] if bias == "bullish" else [],
        confidence=bull_pct / 100,
        summary="Historical replay structure-only bullish evidence.",
    )
    bearish = AgentEvidence(
        agent="backtest_structure_bearish",
        direction="bearish",
        items=[evidence] if bias == "bearish" else [],
        confidence=bear_pct / 100,
        summary="Historical replay structure-only bearish evidence.",
    )
    debate = ResearchDebate(
        bullish=bullish,
        bearish=bearish,
        consensus_bias=bias,
        consensus_strength=strength,
        discussion_notes=[
            "Backtest uses structure-only debate to avoid live macro/news leakage.",
            f"Replay vote: bullish {bull_pct:.1f}% / bearish {bear_pct:.1f}% / ranging {sentiment.get('ranging', 0.0):.1f}%",
            *macro_notes,
        ],
    )
    proposal, signals = run_trader_agent(ctx, debate, signals)
    reviews = run_risk_team(proposal, len(signals))
    decision = run_manager(proposal, reviews)
    selected = [
        signals[i]
        for i in decision.selected_signal_indices
        if i < len(signals)
        and signals[i].status != "invalid"
    ]
    return selected, {
        "decision": decision.to_dict(),
        "proposal": proposal.to_dict(),
        "sentiment": sentiment,
        "macro": macro_state.to_dict() if macro_state is not None else None,
    }


def _iter_signal_points(df_5m: pd.DataFrame, config: BacktestConfig) -> Iterable[int]:
    stop = len(df_5m) - max(config.max_holding_bars, 1)
    return range(config.warmup_bars, max(config.warmup_bars, stop), config.step_bars)


def _macro_data_for_run(config: BacktestConfig, dxy_daily: pd.DataFrame | None) -> tuple[pd.DataFrame | None, str | None]:
    if not config.use_macro:
        return None, None
    try:
        if dxy_daily is not None:
            return normalize_macro_ohlcv(dxy_daily), None
        return fetch_historical_dxy(config.dxy_bars), None
    except Exception as exc:
        return None, str(exc)


def run_backtest(
    df_5m: pd.DataFrame,
    config: BacktestConfig | None = None,
    *,
    dxy_daily: pd.DataFrame | None = None,
) -> BacktestResult:
    cfg = config or BacktestConfig()
    history = normalize_ohlcv(df_5m)
    macro_data, macro_error = _macro_data_for_run(cfg, dxy_daily)
    trades: list[TradeResult] = []
    skipped = 0
    evaluated = 0
    macro_used = 0

    for i in _iter_signal_points(history, cfg):
        evaluated += 1
        past = history.iloc[: i + 1]
        future = history.iloc[i + 1 : i + 1 + cfg.max_holding_bars]
        selected, metadata = _selected_signals(past, config=cfg, dxy_daily=macro_data)
        if metadata.get("macro"):
            macro_used += 1
        if not selected:
            skipped += 1
            continue
        for signal in selected:
            if float(getattr(signal, "score_total", 0.0) or 0.0) < cfg.min_score:
                continue
            trades.append(simulate_signal(signal, future, history.index[i], cfg))

    summary = summarize_trades(trades)
    diagnostics = {
        "evaluated_points": evaluated,
        "skipped_points": skipped,
        "bars": len(history),
        "start": str(history.index[0]) if len(history) else "",
        "end": str(history.index[-1]) if len(history) else "",
        "methodology": [
            "point-in-time replay",
            "rule-only agent stack",
            "conservative same-bar stop-first execution",
            "R-multiple performance accounting",
        ],
        "macro_enabled": cfg.use_macro,
        "macro_used_points": macro_used,
        "macro_error": macro_error,
    }
    return BacktestResult(
        config=cfg,
        trades=trades,
        summary=summary,
        by_setup=group_trades(trades, "setup_type"),
        by_direction=group_trades(trades, "direction"),
        diagnostics=diagnostics,
    )


def run_random_window_backtest(
    df_5m: pd.DataFrame,
    config: BacktestConfig | None = None,
    *,
    dxy_daily: pd.DataFrame | None = None,
) -> BacktestResult:
    base = config or BacktestConfig(mode=BacktestMode.RANDOM_WINDOWS)
    cfg = replace(base, mode=BacktestMode.RANDOM_WINDOWS)
    history = normalize_ohlcv(df_5m)
    macro_data, macro_error = _macro_data_for_run(cfg, dxy_daily)
    rng = random.Random(cfg.random_seed)
    min_len = cfg.warmup_bars + cfg.max_holding_bars + cfg.step_bars
    window = max(cfg.random_window_bars, min_len)
    if len(history) <= window:
        return run_backtest(history, cfg, dxy_daily=macro_data)

    all_trades: list[TradeResult] = []
    window_stats: list[dict] = []
    seen: set[tuple] = set()
    max_start = len(history) - window
    for n in range(cfg.random_windows):
        start = rng.randint(0, max_start)
        segment = history.iloc[start : start + window]
        result = run_backtest(segment, cfg, dxy_daily=macro_data)
        for trade in result.trades:
            key = (trade.signal_time, trade.direction, trade.signal_name, trade.entry_price)
            if key not in seen:
                seen.add(key)
                all_trades.append(trade)
        window_stats.append(
            {
                "window": n + 1,
                "start": str(segment.index[0]),
                "end": str(segment.index[-1]),
                **result.summary,
            }
        )

    all_trades.sort(key=lambda t: t.signal_time)

    summary = summarize_trades(all_trades)
    avg_window_r = sum(row["total_r"] for row in window_stats) / len(window_stats) if window_stats else 0.0
    sorted_r = sorted(row["total_r"] for row in window_stats)
    p10 = sorted_r[max(0, int(len(sorted_r) * 0.10) - 1)] if sorted_r else 0.0
    summary.update({"avg_window_total_r": round(avg_window_r, 4), "p10_window_total_r": round(p10, 4)})
    return BacktestResult(
        config=cfg,
        trades=all_trades,
        summary=summary,
        by_setup=group_trades(all_trades, "setup_type"),
        by_direction=group_trades(all_trades, "direction"),
        diagnostics={
            "windows": window_stats,
            "bars": len(history),
            "macro_enabled": cfg.use_macro,
            "macro_error": macro_error,
            "trades_deduped": True,
            "note": "Aggregate trade stats dedupe overlapping windows; use per-window rows for distribution.",
        },
    )
