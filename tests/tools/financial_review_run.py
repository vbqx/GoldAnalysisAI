"""One-shot financial review snapshot — rule mode pipeline."""

from __future__ import annotations

import json
import sys

from tests._bootstrap import ROOT, configure_stdio, load_dotenv, setup_path

setup_path()
load_dotenv()
configure_stdio()

from src.core.progress import ProgressReporter, reset_progress, set_progress
from src.core.run_config import apply_run_config, run_config_for_mode
from src.pipeline import run_analysis


def main() -> int:
    apply_run_config(run_config_for_mode("rule"))
    reporter = ProgressReporter()
    token = set_progress(reporter)
    try:
        report, data, analyses = run_analysis()
    finally:
        reset_progress(token)

    trace = report.get("agent_trace", {})
    debate = trace.get("debate", {})
    proposal = trace.get("proposal", {})
    decision = trace.get("decision", {})
    bull = debate.get("bullish", {})
    bear = debate.get("bearish", {})

    bull_score = bull.get("confidence", 0) * max(len(bull.get("items", [])), 1)
    bear_score = bear.get("confidence", 0) * max(len(bear.get("items", [])), 1)
    sent = report["sentiment"]
    combined_bull = bull_score + sent["bullish"] / 100
    combined_bear = bear_score + sent["bearish"] / 100

    signals_out = []
    for sig in report.get("signals", []):
        entry_mid = (sig["entry_low"] + sig["entry_high"]) / 2
        tp1 = sig["take_profits"][0] if sig.get("take_profits") else None
        geom_ok = True
        if sig["direction"] == "SELL" and tp1 is not None:
            geom_ok = tp1 < entry_mid and sig["stop_loss"] > entry_mid
        if sig["direction"] == "BUY" and tp1 is not None:
            geom_ok = tp1 > entry_mid and sig["stop_loss"] < entry_mid
        signals_out.append(
            {
                "name": sig["name"],
                "direction": sig["direction"],
                "theme": sig.get("theme"),
                "entry": [sig["entry_low"], sig["entry_high"]],
                "entry_mid": round(entry_mid, 2),
                "stop_loss": sig["stop_loss"],
                "take_profits": sig["take_profits"],
                "risk_reward": sig.get("risk_reward"),
                "geom_ok": geom_ok,
                "selected": sig["name"] in {
                    report["signals"][i]["name"]
                    for i in proposal.get("signal_indices", [])
                    if i < len(report["signals"])
                },
            }
        )

    out = {
        "run_at": report["meta"]["updated_at"],
        "mode": "rule",
        "price": report["metrics"]["current_price"],
        "close_5m": float(data["5m"]["Close"].iloc[-1]),
        "sentiment": sent,
        "structure": {tf: analyses[tf].trend for tf in ("1d", "4h", "1h", "15m", "5m")},
        "analyst_team": trace.get("analyst_team", {}),
        "research": {
            "bull_items": len(bull.get("items", [])),
            "bull_conf": bull.get("confidence"),
            "bear_items": len(bear.get("items", [])),
            "bear_conf": bear.get("confidence"),
            "bull_score": round(bull_score, 3),
            "bear_score": round(bear_score, 3),
            "combined_bull": round(combined_bull, 3),
            "combined_bear": round(combined_bear, 3),
        },
        "debate": {
            "consensus_bias": debate.get("consensus_bias"),
            "consensus_strength": debate.get("consensus_strength"),
        },
        "conclusion": {
            "market_sentiment": report["conclusion"].get("market_sentiment"),
            "direction_summary": report["conclusion"].get("direction_summary"),
            "action": report["conclusion"].get("action"),
        },
        "trader": {
            "primary_direction": proposal.get("primary_direction"),
            "signal_indices": proposal.get("signal_indices"),
        },
        "manager": {
            "action": decision.get("action"),
            "direction": decision.get("direction"),
            "confidence": decision.get("confidence"),
            "summary": decision.get("summary"),
        },
        "risk_reviews": trace.get("risk_reviews", []),
        "signals": signals_out,
        "projections": report.get("projections", []),
        "swing": {
            "high": report["chart"].get("swing_high"),
            "low": report["chart"].get("swing_low"),
        },
    }

    path = ROOT / "tests" / "reports" / "financial_review_snapshot.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"Saved: {path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
