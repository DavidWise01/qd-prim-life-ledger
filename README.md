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


## Emergence from seeds

The Aeon hierarchy is now derivable from a small seed lattice rather than being only a list of fixed outputs.

```text
root0
  -> q.d axes = 3           -> 2^3 = 8
  -> gravity 10 x depth 3   -> 10^3 = 1000:1
  -> turn 360 + 3L + 3R     -> 366 addresses
  -> hub/control remainder 10
  -> (360 - 10) / 17.5      -> 20 rings
  -> 4 phases x 90          -> 360 per ring
  -> 40 x 2 x 90            -> 7200 corpus
  -> 60 x 40 x 3            -> 7200 metronome
  -> 30 x 2/3 = 20          -> 20^3 / 20 = 400
```

`tools/toph_aeon_hierarchy.py::derive()` recomputes these values from `data/toph_aeon_hierarchy.json::emergence.seeds`. GitHub Pages exposes the same derivation as an interactive root0 growth sequence.


## Memristic spinor lifecycle overlay

The literal `-+` is now also available as a history-dependent spinor overlay:

```text
-+ = one spinor
10 lives
10,000 model-years nominal
±20% envelope = 8,000..12,000 model-years
```

Derived per-life envelope:

```text
nominal = 1000 years
minimum = 800 years
maximum = 1200 years
```

Memristic phase cycle:

```text
every 3 years:
-m -> +m -> -f -> +f
-1 ->  0 -> -1 ->  0

one quartet = 12 years
advanced-tech quartet + dirt-poor quartet = 24-year context sweep
```

Each state stores the SHA-256 digest of its previous state as `parent_hash`, so the current phase depends on an explicit retained history. The advanced-tech and dirt-poor conditions are simulation contexts applied to all four phase states, not historical claims.

The first historical overlay anchor is **Enheduanna**, approximately 2300 BCE, attached read-only to the nearest existing corpus window (slot 3, `-2295..-2205`). The underlying 40-life source corpus is unchanged.


## {{2^3}} interactive walkthrough

The GitHub Pages surface now exposes exactly eight navigable layers:

```text
0 root0
1 {{2^3}} q.d
2 memristic -+
3 serial gravity 10^3
4 dual toroid 366
5 tetraphasic corpus 7200
6 metronome / foam
7 frozen kernel / 0/0 closure
```

Each layer control is a normal anchor first, so navigation still works without JavaScript. `docs/assets/app-v2.js` adds animation, memristic stepping, active-layer state, and visible runtime/self-check badges. `docs/assets/app.js` mirrors the v2 controller for stale-page compatibility.


## Native control v9

The Pages controls no longer depend on JavaScript for state changes.

- root0 emergence uses 9 native radio states: root + 8 derived layers.
- memristic spinor uses 8 native radio states: four rotations in each of two contexts.
- visible controls are `label[for]` bindings to those states.
- CSS renders the selected state.
- `app-v3.js` supplies only animation, active-layer highlighting, and diagnostics.

If JavaScript is blocked or stale, the controls still change state.
