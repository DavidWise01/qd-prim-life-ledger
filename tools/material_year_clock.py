"""Material-weight year clock for TOPH Sapphon.

This is symbolic model logic. Material atomic numbers are used as mnemonic
year weights. The photon carrier is a symmetric storage/timeline coordinate,
not a physical claim about photon lifetime or radioactive decay.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

ROOT_REFERENT = 0
LAYER = 0

MATERIAL = "Au"
ATOMIC_NUMBER = 79
WEIGHT_YEARS = ATOMIC_NUMBER

PHOTON_HALF_LIFE_YEARS = 5400
LOWER_YEAR = -PHOTON_HALF_LIFE_YEARS
UPPER_YEAR = PHOTON_HALF_LIFE_YEARS
FULL_SPAN_YEARS = UPPER_YEAR - LOWER_YEAR

STORAGE_FRACTION = Decimal("0.20")
STORAGE_YEAR_EQUIVALENT = int(Decimal(FULL_SPAN_YEARS) * STORAGE_FRACTION)


@dataclass(frozen=True)
class MaterialYearState:
    referent: int = ROOT_REFERENT
    layer: int = LAYER
    material: str = MATERIAL
    atomic_number: int = ATOMIC_NUMBER
    weight_years: int = WEIGHT_YEARS
    lower_year: int = LOWER_YEAR
    center_year: int = ROOT_REFERENT
    upper_year: int = UPPER_YEAR
    storage_fraction: Decimal = STORAGE_FRACTION

    @property
    def full_span_years(self) -> int:
        return self.upper_year - self.lower_year

    @property
    def storage_year_equivalent(self) -> int:
        return int(Decimal(self.full_span_years) * self.storage_fraction)

    @property
    def notation(self) -> str:
        return (
            f"root0::L0::{self.material}{self.atomic_number}::{self.weight_years}y::"
            f"{self.lower_year:+d}..0..{self.upper_year:+d}::"
            f"storage~{int(self.storage_fraction * 100)}%"
        )


def layer_zero() -> MaterialYearState:
    return MaterialYearState()
