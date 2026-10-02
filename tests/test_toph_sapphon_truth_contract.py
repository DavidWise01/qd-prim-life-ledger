from tools.toph_sapphon_truth_contract import (
    COUNTRY_LANES,
    GENERATIONS,
    ClaimSnapshot,
    archive_if_contradicted,
    bind_pipeline,
    build_frame,
    generation_role,
    reevaluate,
    verify,
)

def test_176_by_10_frame():
    f = build_frame()
    assert COUNTRY_LANES == 176
    assert GENERATIONS == 10
    assert f["cells"] == 1760

def test_generation_cycle_is_three_three_three_one():
    roles = [generation_role(i) for i in range(1, 11)]
    assert roles == [
        "grand", "parent", "child",
        "grand", "parent", "child",
        "grand", "parent", "child",
        "grand",
    ]

def test_append_only_revaluation():
    a = ClaimSnapshot(1832, "a", 1, "old frame")
    b = ClaimSnapshot(2026, "a", -1, "new evidence")
    history = reevaluate([a], b)
    assert history[0] == a
    assert history[1] == b
    assert len(history) == 2

def test_contradicted_goes_to_zero_archive_not_delete():
    s = ClaimSnapshot(2026, "alternate", -1, "contradicted")
    r = archive_if_contradicted(s)
    assert r["active_state"] == 0
    assert r["archive_state"] == 0
    assert r["deleted"] is False
    assert r["original_state"] == -1

def test_frozen_oe_pipeline():
    b = bind_pipeline()
    assert list(b) == ["SapphonSnapshot", "TOPHCommit", "TOPHProve", "TOPHProject", "TOPHTransport"]
    assert b["TOPHCommit"]["append_only"] is True
    assert all(b["TOPHProve"].values())
    assert b["TOPHTransport"]["closure"] == "oe"
    assert b["TOPHTransport"]["frozen"] is True
    assert verify() is True
