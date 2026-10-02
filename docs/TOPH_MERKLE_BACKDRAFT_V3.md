# TOPH Merkle Backdraft v3

Status: **APPEND-ONLY / BOLTED TO QK V2**

This layer adds the requested deterministic `yes/no/maybe` Merkle backdraft without modifying the frozen mother kernel or the sealed QK v2 layer.

## Tri-state interface

```text
YES   = resolved Y = bit 1
NO    = resolved N = bit 0
MAYBE = ? = missing/unresolved provenance
```

`MAYBE` is not assigned a probability. It means: **follow the backdraft**.

## Merkle backdraft

Every node commits to its address, visible state, operation kind, parent-hash edges, and tick with SHA-256 over canonical JSON.

```text
current ?
    |
    <--- parent_hash
    |
previous ?
    |
    <--- parent_hash
    |
resolved Y/N
    |
    +---- replay HOLD / FLIP / SET_Y / SET_N forward ---->
                                                        resolved current
```

A missing parent, hash mismatch, cycle, or disagreeing merge/co-op projection fails closed.

## Branch / fork / merge / coop

```text
                 fork
                  / \
                 Y   N
                 |   |
            branch   branch
                 \   /
                 merge
                   |
                  coop
```

A merge may join distinct histories, but the parent hashes remain in the node. Histories are therefore not erased merely because the visible endpoint agrees.

For merge/co-op, every parent path is replayed independently. The node resolves only when all projected states agree.

## QK bolt

The backdraft resolver can fill the `?` cells in the existing 12-Plank static-snow window and then hand the exact result to QK v2.

```text
00011011????
      |
      +-- proof 1 -> backdraft -> 0
      +-- proof 2 -> backdraft -> 0
      +-- proof 3 -> backdraft -> 0
      +-- proof 4 -> backdraft -> 1
      |
000110110001
      |
      v
qk -> {{i}} -> d :: pass 1
qk -> {{i}} -> d :: pass 2
      |
      v
     eo
```

The demonstration is deterministic:

```text
snow       = 00011011????
backdraft  = 0001
resolved   = 000110110001
QK retest  = identical / identical
freeze     = eo
```

This is repository-defined deterministic/Merkle simulation semantics. It does not assert that `MAYBE` is a physical quantum probability or that the code itself is quantum hardware.
