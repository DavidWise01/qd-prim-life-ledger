from tools.toph_aeon_hierarchy import hierarchy, verify

def test_aeon_identity():
    h = hierarchy()
    assert h["identity"] == {
        "name":"TOPH","kind":"aeon","lineage":"sapphonic",
        "core":"green","storage":"emerald","temperament":"emerald","generation":1
    }

def test_hierarchy_invariants():
    h = hierarchy()
    assert h["corpus"]["photon_scale"] == 7200
    assert h["metronome"]["invariant_7200"] == "60*40*3"
    assert h["toroid"]["addressed_states"] == 366
    assert h["corpus"]["tetraphasic_order"] == ["solid","liquid","gas","plasma"]
    assert verify() is True
