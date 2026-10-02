from tools.generational_crystallization import (
    REDUCTION,
    bind_pipeline,
    crystallize,
    verify,
)

def test_x_is_four_daughters_times_four_permutations():
    r = crystallize()
    assert r.daughters == 4
    assert r.permutations_per_daughter == 4
    assert r.x_states == 16

def test_x_splits_into_two_eight_state_volumes():
    r = crystallize()
    assert r.volumes == (8, 8)
    assert sum(r.volumes) == 16

def test_each_volume_uses_frozen_reduction_to_zero():
    assert REDUCTION == (8, 3, 2, 1, 1, "..", 0)
    r = crystallize()
    assert r.terminal_pair == (0, 0)
    assert r.closure == "oe"

def test_signed_seed_resolves_to_nested_zero_seed():
    r = crystallize()
    assert r.active_seed == "+k.0.k-"
    assert r.resolved_seed == "0.0.0"

def test_final_kernel_binding_is_append_only_and_complete():
    b = bind_pipeline()
    assert list(b) == ["Event", "Commit", "Prove", "Project", "Transport"]
    assert b["Commit"]["append_only"] is True
    assert all(b["Prove"].values())
    assert b["Transport"]["closure"] == "oe"
    assert b["Transport"]["resolved_seed"] == "0.0.0"
    assert verify() is True
