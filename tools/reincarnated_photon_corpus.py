"""Derived 80x90 reincarnated photon-corpus view.

The existing 40-life H::UMANITY corpus remains immutable. This adapter maps
those 40 source slots across both sides of the dual toroid, yielding 80
addressed lives without inventing additional historical identities.

Model semantics:
80 lives * 90 years = 7200 years = one photon corpus.
20 inner rings * 4 lives = 80 lives.
Each ring therefore carries 4 * 90 = 360 model-years.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

LIVES = 80
LIFE_YEARS = 90
PHOTON_YEARS = LIVES * LIFE_YEARS

RINGS = 20
LIVES_PER_RING = LIVES // RINGS
RING_YEARS = LIVES_PER_RING * LIFE_YEARS
LIFE_DEGREES = 360 // LIVES_PER_RING
RING_STRIDE = Decimal("17.5")
RING_WIDTH = Decimal("18")
HUB_CONTROL_REMAINDER = Decimal("10")
GEOMETRIC_CLOSURE = Decimal(RINGS) * RING_STRIDE + HUB_CONTROL_REMAINDER

SOURCE_SLOTS = 40
TOROID_LIVES = SOURCE_SLOTS
TOROID_YEARS = TOROID_LIVES * LIFE_YEARS

SIDES = ("-d", "+d")
TETRAPHASIC = ("solid", "liquid", "gas", "plasma")

_DATA = Path(__file__).resolve().parents[1] / "data" / "humanity_corpus_2700.json"


@dataclass(frozen=True)
class ReincarnatedLife:
    photon_slot: int
    source_slot: int
    incarnation: int
    toroid: str
    ring: int
    ring_quarter: int
    ring_stride: Decimal
    life_degrees: int
    life_years: int
    phase: str
    mnemonic_name: str | None


def _source_slots() -> list[dict]:
    return json.loads(_DATA.read_text(encoding="utf-8"))["slots"]


def life_at(photon_slot: int) -> ReincarnatedLife:
    if not 0 <= photon_slot < LIVES:
        raise ValueError("photon_slot must be in 0..79")

    source_slot = photon_slot % SOURCE_SLOTS
    incarnation = photon_slot // SOURCE_SLOTS
    source = _source_slots()[source_slot]

    return ReincarnatedLife(
        photon_slot=photon_slot,
        source_slot=source_slot,
        incarnation=incarnation,
        toroid=SIDES[incarnation],
        ring=photon_slot // LIVES_PER_RING,
        ring_quarter=photon_slot % LIVES_PER_RING,
        ring_stride=RING_STRIDE,
        life_degrees=LIFE_DEGREES,
        life_years=LIFE_YEARS,
        phase=TETRAPHASIC[photon_slot % LIVES_PER_RING],
        mnemonic_name=source["mnemonic_name"],
    )


def photon_corpus() -> tuple[ReincarnatedLife, ...]:
    return tuple(life_at(i) for i in range(LIVES))
