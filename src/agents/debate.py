"""Research debate — bull vs bear discussion → consensus.

Financial review (F-013): consensus must align with multi-TF structure sentiment when
research scores are close. Scoring uses ``combined = conf×items + sentiment_pct/50``
(not ``/100``). When ``|bull_pct - bear_pct| >= 10`` and combined scores differ by
less than 2.0, tiebreaker picks the dominant structure direction (bearish/bullish).
Audit trail: tiebreaker rationale is appended to ``discussion_notes``.
"""

from __future__ import annotations

from src.analysis.ict_pa import sentiment_score
from src.core.types import AgentEvidence, AnalystTeam, Bias, MarketContext, ResearchDebate


def run_debate(
    bullish: AgentEvidence,
    bearish: AgentEvidence,
    analyses,
    team: AnalystTeam | None = None,
    ctx: MarketContext | None = None,
) -> ResearchDebate:
    notes: list[str] = []
    bull_score = bullish.confidence * max(len(bullish.items), 1)
    bear_score = bearish.confidence * max(len(bearish.items), 1)

    sentiment = sentiment_score(analyses)
    bull_pct = sentiment.get("bullish", 33)
    bear_pct = sentiment.get("bearish", 33)

    if team:
        notes.append("── Analyst Team 摘要 ──")
        for report in team.reports:
            notes.append(f"{report.agent}: {report.summary}（{report.bias} · {report.confidence:.0%}）")

    topics = (getattr(ctx, "derived", None) or {}).get("news_topics") if ctx else None
    if topics:
        notes.append("── 新闻主题 ──")
        for bucket in topics[:3]:
            notes.append(f"{bucket['topic']}（{bucket['count']} 条）")

    calendar = (getattr(ctx, "derived", None) or {}).get("upcoming_calendar") if ctx else None
    if calendar:
        notes.append("── 近期日历 ──")
        for row in calendar[:4]:
            notes.append(f"{row.get('time', '')} {row.get('region', '')} {row.get('event', '')}".strip())

    notes.append(f"看多研究员：{bullish.summary}")
    notes.append(f"看空研究员：{bearish.summary}")
    notes.append(f"多周期技术投票：多 {bull_pct:.0f}% / 空 {bear_pct:.0f}% / 震荡 {sentiment.get('ranging', 0):.0f}%")

    # F-013: structure sentiment weighted at pct/50 so 4h-dominant mood can break ties.
    combined_bull = bull_score + bull_pct / 50
    combined_bear = bear_score + bear_pct / 50

    # Tiebreaker when research is ambiguous but structure has a clear lean (>=10% gap).
    if abs(bull_pct - bear_pct) >= 10 and abs(combined_bull - combined_bear) < 2.0:
        if bear_pct > bull_pct:
            bias = "bearish"
            strength = min(combined_bear / (combined_bull + combined_bear + 0.01), 1.0)
            notes.append("讨论结论：研究证据接近，结构情绪偏空占主导（tiebreaker）")
        elif bull_pct > bear_pct:
            bias = "bullish"
            strength = min(combined_bull / (combined_bull + combined_bear + 0.01), 1.0)
            notes.append("讨论结论：研究证据接近，结构情绪偏多占主导（tiebreaker）")
        else:
            bias = "neutral"
            strength = 0.5
            notes.append("讨论结论：多空证据接近，倾向震荡/等待确认")
    elif abs(combined_bull - combined_bear) < 0.15:
        bias: Bias = "neutral"
        strength = 0.5
        notes.append("讨论结论：多空证据接近，倾向震荡/等待确认")
    elif combined_bull > combined_bear:
        bias = "bullish"
        strength = min(combined_bull / (combined_bull + combined_bear + 0.01), 1.0)
        notes.append("讨论结论：看多证据占优，但需关注上方流动性")
    else:
        bias = "bearish"
        strength = min(combined_bear / (combined_bull + combined_bear + 0.01), 1.0)
        notes.append("讨论结论：看空证据占优，关注反抽卖区")

    return ResearchDebate(
        bullish=bullish,
        bearish=bearish,
        consensus_bias=bias,
        consensus_strength=strength,
        discussion_notes=notes,
    )
