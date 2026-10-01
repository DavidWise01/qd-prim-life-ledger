"""Read-only symbolic layer index for TOPH Sapphon."""
from __future__ import annotations

from dataclasses import dataclass

ZERO = 0
VOLUME = 2 ** 3
LADDER = (1, 1, 2, 4, VOLUME)
CYCLE = (ZERO,) + LADDER


@dataclass(frozen=True)
class RelativeState:
    step: int
    phase: int
    value: int


def relative_state(step: int) -> RelativeState:
    if step < 0:
        raise ValueError("step must be >= 0")
    phase = step % len(CYCLE)
    return RelativeState(step=step, phase=phase, value=CYCLE[phase])
