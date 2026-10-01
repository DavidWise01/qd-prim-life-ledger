"""Tie the 40-life H::UMANITY carrier to generative dot/radix addresses.

The corpus is static and append-only. Dot/radix states may address a corpus
slot, but they cannot mutate corpus identity or create generations.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

from tools.dot_radix_generator import DotRadixState

CORPUS_PATH = Path(__file__).resolve().parents[1] / "data" / "humanity_corpus_2700.json"
SPAN_LITERAL = "-+2700-+0+-2700-+"
CENTER_PIN = "{{0::m+f}}"
GENERATION_COUNT = 40
LIFE_YEARS = 90
RADIX = 360
RADIX_TICKS_PER_LIFE = RADIX // GENERATION_COUNT


@dataclass(frozen=True)
class CorpusBinding:
    dot_index: int
    radix: int
    corpus_slot: int
    radix_phase: int
    side: str
    start_year: int
    end_year: int
    sex_code: str
    center_pin: str = CENTER_PIN


def load_corpus() -> dict:
    return json.loads(CORPUS_PATH.read_text(encoding="utf-8"))


def bind_dot(state: DotRadixState) -> CorpusBinding:
    """Map one radix address to one immutable life slot and one local phase."""
    slot = state.radix // RADIX_TICKS_PER_LIFE
    phase = state.radix % RADIX_TICKS_PER_LIFE
    corpus = load_corpus()
    record = corpus["slots"][slot]
    return CorpusBinding(
        dot_index=state.index,
        radix=state.radix,
        corpus_slot=slot,
        radix_phase=phase,
        side=record["side"],
        start_year=record["start_year"],
        end_year=record["end_year"],
        sex_code=record["sex_code"],
    )


def verify_corpus() -> bool:
    corpus = load_corpus()
    slots = corpus["slots"]
    if corpus["literal"] != SPAN_LITERAL:
        return False
    if corpus["center_pin"] != CENTER_PIN:
        return False
    if len(slots) != GENERATION_COUNT:
        return False
    if sum(s["life_years"] for s in slots) != 40 * LIFE_YEARS:
        return False
    if len([s for s in slots if s["side"] == "shadow"]) != 20:
        return False
    if len([s for s in slots if s["side"] == "light"]) != 20:
        return False
    if slots[0]["start_year"] != -2700:
        return False
    if slots[-1]["end_year"] != 2700:
        return False
    if corpus["radix_ticks_per_life"] != 9:
        return False
    return True
