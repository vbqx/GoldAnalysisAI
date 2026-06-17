"""Fundamentals Analyst — DXY / US10Y macro drivers for gold."""

from __future__ import annotations

from src.core.types import AnalystReport, Bias, EvidenceItem, MarketContext
from src.data.sources.fundamentals import external_macro_evidence

from src.agents.analysts.base import build_report


def _bias_from_quotes(ctx: MarketContext) -> Bias:
    votes = {"bullish": 0, "bearish": 0, "neutral": 0}
    for q in ctx.external.macro_quotes:
        votes[q.bias] = votes.get(q.bias, 0) + 1
    if votes["bullish"] > votes["bearish"]:
        return "bullish"
    if votes["bearish"] > votes["bullish"]:
        return "bearish"
    text = ctx.external.dxy_impact
    if any(k in text for k in ("利空黄金", "偏强")):
        return "bearish"
    if any(k in text for k in ("利好黄金", "偏弱")):
        return "bullish"
    return "neutral"


def _macro_context_evidence(ctx: MarketContext) -> list[EvidenceItem]:
    """Turn macro input quality and event timing into auditable evidence."""
    ext = ctx.external
    items: list[EvidenceItem] = []

    high_impact = [ev for ev in ext.calendar_events if ev.importance >= 3.0]
    if high_impact:
        sample = "；".join(ev.display() for ev in high_impact[:3])
        items.append(
            EvidenceItem(
                category="fundamentals",
                summary=f"高影响宏观日历 {len(high_impact)} 项：{sample}",
                strength=0.45 + min(len(high_impact) * 0.08, 0.25),
                refs={
                    "source": "jin10_calendar",
                    "high_impact_count": len(high_impact),
                },
            )
        )

    countdown = ctx.derived.get("event_countdown") or {}
    if countdown:
        items.append(
            EvidenceItem(
                category="fundamentals",
                summary=(
                    f"下一高影响事件：{countdown.get('region', '')} "
                    f"{countdown.get('event', '')} · {countdown.get('hours_until')}h"
                ).strip(),
                strength=0.55,
                refs={"source": "jin10_calendar", **countdown},
            )
        )

    names = [q.name for q in ext.macro_quotes]
    if ext.macro_quotes:
        missing = [name for name in ("DXY", "US10Y") if name not in names]
        coverage = " + ".join(names)
        summary = f"宏观报价覆盖：{coverage}"
        if missing:
            summary += f"；缺少 {'/'.join(missing)}"
        items.append(
            EvidenceItem(
                category="fundamentals",
                summary=summary,
                strength=0.5 if not missing else 0.35,
                refs={"source": "input_density", "quote_names": names, "missing": missing},
            )
        )

    macro_errors = [
        err for err in ext.fetch_errors if "dxy" in err.lower() or "us10y" in err.lower()
    ]
    if macro_errors:
        items.append(
            EvidenceItem(
                category="fundamentals",
                summary=f"宏观数据源告警：{macro_errors[0][:160]}",
                strength=0.2,
                refs={"source": "fetch_errors", "errors": macro_errors[:3]},
            )
        )

    return items


def run_fundamentals_analyst(ctx: MarketContext) -> AnalystReport:
    ext = ctx.external
    items = external_macro_evidence(ext) + _macro_context_evidence(ctx)
    bias = _bias_from_quotes(ctx)

    live = any(i.refs.get("source") == "tradingview" for i in items)
    names = [q.name for q in ext.macro_quotes] or ["DXY"]
    high_impact = ctx.context_stats.get("analyst_inputs", {}).get("fundamentals", {}).get(
        "high_impact_calendar", 0
    )
    summary = f"基本面：{' + '.join(names)} · 高影响日历 {high_impact} · {ext.dxy_impact[:60]}"
    if not live and "占位" in ext.dxy_impact:
        summary = f"基本面：{ext.dxy_impact}"

    return build_report(agent="fundamentals_analyst", items=items, bias=bias, summary=summary)
