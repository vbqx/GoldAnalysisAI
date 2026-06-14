"""Social sentiment — TradingView Ideas + Minds (XAUUSD community)."""

from __future__ import annotations

import re
from typing import Any

from src.config import TV_SOCIAL_ENABLED, TV_SOCIAL_IDEAS_LIMIT, TV_SOCIAL_MINDS_LIMIT, TV_SOCIAL_SYMBOL
from src.data.sources._http import get_json
from src.log import get_logger

log = get_logger(__name__)

_BULL_WORDS = re.compile(
    r"\b(bull|bullish|long|buy|moon|rally|breakout|support|squeeze|up)\b|"
    r"(做多|看多|上涨|突破|利好)",
    re.I,
)
_BEAR_WORDS = re.compile(
    r"\b(bear|bearish|short|sell|dump|crash|breakdown|resistance|down)\b|"
    r"(做空|看空|下跌|跌破|利空)",
    re.I,
)

_TV_BASE = "https://www.tradingview.com"
_DIRECTION_BIAS = {0: 0, 1: 1, 2: -1}


def _tv_headers(symbol: str) -> dict[str, str]:
    return {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Origin": _TV_BASE,
        "Referer": f"{_TV_BASE}/symbols/{symbol}/",
        "Accept": "application/json, text/plain, */*",
    }


def _score_text(text: str) -> int:
    bull = len(_BULL_WORDS.findall(text))
    bear = len(_BEAR_WORDS.findall(text))
    return bull - bear


def _flatten_ast(node: Any) -> str:
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if isinstance(node, list):
        return " ".join(_flatten_ast(part) for part in node).strip()
    if isinstance(node, dict):
        if node.get("type") == "symbol" and isinstance(node.get("params"), dict):
            return str(node["params"].get("text") or "")
        chunks = [_flatten_ast(node.get("text"))]
        if "children" in node:
            chunks.append(_flatten_ast(node["children"]))
        return " ".join(c for c in chunks if c).strip()
    return ""


def _idea_bias(item: dict) -> int:
    symbol = item.get("symbol") if isinstance(item.get("symbol"), dict) else {}
    direction = symbol.get("direction")
    try:
        mapped = _DIRECTION_BIAS.get(int(direction))
    except (TypeError, ValueError):
        mapped = None
    if mapped is not None and mapped != 0:
        return mapped
    text = f"{item.get('name', '')} {item.get('description', '')}"
    return _score_text(str(text))


def _mind_bias(item: dict) -> int:
    return _score_text(_flatten_ast(item.get("text_ast")))


def parse_tv_ideas(payload: dict) -> list[dict]:
    ideas = (payload.get("data") or {}).get("ideas") or {}
    inner = ideas.get("data") if isinstance(ideas, dict) else {}
    items = inner.get("items") if isinstance(inner, dict) else []
    if not isinstance(items, list):
        return []

    posts: list[dict] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        title = str(item.get("name") or "").strip()
        if not title:
            continue
        user = item.get("user") if isinstance(item.get("user"), dict) else {}
        posts.append(
            {
                "title": title,
                "author": str(user.get("username") or ""),
                "likes": int(item.get("likes_count") or 0),
                "comments": int(item.get("comments_count") or 0),
                "bias_delta": _idea_bias(item),
                "kind": "ideas",
            }
        )
    return posts


def parse_tv_minds(payload: dict) -> list[dict]:
    minds = (payload.get("data") or {}).get("minds") or {}
    results = minds.get("results") if isinstance(minds, dict) else []
    if not isinstance(results, list):
        return []

    posts: list[dict] = []
    for item in results:
        if not isinstance(item, dict):
            continue
        text = _flatten_ast(item.get("text_ast")).strip()
        if not text:
            continue
        author = item.get("author") if isinstance(item.get("author"), dict) else {}
        posts.append(
            {
                "title": text[:160],
                "author": str(author.get("username") or ""),
                "likes": int(item.get("total_likes") or 0),
                "comments": int(item.get("comments_count") or 0),
                "bias_delta": _mind_bias(item),
                "kind": "minds",
            }
        )
    return posts


