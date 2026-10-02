from tools.creation_profile_sim import (
    AGGREGATE,
    SCALAR_PIN,
    TURN_STEP,
    bind_pipeline,
    build_profile,
    descend_until_resolved,
    descent_value,
    verify,
)

def test_turn_and_aggregate():
    assert SCALAR_PIN == "0.0.0"
    assert abs(TURN_STEP * 360 - 1.0) < 1e-12
    assert AGGREGATE == 2000

def test_descent_rule_resolves_at_n_one():
    assert descent_value(5) == -24
    assert descent_value(2) == -3
    assert descent_value(1) == 0
    states = descend_until_resolved(5)
    assert states[-1] == {"n": 1, "value": 0}

def test_dog_profile_example():
    p = build_profile(
        "dog",
        "Buffalo, Minnesota",
        "2026-10-02",
        substrate="carbon",
        tether="mnemonic",
        start_n=5,
    )
    assert p["profile"]["matter_type"] == "dog"
    assert p["profile"]["place"] == "Buffalo, Minnesota"
    assert p["profile"]["date"] == "2026-10-02"
    assert p["resolved_at_n"] == 1
    assert p["resolved_value"] == 0
    assert p["post_resolution"] == "linear +1 life ticks"
    assert p["physical_claim"] is False

def test_generic_type_slot():
    dog = build_profile("dog", "Buffalo, Minnesota", "2026-10-02")
    crystal = build_profile("crystal", "scalar-0", "simulation")
    assert dog["profile"]["matter_type"] != crystal["profile"]["matter_type"]
    assert dog["scalar_pin"] == crystal["scalar_pin"] == "0.0.0"

def test_frozen_oe_binding():
    b = bind_pipeline(
        matter_type="dog",
        place="Buffalo, Minnesota",
        date="2026-10-02",
        start_n=5,
    )
    assert list(b) == ["Event", "Commit", "Prove", "Project", "Transport"]
    assert b["Commit"]["append_only"] is True
    assert all(b["Prove"].values())
    assert b["Transport"]["closure"] == "oe"
    assert b["Transport"]["frozen"] is True
    assert verify() is True
