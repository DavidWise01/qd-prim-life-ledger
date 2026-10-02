# TOPH QK handoff v2

Status: **APPEND-ONLY / SEALED ON `eo`**

This layer extends `toph_sapphon_realign_v1` without modifying the frozen mother kernel or the v1 overlay.

## Kernel and gate

```text
{{qk{{i::d::}}}}

00 11 {{2442{}}} 11 00
          |
          +-- sealed throat

qk --{{i}}--> d
```

`qk` is the repository's sealed symbolic quantum-kernel model, `{{i}}` is the implication/handoff relation, and `d` is the resolved digital projection. The model forbids digital writeback into an unresolved kernel state.

## Fixed point and address

`000` is not assumed merely because it is convenient. The verifier exposes `detect_fixed_points(...)`, which refuses a fixed-point claim until every state of the finite map under test is supplied.

```text
000
 |
 +-- vector
      |
      +-- voxel
           |
           +-- vogel
```

The transition law itself remains an explicit input to the mapper; this overlay does not invent a physical transition law.

## Bubble clock -> VSync

```text
2 Plank = 1 frame
6 frames = 1 velocity window
1 frame = 1/6 velocity window

frame seconds     = 1/f
model Plank       = 1/(2f)
velocity window   = 6/f
non-overlap rate  = f/6
rolling cadence   = f
```

where `f` is the digital VSync/refresh rate in Hz.

Each frame consumes two resolved binary cells and maps to a cardinal address:

```text
00 -> U
01 -> R
10 -> L
11 -> D

U <-> D
L <-> R
```

`.25` is preserved as one quarter-turn (`1/4 = 90 degrees`), not `.25%`.

## Inference window: static snow

The six-frame window contains twelve Plank cells. Unknown cells are rendered conceptually as TV static or **snow**.

```text
candidate_count = 2 ^ unknown_plank_cells
```

That number is an address-candidate count, **not a probability**. When all twelve cells are resolved, the window has one exact candidate.

A resolved window is handed from `qk` through `{{i}}` to `d` twice. Both digital projections are canonically hashed. The layer freezes on literal sentinel `eo` only when both handoffs are byte-for-byte equivalent at the payload level and have the same digest.

```text
snow
  |
  v
resolve 12 cells
  |
  +--> qk -> {{i}} -> d :: pass 1
  |
  +--> qk -> {{i}} -> d :: pass 2
                      |
             exact match?
                 | yes
                 v
                eo
              FROZEN
```

This is repository-defined deterministic simulation semantics, not a claim that the code implements physical quantum hardware.
