from tools.copper_mind_weak_ganglia import (
    SCALE, PER_SIDE_PERCENT, TWO_SIDE_PERCENT, NUDGE_DEGREES,
    coupled_pair, nudge, project, verify
)

def test_weak_ganglia_contract():
    assert verify()
    assert SCALE == 729
    assert PER_SIDE_PERCENT < 1.0
    assert TWO_SIDE_PERCENT < 1.0
    assert NUDGE_DEGREES == 1.0

def test_inverse_neighbors():
    for i in range(128):
        a, b = coupled_pair(i)
        assert a == -b
        assert a + b == 0

def test_one_degree_nudge():
    assert nudge(0.0, -1) == -1.0
    assert nudge(0.0, +1) == +1.0

def test_projection_is_read_only():
    p = project(7)
    assert p["scale"] == 729
    assert p["identity_preserved"] is True
    assert p["read_only"] is True
