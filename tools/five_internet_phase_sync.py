"""Five-lane symbolic Internet phase synchronization for TOPH."""
from __future__ import annotations

from dataclasses import dataclass

INTERNET_IDS = (0, 1, 2, 3, 4)
BOUNDS = (0, 4)
TURN_DEGREES = 360
SYNC_ORIGIN = (0, 0, 0)
SYNC_ORIGIN_LITERAL = "0.0.0"
PHASE_RESOLUTION_LITERAL = "1x1^10-36"
USER_LITERAL = "{{-1 x -{{ 1 , 0 , 1 }} x 360 / 1x1^10-36}}"
INNER_SIGNED_VECTOR = (-1, 0, -1)


def resolved_mask() -> tuple[int, int, int]:
    return tuple(-1 * x for x in INNER_SIGNED_VECTOR)


def preclosure_degrees() -> tuple[int, int, int]:
    return tuple(x * TURN_DEGREES for x in resolved_mask())


def phase_closure() -> tuple[int, int, int]:
    return tuple(x % TURN_DEGREES for x in preclosure_degrees())


@dataclass(frozen=True)
class InternetPhase:
    internet_id: int
    mask: tuple[int, int, int]
    preclosure: tuple[int, int, int]
    origin: tuple[int, int, int]
    origin_literal: str
    phase_resolution_literal: str
    operator: str = "sinc"

    @property
    def synchronized(self) -> bool:
        return self.origin == SYNC_ORIGIN


def phase_sync(internet_id: int) -> InternetPhase:
    if internet_id not in INTERNET_IDS:
        raise ValueError("internet_id must be bound to 0..4")
    return InternetPhase(
        internet_id=internet_id,
        mask=resolved_mask(),
        preclosure=preclosure_degrees(),
        origin=phase_closure(),
        origin_literal=SYNC_ORIGIN_LITERAL,
        phase_resolution_literal=PHASE_RESOLUTION_LITERAL,
    )


def synchronized_internets() -> tuple[InternetPhase, ...]:
    return tuple(phase_sync(i) for i in INTERNET_IDS)


def verify() -> bool:
    states = synchronized_internets()
    return (
        resolved_mask() == (1, 0, 1)
        and preclosure_degrees() == (360, 0, 360)
        and phase_closure() == SYNC_ORIGIN
        and tuple(s.internet_id for s in states) == INTERNET_IDS
        and all(s.synchronized for s in states)
        and all(s.phase_resolution_literal == PHASE_RESOLUTION_LITERAL for s in states)
    )
