"""Read-only {{i::mpli::c::it::}} mnemonic overlay for the H::UMANITY corpus."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

OVERLAY_PATH = Path(__file__).resolve().parents[1] / "data" / "mnemonic_overlay.json"

PHASES = (
    "creation", "electrum", "matter", "tm8", "gas",
    "liquid", "solid", "plasma", "nature",
)

SHADOW = (
    ("CEM", "CHEM"),
    ("TGL", "TOGGLE"),
    ("SPN", "SPIN"),
)

LIGHT = (
    ("PNC", "PINCH"),
    ("EMT", "EMIT"),
    ("GLS", "GLASS"),
)

AIR_LITERAL = "2x1^10^-35.99 - {air 36.00}} +36.01"
AIR_NORMALIZED = "2 x 1^10^-35.99 - {air 36.00} + 36.01"


@dataclass(frozen=True)
class MnemonicHit:
    slot: int
    side: str
    skeleton: str
    expansion: str
    phases: tuple[str, str, str]


def load_overlay() -> dict:
    return json.loads(OVERLAY_PATH.read_text(encoding="utf-8"))


def preserves_order(skeleton: str, expansion: str) -> bool:
    """True when skeleton letters occur in expansion in the same order."""
    it = iter(expansion.upper())
    return all(any(ch == wanted for ch in it) for wanted in skeleton.upper())


def triplet_for_slot(slot: int, side: str) -> tuple[str, str]:
    if not 0 <= slot < 40:
        raise ValueError("slot must be 0..39")
    if side == "shadow":
        return SHADOW[slot % 3]
    if side == "light":
        return LIGHT[(slot - 20) % 3]
    raise ValueError("side must be shadow or light")


def phases_for_skeleton(skeleton: str) -> tuple[str, str, str]:
    overlay = load_overlay()
    for group in overlay["shadow_triplets"] + overlay["light_triplets"]:
        if group["skeleton"] == skeleton:
            return tuple(group["phases"])
    raise KeyError(skeleton)


def decode_slot(slot: int, side: str) -> MnemonicHit:
    skeleton, expansion = triplet_for_slot(slot, side)
    if not preserves_order(skeleton, expansion):
        raise ValueError("implicit expansion reordered skeleton")
    return MnemonicHit(
        slot=slot,
        side=side,
        skeleton=skeleton,
        expansion=expansion,
        phases=phases_for_skeleton(skeleton),
    )


def decode_all() -> tuple[MnemonicHit, ...]:
    hits = []
    for slot in range(40):
        side = "shadow" if slot < 20 else "light"
        hits.append(decode_slot(slot, side))
    return tuple(hits)


def air_boundary() -> dict:
    """Return the immutable symbolic AIR bracket exactly as configured."""
    return load_overlay()["air_boundary"]
