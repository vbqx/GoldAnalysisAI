"""Plotly chart builder for the analysis dashboard."""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go


def build_sentiment_donut(sentiment: dict[str, float]) -> go.Figure:
    labels = ["做空", "做多", "震荡"]
    values = [sentiment["bearish"], sentiment["bullish"], sentiment["ranging"]]
    colors = ["#ef4444", "#22c55e", "#94a3b8"]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.55,
                marker=dict(colors=colors),
                textinfo="label+percent",
                textfont=dict(size=12),
            )
        ]
    )
    fig.update_layout(
        title=dict(text="多空结构权重", font=dict(size=13)),
        height=165,
        margin=dict(t=36, b=12, l=8, r=8),
        showlegend=False,
    )
    return fig


def build_projection_chart(projections: list[dict]) -> go.Figure:
    fig = go.Figure()
    for proj in projections:
        steps = proj["steps"]
        fig.add_trace(
            go.Scatter(
                x=[s["label"] for s in steps],
                y=[s["price"] for s in steps],
                mode="lines+markers+text",
                name=f"{proj['name']} ({proj['probability']}%)",
                line=dict(color=proj["color"], dash="dash", width=2),
                text=[f"{s['price']}" for s in steps],
                textposition="top center",
            )
        )
    fig.update_layout(
        title=dict(text="未来趋势推演", font=dict(size=14)),
        height=240,
        template="plotly_white",
        margin=dict(t=45, b=30, l=40, r=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=10)),
    )
    fig.update_yaxes(title="价格")
    return fig
