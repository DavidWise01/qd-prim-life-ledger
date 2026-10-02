from tools.final_kernel_contract import PIPELINE, STATUS, load_contract, verify


def test_final_kernel_status_is_terminal():
    c = load_contract()
    assert STATUS == "FINAL / FROZEN / APPEND-ONLY"
    assert c["kernel_boundary"]["final"] is True
    assert c["kernel_boundary"]["frozen"] is True
    assert c["kernel_boundary"]["new_kernel_semantics_allowed"] is False


def test_single_unified_pipeline():
    c = load_contract()
    assert tuple(c["pipeline"]) == PIPELINE == (
        "Event", "Commit", "Prove", "Project", "Transport"
    )


def test_final_kernel_preserves_existing_primitives():
    c = load_contract()
    assert c["primitive"]["prim"] == [1, 1, 2, 8]
    assert c["primitive"]["mother"] == [5, 3, 2, 1, 1]
    assert c["primitive"]["dot"] == "sapphon"
    assert c["primitive"]["base_tick"] == "1e-35 s"
    assert c["primitive"]["tick_delta"] == -1


def test_no_source_overwrite_or_recursive_generation():
    c = load_contract()
    b = c["kernel_boundary"]
    assert b["source_overwrite"] is False
    assert b["recursive_generation"] is False


def test_contract_verifies():
    assert verify()
