from tools.copper_mind_spinor_sphere import (
    PASS_ORDER, RING_DEG, SECTOR_DEG, SECTORS_PER_RING, SPINOR_DEG,
    TOTAL_DEG, inversion_count, prove, route_cycle, verify
)

def test_angular_closure():
    assert SECTOR_DEG * SECTORS_PER_RING == RING_DEG == 360
    assert RING_DEG * 4 == TOTAL_DEG == 1440
    assert SPINOR_DEG * 2 == TOTAL_DEG

def test_sector_step_closure():
    assert 720 // 15 == 48
    assert 1440 // 15 == 96
    assert 24 * 4 == 96
    assert 180 // 15 == 12

def test_pass_order_is_closed_even_four_cycle():
    assert PASS_ORDER == (1,3,4,2)
    assert route_cycle() == (1,3,4,2,1)
    assert inversion_count(PASS_ORDER) % 2 == 0

def test_all_derived_invariants():
    assert all(prove().values())
    assert verify()
