"""Social sentiment — Reddit public JSON (r/Gold, r/Forex)."""

from __future__ import annotations

import re

from src.config import REDDIT_ENABLED
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

_SUBREDDITS = ("Gold", "Forex")
_REDDIT_BASES = ("https://www.reddit.com", "https://old.reddit.com")
_REDDIT_UA = "GoldAnalysisAI/1.0 (+https://github.com/vbqx/GoldAnalysisAI; sentiment bot)"


def _fetch_subreddit_posts(subreddit: str, *, limit: int = 15) -> list[dict]:
    last_exc: Exception | None = None
    for base in _REDDIT_BASES:
        url = f"{base}/r/{subreddit}/hot.json"
        try:
            data = get_json(
                url,
                params={"limit": limit, "raw_json": 1},
                headers={"User-Agent": _REDDIT_UA},
            )
            children = (data.get("data") or {}).get("children") or []
            posts: list[dict] = []
            for child in children:
                if not isinstance(child, dict):
                    continue
                post = child.get("data") or {}
                title = str(post.get("title", "")).strip()
                if not title or post.get("stickied"):
                    continue
                posts.append(
                    {
                        "title": title,
                        "score": int(post.get("score") or 0),
                        "upvote_ratio": float(post.get("upvote_ratio") or 0.5),
                        "subreddit": subreddit,
                    }
                )
            if posts:
                return posts
        except Exception as exc:
            last_exc = exc
            log.debug("reddit %s via %s failed: %s", subreddit, base, exc)
    if last_exc:
        raise last_exc
    return []


def _score_post(title: str) -> int:
    bull = len(_BULL_WORDS.findall(title))
    bear = len(_BEAR_WORDS.findall(title))
    return bull - bear


def fetch_social_sentiment() -> tuple[str, list[dict], dict]:
    """
    Return (summary text, evidence rows, refs).
    """
    if not REDDIT_ENABLED:
        return "—", [], {"source": "disabled"}

    try:
        posts: list[dict] = []
        for sub in _SUBREDDITS:
            posts.extend(_fetch_subreddit_posts(sub))

        if not posts:
            return "—", [], {"source": "placeholder", "error": "no posts"}

        bull_score = 0
        bear_score = 0
        samples: list[dict] = []
        for post in posts[:20]:
            delta = _score_post(post["title"])
            weight = max(post["score"], 1)
            if delta > 0:
                bull_score += weight
            elif delta < 0:
                bear_score += weight
            if abs(delta) > 0 and len(samples) < 5:
                samples.append(post)

        total = bull_score + bear_score
        if total == 0:
            summary = f"Reddit r/Gold+r/Forex：中性（{len(posts)} 帖 · 无明显方向关键词）"
            bias = "neutral"
        elif bull_score > bear_score * 1.2:
            pct = bull_score / total * 100
            summary = f"Reddit 偏多（{pct:.0f}% 加权 · {len(posts)} 帖）"
            bias = "bullish"
        elif bear_score > bull_score * 1.2:
            pct = bear_score / total * 100
            summary = f"Reddit 偏空（{pct:.0f}% 加权 · {len(posts)} 帖）"
            bias = "bearish"
        else:
            summary = f"Reddit 分歧（多 {bull_score} / 空 {bear_score} · {len(posts)} 帖）"
            bias = "neutral"

        refs = {
            "source": "reddit",
            "subreddits": list(_SUBREDDITS),
            "post_count": len(posts),
            "bias": bias,
            "bull_weight": bull_score,
            "bear_weight": bear_score,
        }
        return summary, samples, refs
    except Exception as exc:
        log.warning("reddit sentiment failed: %s", exc)
        return "—", [], {"source": "placeholder", "error": str(exc)}