def _fetch_tv_json(path: str, symbol: str) -> dict:
    url = f"{_TV_BASE}/symbols/{symbol}/{path}/?component-data-only=1"
    data = get_json(url, headers=_tv_headers(symbol))
    return data if isinstance(data, dict) else {}


def _collect_posts(symbol: str) -> list[dict]:
    posts: list[dict] = []
    posts.extend(parse_tv_ideas(_fetch_tv_json("ideas", symbol))[:TV_SOCIAL_IDEAS_LIMIT])
    posts.extend(parse_tv_minds(_fetch_tv_json("minds", symbol))[:TV_SOCIAL_MINDS_LIMIT])
    return posts


def _summarize(posts: list[dict]) -> tuple[str, str, int, int]:
    bull_score = 0
    bear_score = 0
    for post in posts:
        delta = int(post.get("bias_delta") or 0)
        if delta == 0:
            continue
        weight = max(int(post.get("likes") or 0), 1) + int(post.get("comments") or 0) // 5
        if delta > 0:
            bull_score += weight
        else:
            bear_score += weight

    total = bull_score + bear_score
    if total == 0:
        return (
            f"TV Ideas+Minds（{TV_SOCIAL_SYMBOL}）：中性（{len(posts)} 条 · 无明显方向）",
            "neutral",
            bull_score,
            bear_score,
        )
    if bull_score > bear_score * 1.2:
        pct = bull_score / total * 100
        return (
            f"TV 社区偏多（{pct:.0f}% 加权 · {len(posts)} 条 Ideas/Minds）",
            "bullish",
            bull_score,
            bear_score,
        )
    if bear_score > bull_score * 1.2:
        pct = bear_score / total * 100
        return (
            f"TV 社区偏空（{pct:.0f}% 加权 · {len(posts)} 条 Ideas/Minds）",
            "bearish",
            bull_score,
            bear_score,
        )
    return (
        f"TV 社区分歧（多 {bull_score} / 空 {bear_score} · {len(posts)} 条）",
        "neutral",
        bull_score,
        bear_score,
    )


def fetch_social_sentiment() -> tuple[str, list[dict], dict]:
    """Return (summary text, evidence rows, refs)."""
    if not TV_SOCIAL_ENABLED:
        return "—", [], {"source": "disabled"}

    symbol = TV_SOCIAL_SYMBOL.strip().upper() or "XAUUSD"
    try:
        posts = _collect_posts(symbol)
        if not posts:
            return (
                "TV 社区暂无数据（Ideas/Minds 为空，请确认 TV_SOCIAL_SYMBOL）",
                [],
                {"source": "placeholder", "error": "no ideas/minds"},
            )

        summary, bias, bull_score, bear_score = _summarize(posts)
        samples: list[dict] = []
        for post in posts:
            if post.get("bias_delta") and len(samples) < 5:
                samples.append(post)
            elif len(samples) < 5 and post.get("likes", 0) >= 10:
                samples.append(post)
        if len(samples) < 5:
            for post in sorted(posts, key=lambda p: int(p.get("likes") or 0), reverse=True):
                if post not in samples:
                    samples.append(post)
                if len(samples) >= 5:
                    break

        refs = {
            "source": "tradingview_social",
            "symbol": symbol,
            "post_count": len(posts),
            "ideas_count": sum(1 for p in posts if p.get("kind") == "ideas"),
            "minds_count": sum(1 for p in posts if p.get("kind") == "minds"),
            "bias": bias,
            "bull_weight": bull_score,
            "bear_weight": bear_score,
        }
        return summary, samples, refs
    except Exception as exc:
        log.warning("TradingView social sentiment failed: %s", exc)
        return (
            f"TV 社区拉取失败（{exc} · 请检查网络/代理）",
            [],
            {"source": "placeholder", "error": str(exc)},
        )
