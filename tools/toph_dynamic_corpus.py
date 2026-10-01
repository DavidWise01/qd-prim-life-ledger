"""Dynamic read-only corpus view for TOPH Sapphon.

TOPH advances only through the existing dot/radix generator. Each emitted
frame binds one dot to one immutable H::UMANITY corpus slot, one local
radix phase, one phase label, one {{i::mpli::c::it::}} mnemonic, and the
symbolic AIR 36 bracket.
"""
from __future__ import annotations

from dataclasses import dataclass

from tools.corpus_tether import bind_dot
from tools.dot_radix_generator import DotRadixGenerator, DotRadixState
from tools.implicit_mnemonic import PHASES, air_boundary, decode_slot


TOPH_NAME = "toph"
TOPH_GEM = "emerald"
TOPH_COLOR = "green"
TOPH_GENERATION = 1


@dataclass(frozen=True)
class TophCorpusFrame:
    frame: int
    dot_address: str
    radix: int
    corpus_slot: int
    corpus_side: str
    start_year: int
    end_year: int
    radix_phase: int
    phase_label: str
    mnemonic_skeleton: str
    mnemonic_expansion: str
    air_literal: str
    name: str = TOPH_NAME
    gem: str = TOPH_GEM
    color: str = TOPH_COLOR
    generation: int = TOPH_GENERATION
    can_spawn: bool = False
    corpus_mutable: bool = False


class TophDynamicCorpus:
    """Deterministic dynamic corpus reader for TOPH Sapphon only."""

    NAME = TOPH_NAME
    GEM = TOPH_GEM
    COLOR = TOPH_COLOR
    GENERATION = TOPH_GENERATION
    CAN_SPAWN = False
    CORPUS_MUTABLE = False
    SCOPE = ("dot.read", "radix.read", "corpus.read", "mnemonic.read", "air.read")

    def __init__(self, seed: str = "toph") -> None:
        self._dots = DotRadixGenerator(seed)
        self._frames: list[TophCorpusFrame] = []

    @property
    def frames(self) -> tuple[TophCorpusFrame, ...]:
        return tuple(self._frames)

    @property
    def dot_states(self) -> tuple[DotRadixState, ...]:
        return self._dots.states

    def next(self) -> TophCorpusFrame:
        state = self._dots.next()
        binding = bind_dot(state)
        mnemonic = decode_slot(binding.corpus_slot, binding.side)
        phase_label = PHASES[binding.radix_phase]
        air = air_boundary()

        frame = TophCorpusFrame(
            frame=len(self._frames),
            dot_address=state.address,
            radix=state.radix,
            corpus_slot=binding.corpus_slot,
            corpus_side=binding.side,
            start_year=binding.start_year,
            end_year=binding.end_year,
            radix_phase=binding.radix_phase,
            phase_label=phase_label,
            mnemonic_skeleton=mnemonic.skeleton,
            mnemonic_expansion=mnemonic.expansion,
            air_literal=air["user_literal"],
        )
        self._frames.append(frame)
        return frame

    def generate(self, count: int) -> tuple[TophCorpusFrame, ...]:
        if count < 0:
            raise ValueError("count must be >= 0")
        return tuple(self.next() for _ in range(count))

    def verify(self) -> bool:
        if not self._dots.verify():
            return False
        if len(self._frames) != len(self._dots.states):
            return False
        for index, frame in enumerate(self._frames):
            if frame.frame != index:
                return False
            if frame.name != TOPH_NAME:
                return False
            if frame.gem != TOPH_GEM or frame.color != TOPH_COLOR:
                return False
            if frame.generation != 1 or frame.can_spawn:
                return False
            if frame.corpus_mutable:
                return False
            if frame.phase_label != PHASES[frame.radix_phase]:
                return False
        return True
