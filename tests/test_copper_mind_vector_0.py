from tools.copper_mind_vector_0 import (
    BREAKOUT_THRESHOLD, CENTER, FORCE_CYCLE, G, PUSH, PUSHES_PER_SHELL,
    SHELL_WIDTH, SIGN_CYCLE, SUPERCYCLES, breakout, force_state,
    prove, ripple_point, verify
)

def test_ripple_center():
    for shell in range(72):
        for j in range(9):
            p=ripple_point(shell,j)
            assert p.forward + p.reverse == 10.0
            assert p.center == 5.0

def test_internal_push_width():
    assert PUSH * PUSHES_PER_SHELL == SHELL_WIDTH == 10.0
    assert CENTER == 5.0

def test_three_shell_phase_reset():
    a=[ripple_point(s,0).ternary_phase for s in range(3)]
    b=[ripple_point(s,0).ternary_phase for s in range(3,6)]
    assert a == b
    assert SUPERCYCLES == 24

def test_force_and_sign_cycle():
    assert FORCE_CYCLE == ("strong","middle","weak","weak","middle","strong")
    assert SIGN_CYCLE == "-++--+"
    assert [force_state(i) for i in range(6)] == list(zip(FORCE_CYCLE,SIGN_CYCLE))

def test_model_local_breakout():
    assert G == 1.0
    assert BREAKOUT_THRESHOLD == 1.02
    assert breakout(-0.02)
    assert not breakout(+0.02)

def test_full_proof():
    assert all(prove().values())
    assert verify()
