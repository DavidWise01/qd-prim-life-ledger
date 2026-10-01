from decimal import Decimal

from tools.material_year_clock import (
    ATOMIC_NUMBER,
    FULL_SPAN_YEARS,
    LOWER_YEAR,
    MATERIAL,
    PHOTON_HALF_LIFE_YEARS,
    ROOT_REFERENT,
    STORAGE_FRACTION,
    STORAGE_YEAR_EQUIVALENT,
    UPPER_YEAR,
    WEIGHT_YEARS,
    layer_zero,
)


def test_layer_zero_gold_weight():
    state = layer_zero()
    assert state.referent == ROOT_REFERENT == 0
    assert state.layer == 0
    assert MATERIAL == "Au"
    assert ATOMIC_NUMBER == 79
    assert WEIGHT_YEARS == 79
    assert state.weight_years == 79


def test_photon_carrier_is_symmetric_about_zero():
    assert PHOTON_HALF_LIFE_YEARS == 5400
    assert LOWER_YEAR == -5400
    assert UPPER_YEAR == 5400
    assert FULL_SPAN_YEARS == 10800
    assert layer_zero().full_span_years == 10800


def test_storage_fraction_is_twenty_percent_of_full_span():
    assert STORAGE_FRACTION == Decimal("0.20")
    assert STORAGE_YEAR_EQUIVALENT == 2160
    assert layer_zero().storage_year_equivalent == 2160


def test_notation_is_deterministic():
    assert layer_zero().notation == "root0::L0::Au79::79y::-5400..0..+5400::storage~20%"
