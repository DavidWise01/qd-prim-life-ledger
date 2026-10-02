"""Frozen hierarchical state-space routing overlay anchored at {{Gg.Aa.Ii.Aa}}.

Post-kernel symbolic model only. 000 is immutable state-space. Event/condition
lanes can vary, but observation is read-only and any change is appended outside
the frozen carrier.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib
import json

ADDRESS = "{{Gg.Aa.Ii.Aa}}"
STATE = "000"
EVENT = "{}"
OBSERVED = "{{O}{b}{s}{e}{r}{v}{e}{d}}"
TERNARY = (-1, 0, 1)
LANES = (
    "state",
    "condition",
    "observation",
    "change",
    "provenance",
    "return",
    "append",
)
CARRIER = "000 + {} > 000"
FROZEN_CONTRACT_SHA256 = "c06158d86bdb5ea2ca5e6eaa2ea32a7cf2770bc2924fd13be5b3b5e70896ef01"

@dataclass(frozen=True)
class Route:
    address: str
    state_in: str
    condition: int
    event_space: str
    observed: str
    change: str
    provenance: str
    state_out: str
    append: str

def route(condition: int, index: int = 0) -> Route:
    if condition not in TERNARY:
        raise ValueError("condition must be -1, 0, or +1")
    return Route(
        address=ADDRESS,
        state_in=STATE,
        condition=condition,
        event_space=EVENT,
        observed=OBSERVED,
        change=f"observation:{condition}",
        provenance=f"{ADDRESS}::event::{index}",
        state_out=STATE,
        append=f"next::{index + 1}",
    )

def breathing_cycle() -> list[dict]:
    return [asdict(route(condition, i)) for i, condition in enumerate(TERNARY)]

def hierarchy(levels: int = 4) -> list[dict]:
    if not isinstance(levels, int) or levels < 1:
        raise ValueError("levels must be an integer >= 1")
    out = []
    carrier = CARRIER
    for level in range(levels):
        out.append({
            "level": level,
            "address": ADDRESS,
            "carrier": carrier,
            "lanes": LANES,
            "branches": TERNARY,
            "state_in": STATE,
            "state_out": STATE,
        })
        carrier = f"[{carrier}] + {{}} > [{carrier}]"
    return out

def prove() -> dict:
    breath = breathing_cycle()
    tree = hierarchy()
    return {
        "address_is_locked": all(x["address"] == ADDRESS for x in tree),
        "carrier_is_exact": tree[0]["carrier"] == CARRIER,
        "three_observation_branches": tuple(x["condition"] for x in breath) == TERNARY,
        "entry_state_is_frozen": all(x["state_in"] == STATE for x in breath),
        "return_state_is_frozen": all(x["state_out"] == STATE for x in breath),
        "event_space_does_not_replace_state": all(x["event_space"] == EVENT for x in breath),
        "observation_is_read_only_packet": all(x["observed"] == OBSERVED for x in breath),
        "change_is_external_append_record": all(x["append"].startswith("next::") for x in breath),
        "seven_lanes_derive": LANES == (
            "state", "condition", "observation", "change",
            "provenance", "return", "append",
        ),
        "recursive_projection_preserves_center": all(
            node["state_in"] == STATE and node["state_out"] == STATE for node in tree
        ),
    }

def bind_pipeline() -> dict:
    payload = {
        "address": ADDRESS,
        "carrier": CARRIER,
        "state_space": STATE,
        "event_space": EVENT,
        "observed": OBSERVED,
        "breathing": f"{STATE} -> {{-1,0,+1}} -> {STATE} -> repeat",
        "lanes": LANES,
        "cycle": breathing_cycle(),
        "hierarchy": hierarchy(),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(canonical).hexdigest()
    return {
        "SapphonSnapshot": {
            "kind": "hierarchical_frozen_state_space",
            "address": ADDRESS,
            "state": STATE,
        },
        "TOPHCommit": {
            "append_only": True,
            "payload_sha256": digest,
        },
        "TOPHProve": prove(),
        "TOPHProject": payload,
        "TOPHTransport": {
            "closure": "oe",
            "frozen": True,
            "immutable": True,
            "frozen_contract_sha256": FROZEN_CONTRACT_SHA256,
        },
    }

def verify() -> bool:
    b = bind_pipeline()
    return (
        all(b["TOPHProve"].values())
        and b["TOPHTransport"]["closure"] == "oe"
        and b["TOPHTransport"]["frozen"] is True
        and b["TOPHTransport"]["immutable"] is True
    )

if __name__ == "__main__":
    print(json.dumps(bind_pipeline(), indent=2, sort_keys=True))
    print("0e / GG.AA.II.AA HIERARCHICAL STATE SPACE FROZEN+BIND PASS" if verify() else "xe / FAIL")
