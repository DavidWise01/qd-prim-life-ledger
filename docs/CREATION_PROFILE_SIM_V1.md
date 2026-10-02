# TOPH Creation Profile Simulation v1

**Status:** FROZEN / IMMUTABLE / POST-KERNEL SIMULATION  
**Closure:** `oe`  
**Final q.d kernel modified:** no

This adapter generalizes the type slot in the scalar-zero constructor.

```text
? creation type
      ↓
type + place + date + substrate + tether
      ↓
scalar 0.0.0
      ↓
1/360 toroidal cursor × 360 = one full turn
      ↓
2000 aggregate profile field
      ↓
descend by 1 - n²
      ↓
n = 1 → 0
      ↓
linear +1 life ticks
      ↓
oe
```

Example simulation:

```text
type      = dog
place     = Buffalo, Minnesota
date      = 2026-10-02
substrate = carbon
tether    = mnemonic
```

The same constructor can accept another model type by replacing `dog`.

## Deterministic closure

```text
f(n) = 1 - n²

f(5) = -24
f(4) = -15
f(3) = -8
f(2) = -3
f(1) = 0
```

Thus the simulated construction search terminates at `n=1`, resolves to scalar zero, and only then begins the append-only `+1` timeline.

## Scope

This is a symbolic/computational model. It is not a mechanism for creating a real dog, human, organism, material, or physical object, and it makes no claim that real biology follows this constructor.

Contract SHA-256:

```text
7b9fafaeb2995502d270c9220e6bd0f5038996db6ade37111174b4f69db6b2eb
```
