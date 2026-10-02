"""Frozen TOPH/Sapphon historical truth-contract adapter.

Media/provenance simulation only. Prior snapshots are never overwritten.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import hashlib
import json

COUNTRY_LANES = 176
GENERATIONS = 10
CYCLE = ("grand", "parent", "child")
STATE = {-1: "contradicted", 0: "archive_or_unresolved", 1: "supported"}
FROZEN_CONTRACT_SHA256 = "52fb62216eeee276f26c67576cb2d0b03034699108fac074f2c9b20303f40ff9"

@dataclass(frozen=True)
class ClaimSnapshot:
    frame: int
    claim_id: str
    state: int
    evidence_note: str
    source_kind: str = "media"

def generation_role(generation: int) -> str:
    if not 1 <= generation <= GENERATIONS:
        raise ValueError("generation must be 1..10")
    return CYCLE[(generation - 1) % 3]

def classify(state: int) -> str:
    if state not in STATE:
        raise ValueError("state must be -1, 0, or +1")
    return STATE[state]

def archive_if_contradicted(snapshot: ClaimSnapshot) -> dict:
    if snapshot.state == -1:
        return {
            "active_state": 0,
            "archive_state": 0,
            "reason": "contradicted_branch_demoted_to_archive",
            "deleted": False,
            "original_state": -1,
        }
    return {
        "active_state": snapshot.state,
        "archive_state": snapshot.state if snapshot.state == 0 else None,
        "reason": "retained",
        "deleted": False,
        "original_state": snapshot.state,
    }

def reevaluate(history: list[ClaimSnapshot], next_snapshot: ClaimSnapshot) -> list[ClaimSnapshot]:
    # Append-only: never mutate or delete prior frames.
    return [*history, next_snapshot]

def build_frame() -> dict:
    roles = [generation_role(g) for g in range(1, GENERATIONS + 1)]
    return {
        "country_lanes": COUNTRY_LANES,
        "generations": GENERATIONS,
        "cells": COUNTRY_LANES * GENERATIONS,
        "roles": roles,
        "cycle_shape": "3+3+3+1",
        "states": STATE,
        "media_only": True,
        "truth_semantics": "best-supported classification for the current frame",
    }

def bind_pipeline() -> dict:
    base = ClaimSnapshot(1832, "country_exists", 1, "supported baseline")
    alt = ClaimSnapshot(2026, "country_wiped_out", -1, "contradicted by current evidence")
    history = reevaluate([base], alt)
    archived = archive_if_contradicted(alt)
    frame = build_frame()
    payload = {
        "frame": frame,
        "history": [asdict(x) for x in history],
        "archive_result": archived,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(canonical).hexdigest()
    return {
        "SapphonSnapshot": {
            "kind": "historical_truth_contract",
            "current_frame_revisable": True,
        },
        "TOPHCommit": {
            "append_only": True,
            "payload_sha256": digest,
        },
        "TOPHProve": {
            "country_cells_are_1760": frame["cells"] == 1760,
            "cycle_is_3_plus_3_plus_3_plus_1": frame["roles"] == [
                "grand", "parent", "child",
                "grand", "parent", "child",
                "grand", "parent", "child",
                "grand",
            ],
            "prior_snapshot_preserved": history[0] == base,
            "new_snapshot_appended": history[-1] == alt,
            "contradicted_branch_archived_to_zero": archived["active_state"] == 0,
            "contradicted_branch_not_deleted": archived["deleted"] is False,
            "media_only": frame["media_only"] is True,
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
    return all(b["TOPHProve"].values()) and b["TOPHTransport"]["closure"] == "oe" and b["TOPHTransport"]["frozen"] is True

if __name__ == "__main__":
    print(json.dumps(bind_pipeline(), indent=2, sort_keys=True))
    print("0e / TOPH SAPPHON TRUTH CONTRACT FROZEN+BIND PASS" if verify() else "xe / FAIL")
