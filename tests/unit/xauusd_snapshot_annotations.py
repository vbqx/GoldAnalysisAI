"""XAUUSD point-in-time snapshot annotations for report credibility (#32).

Each golden report may ship a sibling ``*.annotation.json`` describing must-have
facts, allowed prices, prohibited phrases, and expected observation/execution mode.
CI runs the deterministic (zero-token) subset only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "golden_reports"

REQUIRED_ANNOTATION_KEYS = (
    "id",
    "scenario",
    "must_appear",
    "allowed_prices",
    "prohibited_phrases",
    "expected_mode",
)


def annotation_path(report_name: str) -> Path:
    stem = Path(report_name).stem
    return FIXTURES / f"{stem}.annotation.json"


def load_annotation(report_name: str) -> dict[str, Any]:
    path = annotation_path(report_name)
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = [k for k in REQUIRED_ANNOTATION_KEYS if k not in data]
    if missing:
        raise AssertionError(f"{path.name}: missing keys {missing}")
    return data


def _report_text_blob(report: dict[str, Any]) -> str:
    return json.dumps(report, ensure_ascii=False)


def check_snapshot_annotation(
    report: dict[str, Any],
    annotation: dict[str, Any],
    *,
    invariant_codes: list[str] | None = None,
) -> list[str]:
    """Return human-readable violation messages (empty = pass)."""
    violations: list[str] = []
    blob = _report_text_blob(report)

    for phrase in annotation.get("must_appear") or []:
        if str(phrase) not in blob:
            violations.append(f"missing must_appear: {phrase}")

    for phrase in annotation.get("prohibited_phrases") or []:
        if str(phrase) in blob:
            violations.append(f"prohibited phrase present: {phrase}")

    expected_mode = str(annotation.get("expected_mode") or "").lower()
    meta = report.get("meta") or {}
    decision = meta.get("manager_decision") or meta.get("final_decision") or {}
    action = str(decision.get("action") or "").lower()
    conclusion = report.get("conclusion") or {}
    header = str(conclusion.get("header_conclusion") or "")
    if expected_mode in ("", "any"):
        pass
    elif expected_mode == "wait":
        if action and action not in ("wait", "hold", "observe", "reduce"):
            violations.append(f"expected_mode wait but manager action={action}")
        if meta.get("execution_authorized") is True:
            violations.append("expected_mode wait but execution_authorized=true")
        if header and "执行" in header and "观望" not in header and "等待" not in header:
            violations.append(f"expected wait header, got: {header}")
    elif expected_mode == "execute":
        if meta.get("execution_authorized") is not True:
            violations.append("expected_mode execute but execution_authorized is not true")
    elif expected_mode == "observe":
        if meta.get("observation_mode") is not True and action not in ("wait", "observe"):
            violations.append("expected_mode observe but observation_mode/action mismatch")

    expected_codes = annotation.get("expect_invariant_codes") or []
    if expected_codes:
        codes = set(invariant_codes or [])
        for code in expected_codes:
            if code not in codes:
                violations.append(f"missing expected invariant code: {code}")

    allowed = annotation.get("allowed_prices")
    if allowed is not None:
        allowed_set = {float(x) for x in allowed}
        geometry_prices: set[float] = set()
        for signal in report.get("signals") or []:
            for key in ("entry_low", "entry_high", "stop_loss"):
                if signal.get(key) is not None:
                    geometry_prices.add(float(signal[key]))
            for tp in signal.get("take_profits") or []:
                geometry_prices.add(float(tp))
        metrics = report.get("metrics") or {}
        for key in ("current_price", "daily_low", "daily_high", "prev_close"):
            if metrics.get(key) is not None:
                geometry_prices.add(float(metrics[key]))
        extras = sorted(p for p in geometry_prices if not any(abs(p - a) < 1e-6 for a in allowed_set))
        if extras:
            violations.append(f"unauthorized geometry prices: {extras}")

    return violations


def iter_annotated_snapshots() -> list[tuple[str, dict[str, Any], dict[str, Any]]]:
    rows: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    for ann_path in sorted(FIXTURES.glob("*.annotation.json")):
        report_name = ann_path.name.replace(".annotation.json", ".json")
        report_path = FIXTURES / report_name
        if not report_path.exists():
            raise AssertionError(f"annotation without report: {ann_path.name}")
        report = json.loads(report_path.read_text(encoding="utf-8"))
        annotation = load_annotation(report_name)
        rows.append((report_name, report, annotation))
    return rows
