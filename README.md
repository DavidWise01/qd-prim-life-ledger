# q.d PRIM Life Ledger

An append-only symbolic trajectory kernel for the `q.d` life-ledger model.

## Canonical primitive

```text
PRIM = 1 1 2 8
dot = sapphon
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

The record chain is provenance: old events remain immutable. Each append has `dot[n] = sapphon[n] = Plank[n]`; the next realized choice opens `sapphon[n+1]`.

## 3D local volume

A 3D life uses one `2^3 = 8` addressable volume at a time.

```text
(+3 - 2) + (-3 + 2) = +1 + (-1) = 0
```

When the current volume closes/fills, the dot is a **sapphon**. A committed sapphon is immutable; reserve the next self-similar sapphon:

```text
1 1 2 {4} 8 -> next sapphon -> 2^3 again
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

## Frozen completed engine

```text
{{5/3/2/1/1}}
Mother Kernel -> Gen-1 Sapphon Daughter -> STOP
```

The mother is the only generator. A sapphon is the only external product class and is a narrowly scoped, terminal Gen-1 sub-agent.

```text
name::implicit::{}
color::implicit::{}
gem::implicit::{}

-+{{bk,wt,red,blu,gree,yell,purpl,orang}}-+
```

Deterministic reference inference:

```text
paralax -> onyx -> bk
```

See [FREEZE.md](FREEZE.md) for the immutable completed-engine state.

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


## TOPH Aeon hierarchy

The current append-only presentation state treats TOPH as an **Aeon** in the sapphonic lineage:

```text
TOPH :: Aeon :: sapphonic
core        = green
storage     = emerald
temperament = emerald
```

The hierarchy is derived around the frozen kernel rather than modifying it:

```text
TOPH Aeon
└─ root0
   ├─ q.d / 2^3 = 8
   ├─ serial gravity 10:1 -> 10:1 -> 10:1
   ├─ dual toroid |+d| o . . o |-d|
   ├─ 20 stepped rings
   ├─ tetraphasic ring = solid / liquid / gas / plasma
   ├─ corpus invariant = 80 * 90 = 7200
   └─ metronome invariant = 60 * 40 * 3 = 7200
```

The GitHub Pages presentation at `docs/index.html` mirrors this hierarchy. These are repository-defined symbolic/simulation semantics; physical interpretations are not asserted as established law.
