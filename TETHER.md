# Tether Map

This repository is intentionally tethered: every executable, test, notation file, and specification points back to one canonical PRIM root.

```text
                         CANONICAL ROOT
                         {{5/3/2/1/1}} FROZEN
                         PRIM = 1 1 2 8
                         dot = sapphon
                    append only -> add next
                                |
              +-----------------+-----------------+
              |                 |                 |
              v                 v                 v
          SPEC.md         docs/NOTATION.md     src/qd_prim.py
              |                 |                 |
              +-----------------+-----------------+
                                |
                                v
                         tests/test_qd_prim.py
                                |
                                v
                      .github/workflows/test.yml
                                |
                                v
                           MANIFEST.json
```

## Canonical relationships

1. `FREEZE.md` pins the completed Gen-1 mother/daughter kernel state.
2. `README.md` is the human entry point.
3. `SPEC.md` defines normative model behavior.
4. `docs/NOTATION.md` preserves literal symbolic notation and semantic glosses.
5. `src/qd_prim.py` is the executable reference implementation.
6. `tests/test_qd_prim.py` checks the executable invariants, including Paralax daughter inference.
7. `.github/workflows/test.yml` re-runs the invariants on every push and pull request.
8. `MANIFEST.json` hashes the tethered files and supplies one deterministic root hash.

## Append-only tether

At repository level, Git history supplies the outer provenance chain. At q.d level, `parent_hash` supplies the inner trajectory chain. Each append also tethers `dot[n] = sapphon[n] = Plank[n]`.

```text
Git commit n ---> Git commit n+1
      |                |
      v                v
q.d event n ----> q.d event n+1
 sapphon[n]       sapphon[n+1]
        parent_hash = SHA256(event n)
```

## Manifest rule

`MANIFEST.json` hashes all canonical tether files except itself. Its `root_sha256` is computed from sorted lines of:

```text
path:sha256
```

This avoids self-hash recursion while giving the repository a single auditable tether root.


## Append-only skill adapter

The frozen mother kernel is unchanged. Skill assessment is appended outside the freeze:

```text
frozen q.d ledger
      |
      v
tools/skill_probe.py
      |
      v
tests/test_skill_probe.py
```

The probe reports demonstrated structural complexity from 0..5:
`1=unary`, `2=binary`, `3=ternary`, `4=ternary+4 payloads`, `5=ternary+5 payloads`.
It reads committed q.d evidence only and never grants generation authority.


## Generative dot/radix adapter

The frozen mother kernel remains non-generative. Deterministic generation is permitted only for append-only dot/radix addressing:

```text
seed
  |
  v
dot[n] -> {band 1..11, gravity 1..8, radix 0..359}
  |
  v
dot[n+1]
```

Envelope:

```text
MAX_STEP = (11 * 8 * 10^-36) / 360
         = 2.444444444444... * 10^-37
```

Scope is exactly `{dot, radix}`. The adapter cannot spawn sapphon daughters, create mother kernels, or modify frozen identity semantics. Each generated state is parent-hash tethered to the previous generated dot.


## H::UMANITY corpus tether

The earlier mnemonic corpus is now attached as a read-only carrier:

```text
-+2700-+0+-2700-+
       |
       +-- {{0::m+f}}
       |
       +-- 20 shadow life slots
       +-- 20 light life slots
       +-- 90 years per life
       +-- 9 radix phases per life
```

The structural corpus lives in `data/humanity_corpus_2700.json`. `tools/corpus_tether.py` maps a generated radix address into exactly one immutable corpus slot and local phase. No corpus binding can spawn, append, or mutate a generation.


## {{i::mpli::c::it::}} mnemonic overlay

The mnemonic layer is derived and read-only:

```text
H::UMANITY corpus
      |
      v
{{i::mpli::c::it::}}
      |
      +-- CEM -> CHEM
      +-- TGL -> TOGGLE
      +-- SPN -> SPIN
      +-- PNC -> PINCH
      +-- EMT -> EMIT
      +-- GLS -> GLASS
      |
      +-- AIR bracket
          2x1^10^-35.99 - {air 36.00}} +36.01
```

The overlay may emit mnemonic labels but cannot rewrite corpus slots, generate people, spawn daughters, or mutate the frozen mother kernel.


## TOPH Sapphon dynamic corpus

`tools/toph_dynamic_corpus.py` composes the existing adapters without changing their authority:

```text
TOPH Sapphon
     |
     v
DotRadixGenerator
     |
     v
CorpusBinding
     |
     v
{{i::mpli::c::it::}}
     |
     +-- phase label
     +-- mnemonic
     +-- AIR 36 bracket
     |
     v
TophCorpusFrame[n]
```

Dynamic means the addressed view changes as the append-only dot/radix state advances. The underlying corpus, mnemonic table, TOPH identity, and Gen-1 generation ceiling remain immutable.


## TOPH Internet toroid tracker

`tools/toph_relative_layers.py` tracks the local six-hop toroid traversal:

```text
0 --200ms--> 2 --200ms--> 4 --200ms--> 6
                                  |
                                  v
4 <--200ms-- 10 <--200ms-- 8 <--200ms
```

Equivalent ordered forward path:

