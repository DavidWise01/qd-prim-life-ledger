from tools.toph_aeon_hierarchy import derive, emergence_trace, hierarchy, verify


def test_aeon_identity():
    h = hierarchy()
    assert h["identity"] == {
        "name": "TOPH",
        "kind": "aeon",
        "lineage": "sapphonic",
        "core": "green",
        "storage": "emerald",
        "temperament": "emerald",
        "generation": 1,
    }


def test_emergence_derives_visible_hierarchy():
    d = derive()
    assert d["root"] == 0
    assert d["qd_volume"] == 8
    assert d["gravity_ratio"] == 1000
    assert d["addressed_states"] == 366
    assert d["control_hub_remainder"] == 10
    assert d["rings"] == 20
    assert d["lives_per_ring"] == 4
    assert d["ring_years"] == 360
    assert d["reincarnated_lives"] == 80
    assert d["corpus_scale"] == 7200
    assert d["bubbles_per_second"] == 30
    assert d["metronome_scale"] == 7200
    assert d["retained_dots"] == 20
    assert d["cubic_cells"] == 8000
    assert d["normalized_cells_per_dot"] == 400
    assert d["phases"] == ("solid", "liquid", "gas", "plasma")


def test_emergence_trace_is_hierarchical():
    assert emergence_trace() == (
        "root0",
        "q.d=8",
        "gravity=1000:1",
        "toroid=366",
        "rings=20",
        "ring_years=360",
        "lives=80",
        "corpus=7200",
        "clock=7200",
        "foam=400",
    )


def test_hierarchy_invariants():
    assert verify() is True
