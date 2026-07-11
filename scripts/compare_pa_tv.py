"""Compare DGT PA output with TradingView screenshot reference."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.analysis.dgt_price_action import analyze_dgt_price_action, build_volume_profile
from src.analysis.ict_pa import analyze_timeframe, sentiment_score
from src.analysis.price_action_facts import build_price_action_summaries
from src.analysis.report_engine import generate_trading_signals
from src.data.fetch_pipeline import fetch_all_data
from src.indicators.technical import enrich

TV_15M = {
    "poc": 4125.767,
    "vah": 4147.192,
    "val": 4074.188,
    "profile_high": 4180.520,
    "profile_low": 4021.815,
}


def _delta(ours: float | None, tv: float) -> str:
    if ours is None:
        return "n/a"
    return f"{ours - tv:+.2f}"


def main() -> None:
    fetched = fetch_all_data()
    enriched = {tf: enrich(df) for tf, df in fetched.raw.items()}
    price = float(enriched["5m"]["Close"].iloc[-1])
    print(f"price (OANDA 5m close): {price:.3f}")
    print(f"TV screenshot price:    4120.670")
    print()

    df15 = enriched["15m"]
    ltf = enriched["5m"]

    print("=== 15m Volume Profile vs TV (visible range) ===")
    for lookback in (120, 200, 360, 500, 800):
        window = df15.tail(lookback)
        profile_bars = ltf.loc[(ltf.index >= window.index[0]) & (ltf.index <= window.index[-1])]
        result = analyze_dgt_price_action(df15, "15m", lookback=lookback, profile_bars=profile_bars)
        vp = result.volume_profile
        if not vp or vp.poc is None:
            print(f"lookback={lookback}: no profile")
            continue
        print(
            f"lookback={lookback:3d} | POC {vp.poc} ({_delta(vp.poc, TV_15M['poc'])}) "
            f"VAH {vp.vah} ({_delta(vp.vah, TV_15M['vah'])}) "
            f"VAL {vp.val} ({_delta(vp.val, TV_15M['val'])}) "
            f"range {vp.profile_low}-{vp.profile_high}"
        )

    # Approximate TV visible range (profile low ~4021)
    anchor = df15[df15["Low"] <= 4025]
    if not anchor.empty:
        start = anchor.index[0]
        vis_15m = df15.loc[start:]
        vis_5m = ltf.loc[ltf.index >= start]
        vp_vis = build_volume_profile(vis_5m)
        print()
        print(f"visible-style window from {start} ({len(vis_15m)} x 15m bars)")
        if vp_vis.poc:
            print(
                f"  POC {vp_vis.poc} ({_delta(vp_vis.poc, TV_15M['poc'])}) "
                f"VAH {vp_vis.vah} ({_delta(vp_vis.vah, TV_15M['vah'])}) "
                f"VAL {vp_vis.val} ({_delta(vp_vis.val, TV_15M['val'])}) "
                f"range {vp_vis.profile_low}-{vp_vis.profile_high}"
            )

    print()
    print("=== Default pipeline PA summaries ===")
    pa = build_price_action_summaries(enriched)
    for tf in ("5m", "15m"):
        vp = (pa.get(tf) or {}).get("volume_profile") or {}
        print(f"{tf}: POC={vp.get('poc')} VAH={vp.get('vah')} VAL={vp.get('val')} "
              f"hi={vp.get('profile_high')} lo={vp.get('profile_low')}")
        sr = pa[tf].get("sr_levels") or []
        near = [x for x in sr if abs(float(x["price"]) - price) < 30]
        print(f"  S/R near price: {[(x['price'], x.get('label')) for x in near[-6:]]}")

    print()
    print("=== SMC OB on 15m (Lux) ===")
    analyses = {tf: analyze_timeframe(enriched[tf], tf) for tf in ("5m", "15m", "1h", "4h")}
    for ob in analyses["15m"].order_blocks[-5:]:
        print(f"  OB {ob.direction}: {ob.low:.1f}-{ob.high:.1f}")

    print()
    print("=== Trading plans (5m PA primary) ===")
    metrics = {
        "daily_high": float(enriched["1d"]["High"].iloc[-1]),
        "daily_low": float(enriched["1d"]["Low"].iloc[-1]),
    }
    signals = generate_trading_signals(
        price,
        analyses["5m"],
        analyses["15m"],
        analyses["4h"].swing_high or 0,
        analyses["4h"].swing_low or 0,
        sentiment_score(analyses),
        price_action=pa,
        metrics=metrics,
    )
    for sig in signals:
        smc = [r for r in sig.score_reasons if "SMC" in r or "共振" in r]
        print(f"  {sig.name}: {sig.entry_low}-{sig.entry_high} SL={sig.stop_loss}")
        print(f"    setup={sig.setup_type} | SMC filter: {smc}")


if __name__ == "__main__":
    main()
