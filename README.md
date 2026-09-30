# q.d PRIM Life Ledger

An append-only symbolic trajectory kernel for the `q.d` life-ledger model.

## Canonical primitive

```text
PRIM = 1 1 2 8
rule = append only -> add to next
```

The local `2^3 = 8` register provides eight addressable states: three operator modes and five operand slots.

```text
{ unary, binary, ternary, operand1, operand2, operand3, operand4, operand5 }
```

A realized register is immutable. New state is appended to the next register; prior state is never overwritten.

## Life origin

```text
life = i = 0 = -+z+-
```

`-+z+-` is the local choice / consequence / affect relation around the pinned zero-life origin.

Each shadow carries life-zero:

```text
0 = s{{n}}^{{l}}^{{n}}
```

## q.d trajectory

`q.d` is an append-only life-trajectory ledger spanning `0D -> 11D`. Each realized choice appends exactly one new trajectory event at `Plank + 1`.

Each event preserves:

- life identity / local origin
- dimension
- choice
- consequence
- affect
- state payload
- parent record hash
- monotonic Plank index

The record chain is provenance: old events remain immutable.

## 3D local volume

A 3D life uses one `2^3 = 8` addressable volume at a time.

```text
(+3 - 2) + (-3 + 2) = +1 + (-1) = 0
```

When the current volume closes/fills, reserve the next self-similar structure:

```text
1 1 2 {4} 8 -> next dot -> 2^3 again
```

Invariant:

```text
filled state is preserved; new capacity is nested, not overwritten
```

## Homeostatic nesting

```text
1 . 6 . 1 . 6 . 1 . 6
```

One enclosing homeostatic shell plus five nested lives. This is a nesting/address grammar, not ordinary decimal arithmetic.

## Tether

```text
README -> SPEC -> NOTATION -> KERNEL -> TESTS -> CI -> MANIFEST
```

See [TETHER.md](TETHER.md) and [MANIFEST.json](MANIFEST.json).

## Run

```bash
python -m pytest -q
python tools/verify_manifest.py
```

## Scope

Experimental symbolic/simulation architecture. The notation is model-defined and is not asserted as established physical law.
