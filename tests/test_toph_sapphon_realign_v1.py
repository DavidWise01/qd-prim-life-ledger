from tools.toph_sapphon_realign_v1 import derive, model, verify


def test_realign_is_append_only_and_deterministic():
    m = model()
    assert m["schema"] == "toph.sapphon.realign.v1"
    assert m["authority"]["frozen_mother_kernel_modified"] is False
    assert m["determinism"]["probability_layer"] is False
    assert m["determinism"]["unknown"] == "fixed reality; observer missing state"


def test_scalar_prim_and_toroid_invariants():
    m = model()
    d = derive()
    assert d["vector_pair_sum"] == "0.0000"
    assert d["vector_total"] == "33.0000"
    assert d["prim_mirror"] is True
    assert m["toroid"]["literal"] == "(Au(Ag))-+-+(Ag(Au))"
    assert m["toroid"]["dual_pin_literal"] == "pin - pin | pin + pin - pin | pin +"
    assert d["force_total"] == "1"


def test_homeo_gate_spinor_epoch_invariants():
    m = model()
    d = derive()
    assert m["homeostasis"]["envelope_literal"] == "{-{{-5{0}5+}}+}"
    assert d["active_spinors"] == 10
    assert d["spinor_pairs"] == 5
    assert d["composite_spinor_degrees"] == 7200
    assert d["stargate_palindrome"] is True
    assert d["nested_box_positions"] == 2304
    assert m["stargate"]["throat"] == "4224"
    assert d["epoch_internal_ticks"] == 576
    assert d["epoch_external_ticks"] == 864


def test_matter_lineage_and_decomposition_clock():
    m = model()
    d = derive()
    assert d["matter_total"] == "1"
    assert m["ancestry"]["trace_horizon_years"] == 100000
    assert m["ancestry"]["reconstruction_window_years"] == 10000
    assert m["ancestry"]["decomposition_reserve_literal"] == "+20% if available"
    assert d["subgeneration_capacity"] == 729
    assert [g["label"] for g in m["life_development"]["generations"]] == ["Aa", "Bb", "Cc", "Dd", "Ee"]


def test_i_is_morphic_implication_not_state_index():
    m = model()
    assert m["implication"]["literal"] == "{{i}}"
    assert m["implication"]["meaning"] == "aether morphic implication"
    assert m["implication"]["state_space_index"] is False


def test_public_fixture_omits_personal_health_and_birth_example():
    m = model()
    assert m["public_fixture_policy"]["personal_named_birth_or_medical_example_committed"] is False


def test_full_verifier():
    assert verify() is True
