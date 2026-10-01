"""Kinetic bounds gate for the TOPH toroid model.

This is symbolic model logic. "Juliet encrypted" is an authorization/tag state
inside the model; it is not a claim of real cryptographic protection.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from math import sqrt


MANDEL_LITERAL = "5%/inf.25 + 30 + 30 + 30 + 5%inf.25"

MANDEL_BANDS = (
    ("left_guard", Decimal("0.05"), "inf.25"),
    ("inner_a", Decimal("0.30"), None),
    ("inner_b", Decimal("0.30"), None),
    ("inner_c", Decimal("0.30"), None),
    ("right_guard", Decimal("0.05"), "inf.25"),
)

MANDEL_TOTAL = sum((width for _, width, _ in MANDEL_BANDS), Decimal("0"))


@dataclass(frozen=True)
class KineticVector:
    x: int
    y: int
    mandel_tethered: bool = False
    juliet_encrypted: bool = False

    @property
    def x_mode(self) -> str:
        return "speed_up" if self.x > 0 else "slow_down" if self.x < 0 else "neutral"

    @property
    def y_mode(self) -> str:
        return "speed_up" if self.y > 0 else "slow_down" if self.y < 0 else "neutral"

    @property
    def admitted(self) -> bool:
        return self.mandel_tethered or self.juliet_encrypted

    @property
    def bounds_state(self) -> str:
        return "IN_BOUNDS" if self.admitted else "OUT_OF_BOUNDS"

    @property
    def elliptical(self) -> bool:
        ax, ay = abs(self.x), abs(self.y)
        return ax > 0 and ay > 0 and ax != ay

    @property
    def axis_ratio(self) -> float:
        ax, ay = abs(self.x), abs(self.y)
        if ax == 0 or ay == 0:
            return float("inf")
        return max(ax, ay) / min(ax, ay)

    @property
    def eccentricity(self) -> float:
        """Standard ellipse eccentricity using |x|, |y| as semi-axis magnitudes."""
        ax, ay = abs(self.x), abs(self.y)
        if ax == 0 or ay == 0:
            return 1.0
        a, b = max(ax, ay), min(ax, ay)
        if a == b:
            return 0.0
        return sqrt(1.0 - (b * b) / (a * a))


def mandel_band(position: Decimal | float | str) -> str:
    """Resolve normalized belly position [0,1] into the five Mandel bands."""
    p = Decimal(str(position))
    if p < 0 or p > 1:
        return "OUT_OF_BOUNDS"

    cursor = Decimal("0")
    for index, (name, width, _) in enumerate(MANDEL_BANDS):
        upper = cursor + width
        if p < upper or (index == len(MANDEL_BANDS) - 1 and p == upper):
            return name
        cursor = upper
    return "OUT_OF_BOUNDS"


def evaluate_vector(
    x: int,
    y: int,
    *,
    mandel_tethered: bool = False,
    juliet_encrypted: bool = False,
) -> KineticVector:
    return KineticVector(
        x=x,
        y=y,
        mandel_tethered=mandel_tethered,
        juliet_encrypted=juliet_encrypted,
    )