```text
0 -> 2 -> 4 -> 6 -> 8 -> 10 -> 4
```

The exact reverse path is the Benjamin traversal:

```text
4 -> 10 -> 8 -> 6 -> 4 -> 2 -> 0
```

Six hops at 200 ms each close the traversal at 1200 ms. Node `4` is the hub and the tracker is tagged `OSI layer 2`. It is read-only symbolic state and does not perform network inspection.


## Mandel / Juliet kinetic gate

`tools/kinetic_bounds.py` gates kinetic vectors before they are admitted to the TOPH toroid model.

```text
vector
  |
  +-- + component -> speed up / toward
  +-- - component -> slow down / away
  |
  v
anisotropy check
  |
  +-- (x+3,y-2) -> 3:2 ellipse
  |
  v
admission gate
  |
  +-- Mandel tether ---------+
  |                          |
  +-- Juliet encrypted/tag --+--> IN_BOUNDS
  |
  +-- neither ------------------> OUT_OF_BOUNDS
```

Mandel belly partition:

```text
[5%/inf.25][30][30][30][5%/inf.25]
```

The partition is normalized to `1.00`. This remains symbolic/local model logic and does not perform live network inspection.


## Layer 0 material-weight clock

`tools/material_year_clock.py` adds a read-only mnemonic material clock rooted at zero:

```text
root 0
  |
  +-- Layer 0
       |
       +-- Au / 79
       |    \-- weight = 79 years
       |
       +-- photon carrier
            -5400 ---- 0 ---- +5400
                full span = 10800 years
                storage ~= 20% = 2160-year equivalent
```

This layer uses real material identifiers only as referents. Atomic number and mnemonic year weight are deliberately separated; the timeline is model storage space, not a physical statement about gold or photon decay.


## Reincarnated photon corpus tether

`tools/reincarnated_photon_corpus.py` projects the existing immutable 40-slot corpus across the dual toroid:

```text
                    1 photon corpus
                     80 × 90 = 7200
                           |
             +-------------+-------------+
             |                           |
           |-d|                        |+d|
       40 × 90 = 3600             40 × 90 = 3600
             |                           |
          rings 0..9                 rings 10..19
             \                           /
              +------- 20 rings --------+
                         |
                  4 lives / ring
                         |
                   4 × 90 = 360
                         |
                90° + 90° + 90° + 90°
```

Each photon slot stores its original `source_slot`, incarnation number, toroid side, ring index, and quarter index. The adapter never mutates or duplicates the underlying source identities; it only supplies a second address pass over them.

The geometric ring stride remains `17.5`, width `18`, with `20 × 17.5 + 10 = 360` closure.


## TOPH Aeon hierarchy tether

The presentation hierarchy is stored in `data/toph_aeon_hierarchy.json` and verified by `tools/toph_aeon_hierarchy.py`.

```text
frozen q.d kernel
      |
      v
TOPH :: Aeon :: sapphonic
      |
      +-- green core
      +-- emerald storage
      +-- emerald temperament
      |
      v
root0
      |
      +-- 2^3 q.d
      +-- serial 10:1 x3
      +-- dual toroid / 20 rings
      +-- tetraphasic 80x90 corpus
      +-- 60x40x3 metronome
      |
      v
shared invariant = 7200
      |
      v
docs/index.html
```

The site, data hierarchy, executable verifier, corpus adapter, tests, notation, and manifest are tethered to the same derived state. The frozen mother/daughter kernel remains unchanged.


## Emergence tether

`data/toph_aeon_hierarchy.json::emergence.seeds` is the minimal presentation seed set.

`tools/toph_aeon_hierarchy.py::derive()` recomputes the hierarchy and `verify()` compares those results with the stored Aeon state. The Pages emergence lattice renders the same derivation in order:

```text
root0 -> 8 -> 1000:1 -> 366 -> 20 -> 360 -> 7200 == 7200 -> 400
```

This makes the hierarchy generative at the derived-view level while leaving the frozen mother kernel and immutable source corpus unchanged.


## Memristic spinor tether

```text
data/memristic_spinor_overlay.json
        |
        v
tools/memristic_spinor_overlay.py
        |
        +-- 10-life / 10,000y lifecycle
        +-- ±20% -> 8,000..12,000y
        +-- 3y phase shift
        +-- -m/+m/-f/+f quartet
        +-- advanced-tech / dirt-poor contexts
        +-- parent-hash memory
        |
        v
tests/test_memristic_spinor_overlay.py
        |
        v
TOPH emergence seeds
        |
        v
docs/index.html memristic overlay
```

Enheduanna is anchor 00 on the nearest existing corpus slot only. No historical wealth/technology state is inferred, and neither the immutable source corpus nor frozen kernel is modified.


## {{2^3}} Pages UI tether

The interactive presentation now has an explicit eight-layer contract.

```text
docs/index.html
  -> 8 native anchor layers
  -> app-v2.js?v=8 enhancement
  -> app.js compatibility mirror
  -> visible JS ONLINE / 8/8 UI TETHER PASS diagnostics
  -> tests/test_pages_ui.py
```

The UI test verifies all eight fallback targets, all enhanced action fallbacks, the v2 controller reference, delegated action wiring, and JavaScript syntax when Node is available.
