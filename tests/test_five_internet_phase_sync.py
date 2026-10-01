from tools.five_internet_phase_sync import (
    BOUNDS,
    INTERNET_IDS,
    PHASE_RESOLUTION_LITERAL,
    SYNC_ORIGIN,
    USER_LITERAL,
    phase_closure,
    phase_sync,
    preclosure_degrees,
    resolved_mask,
    synchronized_internets,
    verify,
)


def test_double_negative_resolves_phase_mask():
    assert resolved_mask() == (1, 0, 1)


def test_full_turn_closes_to_zero_origin():
    assert preclosure_degrees() == (360, 0, 360)
    assert phase_closure() == (0, 0, 0) == SYNC_ORIGIN


def test_five_internets_are_bound_zero_through_four():
    assert BOUNDS == (0, 4)
    assert INTERNET_IDS == (0, 1, 2, 3, 4)
    states = synchronized_internets()
    assert [s.internet_id for s in states] == [0, 1, 2, 3, 4]
    assert all(s.origin_literal == "0.0.0" for s in states)
    assert all(s.synchronized for s in states)


def test_resolution_and_literal_are_preserved():
    assert PHASE_RESOLUTION_LITERAL == "1x1^10-36"
    assert USER_LITERAL == "{{-1 x -{{ 1 , 0 , 1 }} x 360 / 1x1^10-36}}"
    assert phase_sync(4).phase_resolution_literal == PHASE_RESOLUTION_LITERAL


def test_out_of_bounds_internet_rejected():
    for bad in (-1, 5):
        try:
            phase_sync(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("out-of-bounds internet id must fail")


def test_phase_sync_verifies():
    assert verify() is True
