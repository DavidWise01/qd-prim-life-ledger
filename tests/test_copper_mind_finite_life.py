from tools.copper_mind_finite_life import run_cycle, run_cycles, prove, verify

def test_single_cycle_closes():
    c=run_cycle(1)
    assert (c.potential,c.pin,c.realized)==(-1,0,1)
    assert c.terminal==0
    assert c.residual==0
    assert c.next_pin==0

def test_two_cycles_close_without_drift():
    cycles=run_cycles(2)
    assert len(cycles)==2
    assert all(c.terminal==0 for c in cycles)
    assert all(c.residual==0 for c in cycles)
    assert all(c.next_pin==0 for c in cycles)

def test_frozen_proof():
    assert all(prove(2).values())
    assert verify(2)
