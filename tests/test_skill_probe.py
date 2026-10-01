from src.qd_prim import MotherKernel, QDLedger
from tools.skill_probe import assess_skill


def _append_demo(qd: QDLedger, count: int):
    operator = "unary" if count == 1 else "binary" if count == 2 else "ternary"
    return qd.append(
        dimension=3,
        choice=f"skill-{count}",
        consequence="demonstrate",
        affect="append-only",
        state={"operator": operator, "operands": list(range(1, count + 1))},
    )


def test_empty_qd_skill_is_zero():
    result = assess_skill(QDLedger("paralax"))
    assert result.level == 0
    assert result.operator_mode == "none"
    assert result.evidence_plank is None
    assert result.valid_chain is True


def test_paralax_qd_skill_progresses_append_only_1_to_5():
    daughter = MotherKernel.infer_daughter("paralax")
    qd = QDLedger(daughter.name)
    observed = []
    for count in range(1, 6):
        _append_demo(qd, count)
        result = assess_skill(qd)
        observed.append(result.level)
        assert result.level == count
        assert result.max_operands == count
        assert result.evidence_plank == count - 1
        assert qd.verify()
    assert observed == [1, 2, 3, 4, 5]
    assert assess_skill(qd).operator_mode == "ternary"


def test_skill_probe_ignores_bad_operator_claim():
    qd = QDLedger("paralax")
    qd.append(
        dimension=3, choice="invalid-skill-claim", consequence="ignored",
        affect="append-only",
        state={"operator": "unary", "operands": [1, 2, 3, 4, 5]},
    )
    assert assess_skill(qd).level == 0


def test_skill_probe_caps_at_five_payload_primitive():
    qd = QDLedger("paralax")
    qd.append(
        dimension=3, choice="six-payload-overflow", consequence="ignored",
        affect="append-only",
        state={"operator": "ternary", "operands": [1, 2, 3, 4, 5, 6]},
    )
    assert assess_skill(qd).level == 0
