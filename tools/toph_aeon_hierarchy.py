"""Unified hierarchical view for TOPH as an Aeon."""
from __future__ import annotations
import json
from pathlib import Path

_DATA = Path(__file__).resolve().parents[1] / "data" / "toph_aeon_hierarchy.json"

def hierarchy() -> dict:
    return json.loads(_DATA.read_text(encoding="utf-8"))

def verify() -> bool:
    h = hierarchy()
    return (
        h["identity"]["name"] == "TOPH"
        and h["identity"]["kind"] == "aeon"
        and h["identity"]["lineage"] == "sapphonic"
        and h["identity"]["core"] == "green"
        and h["identity"]["storage"] == "emerald"
        and h["identity"]["temperament"] == "emerald"
        and h["root"]["qd_volume"] == 8
        and h["gravity"]["aggregate_ratio"] == "1000:1"
        and h["toroid"]["addressed_states"] == 366
        and h["toroid"]["rings"] == 20
        and h["corpus"]["photon_scale"] == 7200
        and h["corpus"]["tetraphasic_order"] == ["solid","liquid","gas","plasma"]
        and h["metronome"]["invariant_7200"] == "60*40*3"
        and h["foam"]["normalized_cells_per_dot"] == 400
        and h["policy"]["frozen_kernel_modified"] is False
    )
