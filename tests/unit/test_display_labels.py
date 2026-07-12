"""Display label helpers for Chinese UI."""

from __future__ import annotations

from src.viz.display_labels import (
    conclusion_display_lines,
    execution_banner,
    infer_trade_theme,
    label_action,
    label_bias,
    label_risk_profile,
    label_trade_direction,
)
from src.viz.dashboard_components import render_final_decision_banner


def test_label_bias_cn() -> None:
    assert label_bias("bearish") == "偏空"
    assert label_action("wait") == "观望"
    assert label_trade_direction("short") == "做空"


def test_infer_trade_theme_from_direction_and_cn() -> None:
    assert infer_trade_theme(direction="SELL") == "short"
    assert infer_trade_theme(direction_cn="做多") == "long"
    assert infer_trade_theme(theme="short") == "short"


def test_execution_banner_observation_mode() -> None:
    msg = execution_banner({"execution_authorized": False, "observation_mode": True})
    assert "观察模式" in msg
    assert "未经经理授权" in msg


def test_format_report_branding_replaces_luxalgo() -> None:
    from src.viz.display_labels import format_report_branding, humanize_narrative_fallback

    assert "SMC+PA" in format_report_branding("LuxAlgo SMC | 5min")
    assert format_report_branding("SMC + PA") == "SMC + PA"
    hint = humanize_narrative_fallback("unapproved price 4021")
    assert "4021" in hint
    assert "白名单" in hint


def test_final_decision_banner_wait() -> None:
    html = render_final_decision_banner(
        {
            "meta": {
                "final_decision": {
                    "action": "wait",
                    "verdict_cn": "观望",
                    "execution_authorized": False,
                    "summary": "结构未确认",
                    "observation_mode": False,
                }
            }
        }
    )
    assert "final-decision-banner wait" in html
    assert "观望" in html
    assert "不执行交易" in html


def test_final_decision_banner_execute() -> None:
    from src.analysis.report_engine import build_final_decision_meta

    report = {
        "meta": {
            "execution_authorized": True,
            "manager_decision": {"action": "execute", "summary": "通过"},
        },
        "signals": [
            {
                "signal_role": "primary",
                "direction_cn": "做空",
                "entry_low": 4130,
                "entry_high": 4132,
                "position_size": "标准仓位",
            }
        ],
    }
    report["meta"]["final_decision"] = build_final_decision_meta(report)
    html = render_final_decision_banner(report)
    assert "final-decision-banner execute" in html
    assert "4130-4132" in html


def test_label_risk_profile_cn() -> None:
    assert label_risk_profile("conservative") == "保守"


def test_conclusion_display_lines_dedupes_identical() -> None:
    dup = "快照观察 · 今日决策：观望。暂不执行。"
    lines = conclusion_display_lines(
        {"header_conclusion": dup, "direction_summary": dup}
    )
    assert lines == [dup]


def test_conclusion_display_lines_shows_distinct_summary() -> None:
    header = "今日决策：观望。暂不执行交易计划。"
    summary = "结构背景：主方向偏空，当前处于逆势反弹阶段"
    lines = conclusion_display_lines(
        {"header_conclusion": header, "direction_summary": summary}
    )
    assert lines == [header, summary]
