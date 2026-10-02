import pytest

from tools.toph_qk_handoff_v2 import (
    detect_fixed_points,
    handoff_twice_and_freeze,
    inference_window,
    model,
    verify,
)


def test_full_map_required_before_fixed_point_claim():
    with pytest.raises(ValueError):
        detect_fixed_points({"000": "000"})

    complete = {
        "000": "000",
        "001": "000",
        "010": "001",
        "011": "001",
        "100": "010",
        "101": "010",
        "110": "011",
        "111": "011",
    }
    assert detect_fixed_points(complete) == ["000"]


def test_static_snow_is_candidate_count_not_probability():
    x = inference_window("00??????????")
    assert x["unknown_plank_cells"] == 10
    assert x["candidate_count"] == 2**10
    assert x["resolved"] is False
    assert x["directions"] is None


def test_two_plank_per_frame_six_frames_per_velocity():
    m = model()
    assert m["clock"]["plank_per_frame"] == 2
    assert m["clock"]["frames_per_velocity_window"] == 6
    assert m["inference_window"]["plank_cells"] == 12


def test_cardinal_quarter_and_inverse():
    m = model()
    assert m["direction"]["mapping"] == {"00": "U", "01": "R", "10": "L", "11": "D"}
    assert m["direction"]["inverse"] == {"U": "D", "D": "U", "L": "R", "R": "L"}
    assert m["direction"]["quarter_turn_literal"] == ".25"
    assert m["direction"]["quarter_turn_is_percent"] is False


def test_retest_two_identical_handoffs_freezes_on_eo():
    sample = model()["sample"]["plank_bits"]
    out = handoff_twice_and_freeze(sample, 60)
    assert out["freeze"] is True
    assert out["status"] == "eo"
    assert out["sentinel"] == "eo"
    assert len(out["handoffs"]) == 2
    assert out["handoffs"][0]["digest"] == out["handoffs"][1]["digest"]
    assert out["handoffs"][0]["payload"] == out["handoffs"][1]["payload"]


def test_unresolved_snow_never_handoffs_or_freezes():
    out = handoff_twice_and_freeze("????????????", 60)
    assert out["freeze"] is False
    assert out["status"] == "snow"
    assert out["handoffs"] == []
    assert out["window"]["candidate_count"] == 2**12


def test_full_verifier():
    assert verify() is True
