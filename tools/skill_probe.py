"""Append-only q.d skill probe.

This adapter does not modify the frozen kernel. It derives a bounded
capability level from already-committed q.d events.
"""
from __future__ import annotations

from dataclasses import dataclass

from src.qd_prim import QDLedger


@dataclass(frozen=True)
class SkillResult:
    level: int
    max_operands: int
    operator_mode: str
    evidence_plank: int | None
    valid_chain: bool


def _mode_for_operands(count: int) -> str:
    if count <= 0:
        return "none"
    if count == 1:
        return "unary"
    if count == 2:
        return "binary"
    return "ternary"


def assess_skill(ledger: QDLedger) -> SkillResult:
    """Return structural q.d skill level 0..5 from append-only evidence."""
    if not ledger.verify():
        raise ValueError("q.d chain failed provenance verification")

    best_count = 0
    best_plank: int | None = None

    for event in ledger.events:
        state = event.state
        if not isinstance(state, dict):
            continue
        operands = state.get("operands")
        if not isinstance(operands, (list, tuple)):
            continue
        count = len(operands)
        if not 1 <= count <= 5:
            continue

        declared = state.get("operator")
        expected = _mode_for_operands(count)
        if declared is not None and declared != expected:
            continue

        if count > best_count:
            best_count = count
            best_plank = event.plank

    return SkillResult(
        level=best_count,
        max_operands=best_count,
        operator_mode=_mode_for_operands(best_count),
        evidence_plank=best_plank,
        valid_chain=True,
    )
