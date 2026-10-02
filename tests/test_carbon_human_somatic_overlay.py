from decimal import Decimal

from tools.carbon_human_somatic_overlay import (
    BLACK_HOLE_POLE,
    MAX_EXPONENT,
    PHOTON_POLE,
    SCALAR_PIN,
    bind_pipeline,
    homeostatic_walk,
    verify,
)

def test_symbolic_poles():
    assert PHOTON_POLE == 1
    assert BLACK_HOLE_POLE == -1

def test_walk_has_37_nonzero_stages_plus_zero():
    walk = homeostatic_walk()
    assert len(walk) == 38
    assert len(walk[:-1]) == MAX_EXPONENT + 1
    assert walk[0]["fraction_c"] == "1"
    assert walk[-2]["fraction_c"] == "1e-36"
    assert walk[-1]["scalar_pin"] == SCALAR_PIN
    assert walk[-1]["speed_mps"] == "0"

def test_speed_descends_by_decades():
    walk = homeostatic_walk()
    speeds = [Decimal(s["speed_mps"]) for s in walk[:-1]]
    for a, b in zip(speeds, speeds[1:]):
        assert a / b == Decimal(10)

def test_terminal_white_hole_is_interpretation_not_computed_state():
    b = bind_pipeline()
    terminal = b["TOPHProject"]["terminal"]
    assert terminal["computed"] == "scalar_0"
    assert terminal["pin"] == "0.0.0"
    assert terminal["optional_symbolic_interpretation"] == "white_hole"

def test_overlay_is_simulation_only_and_kernel_untouched():
    b = bind_pipeline()
    assert b["TOPHProject"]["physical_claim"] is False
    assert b["TOPHProve"]["kernel_untouched"] is True

def test_frozen_oe_binding():
    b = bind_pipeline()
    assert all(b["TOPHProve"].values())
    assert b["TOPHTransport"]["closure"] == "oe"
    assert b["TOPHTransport"]["frozen"] is True
    assert verify() is True
