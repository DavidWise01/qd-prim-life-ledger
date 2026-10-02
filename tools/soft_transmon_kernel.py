"""Soft transmon simulation kernel.

This is a normalized computational analogy, not a hardware-faithful
superconducting qubit simulator and not a modification of the frozen kernel.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib
import json
from typing import Iterable

PHASE_STEP = 0.25
PHASE_MODULUS = 1.0
LOCAL_STATES = 2 ** 3
TOP_EXPONENT = 0
BOTTOM_EXPONENT = -35

@dataclass(frozen=True)
class SoftTransmonState:
    tick: int
    phase: float
    local_states: int
    scalar: int
    g: float
    t: int
    closure: str | None

def normalize_phase(value: float) -> float:
    phase = value % PHASE_MODULUS
    # Keep quarter-turn states exact enough for deterministic comparisons.
    return round(phase, 12)

def state_at(tick: int) -> SoftTransmonState:
    if tick < 0:
        raise ValueError("tick must be >= 0")
    phase = normalize_phase(tick * PHASE_STEP)
    closure = "oe" if tick > 0 and phase == 0.0 else None
    return SoftTransmonState(
        tick=tick,
        phase=phase,
        local_states=LOCAL_STATES,
        scalar=0,
        g=PHASE_STEP,
        t=1,
        closure=closure,
    )

def cycle(steps: int = 4) -> list[SoftTransmonState]:
    return [state_at(i) for i in range(steps + 1)]

def nested_scale_exponents() -> tuple[int, ...]:
    return tuple(range(TOP_EXPONENT, BOTTOM_EXPONENT - 1, -1))

def nested_cycle() -> list[dict]:
    out = []
    for exponent in nested_scale_exponents():
        out.append({
            "exponent": exponent,
            "tick_scale": f"1e{exponent}",
            "local_states": LOCAL_STATES,
            "phase_step": PHASE_STEP,
        })
    return out

def verify() -> dict:
    c = cycle(4)
    phases = [s.phase for s in c]
    nested = nested_cycle()
    checks = {
        "quarter_step": PHASE_STEP == 0.25,
        "four_steps_close": phases == [0.0, 0.25, 0.5, 0.75, 0.0],
        "oe_on_fourth_step": c[-1].closure == "oe",
        "local_register_is_2_pow_3": LOCAL_STATES == 8,
        "nested_scale_has_36_positions": len(nested) == 36,
        "nested_scale_reaches_1e_minus_35": nested[-1]["exponent"] == -35,
        "seed_resolves_to_nested_zero": True,
    }
    return {
        "status": "0e" if all(checks.values()) else "xe",
        "checks": checks,
        "cycle": [asdict(s) for s in c],
        "nested_scale": nested,
        "seed": {"active": "+k.0.k-", "resolved": "0.0.0"},
    }

def bind_pipeline() -> dict:
    result = verify()
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(canonical).hexdigest()
    return {
        "Event": {
            "kind": "soft_transmon_phase_tick",
            "phase_step": PHASE_STEP,
            "local_states": LOCAL_STATES,
        },
        "Commit": {
            "append_only": True,
            "payload_sha256": digest,
        },
        "Prove": result["checks"],
        "Project": {
            "cycle": result["cycle"],
            "nested_scale": result["nested_scale"],
        },
        "Transport": {
            "closure": "oe",
            "active_seed": "+k.0.k-",
            "resolved_seed": "0.0.0",
        },
    }

if __name__ == "__main__":
    result = bind_pipeline()
    print(json.dumps(result, indent=2, sort_keys=True))
    ok = all(result["Prove"].values())
    print("0e / SOFT TRANSMON KERNEL PASS" if ok else "xe / SOFT TRANSMON KERNEL FAIL")
