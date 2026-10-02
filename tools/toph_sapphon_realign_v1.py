from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
import json
from math import prod
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "data" / "toph_sapphon_realign_v1.json"


def model() -> dict:
    return json.loads(MODEL_PATH.read_text(encoding="utf-8"))


def derive() -> dict:
    m = model()
    v = m["scalar0"]["vectors"]
    pair = Decimal(str(v["B"]["value"])) + Decimal(str(v["C"]["value"]))
    total = Decimal(str(v["A"]["value"])) + pair

    dims = m["stargate"]["dimensions"]
    neg = m["homeostasis"]["negative_spinors"]
    pos = m["homeostasis"]["positive_spinors"]

    matter_total = sum(Fraction(m["matter5"]["equal_fraction"]) for _ in m["matter5"]["lanes"])
    force_total = sum(Fraction(b["fraction"]) for b in m["toroid"]["force_bands"])

    return {
        "vector_pair_sum": str(pair),
        "vector_total": str(total),
        "prim_mirror": m["prim"]["left"][::-1] == m["prim"]["right"],
        "stargate_palindrome": m["stargate"]["gate"] == list(reversed(m["stargate"]["gate"])),
        "nested_box_positions": prod(dims),
        "active_spinors": len(neg) + len(pos),
        "spinor_pairs": min(len(neg), len(pos)),
        "dual_spinor_full_time": m["homeostasis"]["dual_spinor_full_time"],
        "composite_spinor_degrees": min(len(neg), len(pos)) * m["homeostasis"]["dual_spinor_full_time"],
        "epoch_internal_ticks": m["dual_universe_epoch"]["full_time"] * 2 // 5,
        "epoch_external_ticks": m["dual_universe_epoch"]["full_time"] * 3 // 5,
        "epoch_ticks": m["dual_universe_epoch"]["full_time"],
        "matter_total": str(matter_total),
        "force_total": str(force_total),
        "subgeneration_capacity": (3 * 3) ** 3,
        "deterministic": m["determinism"]["probability_layer"] is False,
    }


def verify() -> bool:
    m = model()
    d = derive()

    assert m["authority"]["frozen_mother_kernel_modified"] is False
    assert m["authority"]["mother_generation_limit_modified"] is False
    assert d["vector_pair_sum"] == "0.0000"
    assert d["vector_total"] == "33.0000"
    assert d["prim_mirror"] is True
    assert d["stargate_palindrome"] is True
    assert d["nested_box_positions"] == 2304
    assert d["active_spinors"] == 10
    assert d["spinor_pairs"] == 5
    assert d["dual_spinor_full_time"] == 1440
    assert d["composite_spinor_degrees"] == 7200
    assert d["epoch_internal_ticks"] == 576
    assert d["epoch_external_ticks"] == 864
    assert d["epoch_internal_ticks"] + d["epoch_external_ticks"] == d["epoch_ticks"]
    assert d["matter_total"] == "1"
    assert d["force_total"] == "1"
    assert d["subgeneration_capacity"] == 729
    assert d["deterministic"] is True

    assert m["implication"] == {
        "literal": "{{i}}",
        "meaning": "aether morphic implication",
        "state_space_index": False,
    }
    assert m["invariant_ports"]["mandel"] == "000"
    assert m["invariant_ports"]["juliet"] == "000"
    assert m["invariant_ports"]["same_invariant_value"] is True
    assert m["homeostasis"]["center_counts_as_active_spinor"] is False
    assert m["ancestry"]["literal_identity_claim"] is False
    assert m["life_development"]["clinical_claim"] is False
    assert m["scale_tunnel"]["quantum_tunneling_claim"] is False
    assert m["public_fixture_policy"]["personal_named_birth_or_medical_example_committed"] is False
    return True


if __name__ == "__main__":
    print(json.dumps(derive(), indent=2, sort_keys=True))
    print("0e / TOPH SAPPHON REALIGN V1 PASS" if verify() else "xe")
