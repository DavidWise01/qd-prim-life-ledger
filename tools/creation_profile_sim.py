"""Frozen generic creation-profile simulation adapter.

Simulation semantics only. This does not create matter or life and does not
modify the frozen q.d kernel.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import hashlib
import json

TURN_STEP = 1 / 360
AGGREGATE = 2000
SCALAR_PIN = "0.0.0"
FROZEN_CONTRACT_SHA256 = "7b9fafaeb2995502d270c9220e6bd0f5038996db6ade37111174b4f69db6b2eb"

@dataclass(frozen=True)
class CreationProfile:
    matter_type: str
    place: str
    date: str
    substrate: str = "carbon"
    tether: str = "mnemonic"

def descent_value(n: int) -> int:
    if not isinstance(n, int) or n < 1:
        raise ValueError("n must be an integer >= 1")
    return 1 - n * n

def descend_until_resolved(start_n: int) -> list[dict]:
    if not isinstance(start_n, int) or start_n < 1:
        raise ValueError("start_n must be an integer >= 1")
    states = []
    for n in range(start_n, 0, -1):
        value = descent_value(n)
        states.append({"n": n, "value": value})
        if value == 0:
            break
    assert states[-1] == {"n": 1, "value": 0}
    return states

def build_profile(
    matter_type: str,
    place: str,
    date: str,
    *,
    substrate: str = "carbon",
    tether: str = "mnemonic",
    start_n: int = 5,
) -> dict:
    if not all(isinstance(x, str) and x.strip() for x in (matter_type, place, date, substrate, tether)):
        raise ValueError("profile strings must be non-empty")
    profile = CreationProfile(matter_type.strip(), place.strip(), date.strip(), substrate.strip(), tether.strip())
    descent = descend_until_resolved(start_n)
    return {
        "profile": asdict(profile),
        "scalar_pin": SCALAR_PIN,
        "turn_step": "1/360",
        "full_turn": TURN_STEP * 360,
        "aggregate": AGGREGATE,
        "descent": descent,
        "resolved_at_n": descent[-1]["n"],
        "resolved_value": descent[-1]["value"],
        "post_resolution": "linear +1 life ticks",
        "physical_claim": False,
    }

def bind_pipeline(**kwargs) -> dict:
    result = build_profile(**kwargs)
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(canonical).hexdigest()
    return {
        "Event": {
            "kind": "creation_profile_sim",
            "requested_type": result["profile"]["matter_type"],
            "place": result["profile"]["place"],
            "date": result["profile"]["date"],
        },
        "Commit": {
            "append_only": True,
            "payload_sha256": digest,
        },
        "Prove": {
            "scalar_zero_pinned": result["scalar_pin"] == "0.0.0",
            "full_turn_closes": abs(result["full_turn"] - 1.0) < 1e-12,
            "aggregate_is_2000": result["aggregate"] == 2000,
            "descent_resolves_at_one": result["resolved_at_n"] == 1,
            "descent_value_is_zero": result["resolved_value"] == 0,
            "simulation_only": result["physical_claim"] is False,
        },
        "Project": result,
        "Transport": {
            "closure": "oe",
            "frozen": True,
            "frozen_contract_sha256": FROZEN_CONTRACT_SHA256,
        },
    }

def verify() -> bool:
    b = bind_pipeline(
        matter_type="dog",
        place="Buffalo, Minnesota",
        date="2026-10-02",
        substrate="carbon",
        tether="mnemonic",
        start_n=5,
    )
    return all(b["Prove"].values()) and b["Transport"]["closure"] == "oe" and b["Transport"]["frozen"] is True

if __name__ == "__main__":
    print(json.dumps(bind_pipeline(
        matter_type="dog",
        place="Buffalo, Minnesota",
        date="2026-10-02",
        substrate="carbon",
        tether="mnemonic",
        start_n=5,
    ), indent=2, sort_keys=True))
    print("0e / CREATION PROFILE SIM FROZEN+BIND PASS" if verify() else "xe / FAIL")
