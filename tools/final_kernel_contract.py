"""Verifier for the terminal q.d final-kernel contract."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "data" / "final_kernel_contract.json"

PIPELINE = ("Event", "Commit", "Prove", "Project", "Transport")
STATUS = "FINAL / FROZEN / APPEND-ONLY"


def load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def verify() -> bool:
    c = load_contract()
    assert c["schema"] == "qd.final.kernel.v1"
    assert c["status"] == STATUS
    assert tuple(c["pipeline"]) == PIPELINE
    assert c["primitive"]["prim"] == [1, 1, 2, 8]
    assert c["primitive"]["mother"] == [5, 3, 2, 1, 1]
    assert c["primitive"]["dot"] == "sapphon"
    assert c["primitive"]["append_rule"] == "prim, append only, add to next"
    assert c["primitive"]["base_tick"] == "1e-35 s"
    assert c["primitive"]["tick_delta"] == -1

    boundary = c["kernel_boundary"]
    assert boundary["final"] is True
    assert boundary["frozen"] is True
    assert boundary["source_overwrite"] is False
    assert boundary["recursive_generation"] is False
    assert boundary["new_kernel_semantics_allowed"] is False

    covered = set()
    for role in PIPELINE:
        paths = c["roles"][role]
        assert paths, f"{role} must have at least one implementation"
        for rel in paths:
            assert (ROOT / rel).exists(), f"missing {role} implementation: {rel}"
            covered.add(rel)

    # Core spine must participate in the intended unified roles.
    assert "src/qd_prim.py" in c["roles"]["Event"]
    assert "tools/l0_osi_stack.py" in c["roles"]["Event"]
    assert "tools/l0_osi_stack.py" in c["roles"]["Commit"]
    assert "tools/l0_osi_stack.py" in c["roles"]["Prove"]
    assert "tools/l0_osi_stack.py" in c["roles"]["Transport"]
    assert "tools/toph_merkle_backdraft_v3.py" in c["roles"]["Prove"]
    assert len(covered) >= 10
    return True


if __name__ == "__main__":
    print("0e / FINAL KERNEL PASS" if verify() else "xe")
