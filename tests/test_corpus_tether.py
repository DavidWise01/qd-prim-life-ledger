from tools.corpus_tether import (
    CENTER_PIN,
    GENERATION_COUNT,
    LIFE_YEARS,
    RADIX_TICKS_PER_LIFE,
    SPAN_LITERAL,
    bind_dot,
    load_corpus,
    verify_corpus,
)
from tools.dot_radix_generator import DotRadixGenerator


def test_humanity_literal_and_center_are_preserved():
    corpus = load_corpus()
    assert SPAN_LITERAL == "-+2700-+0+-2700-+"
    assert corpus["literal"] == SPAN_LITERAL
    assert CENTER_PIN == "{{0::m+f}}"
    assert corpus["center_pin"] == CENTER_PIN


def test_40_lives_cover_3600_years_inside_5400_year_carrier():
    corpus = load_corpus()
    slots = corpus["slots"]
    assert GENERATION_COUNT == 40
    assert len(slots) == 40
    assert all(slot["life_years"] == LIFE_YEARS == 90 for slot in slots)
    assert sum(slot["life_years"] for slot in slots) == 3600
    assert corpus["carrier_years"] == 5400
    assert corpus["seam_years"] == 1800
    assert slots[0]["start_year"] == -2700
    assert slots[-1]["end_year"] == 2700


def test_shadow_center_light_geometry():
    corpus = load_corpus()
    shadow = [s for s in corpus["slots"] if s["side"] == "shadow"]
    light = [s for s in corpus["slots"] if s["side"] == "light"]
    assert len(shadow) == len(light) == 20
    assert shadow[-1]["end_year"] == -45
    assert light[0]["start_year"] == 45
    assert light[-1]["end_year"] == 2700
    assert verify_corpus()


def test_360_radix_maps_to_40_lives_with_nine_phases_each():
    assert RADIX_TICKS_PER_LIFE == 9
    seen = {slot: set() for slot in range(40)}
    gen = DotRadixGenerator("humanity-corpus")
    for state in gen.generate(3600):
        binding = bind_dot(state)
        seen[binding.corpus_slot].add(binding.radix_phase)
        assert 0 <= binding.corpus_slot < 40
        assert 0 <= binding.radix_phase < 9
    assert all(phases <= set(range(9)) for phases in seen.values())


def test_binding_is_read_only_and_does_not_create_generation():
    state = DotRadixGenerator("toph").next()
    binding = bind_dot(state)
    assert not hasattr(binding, "spawn")
    assert not hasattr(binding, "append")
    assert binding.center_pin == "{{0::m+f}}"
