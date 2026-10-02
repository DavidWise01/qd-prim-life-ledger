"""Read-only alchemical cipher projected over the frozen humanity corpus."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

from tools.corpus_tether import load_corpus
from tools.implicit_mnemonic import decode_slot, PHASES

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "data" / "alchemical_cipher_v1.json"

LIFE_YEARS = 90
RADIX_POSITIONS_PER_LIFE = 9
YEARS_PER_RADIX_POSITION = LIFE_YEARS // RADIX_POSITIONS_PER_LIFE

CIPHER = {
    "1m": {
        "sex": "male",
        "axis": "y",
        "roles": ("base",),
        "literal": "male = y = base",
    },
    "0f": {
        "sex": "female",
        "axis": "x",
        "roles": ("acid", "philosopher_stone"),
        "literal": "female = x = acid + philosopher stone",
    },
}


@dataclass(frozen=True)
class AlchemicalSlot:
    slot: int
    side: str
    sex_code: str
    sex: str
    axis: str
    roles: tuple[str, ...]
    literal: str
    start_year: int
    end_year: int
    life_years: int
    mnemonic_skeleton: str
    mnemonic_expansion: str
    mnemonic_phases: tuple[str, str, str]


@dataclass(frozen=True)
class AlchemicalTick:
    radix: int
    slot: int
    local_phase: int
    phase_label: str
    start_year: int
    end_year: int
    sex: str
    axis: str
    roles: tuple[str, ...]


def model() -> dict:
    return json.loads(MODEL_PATH.read_text(encoding="utf-8"))


def project_slot(slot: int) -> AlchemicalSlot:
    corpus = load_corpus()
    if not 0 <= slot < len(corpus["slots"]):
        raise ValueError("slot must be 0..39")
    rec = corpus["slots"][slot]
    cipher = CIPHER[rec["sex_code"]]
    mnemonic = decode_slot(slot, rec["side"])
    return AlchemicalSlot(
        slot=slot,
        side=rec["side"],
        sex_code=rec["sex_code"],
        sex=cipher["sex"],
        axis=cipher["axis"],
        roles=cipher["roles"],
        literal=cipher["literal"],
        start_year=rec["start_year"],
        end_year=rec["end_year"],
        life_years=rec["life_years"],
        mnemonic_skeleton=mnemonic.skeleton,
        mnemonic_expansion=mnemonic.expansion,
        mnemonic_phases=mnemonic.phases,
    )


def project_all_slots() -> tuple[AlchemicalSlot, ...]:
    return tuple(project_slot(i) for i in range(40))


def project_radix(radix: int) -> AlchemicalTick:
    if not 0 <= radix < 360:
        raise ValueError("radix must be 0..359")
    slot = radix // RADIX_POSITIONS_PER_LIFE
    local = radix % RADIX_POSITIONS_PER_LIFE
    projected = project_slot(slot)
    start = projected.start_year + local * YEARS_PER_RADIX_POSITION
    end = start + YEARS_PER_RADIX_POSITION
    return AlchemicalTick(
        radix=radix,
        slot=slot,
        local_phase=local,
        phase_label=PHASES[local],
        start_year=start,
        end_year=end,
        sex=projected.sex,
        axis=projected.axis,
        roles=projected.roles,
    )


def project_all_radix() -> tuple[AlchemicalTick, ...]:
    return tuple(project_radix(i) for i in range(360))


def verify() -> bool:
    m = model()
    assert m["kernel_modified"] is False
    assert YEARS_PER_RADIX_POSITION == 10
    slots = project_all_slots()
    assert len(slots) == 40
    assert sum(s.sex == "male" for s in slots) == 20
    assert sum(s.sex == "female" for s in slots) == 20
    assert all(s.axis == ("y" if s.sex == "male" else "x") for s in slots)
    assert all(s.roles == (("base",) if s.sex == "male" else ("acid", "philosopher_stone")) for s in slots)

    ticks = project_all_radix()
    assert len(ticks) == 360
    for slot in range(40):
        chunk = ticks[slot * 9:(slot + 1) * 9]
        source = slots[slot]
        assert chunk[0].start_year == source.start_year
        assert chunk[-1].end_year == source.end_year
        assert [t.local_phase for t in chunk] == list(range(9))
        assert [t.phase_label for t in chunk] == list(PHASES)
    return True


if __name__ == "__main__":
    print("0e / ALCHEMICAL CIPHER USE-CASE PASS" if verify() else "xe")
