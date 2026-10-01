from collections import Counter

from tools.implicit_mnemonic import (
    AIR_LITERAL,
    AIR_NORMALIZED,
    PHASES,
    air_boundary,
    decode_all,
    preserves_order,
)


def test_phase_cycle_is_exact_nine_state_overlay():
    assert PHASES == (
        "creation", "electrum", "matter", "tm8", "gas",
        "liquid", "solid", "plasma", "nature",
    )


def test_all_implicit_expansions_preserve_skeleton_order():
    pairs = {
        "CEM": "CHEM",
        "TGL": "TOGGLE",
        "SPN": "SPIN",
        "PNC": "PINCH",
        "EMT": "EMIT",
        "GLS": "GLASS",
    }
    assert all(preserves_order(k, v) for k, v in pairs.items())


def test_40_slot_overlay_counts_match_mirrored_pattern():
    hits = decode_all()
    assert len(hits) == 40
    shadow = Counter(h.skeleton for h in hits if h.side == "shadow")
    light = Counter(h.skeleton for h in hits if h.side == "light")
    assert shadow == Counter({"CEM": 7, "TGL": 7, "SPN": 6})
    assert light == Counter({"PNC": 7, "EMT": 7, "GLS": 6})


def test_spin_glass_pair_is_present_without_reordering():
    hits = decode_all()
    shadow_spin = [h for h in hits if h.expansion == "SPIN"]
    light_glass = [h for h in hits if h.expansion == "GLASS"]
    assert len(shadow_spin) == 6
    assert len(light_glass) == 6


def test_air_boundary_preserves_user_literal_and_structured_center():
    air = air_boundary()
    assert air["user_literal"] == AIR_LITERAL
    assert air["normalized_symbolic"] == AIR_NORMALIZED
    assert air["center"] == {"label": "air", "coordinate": "36.00"}
    assert air["lower"] == "2 x 1^10^-35.99"
    assert air["upper"] == "+36.01"
    assert air["mutable"] is False
