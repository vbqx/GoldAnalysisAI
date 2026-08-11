"""Deterministic consistency audit for Advice V2."""

from __future__ import annotations

from src.advice.types import AdviceAudit, AdvicePacket


def audit_advice(packet: AdvicePacket) -> AdviceAudit:
    violations: list[str] = []
    warnings: list[str] = []
    setup = packet.primary_setup

    if packet.decision in ("WATCH_LONG", "WATCH_SHORT") and setup is None:
        violations.append("watch decision requires primary_setup")
    if packet.decision in ("WAIT", "AVOID") and setup is not None:
        warnings.append("non-watch decision contains a setup")
    if setup is None:
        return AdviceAudit(passed=not violations, violations=violations, warnings=warnings)

    zone = setup.attention_zone
    if zone.low <= 0 or zone.high <= 0 or zone.low > zone.high:
        violations.append("invalid attention zone geometry")
    if not setup.evidence_ids:
        violations.append("primary setup has no evidence")
    if not setup.confirmation_checklist:
        violations.append("primary setup has no human confirmation checklist")
    if not setup.targets:
        violations.append("primary setup has no target")

    if setup.direction == "BUY":
        if packet.decision != "WATCH_LONG":
            violations.append("BUY setup conflicts with decision")
        if setup.invalidation_level >= zone.low:
            violations.append("BUY invalidation must be below attention zone")
        if any(target <= zone.high for target in setup.targets):
            violations.append("BUY targets must be above attention zone")
        if zone.low > packet.current_price:
            violations.append("BUY attention zone cannot be wholly above current price")
    else:
        if packet.decision != "WATCH_SHORT":
            violations.append("SELL setup conflicts with decision")
        if setup.invalidation_level <= zone.high:
            violations.append("SELL invalidation must be above attention zone")
        if any(target >= zone.low for target in setup.targets):
            violations.append("SELL targets must be below attention zone")
        if zone.high < packet.current_price:
            violations.append("SELL attention zone cannot be wholly below current price")

    if setup.reward_risk_to_targets and max(setup.reward_risk_to_targets) < 1.2:
        warnings.append("available target space is less than 1.2R")

    evidence_ids = {item.evidence_id for item in packet.evidence}
    missing = sorted(set(setup.evidence_ids) - evidence_ids)
    if missing:
        violations.append("setup references missing evidence: " + ", ".join(missing))
    return AdviceAudit(passed=not violations, violations=violations, warnings=warnings)
