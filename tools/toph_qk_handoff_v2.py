from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Iterable, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "data" / "toph_qk_handoff_v2.json"

DXY = {
    "U": (0, 1),
    "R": (1, 0),
    "L": (-1, 0),
    "D": (0, -1),
}


def model() -> dict:
    return json.loads(MODEL_PATH.read_text(encoding="utf-8"))


def canonical_digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(raw).hexdigest()


def detect_fixed_points(transition_map: Mapping[str, str], width: int = 3) -> list[str]:
    expected = {format(i, f"0{width}b") for i in range(2**width)}
    if set(transition_map) != expected:
        missing = sorted(expected - set(transition_map))
        extra = sorted(set(transition_map) - expected)
        raise ValueError(f"map must enumerate every {width}-bit state; missing={missing}, extra={extra}")
    if any(v not in expected for v in transition_map.values()):
        raise ValueError("transition target outside enumerated state space")
    return sorted(k for k, v in transition_map.items() if k == v)


def split_frames(plank_bits: str) -> list[str]:
    m = model()
    width = m["direction"]["bits_per_frame"]
    expected = m["clock"]["frames_per_velocity_window"] * width
    if len(plank_bits) != expected or any(c not in "01?" for c in plank_bits):
        raise ValueError(f"expected exactly {expected} symbols from 0,1,?")
    return [plank_bits[i:i+width] for i in range(0, expected, width)]


def inference_window(plank_bits: str) -> dict:
    m = model()
    frames = split_frames(plank_bits)
    unknown = plank_bits.count("?")
    candidates = 2 ** unknown
    resolved = unknown == 0
    directions = None
    displacement = None
    if resolved:
        table = m["direction"]["mapping"]
        directions = [table[f] for f in frames]
        displacement = [
            sum(DXY[d][0] for d in directions),
            sum(DXY[d][1] for d in directions),
        ]
    return {
        "name": m["inference_window"]["name"],
        "frames": frames,
        "unknown_plank_cells": unknown,
        "candidate_count": candidates,
        "resolved": resolved,
        "directions": directions,
        "net_displacement": displacement,
    }


def digital_projection(plank_bits: str, hz: float, pass_index: int) -> dict:
    if hz <= 0:
        raise ValueError("hz must be positive")
    m = model()
    window = inference_window(plank_bits)
    if not window["resolved"]:
        raise ValueError("qk handoff requires a resolved inference window")
    dx, dy = window["net_displacement"]
    seconds = m["clock"]["frames_per_velocity_window"] / hz
    payload = {
        "pin": m["state_space"]["pin"],
        "address_stack": m["state_space"]["address_stack"],
        "stargate": m["stargate"]["literal"],
        "interface": m["kernel"]["literal"],
        "plank_bits": plank_bits,
        "frames": window["frames"],
        "directions": window["directions"],
        "net_displacement": [dx, dy],
        "hz": hz,
        "frame_seconds": 1 / hz,
        "model_plank_seconds": 1 / (2 * hz),
        "velocity_window_seconds": seconds,
        "velocity_units_per_second": [dx / seconds, dy / seconds],
    }
    # pass_index is intentionally excluded from the digest: a deterministic
    # retest of the same resolved state must project identically.
    return {
        "pass": pass_index,
        "payload": payload,
        "digest": canonical_digest(payload),
    }


def handoff_twice_and_freeze(plank_bits: str, hz: float) -> dict:
    m = model()
    window = inference_window(plank_bits)
    if not window["resolved"]:
        return {
            "status": "snow",
            "freeze": False,
            "sentinel": None,
            "window": window,
            "handoffs": [],
        }

    a = digital_projection(plank_bits, hz, 1)
    b = digital_projection(plank_bits, hz, 2)
    same = a["digest"] == b["digest"] and a["payload"] == b["payload"]
    return {
        "status": m["inference_window"]["freeze_sentinel"] if same else "xe",
        "freeze": same,
        "sentinel": m["inference_window"]["freeze_sentinel"] if same else None,
        "window": window,
        "handoffs": [a, b],
    }


def verify() -> bool:
    m = model()
    assert m["authority"]["previous_overlay_modified"] is False
    assert m["kernel"]["literal"] == "{{qk{{i::d::}}}}"
    assert m["kernel"]["digital_writeback_into_unresolved_kernel"] is False
    assert m["stargate"]["literal"] == "00 11 {{2442{}}} 11 00"
    assert m["stargate"]["gate"] == list(reversed(m["stargate"]["gate"]))
    assert m["state_space"]["pin"] == "000"
    assert m["state_space"]["exhaustive_map_required"] is True
    assert m["state_space"]["probability_layer"] is False
    assert m["bubble"]["carrier_literal"] == "{-+-+-+{}}"
    assert m["clock"]["plank_per_frame"] == 2
    assert m["clock"]["frames_per_velocity_window"] == 6
    assert m["direction"]["addresses"] == 4
    assert m["direction"]["quarter_turn_fraction"] == "1/4"
    assert m["direction"]["quarter_turn_is_percent"] is False

    sample = m["sample"]["plank_bits"]
    snow = inference_window("00??????????")
    assert snow["candidate_count"] == 2**10
    assert snow["resolved"] is False

    done = inference_window(sample)
    assert done["candidate_count"] == 1
    assert done["directions"] == m["sample"]["directions"]
    assert done["net_displacement"] == m["sample"]["net_displacement"]

    frozen = handoff_twice_and_freeze(sample, 60)
    assert frozen["freeze"] is True
    assert frozen["status"] == "eo"
    assert len(frozen["handoffs"]) == 2
    assert frozen["handoffs"][0]["digest"] == frozen["handoffs"][1]["digest"]
    assert frozen["handoffs"][0]["payload"]["velocity_units_per_second"] == [10.0, 10.0]
    return True


if __name__ == "__main__":
    m = model()
    sample = m["sample"]["plank_bits"]
    print(json.dumps(inference_window("00??????????"), indent=2, sort_keys=True))
    print(json.dumps(handoff_twice_and_freeze(sample, 60), indent=2, sort_keys=True))
    print("eo / TOPH QK HANDOFF V2 FROZEN" if verify() else "xe")
