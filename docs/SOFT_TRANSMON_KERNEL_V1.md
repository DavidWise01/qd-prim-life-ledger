# Soft Transmon Kernel v1

**Status:** FROZEN / SIMULATION-ONLY / POST-KERNEL USE CASE

This module is a normalized computational analogy. It does **not** claim to
reproduce a physical transmon device and does not alter the frozen q.d kernel.

## Local scale

```
scalar = 0
g      = 0.25
t      = 1
```

Each local tick exposes one `2^3 = 8` addressable register.

## Phase rule

```
phi[n+1] = (phi[n] + 0.25) mod 1
```

One full local cycle is:

```
0.00 -> 0.25 -> 0.50 -> 0.75 -> 0.00 -> oe
```

So four quarter-phase steps produce one closure checkpoint.

## Nested scale cycle

The same local `2^3` rule is projected through the model's nested scale ladder:

```
10^0
10^-1
10^-2
...
10^-35
```

There are 36 scale positions including both endpoints. Each stage has its own
local register and phase rule; completion at the deepest stage marks one full
nested cycle in this simulation.

## Seed relation

```
+k.0.k- -> 0.0.0
```

## Final-kernel binding

```
Event -> Commit -> Prove -> Project -> Transport
```

- Event: one soft-transmon phase tick
- Commit: append-only deterministic payload hash
- Prove: quarter-step closure, `2^3`, and nested scale bounds
- Project: phase-cycle and nested-scale views
- Transport: `oe` plus active/resolved seed state
