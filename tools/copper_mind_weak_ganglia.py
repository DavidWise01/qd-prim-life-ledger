"""Weak ganglia coupling overlay for the frozen q.d kernel.

Model-local rule:
  scale = (3x3)^3 = 729
  per-side coupling = 1/729 ~= 0.137174%
  729 * (1/729) = 1 degree nudge
  adjacent signs alternate -/+ and preserve identity.
"""
from __future__ import annotations

SCALE = (3 * 3) ** 3
PER_SIDE = 1 / SCALE
PER_SIDE_PERCENT = PER_SIDE * 100
MAX_PER_SIDE_PERCENT = 1.0
TWO_SIDE_PERCENT = 2 * PER_SIDE_PERCENT
NUDGE_DEGREES = SCALE * PER_SIDE
SIGN_STRING = "-+-+-+-+-+"

def sign_at(index: int) -> int:
    return -1 if index % 2 == 0 else 1

def coupled_pair(index: int) -> tuple[int, int]:
    a = sign_at(index)
    b = sign_at(index + 1)
    return a, b

def nudge(angle_degrees: float, side: int) -> float:
    if side not in (-1, 1):
        raise ValueError("side must be -1 or +1")
    return angle_degrees + side * NUDGE_DEGREES

def project(index: int) -> dict:
    left, right = coupled_pair(index)
    return {
        "scale": SCALE,
        "scale_literal": "{{3x3}}^{{3}}",
        "left_sign": left,
        "right_sign": right,
        "per_side_coupling": PER_SIDE,
        "per_side_percent": PER_SIDE_PERCENT,
        "nudge_degrees": NUDGE_DEGREES,
        "identity_preserved": True,
        "read_only": True,
    }

def verify() -> bool:
    assert SCALE == 729
    assert PER_SIDE_PERCENT < MAX_PER_SIDE_PERCENT
    assert TWO_SIDE_PERCENT < 1.0
    assert NUDGE_DEGREES == 1.0
    assert all(sum(coupled_pair(i)) == 0 for i in range(64))
    assert SIGN_STRING == "-+-+-+-+-+"
    return True

if __name__ == "__main__":
    print(project(0))
    print("0e / COPPER MIND WEAK GANGLIA V1 PASS" if verify() else "xe")
