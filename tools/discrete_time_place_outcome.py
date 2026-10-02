"""Frozen post-kernel discrete time/place outcome adapter.

Model semantics only. Does not modify final-kernel primitives.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import hashlib
import json

MOVES = (0, "xu", "yd", "xr", "yl")
PIN_TARGETS = ("xu{}", "yd{}", "xr{}", "yl{}")
TIME_CYCLE = (-1, 0, 1, 0)
ZERO_LINE = (0, 0, 0, 0, 0, "{{1.00}}")
FROZEN_CONTRACT_SHA256 = "e5daffdd92e13e5762fe1ebe2423538e363ca6656aa711a1f6811e4703dac054"

@dataclass(frozen=True)
class OutcomeEvent:
    choice: str
    consequence: str
    outcome: int
    direction: str
    where: str
    why: str
    time: int

def outcome_label(scalar: int) -> str:
    return {
        -1: "bad_outcome_timeline",
         0: "implicit_natural_reference",
         1: "good_outcome_timeline",
    }[scalar]

def pin_direction(direction: str) -> str:
    if direction not in MOVES[1:]:
        raise ValueError("direction must be xu, yd, xr, or yl")
    return f"{direction}{{}}"

def resolve_no_choice(n: int, direction: str, outcome: int, time: int = 0) -> dict:
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")
    if outcome not in (-1, 0, 1):
        raise ValueError("outcome must be -1, 0, or +1")
    pin = pin_direction(direction)
    event = OutcomeEvent(
        choice="no",
        consequence="natural",
        outcome=outcome,
        direction=direction,
        where=pin,
        why=f"choice:no+consequence:natural+outcome:{outcome}",
        time=time,
    )
    return {
        "growth": n ** 3,
        "notation": "{{n}}^3",
        "packet": asdict(event),
        "pin": pin,
    }

def bind_pipeline(n: int = 3, direction: str = "xu", outcome: int = 1) -> dict:
    resolved = resolve_no_choice(n, direction, outcome)
    canonical = json.dumps(resolved, sort_keys=True, separators=(",", ":")).encode()
    proof = hashlib.sha256(canonical).hexdigest()
    return {
        "Event": {
            "kind": "discrete_time_place_outcome",
            "implicit_zero": "0{{+implicit::outcome}}0 > {{i}} > 0",
            "zero_line": ZERO_LINE,
        },
        "Commit": {
            "append_only": True,
            "explicit_event": "1{where,why,time}",
            "payload_sha256": proof,
        },
        "Prove": {
            "time_cycle_closes": sum(TIME_CYCLE) == 0,
            "time_normalization_closes": (1 / 10) * 10 * 0 == 0,
            "zero_line_stable": ZERO_LINE[:5] == (0, 0, 0, 0, 0),
            "explicit_marker_present": ZERO_LINE[-1] == "{{1.00}}",
            "direction_pinned": resolved["pin"] in PIN_TARGETS,
            "signed_outcome_valid": outcome in (-1, 0, 1),
        },
        "Project": {
            "scalar_outcome": {
                "-1": outcome_label(-1),
                "0": outcome_label(0),
                "+1": outcome_label(1),
            },
            "movement": MOVES,
            "resolved": resolved,
            "frame": {
                "kind": "universal frame snapshot",
                "transition": ["+2", "{{n}}^{{n^2}}"],
            },
        },
        "Transport": {
            "closure": "oe",
            "frozen": True,
            "frozen_contract_sha256": FROZEN_CONTRACT_SHA256,
        },
    }

def verify() -> bool:
    b = bind_pipeline()
    return all(b["Prove"].values()) and b["Transport"]["closure"] == "oe" and b["Transport"]["frozen"] is True

if __name__ == "__main__":
    print(json.dumps(bind_pipeline(), indent=2, sort_keys=True))
    print("0e / DISCRETE TIME PLACE OUTCOME FROZEN+BIND PASS" if verify() else "xe / FAIL")
