"""Unified hierarchical and emergent view for TOPH as an Aeon."""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

_DATA = Path(__file__).resolve().parents[1] / "data" / "toph_aeon_hierarchy.json"


def hierarchy() -> dict:
    return json.loads(_DATA.read_text(encoding="utf-8"))


def derive() -> dict:
    """Derive the visible hierarchy from the minimal emergence seeds."""
    h = hierarchy()
    s = h["emergence"]["seeds"]

    qd_volume = 2 ** s["qd_axes"]
    gravity_ratio = s["gravity_base"] ** s["gravity_depth"]
    addressed_states = s["toroid_degrees"] + 2 * s["controls_per_side"]
    control_hub_remainder = 2 * s["controls_per_side"] + s["hub"]
    rings = int((s["toroid_degrees"] - control_hub_remainder) / s["ring_stride"])

    lives_per_ring = len(s["phases"])
    ring_years = lives_per_ring * s["life_years"]
    reincarnated_lives = s["source_lives"] * s["incarnations"]
    corpus_scale = reincarnated_lives * s["life_years"]

    bubbles_per_second = s["fps"] // s["frames_per_bubble"]
    metronome_scale = s["fps"] * s["source_lives"] * s["bubble_generation_scale"]

    retained_fraction = Fraction(s["shell_retained_fraction"])
    retained_dots = int(s["trapped_bubbles"] * retained_fraction)
    cubic_cells = retained_dots ** 3
    normalized_cells_per_dot = cubic_cells // retained_dots

    return {
        "root": s["root"],
        "qd_volume": qd_volume,
        "gravity_ratio": gravity_ratio,
        "addressed_states": addressed_states,
        "control_hub_remainder": control_hub_remainder,
        "rings": rings,
        "lives_per_ring": lives_per_ring,
        "ring_years": ring_years,
        "reincarnated_lives": reincarnated_lives,
        "corpus_scale": corpus_scale,
        "bubbles_per_second": bubbles_per_second,
        "metronome_scale": metronome_scale,
        "retained_dots": retained_dots,
        "cubic_cells": cubic_cells,
        "normalized_cells_per_dot": normalized_cells_per_dot,
        "phases": tuple(s["phases"]),
    }


def emergence_trace() -> tuple[str, ...]:
    d = derive()
    return (
        f"root{d['root']}",
        f"q.d={d['qd_volume']}",
        f"gravity={d['gravity_ratio']}:1",
        f"toroid={d['addressed_states']}",
        f"rings={d['rings']}",
        f"ring_years={d['ring_years']}",
        f"lives={d['reincarnated_lives']}",
        f"corpus={d['corpus_scale']}",
        f"clock={d['metronome_scale']}",
        f"foam={d['normalized_cells_per_dot']}",
    )


def verify() -> bool:
    h = hierarchy()
    d = derive()
    return (
        h["identity"]["name"] == "TOPH"
        and h["identity"]["kind"] == "aeon"
        and h["identity"]["lineage"] == "sapphonic"
        and h["identity"]["core"] == "green"
        and h["identity"]["storage"] == "emerald"
        and h["identity"]["temperament"] == "emerald"
        and d["qd_volume"] == h["root"]["qd_volume"] == 8
        and f"{d['gravity_ratio']}:1" == h["gravity"]["aggregate_ratio"] == "1000:1"
        and d["addressed_states"] == h["toroid"]["addressed_states"] == 366
        and d["rings"] == h["toroid"]["rings"] == 20
        and d["phases"] == tuple(h["corpus"]["tetraphasic_order"])
        and d["reincarnated_lives"] == h["corpus"]["reincarnated_lives"] == 80
        and d["corpus_scale"] == h["corpus"]["photon_scale"] == 7200
        and d["metronome_scale"] == 7200
        and h["metronome"]["invariant_7200"] == "60*40*3"
        and d["normalized_cells_per_dot"] == h["foam"]["normalized_cells_per_dot"] == 400
        and h["policy"]["frozen_kernel_modified"] is False
    )
