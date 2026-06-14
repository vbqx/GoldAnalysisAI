"""Gold / XAUUSD relevance filters for headlines and macro events."""

from __future__ import annotations

import re

# Headlines: keep if any keyword matches
GOLD_HEADLINE_KEYWORDS = (
    "gold",
    "xau",
    "xauusd",
    "fed",
    "federal reserve",
    "fomc",
    "inflation",
    "cpi",
    "ppi",
    "pce",
    "nfp",
    "nonfarm",
    "powell",
    "dollar",
    "dxy",
    "treasury",
    "yield",
    "rate hike",
    "rate cut",
    "geopolit",
    "war ",
    "sanction",
    "spdr",
    "etf",
    "precious",
    "bullion",
    "黄金",
    "金价",
    "贵金属",
    "美联储",
    "联储",
    "非农",
    "通胀",
    "cpi",
    "美元",
    "国债",
    "利率",
    "降息",
    "加息",
    "地缘",
    "冲突",
    "避险",
    "白银",
    "silver",
    "原油",
    "oil",
    "铜",
    "金属",
)

# Macro calendar: event text must hit one of these (plus key regions)
GOLD_MACRO_EVENT_KEYWORDS = (
    "cpi",
    "ppi",
    "pce",
    "非农",
    "nonfarm",
    "就业",
    "失业",
    "初请",
    "adp",
    "fed",
    "fomc",
    "联储",
    "美联储",
    "利率",
    "加息",
    "降息",
    "mlf",
    "lpr",
    "通胀",
    "物价",
    "gdp",
    "零售",
    "pmi",
    "ism",
    "消费者",
    "核心",
    "贸易",
    "库存",
    "原油",
    "oil",
    "黄金",
    "gold",
    "xau",
    "贵金属",
    "国债",
    "债券",
    "yield",
    "美元",
    "dxy",
    "鲍威尔",
    "powell",
    "制造业",
    "服务业",
    "褐皮书",
    "会议纪要",
    "主席",
    "讲话",
)

_GOLD_MACRO_REGIONS = ("美国", "中国", "欧元区", "欧洲", "日本", "英国")

# Low gold impact — drop unless headline path
_NOISE_EVENT_PATTERNS = (
    re.compile(r"nahb|housing market index|building permits", re.I),
    re.compile(r"工业产出|industrial production", re.I),
    re.compile(r"房屋|housing starts", re.I),
    re.compile(r"bnz|business nz", re.I),
)


def matches_gold_headline(text: str) -> bool:
    lower = text.lower()
    return any(k in lower for k in GOLD_HEADLINE_KEYWORDS)


def is_gold_macro_event(event: str, region: str = "", *, importance: float | None = None) -> bool:
    """True if macro calendar row is likely to move XAUUSD."""
    text = f"{region} {event}".strip()
    lower = text.lower()
    for pat in _NOISE_EVENT_PATTERNS:
        if pat.search(text):
            return False
    if any(k in lower for k in GOLD_MACRO_EVENT_KEYWORDS):
        return True
    if region in _GOLD_MACRO_REGIONS and importance is not None and importance >= 3:
        return True
    return False
