"""Memristic -+ spinor overlay for the TOPH Aeon model."""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path

_DATA = Path(__file__).resolve().parents[1] / "data" / "memristic_spinor_overlay.json"

SPINOR = ("-", "+")
LIVES_PER_SPINOR = 10
NOMINAL_LIFECYCLE_YEARS = 10_000
LIFECYCLE_MIN_YEARS = 8_000
LIFECYCLE_MAX_YEARS = 12_000
PHASE_SHIFT_YEARS = 3
ROTATION_STATES = ("-m", "+m", "-f", "+f")
CONTEXTS = ("advanced_tech", "dirt_poor")
QUARTET_YEARS = PHASE_SHIFT_YEARS * len(ROTATION_STATES)
CONTEXT_SWEEP_YEARS = QUARTET_YEARS * len(CONTEXTS)


@dataclass(frozen=True)
class MemristicPhase:
    index: int
    years_elapsed: int
    rotation: str
    context: str
    life_index: int
    parent_hash: str | None

    def digest(self) -> str:
        payload = json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def config() -> dict:
    return json.loads(_DATA.read_text(encoding="utf-8"))


def phase_at(index: int) -> MemristicPhase:
    if index < 0:
        raise ValueError("index must be >= 0")
    rotation = ROTATION_STATES[index % len(ROTATION_STATES)]
    context = CONTEXTS[(index // len(ROTATION_STATES)) % len(CONTEXTS)]
    life_index = (index * PHASE_SHIFT_YEARS // (NOMINAL_LIFECYCLE_YEARS // LIVES_PER_SPINOR)) % LIVES_PER_SPINOR

    parent_hash = None
    if index:
        parent_hash = phase_at(index - 1).digest()

    return MemristicPhase(
        index=index,
        years_elapsed=index * PHASE_SHIFT_YEARS,
        rotation=rotation,
        context=context,
        life_index=life_index,
        parent_hash=parent_hash,
    )


def context_sweep(start_index: int = 0) -> tuple[MemristicPhase, ...]:
    """Eight phases: every +/- sex state once in each simulation context."""
    return tuple(phase_at(start_index + i) for i in range(8))


def lifecycle_summary() -> dict:
    return {
        "spinor": "-+",
        "lives": LIVES_PER_SPINOR,
        "nominal_years": NOMINAL_LIFECYCLE_YEARS,
        "min_years": LIFECYCLE_MIN_YEARS,
        "max_years": LIFECYCLE_MAX_YEARS,
        "nominal_years_per_life": NOMINAL_LIFECYCLE_YEARS // LIVES_PER_SPINOR,
        "min_years_per_life": LIFECYCLE_MIN_YEARS // LIVES_PER_SPINOR,
        "max_years_per_life": LIFECYCLE_MAX_YEARS // LIVES_PER_SPINOR,
        "phase_shift_years": PHASE_SHIFT_YEARS,
        "quartet_years": QUARTET_YEARS,
        "context_sweep_years": CONTEXT_SWEEP_YEARS,
    }


def verify() -> bool:
    c = config()
    sweep = context_sweep()
    rotations_by_context = {
        context: {p.rotation for p in sweep if p.context == context}
        for context in CONTEXTS
    }
    return (
        c["spinor"]["literal"] == "-+"
        and c["spinor"]["lives"] == LIVES_PER_SPINOR
        and c["spinor"]["nominal_photon_lifecycle_years"] == NOMINAL_LIFECYCLE_YEARS
        and c["spinor"]["lifecycle_min_years"] == LIFECYCLE_MIN_YEARS
        and c["spinor"]["lifecycle_max_years"] == LIFECYCLE_MAX_YEARS
        and c["memristic"]["rotation_states"] == list(ROTATION_STATES)
        and c["memristic"]["phase_shift_years"] == PHASE_SHIFT_YEARS
        and all(rotations_by_context[x] == set(ROTATION_STATES) for x in CONTEXTS)
        and c["anchor"]["canonical_name"] == "Enheduanna"
        and c["anchor"]["corpus_slot"] == 3
        and c["policy"]["source_corpus_mutable"] is False
        and c["policy"]["frozen_kernel_modified"] is False
    )
