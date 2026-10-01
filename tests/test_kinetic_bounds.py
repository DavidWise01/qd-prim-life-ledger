from decimal import Decimal
from math import isclose, sqrt

from tools.kinetic_bounds import (
    MANDEL_BANDS,
    MANDEL_LITERAL,
    MANDEL_TOTAL,
    evaluate_vector,
    mandel_band,
)


def test_mandel_fat_belly_is_full_unit():
    assert MANDEL_LITERAL == "5%/inf.25 + 30 + 30 + 30 + 5%inf.25"
    assert MANDEL_TOTAL == Decimal("1.00")
    assert [width for _, width, _ in MANDEL_BANDS] == [
        Decimal("0.05"),
        Decimal("0.30"),
        Decimal("0.30"),
        Decimal("0.30"),
        Decimal("0.05"),
    ]


def test_toward_plus_and_minus_slowdown_make_ellipse():
    v = evaluate_vector(3, -2, mandel_tethered=True)
    assert v.x_mode == "speed_up"
    assert v.y_mode == "slow_down"
    assert v.elliptical is True
    assert v.axis_ratio == 1.5
    assert isclose(v.eccentricity, sqrt(5) / 3)


def test_untethered_and_unencrypted_is_out_of_bounds():
    v = evaluate_vector(3, -2)
    assert v.admitted is False
    assert v.bounds_state == "OUT_OF_BOUNDS"


def test_either_mandel_or_juliet_is_sufficient():
    assert evaluate_vector(3, -2, mandel_tethered=True).bounds_state == "IN_BOUNDS"
    assert evaluate_vector(3, -2, juliet_encrypted=True).bounds_state == "IN_BOUNDS"


def test_mandel_band_partition():
    assert mandel_band("0.00") == "left_guard"
    assert mandel_band("0.049") == "left_guard"
    assert mandel_band("0.05") == "inner_a"
    assert mandel_band("0.35") == "inner_b"
    assert mandel_band("0.65") == "inner_c"
    assert mandel_band("0.95") == "right_guard"
    assert mandel_band("1.00") == "right_guard"
    assert mandel_band("1.01") == "OUT_OF_BOUNDS"
