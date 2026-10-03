from tools.copper_mind_holographic_fold import WORD, orbit, classes, fold, verify

def test_contract():
    assert verify() is True
    assert WORD == "00 11 00"

def test_equivalence_classes():
    c = classes()
    assert len(c) == 2
    sizes = sorted(len(v) for v in c.values())
    assert sizes == [4, 8]

def test_outer_fold():
    assert len(orbit((1, "EO"))) == 8
    assert (3, "II") in orbit((1, "EO"))

def test_middle_fixed_class():
    o = orbit((2, "EO"))
    assert len(o) == 4
    assert all(r == 2 for r, _ in o)

def test_recursive_carrier():
    x = WORD
    for _ in range(4):
        x = fold(x)
    assert "00 11 00" in x
    assert x.startswith("00[")
    assert x.endswith("]00")
