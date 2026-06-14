"""Close fixed financial-review GitHub issues #9-#13."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tests.tools.github.close_issues import api  # noqa: E402

CLOSES = [
    {
        "number": 9,
        "comment": """## 修复说明

**改动文件：** `src/agents/risk.py`

- 修正 `approved` 运算符优先级问题：`debate_bias=neutral` 时各档 `approved=False`
- 共识震荡时提示「各档暂不通过，等待方向确认」

## 测试结果

`pytest tests/unit/test_financial_review.py::test_fin_01_neutral_debate_aggressive_should_not_auto_approve -v` ✅ PASSED
""",
    },
    {
        "number": 10,
        "comment": """## 修复说明

**改动文件：** `src/analysis/report_engine.py`、`src/viz/dashboard_components.py`

- `TradingSignal.win_rate` → `sentiment_bias_pct`
- UI 标签改为「结构权重」，并标注「非回测胜率」

## 测试结果

`pytest tests/unit/test_financial_review.py::test_fin_02_win_rate_matches_sentiment_not_backtest -v` ✅ PASSED
""",
    },
    {
        "number": 11,
        "comment": """## 修复说明

**改动文件：** `src/analysis/report_engine.py`

- 新增 `_compute_risk_reward()`，按 entry/SL/TP1 几何计算盈亏比
- 无法计算时返回 `N/A`

## 测试结果

`pytest tests/unit/test_financial_review.py::test_fin_03_risk_reward_should_match_geometry -v` ✅ PASSED
`pytest tests/unit/test_financial_review.py::test_fin_03_sell_signal_sl_entry_tp_order -v` ✅ PASSED
""",
    },
    {
        "number": 12,
        "comment": """## 修复说明

**改动文件：** `src/analysis/report_engine.py`

- 移除 `build_conclusion` 硬编码价位 `4389-4396`
- 无 signals 时不输出具体区间；有 signals 时动态拼接 entry 区间

## 测试结果

`pytest tests/unit/test_financial_review.py::test_fin_06_conclusion_no_hardcoded_price_without_signals -v` ✅ PASSED
""",
    },
    {
        "number": 13,
        "comment": """## 修复说明

**改动文件：** `src/indicators/verify.py`

- Volume 全为 0 或占比 ≥50% 时，在 `indicator_snapshot` notes 中提示 VWAP 可靠性下降

## 测试结果

`pytest tests/unit/test_financial_review.py::test_fin_09_vwap_zero_volume_should_warn -v` ✅ PASSED
""",
    },
]


def main() -> None:
    for item in CLOSES:
        n = item["number"]
        api("POST", f"/repos/vbqx/GoldAnalysisAI/issues/{n}/comments", {"body": item["comment"]})
        api("PATCH", f"/repos/vbqx/GoldAnalysisAI/issues/{n}", {"state": "closed"})
        print(f"Closed #{n}: https://github.com/vbqx/GoldAnalysisAI/issues/{n}")


if __name__ == "__main__":
    main()
