"""Infrastructure bridge: Soft Transmon -> Sapphon -> TOPH.

Simulation-only, append-only, and read-only with respect to frozen contracts.
"""
from __future__ import annotations

import hashlib
import json

from tools.soft_transmon_kernel import state_at, cycle
from tools.toph_sapphon_realign_v1 import verify as verify_toph_sapphon

def frame(tick: int) -> dict:
    s = state_at(tick)
    event = {
        "kind": "sapphon_soft_transmon_frame",
        "tick": s.tick,
        "phase": s.phase,
        "local_states": s.local_states,
        "scalar": s.scalar,
        "g": s.g,
        "t": s.t,
        "closure": s.closure,
        "origin": "0.0.0",
    }
    canonical = json.dumps(event, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(canonical).hexdigest()
    return {
        "SoftTransmonClock": {
            "tick": s.tick,
            "phase": s.phase,
            "local_states": s.local_states,
        },
        "SapphonSnapshot": {
            "globe": f"GLOBE[{s.tick}]",
            "origin": "0.0.0",
            "event": event,
        },
        "TOPHCommit": {
            "append_only": True,
            "sha256": digest,
        },
        "TOPHProve": {
            "phase_in_quarter_grid": s.phase in (0.0, 0.25, 0.5, 0.75),
            "local_states_2_pow_3": s.local_states == 8,
            "scalar_pinned_zero": s.scalar == 0,
            "toph_sapphon_realign_valid": verify_toph_sapphon(),
        },
        "TOPHProject": {
            "phase": s.phase,
            "closure": s.closure,
            "seed_active": "+k.0.k-",
            "seed_resolved": "0.0.0",
        },
        "TOPHTransport": {
            "next": f"GLOBE[{s.tick + 1}]",
            "oe": s.closure == "oe",
        },
    }

def verify_cycle() -> dict:
    frames = [frame(i) for i in range(5)]
    checks = {
        "phase_cycle": [f["SoftTransmonClock"]["phase"] for f in frames]
        == [0.0, 0.25, 0.5, 0.75, 0.0],
        "all_proofs_pass": all(all(f["TOPHProve"].values()) for f in frames),
        "append_only": all(f["TOPHCommit"]["append_only"] for f in frames),
        "oe_on_tick_4": frames[4]["TOPHTransport"]["oe"] is True,
        "no_early_oe": all(not frames[i]["TOPHTransport"]["oe"] for i in range(4)),
        "sapphon_globe_advances": [f["SapphonSnapshot"]["globe"] for f in frames]
        == [f"GLOBE[{i}]" for i in range(5)],
    }
    return {
        "status": "0e" if all(checks.values()) else "xe",
        "checks": checks,
        "frames": frames,
    }

if __name__ == "__main__":
    result = verify_cycle()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("0e / TOPH SAPPHON SOFT TRANSMON INFRA PASS" if result["status"] == "0e" else "xe")
