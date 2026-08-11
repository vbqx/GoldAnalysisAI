"""Advice V2 orchestrator — data → verified facts → human-review suggestion."""

from __future__ import annotations

import json
import time

from src.advice import build_advice_packet, build_advice_report
from src.advice.llm import enhance_advice
from src.analysis.ict_pa import analyze_timeframe
from src.core.orchestrator_hooks import (
    begin_pipeline_run,
    fetch_market_data,
    finalize_pipeline_archive,
    publish_external_snapshot,
)
from src.core.parallel import run_parallel
from src.core.progress import get_progress
from src.core.run_context import get_run_config
from src.data.aggregator import assemble_market_context
from src.indicators.technical import enrich
from src.log import get_logger

log = get_logger(__name__)


def run_advice_pipeline() -> tuple[dict, dict, dict]:
    """Generate one compact suggestion for human review; never authorize execution."""
    run_id, started = begin_pipeline_run()
    prog = get_progress()

    fetched = fetch_market_data()
    publish_external_snapshot(fetched, prog)
    raw = fetched.raw

    prog.start("indicators", "计算技术指标")
    enriched = run_parallel(
        [(tf, lambda d=df: enrich(d)) for tf, df in raw.items()],
        max_workers=5,
        label="indicators",
    )
    prog.done("indicators", "5 个周期")

    prog.start("structure", "提取市场结构", "5m · 15m · 1h · 4h · 1d")
    analyses = run_parallel(
        [
            (tf, lambda t=tf: analyze_timeframe(enriched[t], t))
            for tf in ("5m", "15m", "1h", "4h", "1d")
        ],
        max_workers=5,
        label="structure",
    )
    prog.done("structure")

    ctx = assemble_market_context(enriched, analyses, fetched.external, fetched.source_label)
    log.info("advice context price=%.2f source=%s", ctx.price, ctx.source_label)

    prog.start("advice", "生成人工审核建议", "方向 · 关注区 · 确认清单 · 失效条件")
    advice = build_advice_packet(ctx)
    cfg = get_run_config().normalized()
    advice_source = "rule"
    advisor_trace = None
    if cfg.llm_enabled:
        try:
            advice, advisor_trace = enhance_advice(advice)
            if advisor_trace is not None and not advisor_trace.error:
                advice_source = "llm_explanation"
        except (ValueError, TypeError) as exc:
            log.warning("advisor wording rejected; deterministic advice retained: %s", exc)
    prog.stage_io(
        "advice",
        label="Advice V2",
        input_text=json.dumps(ctx.to_dict(), ensure_ascii=False),
        output_text=json.dumps(advice.to_dict(), ensure_ascii=False),
    )
    prog.done("advice", f"{advice.decision} · {advice.confidence}")

    prog.start("report", "组装人工审核卡")
    report = build_advice_report(ctx, advice, run_id=run_id, run_config=cfg.to_dict())
    report["meta"]["run_config_fingerprint"] = cfg.fingerprint()
    report["meta"]["advice_source"] = advice_source
    report["meta"]["advisor_trace"] = advisor_trace.to_dict() if advisor_trace else None
    report["meta"]["generation_steps"] = prog.snapshot()
    report["meta"]["llm_io"] = prog.llm_io_snapshot()
    prog.done("report")
    # Capture the completed report step as well.
    report["meta"]["generation_steps"] = prog.snapshot()

    elapsed = time.perf_counter() - started
    finalize_pipeline_archive(
        run_id,
        fetched=fetched,
        report=report,
        enriched=enriched,
        analyses=analyses,
        elapsed_s=elapsed,
        run_config=cfg,
    )
    log.info(
        "advice pipeline done decision=%s price=%.2f elapsed=%.2fs run_id=%s",
        advice.decision,
        ctx.price,
        elapsed,
        run_id,
    )
    return report, enriched, analyses


# Public compatibility name for callers; the V1 implementation no longer exists.
def run_trade_agent_pipeline() -> tuple[dict, dict, dict]:
    return run_advice_pipeline()
