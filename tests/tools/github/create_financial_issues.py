"""Create GitHub issues for confirmed FIN-* test failures (2026-06-14)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tests.tools.github.create_issues import create_issue, ensure_label  # noqa: E402

ISSUES = [
    {
        "title": "[Bug] F-001 风控 approved 在 neutral 共识下仍通过 aggressive/neutral 档",
        "labels": ["bug", "P0", "financial-review"],
        "body": """## 发现来源

- **Finding:** F-001 · **用例:** FIN-01
- **测试:** `tests/unit/test_financial_review.py::test_fin_01_neutral_debate_aggressive_should_not_auto_approve` **FAILED**

## 现象

`src/agents/risk.py` L37：

```python
approved = bool(allowed) and proposal.debate_bias != "neutral" or bool(allowed)
```

当 `allowed` 非空时，表达式因运算符优先级恒为 `True`，仅 `conservative` 在后续分支被置为 `False`。

## 期望

`debate_bias=neutral` 且有信号时，aggressive/neutral 档不应默认 `approved=True`（或按产品定义明确降仓/拒绝）。

## 复现

```bash
pytest tests/unit/test_financial_review.py::test_fin_01_neutral_debate_aggressive_should_not_auto_approve -v
```
""",
    },
    {
        "title": "[Bug] F-002 win_rate 字段名暗示回测胜率，实际为 sentiment 权重",
        "labels": ["bug", "P0", "financial-review"],
        "body": """## 发现来源

- **Finding:** F-002 · **用例:** FIN-02（值一致）+ FIN-UI-01
- **测试:** `test_fin_02_win_rate_matches_sentiment_not_backtest` **PASSED**（证实 win_rate=f"{bear_pct}%"）

## 现象

`report_engine.py` 与 UI 使用 `win_rate` 标签，值为 `sentiment.bearish/bullish` 百分比，**非历史回测胜率**。

## 期望

字段重命名为 `sentiment_bias_pct` 或 UI 强制标注「结构权重，非回测」。

## 参考

`docs/archive/domain/financial-review.md` F-002 · `tests/cases/financial-review-cases.md`
""",
    },
    {
        "title": "[Bug] F-003 risk_reward 硬编码，与实际 SL/TP 几何不一致",
        "labels": ["bug", "P1", "financial-review"],
        "body": """## 发现来源

- **Finding:** F-003 · **用例:** FIN-03
- **测试:** `test_fin_03_risk_reward_should_match_geometry` **FAILED**

## 现象

所有做空信号固定 `risk_reward="1:2.5 ~ 1:4"`，与 entry/SL/TP 计算无关。实测 FVG 信号 R:R 约 **1:0.8**，与展示值严重不符。

## 期望

按 `(TP1 - entry_mid) / (entry_mid - SL)` 计算并格式化；无法计算时显示 `N/A`。

## 复现

```bash
pytest tests/unit/test_financial_review.py::test_fin_03_risk_reward_should_match_geometry -v
```
""",
    },
    {
        "title": "[Bug] F-006 build_conclusion 含硬编码价位 4389-4396",
        "labels": ["bug", "P1", "financial-review"],
        "body": """## 发现来源

- **Finding:** F-006 · **用例:** FIN-06
- **测试:** `test_fin_06_conclusion_no_hardcoded_price_without_signals` **FAILED**

## 现象

无 signals 时 `build_conclusion` 仍输出「等待 4389-4396 反弹至阻力区做空」。

## 期望

移除硬编码价位，纯动态从 signals / key_levels 生成；无 signals 时不引用具体区间。

## 复现

```bash
pytest tests/unit/test_financial_review.py::test_fin_06_conclusion_no_hardcoded_price_without_signals -v
```
""",
    },
    {
        "title": "[Bug] F-009 Volume 全 0 时 VWAP 无可用性警告",
        "labels": ["bug", "P2", "financial-review"],
        "body": """## 发现来源

- **Finding:** F-009 · **用例:** FIN-09
- **测试:** `test_fin_09_vwap_zero_volume_should_warn` **FAILED**

## 现象

`add_vwap` 将 Volume=0 替换为 1；`indicator_snapshot` notes 未提示 VWAP 不可靠。

## 期望

Volume 全 0 或缺失占比超阈值时，notes / report 标注 VWAP 不可用。

## 复现

```bash
pytest tests/unit/test_financial_review.py::test_fin_09_vwap_zero_volume_should_warn -v
```
""",
    },
]


def main() -> int:
    for label, color, desc in [
        ("financial-review", "5319E7", "From docs/archive/domain/financial-review.md FIN tests"),
        ("P0", "B60205", "Critical"),
        ("P1", "D93F0B", "High"),
        ("P2", "FBCA04", "Medium"),
    ]:
        ensure_label(label, color, desc)

    urls: list[str] = []
    for item in ISSUES:
        urls.append(create_issue(item["title"], item["body"], item["labels"]))

    print("\nCreated", len(urls), "issues")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
