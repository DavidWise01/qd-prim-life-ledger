"""Exact L0 tick/carry ledger aligned beneath OSI Layer 1.

Repository-defined simulation semantics:
- base tick = 10^-35 seconds (10^-36 * 10)
- one tick carries state delta -1
- decimal carry normalizes 10 units at exponent e into 1 unit at e+1
- physics/chemistry/cellular are overlays; OSI transports records only
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import struct
from time import perf_counter
from typing import Callable

BASE_EXPONENT = -35
TICK_DELTA = -1
OSI_LAYERS = {
    0: "exact_tick_ledger",
    1: "physical",
    2: "data_link",
    3: "network",
    4: "transport",
    5: "session",
    6: "presentation",
    7: "application",
}


@dataclass(frozen=True)
class ExactScale:
    coefficient: int
    exponent: int

    def normalized(self) -> "ExactScale":
        c, e = self.coefficient, self.exponent
        if c == 0:
            return ExactScale(0, e)
        while c % 10 == 0:
            c //= 10
            e += 1
        return ExactScale(c, e)

    def literal(self) -> str:
        n = self.normalized()
        return f"{n.coefficient}e{n.exponent}"


@dataclass(frozen=True)
class L0Record:
    tick: int
    elapsed: ExactScale
    state: int
    physics: dict
    chemistry: dict
    cellular: dict
    parent_hash: str | None

    def canonical_bytes(self) -> bytes:
        payload = {
            "tick": self.tick,
            "elapsed": {
                "coefficient": self.elapsed.normalized().coefficient,
                "exponent": self.elapsed.normalized().exponent,
            },
            "state": self.state,
            "physics": self.physics,
            "chemistry": self.chemistry,
            "cellular": self.cellular,
            "parent_hash": self.parent_hash,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()

    def digest(self) -> str:
        return sha256(self.canonical_bytes()).hexdigest()


class L0Ledger:
    """Append-only exact-integer clock beneath the OSI stack."""

    def __init__(self) -> None:
        self._records: list[L0Record] = []

    @property
    def records(self) -> tuple[L0Record, ...]:
        return tuple(self._records)

    def append(
        self,
        *,
        physics: dict | None = None,
        chemistry: dict | None = None,
        cellular: dict | None = None,
    ) -> L0Record:
        tick = len(self._records) + 1
        elapsed = ExactScale(tick, BASE_EXPONENT).normalized()
        parent = self._records[-1].digest() if self._records else None
        record = L0Record(
            tick=tick,
            elapsed=elapsed,
            state=tick * TICK_DELTA,
            physics=dict(physics or {}),
            chemistry=dict(chemistry or {}),
            cellular=dict(cellular or {}),
            parent_hash=parent,
        )
        self._records.append(record)
        return record

    def verify(self) -> bool:
        for i, rec in enumerate(self._records, start=1):
            if rec.tick != i:
                return False
            if rec.state != -i:
                return False
            if rec.elapsed != ExactScale(i, BASE_EXPONENT).normalized():
                return False
            expected = None if i == 1 else self._records[i - 2].digest()
            if rec.parent_hash != expected:
                return False
        return True


def carry(count: int, exponent: int = BASE_EXPONENT) -> ExactScale:
    if count < 0:
        raise ValueError("count must be nonnegative")
    return ExactScale(count, exponent).normalized()


def encode_l2_frame(record: L0Record) -> bytes:
    """Compact deterministic Layer-2 carrier for one L0 snapshot.

    Header:
      magic 4 bytes | tick u64 | coefficient u64 | exponent i16 | state i64
      digest 32 bytes
    The overlays remain in the canonical hash and can be transported separately.
    """
    n = record.elapsed.normalized()
    if n.coefficient < 0 or n.coefficient > 2**64 - 1:
        raise OverflowError("normalized coefficient does not fit u64")
    digest = bytes.fromhex(record.digest())
    return struct.pack("!4sQQhq32s", b"QD00", record.tick, n.coefficient, n.exponent, record.state, digest)


def decode_l2_header(frame: bytes) -> dict:
    magic, tick, coefficient, exponent, state, digest = struct.unpack("!4sQQhq32s", frame)
    if magic != b"QD00":
        raise ValueError("bad frame magic")
    return {
        "tick": tick,
        "elapsed": ExactScale(coefficient, exponent),
        "state": state,
        "digest": digest.hex(),
    }


def overlay_due(tick: int, stride: int) -> bool:
    if stride <= 0:
        raise ValueError("stride must be positive")
    return tick % stride == 0


def benchmark(iterations: int = 200_000) -> dict:
    if iterations <= 0:
        raise ValueError("iterations must be positive")

    # Arithmetic-only exact tick/carry path.
    t0 = perf_counter()
    last = None
    checksum = 0
    for n in range(1, iterations + 1):
        last = carry(n)
        checksum ^= (last.coefficient & 0xFFFFFFFF) ^ (last.exponent & 0xFFFF)
    arithmetic_s = perf_counter() - t0

    # Full append + SHA-256 provenance + three empty overlays.
    ledger = L0Ledger()
    t1 = perf_counter()
    for _ in range(iterations):
        ledger.append()
    append_s = perf_counter() - t1

    # Compact L2 framing from existing immutable records.
    t2 = perf_counter()
    byte_count = 0
    frame_checksum = 0
    for rec in ledger.records:
        frame = encode_l2_frame(rec)
        byte_count += len(frame)
        frame_checksum ^= frame[-1]
    frame_s = perf_counter() - t2

    return {
        "iterations": iterations,
        "base_tick": "1e-35 s",
        "delta_per_tick": -1,
        "final_state": -iterations,
        "final_elapsed": last.literal() if last else "0e-35",
        "arithmetic_ticks_per_second": iterations / arithmetic_s,
        "append_hash_records_per_second": iterations / append_s,
        "l2_frames_per_second": iterations / frame_s,
        "l2_bytes_per_second": byte_count / frame_s,
        "l2_frame_bytes": len(encode_l2_frame(ledger.records[-1])),
        "ledger_verified": ledger.verify(),
        "checksum": checksum,
        "frame_checksum": frame_checksum,
        "elapsed_seconds": {
            "arithmetic": arithmetic_s,
            "append_hash": append_s,
            "l2_frame": frame_s,
        },
    }


def verify() -> bool:
    assert OSI_LAYERS[0] == "exact_tick_ledger"
    assert OSI_LAYERS[1] == "physical"
    assert carry(9) == ExactScale(9, -35)
    assert carry(10) == ExactScale(1, -34)
    assert carry(100) == ExactScale(1, -33)
    assert carry(1000) == ExactScale(1, -32)

    ledger = L0Ledger()
    for _ in range(100):
        ledger.append()
    assert ledger.verify()
    assert ledger.records[9].elapsed == ExactScale(1, -34)
    assert ledger.records[99].elapsed == ExactScale(1, -33)
    assert ledger.records[-1].state == -100

    frame = encode_l2_frame(ledger.records[-1])
    decoded = decode_l2_header(frame)
    assert decoded["tick"] == 100
    assert decoded["elapsed"] == ExactScale(1, -33)
    assert decoded["state"] == -100
    assert decoded["digest"] == ledger.records[-1].digest()

    assert overlay_due(100, 10)
    assert not overlay_due(101, 10)
    return True


if __name__ == "__main__":
    print("0e / L0-OSI ALIGN PASS" if verify() else "xe")
    print(json.dumps(benchmark(), indent=2, sort_keys=True))
