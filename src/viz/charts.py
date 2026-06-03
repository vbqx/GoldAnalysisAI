"""Plotly chart builder for the analysis dashboard."""

from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.analysis.ict_pa import TimeframeAnalysis


def build_candlestick_chart(
    df: pd.DataFrame,
    analysis: TimeframeAnalysis,
    report: dict[str, Any],
) -> go.Figure:
    df = df.tail(120).copy()
    fig = make_subplots(rows=1, cols=1)

    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Price",
            increasing_line_color="#22c55e",
            decreasing_line_color="#ef4444",
        )
    )

    colors = {"EMA20": "#a855f7", "EMA50": "#eab308", "EMA610": "#ef4444", "VWAP": "#3b82f6"}
    for col, color in colors.items():
        if col in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[col],
                    mode="lines",
                    name=col,
                    line=dict(width=1.2, color=color),
                )
            )

    # Demand zone
    swing_low = report["chart"]["swing_low"]
    fig.add_hrect(
        y0=swing_low - 5,
        y1=swing_low,
        fillcolor="rgba(34,197,94,0.15)",
        line_width=0,
        annotation_text="Demand / Liquidity Zone",
    )

    # Rally sell zones from FVG + OB
    for fvg in analysis.fvgs:
        if fvg.direction == "bearish":
            fig.add_hrect(
                y0=fvg.low,
                y1=fvg.high,
                fillcolor="rgba(244,63,94,0.12)",
                line_width=0,
            )

    for ob in analysis.order_blocks:
        if ob.direction == "bearish":
            fig.add_hrect(
                y0=ob.low,
                y1=ob.high,
                fillcolor="rgba(249,115,22,0.12)",
                line_width=0,
            )

    # Structure events
    for event in analysis.events[-3:]:
        fig.add_annotation(
            x=event.time,
            y=event.price,
            text=event.kind,
            showarrow=True,
            arrowhead=2,
            font=dict(size=10, color="#1e293b"),
        )

    fig.update_layout(
        title="5min Execution Structure",
        xaxis_rangeslider_visible=False,
        template="plotly_white",
        height=480,
        margin=dict(l=40, r=20, t=50, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
    fig.update_yaxes(showgrid=True, gridcolor="#f1f5f9", title="Price")

    return fig


def build_sentiment_donut(sentiment: dict[str, float]) -> go.Figure:
    labels = ["Bearish", "Bullish", "Ranging"]
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
            )
        ]
    )
    fig.update_layout(title="Long/Short Win Rate (Technical)", height=280, margin=dict(t=50, b=20))
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
                line=dict(color=proj["color"], dash="dash"),
                text=[f"{s['price']}" for s in steps],
                textposition="top center",
            )
        )
    fig.update_layout(
        title="Future Trend Projection",
        height=260,
        template="plotly_white",
        margin=dict(t=50, b=30),
    )
    return fig
