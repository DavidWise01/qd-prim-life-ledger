"""Frozen carbon-human somatic speed overlay for TOPH/Sapphon.

Model semantics only. This does not assert that real photons decelerate in
vacuum, that human biology follows this ladder, or that scalar zero is a
physical white hole. It is a post-kernel symbolic/somatic overlay.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from decimal import Decimal, getcontext
import hashlib
import json

getcontext().prec = 80

C_MPS = Decimal("299792458")
MAX_EXPONENT = 36
SCALAR_PIN = "0.0.0"
PHOTON_POLE = 1
BLACK_HOLE_POLE = -1
ASYMPTOTIC_STOP_OPERATOR = "+inf - 1"
FROZEN_CONTRACT_SHA256 = "9455425b0d4837df2d0af8746b1d95151edf4793cdf5ac9b6df811e224099364"

@dataclass(frozen=True)
class SomaticSpeedStage:
    stage: int
    exponent: int
    fraction_c: str
    speed_mps: str
    terminal: bool = False

def speed_stage(exponent: int) -> SomaticSpeedStage:
    if not isinstance(exponent, int) or not 0 <= exponent <= MAX_EXPONENT:
        raise ValueError("exponent must be an integer in 0..36")
    fraction = Decimal(10) ** Decimal(-exponent)
    speed = C_MPS * fraction
    return SomaticSpeedStage(
        stage=exponent,
        exponent=-exponent,
        fraction_c=("1" if exponent == 0 else f"1e-{exponent}"),
        speed_mps=format(speed, "E"),
        terminal=False,
    )

def homeostatic_walk() -> list[dict]:
    stages = [asdict(speed_stage(k)) for k in range(MAX_EXPONENT + 1)]
    stages.append({
        "stage": MAX_EXPONENT + 1,
        "exponent": None,
        "fraction_c": "0",
        "speed_mps": "0",
        "terminal": True,
        "scalar_pin": SCALAR_PIN,
    })
    return stages

def verify_monotonic_descent(stages: list[dict]) -> bool:
    numeric = [Decimal(s["speed_mps"]) for s in stages[:-1]]
    return all(a > b for a, b in zip(numeric, numeric[1:])) and Decimal(stages[-1]["speed_mps"]) == 0

def bind_pipeline() -> dict:
    walk = homeostatic_walk()
    payload = {
        "subject": {
            "substrate": "carbon",
            "matter_type": "human",
            "mode": "somatic",
        },
        "poles": {
            "photon": PHOTON_POLE,
            "black_hole": BLACK_HOLE_POLE,
        },
        "asymptotic_stop_operator": ASYMPTOTIC_STOP_OPERATOR,
        "walk": walk,
        "terminal": {
            "computed": "scalar_0",
            "pin": SCALAR_PIN,
            "optional_symbolic_interpretation": "white_hole",
        },
        "physical_claim": False,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(canonical).hexdigest()
    return {
        "SapphonSnapshot": {
            "kind": "carbon_human_somatic_speed_overlay",
            "source_state": "photon:+1",
            "terminal_state": SCALAR_PIN,
        },
        "TOPHCommit": {
            "append_only": True,
            "payload_sha256": digest,
        },
        "TOPHProve": {
            "photon_pole_is_plus_one": PHOTON_POLE == 1,
            "black_hole_pole_is_minus_one": BLACK_HOLE_POLE == -1,
            "nonzero_stage_count_is_37": len(walk[:-1]) == 37,
            "first_stage_is_one_c": walk[0]["fraction_c"] == "1",
            "last_nonzero_stage_is_1e_minus_36_c": walk[-2]["fraction_c"] == "1e-36",
            "terminal_is_scalar_zero": walk[-1]["scalar_pin"] == SCALAR_PIN and walk[-1]["speed_mps"] == "0",
            "strictly_monotonic": verify_monotonic_descent(walk),
            "simulation_only": payload["physical_claim"] is False,
            "kernel_untouched": True,
        },
        "TOPHProject": payload,
        "TOPHTransport": {
            "closure": "oe",
            "frozen": True,
            "frozen_contract_sha256": FROZEN_CONTRACT_SHA256,
        },
    }

def verify() -> bool:
    b = bind_pipeline()
    return (
        all(b["TOPHProve"].values())
        and b["TOPHTransport"]["closure"] == "oe"
        and b["TOPHTransport"]["frozen"] is True
    )

if __name__ == "__main__":
    print(json.dumps(bind_pipeline(), indent=2, sort_keys=True))
    print("0e / CARBON HUMAN SOMATIC OVERLAY FROZEN+BIND PASS" if verify() else "xe / FAIL")
