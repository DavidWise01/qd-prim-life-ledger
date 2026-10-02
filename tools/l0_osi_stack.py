"""Exact L0 tick/carry ledger aligned beneath OSI Layer 1.

Repository-defined simulation semantics:
- base tick = 10^-35 seconds (10^-36 * 10)
- one tick carries state delta -1
- decimal carry normalizes 10 units at exponent e into 1 unit at e+1
- physics/chemistry/cellular are overlays; OSI transports records only

Optimization v2:
- legacy JSON/SHA path retained for equivalence/A-B benchmarking
- hot path uses fixed binary canonical core + 32-byte overlay digests
- ancestry stays append-only and deterministic
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import struct
from time import perf_counter

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

ZERO_DIGEST = bytes(32)
EMPTY_OVERLAY_DIGEST = sha256(b"{}").digest()
CORE_STRUCT = struct.Struct("!QQhq32s32s32s32s")
L2_STRUCT = struct.Struct("!4sQQhq32s")


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


def canonical_overlay_digest(value: dict | None) -> bytes:
    if not value:
        return EMPTY_OVERLAY_DIGEST
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).digest()


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
    """Legacy append-only JSON/SHA reference path."""

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
            if rec.tick != i or rec.state != -i:
                return False
            if rec.elapsed != ExactScale(i, BASE_EXPONENT).normalized():
                return False
            expected = None if i == 1 else self._records[i - 2].digest()
            if rec.parent_hash != expected:
                return False
        return True


@dataclass(frozen=True)
class FastL0Record:
    tick: int
    elapsed: ExactScale
    state: int
    parent_digest: bytes
    physics_digest: bytes
    chemistry_digest: bytes
    cellular_digest: bytes
    digest_bytes: bytes

    @property
    def digest(self) -> str:
        return self.digest_bytes.hex()


class FastL0Ledger:
    """Optimized fixed-width binary provenance path."""

    def __init__(self, retain_records: bool = True) -> None:
        self._tick = 0
        self._last_digest = ZERO_DIGEST
        self._records: list[FastL0Record] | None = [] if retain_records else None

    @property
    def records(self) -> tuple[FastL0Record, ...]:
        return tuple(self._records or ())

    @property
    def tick(self) -> int:
        return self._tick

    @property
    def last_digest(self) -> str:
        return self._last_digest.hex()

    def append(
        self,
        *,
        physics: dict | None = None,
        chemistry: dict | None = None,
        cellular: dict | None = None,
    ) -> FastL0Record:
        self._tick += 1
        elapsed = ExactScale(self._tick, BASE_EXPONENT).normalized()
        p = canonical_overlay_digest(physics)
        c = canonical_overlay_digest(chemistry)
        b = canonical_overlay_digest(cellular)
        parent = self._last_digest
        packed = CORE_STRUCT.pack(
            self._tick,
            elapsed.coefficient,
            elapsed.exponent,
            self._tick * TICK_DELTA,
            parent,
            p,
            c,
            b,
        )
        digest = sha256(packed).digest()
        record = FastL0Record(
            tick=self._tick,
            elapsed=elapsed,
            state=self._tick * TICK_DELTA,
            parent_digest=parent,
            physics_digest=p,
            chemistry_digest=c,
            cellular_digest=b,
            digest_bytes=digest,
        )
        self._last_digest = digest
        if self._records is not None:
            self._records.append(record)
        return record

    def verify(self) -> bool:
        if self._records is None:
            return self._tick >= 0
        parent = ZERO_DIGEST
        for i, rec in enumerate(self._records, start=1):
            if rec.tick != i or rec.state != -i:
                return False
            if rec.elapsed != ExactScale(i, BASE_EXPONENT).normalized():
                return False
            if rec.parent_digest != parent:
                return False
            packed = CORE_STRUCT.pack(
                rec.tick,
                rec.elapsed.coefficient,
                rec.elapsed.exponent,
                rec.state,
                rec.parent_digest,
                rec.physics_digest,
                rec.chemistry_digest,
                rec.cellular_digest,
            )
            if sha256(packed).digest() != rec.digest_bytes:
                return False
            parent = rec.digest_bytes
        return True


def carry(count: int, exponent: int = BASE_EXPONENT) -> ExactScale:
    if count < 0:
        raise ValueError("count must be nonnegative")
    return ExactScale(count, exponent).normalized()


def encode_l2_frame(record: L0Record | FastL0Record) -> bytes:
    n = record.elapsed.normalized()
    if n.coefficient < 0 or n.coefficient > 2**64 - 1:
        raise OverflowError("normalized coefficient does not fit u64")
    digest = (
        bytes.fromhex(record.digest())
        if isinstance(record, L0Record)
        else record.digest_bytes
    )
    return L2_STRUCT.pack(b"QD00", record.tick, n.coefficient, n.exponent, record.state, digest)


def decode_l2_header(frame: bytes) -> dict:
    magic, tick, coefficient, exponent, state, digest = L2_STRUCT.unpack(frame)
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

    t0 = perf_counter()
    last = None
    checksum = 0
    for n in range(1, iterations + 1):
        last = carry(n)
        checksum ^= (last.coefficient & 0xFFFFFFFF) ^ (last.exponent & 0xFFFF)
    arithmetic_s = perf_counter() - t0

    legacy = L0Ledger()
    t1 = perf_counter()
    for _ in range(iterations):
        legacy.append()
    legacy_s = perf_counter() - t1

    fast = FastL0Ledger(retain_records=True)
    t2 = perf_counter()
    for _ in range(iterations):
        fast.append()
    fast_s = perf_counter() - t2

    t3 = perf_counter()
    byte_count = 0
    frame_checksum = 0
    for rec in fast.records:
        frame = encode_l2_frame(rec)
        byte_count += len(frame)
        frame_checksum ^= frame[-1]
    frame_s = perf_counter() - t3

    legacy_rate = iterations / legacy_s
    fast_rate = iterations / fast_s

    return {
        "iterations": iterations,
        "base_tick": "1e-35 s",
        "delta_per_tick": -1,
        "final_state": -iterations,
        "final_elapsed": last.literal() if last else "0e-35",
        "arithmetic_ticks_per_second": iterations / arithmetic_s,
        "legacy_json_hash_records_per_second": legacy_rate,
        "optimized_binary_hash_records_per_second": fast_rate,
        "speedup_vs_legacy": fast_rate / legacy_rate,
        "l2_frames_per_second": iterations / frame_s,
        "l2_bytes_per_second": byte_count / frame_s,
        "l2_frame_bytes": L2_STRUCT.size,
        "legacy_verified": legacy.verify(),
        "optimized_verified": fast.verify(),
        "checksum": checksum,
        "frame_checksum": frame_checksum,
        "elapsed_seconds": {
            "arithmetic": arithmetic_s,
            "legacy_json_hash": legacy_s,
            "optimized_binary_hash": fast_s,
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

    legacy = L0Ledger()
    fast = FastL0Ledger()
    for n in range(1, 101):
        a = legacy.append()
        b = fast.append()
        assert a.tick == b.tick == n
        assert a.elapsed == b.elapsed
        assert a.state == b.state == -n

    assert legacy.verify()
    assert fast.verify()

    frame = encode_l2_frame(fast.records[-1])
    decoded = decode_l2_header(frame)
    assert decoded["tick"] == 100
    assert decoded["elapsed"] == ExactScale(1, -33)
    assert decoded["state"] == -100
    assert decoded["digest"] == fast.records[-1].digest

    sample = {"event": "p", "value": 1}
    assert canonical_overlay_digest(sample) == canonical_overlay_digest({"value": 1, "event": "p"})
    assert overlay_due(100, 10)
    assert not overlay_due(101, 10)
    return True


if __name__ == "__main__":
    print("0e / L0-OSI OPT V2 PASS" if verify() else "xe")
    print(json.dumps(benchmark(), indent=2, sort_keys=True))


# Optimization v3: batched Merkle commit path
MERKLE_LEAF_STRUCT = struct.Struct("!QQhq32s32s32s")
MERKLE_COMMIT_STRUCT = struct.Struct("!4sQQ32s32s")


def _leaf_digest(
    tick: int,
    elapsed: ExactScale,
    state: int,
    physics_digest: bytes,
    chemistry_digest: bytes,
    cellular_digest: bytes,
) -> bytes:
    return sha256(MERKLE_LEAF_STRUCT.pack(
        tick,
        elapsed.coefficient,
        elapsed.exponent,
        state,
        physics_digest,
        chemistry_digest,
        cellular_digest,
    )).digest()


def _merkle_root(leaves: list[bytes]) -> bytes:
    if not leaves:
        return ZERO_DIGEST
    level = list(leaves)
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [
            sha256(level[i] + level[i + 1]).digest()
            for i in range(0, len(level), 2)
        ]
    return level[0]


@dataclass(frozen=True)
class MerkleCommit:
    first_tick: int
    last_tick: int
    root: bytes
    parent_commit: bytes
    digest_bytes: bytes

    @property
    def digest(self) -> str:
        return self.digest_bytes.hex()


class MerkleL0Ledger:
    """Per-tick immutable leaves, batched append-only Merkle commits."""

    def __init__(self, block_size: int = 16, retain_leaves: bool = True) -> None:
        if block_size <= 0:
            raise ValueError("block_size must be positive")
        self.block_size = block_size
        self.retain_leaves = retain_leaves
        self._tick = 0
        self._pending: list[bytes] = []
        self._pending_first_tick: int | None = None
        self._leaves: list[bytes] | None = [] if retain_leaves else None
        self._commits: list[MerkleCommit] = []
        self._last_commit = ZERO_DIGEST

    @property
    def commits(self) -> tuple[MerkleCommit, ...]:
        return tuple(self._commits)

    @property
    def leaves(self) -> tuple[bytes, ...]:
        return tuple(self._leaves or ())

    @property
    def tick(self) -> int:
        return self._tick

    def append(
        self,
        *,
        physics: dict | None = None,
        chemistry: dict | None = None,
        cellular: dict | None = None,
    ) -> bytes:
        self._tick += 1
        elapsed = ExactScale(self._tick, BASE_EXPONENT).normalized()
        p = canonical_overlay_digest(physics)
        c = canonical_overlay_digest(chemistry)
        b = canonical_overlay_digest(cellular)
        leaf = _leaf_digest(self._tick, elapsed, -self._tick, p, c, b)
        if self._pending_first_tick is None:
            self._pending_first_tick = self._tick
        self._pending.append(leaf)
        if self._leaves is not None:
            self._leaves.append(leaf)
        if len(self._pending) >= self.block_size:
            self.flush()
        return leaf

    def flush(self) -> MerkleCommit | None:
        if not self._pending:
            return None
        first_tick = self._pending_first_tick
        assert first_tick is not None
        last_tick = first_tick + len(self._pending) - 1
        root = _merkle_root(self._pending)
        payload = MERKLE_COMMIT_STRUCT.pack(
            b"QDMK",
            first_tick,
            last_tick,
            root,
            self._last_commit,
        )
        digest = sha256(payload).digest()
        commit = MerkleCommit(
            first_tick=first_tick,
            last_tick=last_tick,
            root=root,
            parent_commit=self._last_commit,
            digest_bytes=digest,
        )
        self._commits.append(commit)
        self._last_commit = digest
        self._pending = []
        self._pending_first_tick = None
        return commit

    def finalize(self) -> bytes:
        self.flush()
        return self._last_commit

    def verify(self) -> bool:
        if self._pending:
            return False
        parent = ZERO_DIGEST
        for commit in self._commits:
            if commit.parent_commit != parent:
                return False
            payload = MERKLE_COMMIT_STRUCT.pack(
                b"QDMK",
                commit.first_tick,
                commit.last_tick,
                commit.root,
                commit.parent_commit,
            )
            if sha256(payload).digest() != commit.digest_bytes:
                return False
            parent = commit.digest_bytes
        if self._leaves is not None:
            pos = 0
            for commit in self._commits:
                count = commit.last_tick - commit.first_tick + 1
                block = self._leaves[pos:pos + count]
                if _merkle_root(block) != commit.root:
                    return False
                pos += count
            if pos != len(self._leaves):
                return False
        return True


def benchmark_merkle_block_sizes(iterations: int = 200_000, block_sizes: tuple[int, ...] = (4, 8, 16, 32, 64)) -> dict:
    results = {}
    for block_size in block_sizes:
        ledger = MerkleL0Ledger(block_size=block_size, retain_leaves=True)
        t0 = perf_counter()
        for _ in range(iterations):
            ledger.append()
        ledger.finalize()
        elapsed = perf_counter() - t0
        results[str(block_size)] = {
            "records_per_second": iterations / elapsed,
            "seconds": elapsed,
            "commit_count": len(ledger.commits),
            "verified": ledger.verify(),
            "final_commit": ledger.commits[-1].digest if ledger.commits else ZERO_DIGEST.hex(),
        }
    best = max(results, key=lambda k: results[k]["records_per_second"])
    return {
        "iterations": iterations,
        "results": results,
        "best_block_size": int(best),
        "best_records_per_second": results[best]["records_per_second"],
    }


def verify_merkle_v3() -> bool:
    for block_size in (4, 8, 16, 32):
        ledger = MerkleL0Ledger(block_size=block_size, retain_leaves=True)
        for _ in range(101):
            ledger.append()
        ledger.finalize()
        assert ledger.tick == 101
        assert ledger.verify()
        assert ledger.commits[0].first_tick == 1
        assert ledger.commits[-1].last_tick == 101
    return True
