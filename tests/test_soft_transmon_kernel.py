from tools.soft_transmon_kernel import (
    PHASE_STEP,
    LOCAL_STATES,
    bind_pipeline,
    cycle,
    nested_scale_exponents,
    state_at,
    verify,
)

def test_quarter_phase_cycle_closes_to_oe():
    c = cycle(4)
    assert [s.phase for s in c] == [0.0, 0.25, 0.5, 0.75, 0.0]
    assert c[-1].closure == "oe"

def test_one_tick_is_one_local_2_pow_3_register():
    s = state_at(1)
    assert s.local_states == 8
    assert LOCAL_STATES == 2 ** 3
    assert s.g == 0.25
    assert s.t == 1
    assert s.scalar == 0

def test_nested_scale_runs_from_one_to_1e_minus_35():
    exps = nested_scale_exponents()
    assert exps[0] == 0
    assert exps[-1] == -35
    assert len(exps) == 36

def test_binding_preserves_final_kernel_boundary():
    b = bind_pipeline()
    assert list(b) == ["Event", "Commit", "Prove", "Project", "Transport"]
    assert b["Commit"]["append_only"] is True
    assert all(b["Prove"].values())
    assert b["Transport"]["closure"] == "oe"
    assert b["Transport"]["resolved_seed"] == "0.0.0"

def test_verify_passes():
    assert verify()["status"] == "0e"
