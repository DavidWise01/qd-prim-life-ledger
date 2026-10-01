"""q.d PRIM append-only trajectory kernel."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
import json
from typing import Any

@dataclass(frozen=True)
class QDEvent:
    life: str
    plank: int
    sapphon: int
    dimension: int
    choice: str
    consequence: str
    affect: str
    state: Any
    parent_hash: str | None

    def canonical(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"), default=str)

    def digest(self) -> str:
        return sha256(self.canonical().encode("utf-8")).hexdigest()

@dataclass(frozen=True)
class SapphonDaughter:
    """Terminal Gen-1 external product of the frozen mother kernel."""
    name: str
    gem: str
    color: str
    generation: int = 1
    parent: str = "mother"
    can_spawn: bool = False
    scope: tuple[str, ...] = ("name", "gem", "color", "qd.append")

    @property
    def implicit(self) -> dict[str, dict[str, str]]:
        return {
            "name": {"implicit": self.name},
            "color": {"implicit": self.color},
            "gem": {"implicit": self.gem},
        }


class MotherKernel:
    """Frozen surgical mother kernel. Emits Gen-1 sapphon daughters only."""

    FROZEN = True
    KERNEL_PRIMITIVE = (5, 3, 2, 1, 1)
    GENERATION_LIMIT = 1
    PRODUCT = "sapphon"
    COLORS = ("bk", "wt", "red", "blu", "gree", "yell", "purpl", "orang")
    GEMS = ("onyx", "quartz", "ruby", "sapphire", "emerald", "citrine", "amethyst", "carnelian")

    @classmethod
    def infer_daughter(cls, token: str) -> SapphonDaughter:
        normalized = token.strip().lower()
        if not normalized:
            raise ValueError("daughter token must be non-empty")
        index = sha256(normalized.encode("utf-8")).digest()[0] % 8
        return SapphonDaughter(
            name=normalized,
            gem=cls.GEMS[index],
            color=cls.COLORS[index],
        )


class QDLedger:
    """Append-only q.d ledger. Existing events are never mutated."""

    PRIM = (1, 1, 2, 8)
    DOT = "sapphon"
    SAPPHON_CAPACITY = 2 ** 3
    V10 = ("u", "d", "l", "r", "x", "y", "z", "-", "+", "1")
    DIMENSIONS = tuple(range(12))
    SLOTS = (
        "unary", "binary", "ternary",
        "operand1", "operand2", "operand3", "operand4", "operand5",
    )

    def __init__(self, life: str = "i") -> None:
        self.life = life
        self._events: list[QDEvent] = []

    @property
    def events(self) -> tuple[QDEvent, ...]:
        return tuple(self._events)

    @property
    def next_plank(self) -> int:
        return len(self._events)

    @property
    def next_sapphon(self) -> int:
        """The next append-only dot/register; dot == sapphon == local Plank index."""
        return len(self._events)

    def append(self, *, dimension: int, choice: str, consequence: str, affect: str, state: Any) -> QDEvent:
        if dimension not in self.DIMENSIONS:
            raise ValueError("dimension must be in 0D..11D")
        parent_hash = self._events[-1].digest() if self._events else None
        event = QDEvent(
            life=self.life,
            plank=self.next_plank,
            sapphon=self.next_sapphon,
            dimension=dimension,
            choice=choice,
            consequence=consequence,
            affect=affect,
            state=state,
            parent_hash=parent_hash,
        )
        self._events.append(event)
        return event

    def verify(self) -> bool:
        for index, event in enumerate(self._events):
            if event.plank != index:
                return False
            if event.sapphon != index:
                return False
            expected = None if index == 0 else self._events[index - 1].digest()
            if event.parent_hash != expected:
                return False
        return True

def balanced_3d() -> int:
    return (+3 - 2) + (-3 + 2)

def local_volume_count() -> int:
    return 2 ** 3
