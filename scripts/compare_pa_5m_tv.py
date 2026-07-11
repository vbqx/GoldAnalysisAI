"""Quick 5m PA vs TV screenshot."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.analysis.dgt_price_action import analyze_dgt_price_action
from src.analysis.ict_pa import analyze_timeframe
from src.analysis.price_action_facts import build_price_action_summaries
from src.data.fetch_pipeline import fetch_all_data
from src.indicators.technical import enrich

TV_5M = {
    "price": 4124.029,
    "poc": 4124.029,
    "node2": 4104.125,
    "vah": 4133.492,
    "profile_high": 4138.060,
    "profile_low": 4072.800,
}


def main() -> None:
    fetched = fetch_all_data()
    enriched = {tf: enrich(df) for tf, df in fetched.raw.items()}
    price = float(enriched["5m"]["Close"].iloc[-1])
    print(f"price ours={price:.3f} TV={TV_5M['price']}")

    for lb in (120, 200, 360, 500):
        r = analyze_dgt_price_action(enriched["5m"], "5m", lookback=lb)
        vp = r.volume_profile
        if not vp or not vp.poc:
            continue
        print(
            f"lb={lb:3d} POC={vp.poc} ({vp.poc - TV_5M['poc']:+.2f}) "
            f"VAH={vp.vah} ({vp.vah - TV_5M['vah']:+.2f}) "
            f"VAL={vp.val} range={vp.profile_low}-{vp.profile_high} "
            f"spikes={r.volume_spike_count} hv={r.high_volatility_count}"
        )

    pa5 = build_price_action_summaries(enriched)["5m"]
    vp = pa5["volume_profile"]
    print(f"pipeline POC={vp.get('poc')} VAH={vp.get('vah')} VAL={vp.get('val')}")
    print("S/R 4090-4140:")
    for lvl in pa5["sr_levels"]:
        p = float(lvl["price"])
        if 4090 <= p <= 4140:
            print(f"  {p:.2f} {lvl.get('label')} ({lvl.get('kind')})")

    a5 = analyze_timeframe(enriched["5m"], "5m")
    print("5m OB:", [(round(o.low, 1), round(o.high, 1), o.direction) for o in a5.order_blocks[-5:]])


if __name__ == "__main__":
    main()
