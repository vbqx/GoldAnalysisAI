"""Generate chart HTML and print overlay summary for comparison."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.pipeline import run_analysis
from src.viz.lightweight_chart import build_lightweight_chart_html


def main() -> None:
    report, data, analyses = run_analysis()
    html = build_lightweight_chart_html(
        data["5m"],
        analysis=analyses["5m"],
        report=report,
        macro_analysis=analyses["15m"],
        timeframe="5m",
        symbol="XAUUSD",
        exchange="OANDA",
        height=520,
        bars=120,
    )
    out = ROOT / "_chart_test.html"
    out.write_text(f"<!DOCTYPE html><html><head><meta charset='utf-8'></head><body>{html}</body></html>", encoding="utf-8")

    m = re.search(r"const overlays = ({.*?});", html, re.S)
    overlays = json.loads(m.group(1)) if m else {}
    price = report["metrics"]["current_price"]
    a5 = analyses["5m"]

    print("=== Chart Compare Test ===")
    print(f"Price: {price:.2f}")
    print(f"5m bars: {len(data['5m'])}")
    print(f"5m trend: {a5.trend} | BOS events: {len(a5.events)}")
    print(f"Zones on chart: {len(overlays.get('zones', []))}")
    for z in overlays.get("zones", []):
        mid = (z["low"] + z["high"]) / 2
        dist = abs(mid - price)
        print(f"  [{z['kind']}] {z['title']} | dist={dist:.1f}")
    print(f"Markers: {[m['text'] for m in overlays.get('markers', [])]}")
    print(f"HTML saved: {out}")


if __name__ == "__main__":
    main()
