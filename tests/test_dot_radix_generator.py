from decimal import Decimal

from tools.dot_radix_generator import (
    BANDS,
    MAX_GRAVITY,
    MAX_STEP,
    RADIX,
    DotRadixGenerator,
)


def test_scale_envelope_matches_user_radix_expression():
    expected = (Decimal(11) * Decimal(8) * Decimal("1e-36")) / Decimal(360)
    assert MAX_STEP == expected
    assert Decimal("2.4444444444444444444444444444444444444444444444444444444444444444444444444444444E-37") == MAX_STEP


def test_dot_radix_generator_is_deterministic():
    a = DotRadixGenerator("toph").generate(16)
    b = DotRadixGenerator("toph").generate(16)
    assert a == b


def test_dot_radix_only_scope_and_no_spawn():
    gen = DotRadixGenerator("toph")
    assert gen.SCOPE == ("dot", "radix")
    assert gen.CAN_SPAWN is False
    assert not hasattr(gen, "spawn")
    assert not hasattr(gen, "infer_daughter")


def test_all_generated_states_stay_inside_11_8_360_envelope():
    gen = DotRadixGenerator("toph")
    states = gen.generate(360)
    assert len(states) == RADIX
    assert gen.verify()
    for state in states:
        assert 1 <= state.band <= BANDS
        assert 1 <= state.gravity <= MAX_GRAVITY
        assert 0 <= state.radix < RADIX
        assert Decimal(state.step) <= MAX_STEP


def test_generation_is_append_only_parent_tethered():
    gen = DotRadixGenerator("toph")
    first, second, third = gen.generate(3)
    assert first.index == 0
    assert first.parent_hash is None
    assert second.parent_hash == first.digest()
    assert third.parent_hash == second.digest()
    assert gen.verify()
