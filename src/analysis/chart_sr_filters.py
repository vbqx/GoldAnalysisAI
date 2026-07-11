"""Filter DGT S/R levels for chart display (5m main + 4h/1h/15m strips)."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.analysis.dgt_price_action import SrLevel

_SR_COLORS = {
    "consecutive_sr": {"support": "#4dd0e1", "resistance": "#4dd0e1"},
    "volume_spike": {"support": "#ffb74d", "resistance": "#ffb74d"},
    "high_volatility": {"support": "#81c784", "resistance": "#81c784"},
}
_KIND_PRIORITY = {"volume_spike": 0, "high_volatility": 1, "consecutive_sr": 2, "rule_anchor": 3}
_MAX_CHART_LINES = 5
_MERGE_TOLERANCE = 1.5
_SR_CHART_TIMEFRAMES = frozenset({"5m", "15m", "1h", "4h"})


def _fmt_price(price: float) -> str:
    rounded = round(price, 2)
    if abs(rounded - round(rounded)) < 0.005:
        return str(int(round(rounded)))
    return f"{rounded:.2f}"


def _short_chart_title(lvl: SrLevel) -> str:
    """Compact right-axis label to reduce overlap."""
    label = (lvl.label or "S/R").replace("量价", "").strip()
    for old, new in (
        ("放量阻力·高点", "放量·高"),
        ("放量阻力·收盘", "放量·收"),
        ("放量支撑·低点", "放量·低"),
        ("放量支撑·收盘", "放量·收"),
        ("高波动阻力", "高波阻"),
        ("高波动支撑", "高波撑"),
        ("量价连续阻力", "连续阻"),
        ("量价连续支撑", "连续撑"),
    ):
        if label == old:
            return new
    return label[:6] if len(label) > 6 else label


def _merge_nearby(levels: list[SrLevel]) -> list[SrLevel]:
    """Keep the higher-priority level when prices are within tolerance."""
    if not levels:
        return []
    ordered = sorted(
        levels,
        key=lambda x: (_KIND_PRIORITY.get(x.kind, 9), x.price),
    )
    kept: list[SrLevel] = []
    for lvl in ordered:
        replaced = False
        for i, existing in enumerate(kept):
            if abs(existing.price - lvl.price) <= _MERGE_TOLERANCE:
                if _KIND_PRIORITY.get(lvl.kind, 9) < _KIND_PRIORITY.get(existing.kind, 9):
                    kept[i] = lvl
                replaced = True
                break
        if not replaced:
            kept.append(lvl)
    return kept


def visible_sr_price_lines(
    sr_levels: list[SrLevel] | list[dict[str, Any]],
    plot_df: pd.DataFrame,
    *,
    max_lines: int = _MAX_CHART_LINES,
    current_price: float | None = None,
) -> list[dict[str, Any]]:
    """Pick nearest, highest-signal S/R lines for the visible range.

    Axis labels show price only; ``hint`` carries the compact type for hover tooltips.
    """
    if plot_df.empty or not sr_levels:
        return []

    vis_lo = float(plot_df["Low"].min())
    vis_hi = float(plot_df["High"].max())
    pad = max((vis_hi - vis_lo) * 0.02, 0.5)
    anchor = current_price if current_price is not None else float(plot_df["Close"].iloc[-1])

    parsed: list[SrLevel] = []
    for row in sr_levels:
        if isinstance(row, SrLevel):
            parsed.append(row)
        else:
            parsed.append(
                SrLevel(
                    price=float(row["price"]),
                    kind=row.get("kind", "consecutive_sr"),
                    direction=row.get("direction", "support"),
                    time=pd.Timestamp(row["time"]) if row.get("time") else plot_df.index[-1],
                    label=str(row.get("label", "S/R")),
                )
            )

    visible = [lvl for lvl in parsed if (vis_lo - pad) <= lvl.price <= (vis_hi + pad)]
    visible = _merge_nearby(visible)
    visible.sort(
        key=lambda x: (
            _KIND_PRIORITY.get(x.kind, 9),
            abs(x.price - anchor),
            -x.time.value,
        )
    )

    # Balance resistance/support so one side does not dominate the chart.
    resist = [lvl for lvl in visible if lvl.direction == "resistance"]
    support = [lvl for lvl in visible if lvl.direction == "support"]
    half = max(max_lines // 2, 2)
    picked = resist[:half] + support[:half]
    if len(picked) < max_lines:
        rest = [lvl for lvl in visible if lvl not in picked]
        picked.extend(rest[: max_lines - len(picked)])
    display = picked[:max_lines]

    lines: list[dict[str, Any]] = []
    for lvl in sorted(display, key=lambda x: x.price):
        colors = _SR_COLORS.get(lvl.kind, _SR_COLORS["consecutive_sr"])
        lines.append(
            {
                "price": lvl.price,
                "color": colors.get(lvl.direction, "#64748b"),
                "style": 2 if lvl.kind == "consecutive_sr" else 0,
                "title": _fmt_price(lvl.price),
                "hint": _short_chart_title(lvl),
                "kind": lvl.kind,
                "direction": lvl.direction,
            }
        )
    return lines
