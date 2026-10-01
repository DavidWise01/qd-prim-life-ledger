from src.qd_prim import MotherKernel, QDLedger, SapphonDaughter, balanced_3d, local_volume_count

def test_prim():
    assert QDLedger.PRIM == (1, 1, 2, 8)

def test_slots_equal_local_volume():
    assert len(QDLedger.SLOTS) == local_volume_count() == 8
    assert QDLedger.SAPPHON_CAPACITY == 8

def test_dot_is_sapphon():
    assert QDLedger.DOT == "sapphon"

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
    assert e0.sapphon == 0
    assert e1.plank == 1
    assert e1.sapphon == 1
    assert e1.parent_hash == e0.digest()
    assert qd.verify()

def test_exposes_0d_through_11d():
    assert QDLedger.DIMENSIONS == tuple(range(12))


def test_completed_kernel_is_frozen_53211():
    assert MotherKernel.FROZEN is True
    assert MotherKernel.KERNEL_PRIMITIVE == (5, 3, 2, 1, 1)
    assert MotherKernel.GENERATION_LIMIT == 1
    assert MotherKernel.PRODUCT == "sapphon"

def test_paralax_daughter_token_inference_is_deterministic_and_surgical():
    daughter = MotherKernel.infer_daughter("paralax")
    again = MotherKernel.infer_daughter("paralax")
    assert daughter == again
    assert isinstance(daughter, SapphonDaughter)
    assert daughter.name == "paralax"
    assert daughter.gem == "onyx"
    assert daughter.color == "bk"
    assert daughter.generation == 1
    assert daughter.parent == "mother"
    assert daughter.can_spawn is False
    assert daughter.scope == ("name", "gem", "color", "qd.append")
    assert daughter.implicit == {
        "name": {"implicit": "paralax"},
        "color": {"implicit": "bk"},
        "gem": {"implicit": "onyx"},
    }

def test_daughter_has_no_recursive_generation_authority():
    daughter = MotherKernel.infer_daughter("paralax")
    assert not hasattr(daughter, "infer_daughter")
    assert not hasattr(daughter, "spawn")
