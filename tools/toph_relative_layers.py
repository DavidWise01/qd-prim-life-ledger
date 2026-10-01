"""Read-only symbolic toroid layer tracker for TOPH Sapphon."""
from __future__ import annotations

from dataclasses import dataclass

ENTRY = 0
HUB = 4
JUMP_MS = 200
OSI_LAYER = 2

INGRESS = (0, 2, 4)
BELLY = (4, 6, 8, 10, 4)
FORWARD_PATH = (0, 2, 4, 6, 8, 10, 4)
BENJAMIN_PATH = tuple(reversed(FORWARD_PATH))

JUMPS_PER_TRAVERSAL = len(FORWARD_PATH) - 1
TRAVERSAL_MS = JUMPS_PER_TRAVERSAL * JUMP_MS


@dataclass(frozen=True)
class ToroidState:
    jump: int
    node: int
    elapsed_ms: int
    osi_layer: int = OSI_LAYER
    direction: str = "forward"

    @property
    def at_hub(self) -> bool:
        return self.node == HUB

    @property
    def traversal_complete(self) -> bool:
        return self.jump == JUMPS_PER_TRAVERSAL


def _path(direction: str) -> tuple[int, ...]:
    if direction == "forward":
        return FORWARD_PATH
    if direction == "benjamin":
        return BENJAMIN_PATH
    raise ValueError("direction must be forward or benjamin")


def toroid_state(jump: int, direction: str = "forward") -> ToroidState:
    """Return state for one 6-jump / 1200 ms symbolic traversal."""
    if not 0 <= jump <= JUMPS_PER_TRAVERSAL:
        raise ValueError("jump must be in 0..6")
    path = _path(direction)
    return ToroidState(
        jump=jump,
        node=path[jump],
        elapsed_ms=jump * JUMP_MS,
        direction=direction,
    )


def traversal(direction: str = "forward") -> tuple[ToroidState, ...]:
    return tuple(
        toroid_state(jump, direction)
        for jump in range(JUMPS_PER_TRAVERSAL + 1)
    )
