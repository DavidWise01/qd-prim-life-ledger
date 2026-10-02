from tools.toph_hierarchical_state_space import (
    ADDRESS,
    CARRIER,
    EVENT,
    LANES,
    OBSERVED,
    STATE,
    TERNARY,
    bind_pipeline,
    breathing_cycle,
    hierarchy,
    route,
    verify,
)

def test_literal_anchor_is_locked():
    assert ADDRESS == "{{Gg.Aa.Ii.Aa}}"

def test_frozen_carrier():
    assert CARRIER == "000 + {} > 000"
    for branch in TERNARY:
        r = route(branch)
        assert r.state_in == "000"
        assert r.state_out == "000"
        assert r.event_space == "{}"

def test_observed_is_read_only_packet():
    for r in breathing_cycle():
        assert r["observed"] == OBSERVED
        assert r["state_in"] == r["state_out"] == STATE

def test_all_three_branches_return_to_zero():
    cycle = breathing_cycle()
    assert tuple(x["condition"] for x in cycle) == (-1, 0, 1)
    assert all(x["state_out"] == "000" for x in cycle)

def test_seven_lanes_fall_out():
    assert LANES == (
        "state",
        "condition",
        "observation",
        "change",
        "provenance",
        "return",
        "append",
    )

def test_hierarchy_preserves_center_at_every_level():
    tree = hierarchy(8)
    assert len(tree) == 8
    assert all(node["address"] == ADDRESS for node in tree)
    assert all(node["state_in"] == node["state_out"] == "000" for node in tree)

def test_frozen_oe_binding():
    b = bind_pipeline()
    assert all(b["TOPHProve"].values())
    assert b["TOPHTransport"]["closure"] == "oe"
    assert b["TOPHTransport"]["frozen"] is True
    assert b["TOPHTransport"]["immutable"] is True
    assert verify() is True
