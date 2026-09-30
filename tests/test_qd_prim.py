from src.qd_prim import QDLedger, balanced_3d, local_volume_count

def test_prim():
    assert QDLedger.PRIM == (1, 1, 2, 8)

def test_slots_equal_local_volume():
    assert len(QDLedger.SLOTS) == local_volume_count() == 8

def test_balance_closes_zero():
    assert balanced_3d() == 0

def test_append_only_plank_progression():
    qd = QDLedger("i")
    e0 = qd.append(
        dimension=0, choice="pin", consequence="origin",
        affect="self", state={"life": "i", "zero": 0},
    )
    e1 = qd.append(
        dimension=3, choice="realize", consequence="volume",
        affect="append-next", state={"volume": 8},
    )
    assert e0.plank == 0
    assert e1.plank == 1
    assert e1.parent_hash == e0.digest()
    assert qd.verify()

def test_exposes_0d_through_11d():
    assert QDLedger.DIMENSIONS == tuple(range(12))
