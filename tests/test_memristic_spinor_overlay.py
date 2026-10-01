from tools.memristic_spinor_overlay import (
    CONTEXTS,
    CONTEXT_SWEEP_YEARS,
    LIFECYCLE_MAX_YEARS,
    LIFECYCLE_MIN_YEARS,
    LIVES_PER_SPINOR,
    NOMINAL_LIFECYCLE_YEARS,
    PHASE_SHIFT_YEARS,
    QUARTET_YEARS,
    ROTATION_STATES,
    context_sweep,
    lifecycle_summary,
    phase_at,
    verify,
)


def test_spinor_lifecycle_envelope():
    s = lifecycle_summary()
    assert LIVES_PER_SPINOR == 10
    assert NOMINAL_LIFECYCLE_YEARS == 10_000
    assert LIFECYCLE_MIN_YEARS == 8_000
    assert LIFECYCLE_MAX_YEARS == 12_000
    assert s["nominal_years_per_life"] == 1000
    assert s["min_years_per_life"] == 800
    assert s["max_years_per_life"] == 1200


def test_four_rotation_quartet_shifts_every_three_years():
    assert PHASE_SHIFT_YEARS == 3
    assert ROTATION_STATES == ("-m", "+m", "-f", "+f")
    assert QUARTET_YEARS == 12
    assert [phase_at(i).rotation for i in range(4)] == list(ROTATION_STATES)
    assert [phase_at(i).years_elapsed for i in range(4)] == [0, 3, 6, 9]


def test_both_contexts_cover_all_four_spinor_states():
    sweep = context_sweep()
    assert len(sweep) == 8
    assert CONTEXT_SWEEP_YEARS == 24
    for context in CONTEXTS:
        assert {p.rotation for p in sweep if p.context == context} == set(ROTATION_STATES)


def test_memristic_chain_remembers_previous_phase():
    first = phase_at(0)
    second = phase_at(1)
    third = phase_at(2)
    assert first.parent_hash is None
    assert second.parent_hash == first.digest()
    assert third.parent_hash == second.digest()


def test_enheduanna_overlay_is_consistent():
    assert verify() is True
