# TOPH + Sapphon + Soft Transmon Infrastructure v1

**Status:** FROZEN / APPEND-ONLY / SIMULATION INFRASTRUCTURE

This binding does not modify the final q.d kernel, the frozen soft-transmon
contract, or the existing TOPH/Sapphon realignment overlay.

## Meaning

The soft-transmon layer acts as a deterministic phase clock:

```
0.00 -> 0.25 -> 0.50 -> 0.75 -> 0.00 -> oe
```

Each tick exposes one local `2^3 = 8` register.

Sapphon acts as the snapshot/state-realization plane:

```
GLOBE[n] -> +1 tick -> GLOBE[n+1]
```

TOPH acts as the proof/provenance/routing plane:

```
Event -> Commit -> Prove -> Project -> Transport
```

## Infrastructure path

```
SoftTransmonClock
      |
      v
SapphonSnapshot
      |
      v
TOPHCommit
      |
      v
TOPHProve
      |
      v
TOPHProject
      |
      v
TOPHTransport
      |
      v
oe
```

At tick 4 the normalized phase returns to zero, producing the `oe` transport
checkpoint. The seed relation remains:

```
+k.0.k- -> 0.0.0
```

This is a simulation architecture, not a claim of hardware-level transmon
behavior or experimentally established quantum infrastructure.
