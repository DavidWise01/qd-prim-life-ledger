"""Deterministic generative adapter for q.d dot/radix addresses only.

This module sits outside the frozen mother kernel. It may generate the next
dot/radix address, but it cannot create daughters, mutate the kernel, or grant
generation authority.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, getcontext
from hashlib import sha256
import json

getcontext().prec = 80

RADIX = 360
BANDS = 11
MAX_GRAVITY = 8
BASE_SCALE = Decimal("1e-36")
MAX_STEP = (Decimal(BANDS) * Decimal(MAX_GRAVITY) * BASE_SCALE) / Decimal(RADIX)


@dataclass(frozen=True)
class DotRadixState:
    seed: str
    index: int
    band: int
    gravity: int
    radix: int
    step: str
    parent_hash: str | None

    @property
    def address(self) -> str:
        return f"dot[{self.index}]::{self.band}/{self.gravity}/{self.radix:03d}"

    def canonical(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))

    def digest(self) -> str:
        return sha256(self.canonical().encode("utf-8")).hexdigest()


class DotRadixGenerator:
    """Append-only deterministic generator bounded to dot/radix geometry."""

    RADIX = RADIX
    BANDS = BANDS
    MAX_GRAVITY = MAX_GRAVITY
    BASE_SCALE = BASE_SCALE
    MAX_STEP = MAX_STEP
    SCOPE = ("dot", "radix")
    CAN_SPAWN = False

    def __init__(self, seed: str) -> None:
        normalized = seed.strip().lower()
        if not normalized:
            raise ValueError("seed must be non-empty")
        self.seed = normalized
        self._states: list[DotRadixState] = []

    @property
    def states(self) -> tuple[DotRadixState, ...]:
        return tuple(self._states)

    def _material(self, index: int, parent_hash: str | None) -> bytes:
        tether = parent_hash or "root"
        return sha256(f"{self.seed}:{index}:{tether}".encode("utf-8")).digest()

    def next(self) -> DotRadixState:
        index = len(self._states)
        parent_hash = self._states[-1].digest() if self._states else None
        material = self._material(index, parent_hash)

        band = 1 + (material[0] % BANDS)
        gravity = 1 + (material[1] % MAX_GRAVITY)
        radix = int.from_bytes(material[2:4], "big") % RADIX
        local_step = (Decimal(band) * Decimal(gravity) * BASE_SCALE) / Decimal(RADIX)

        state = DotRadixState(
            seed=self.seed,
            index=index,
            band=band,
            gravity=gravity,
            radix=radix,
            step=format(local_step, "E"),
            parent_hash=parent_hash,
        )
        self._states.append(state)
        return state

    def generate(self, count: int) -> tuple[DotRadixState, ...]:
        if count < 0:
            raise ValueError("count must be >= 0")
        return tuple(self.next() for _ in range(count))

    def verify(self) -> bool:
        for index, state in enumerate(self._states):
            if state.index != index:
                return False
            if not 1 <= state.band <= BANDS:
                return False
            if not 1 <= state.gravity <= MAX_GRAVITY:
                return False
            if not 0 <= state.radix < RADIX:
                return False
            if Decimal(state.step) > MAX_STEP:
                return False
            expected_parent = None if index == 0 else self._states[index - 1].digest()
            if state.parent_hash != expected_parent:
                return False
        return True
