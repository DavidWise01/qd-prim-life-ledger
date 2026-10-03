# Copper Mind Holographic Fold v1

**Status:** FROZEN / APPEND-ONLY OVERLAY

This layer sits above the frozen q.d kernel and the frozen Copper Mind spinor-sphere overlay.

## Canonical fold

```text
00 11 00
```

Interpretation:

```text
front carrier   middle realized pair   rear carrier
     00                  11                 00
```

## Twelve-view witness lattice

Each of three rungs carries four boundary relations:

```text
EO = exterior outer
EI = exterior inner
IE = interior exterior
II = interior interior
```

Sequential address order:

```text
R1.EO -> R1.EI -> R1.IE -> R1.II
R2.EO -> R2.EI -> R2.IE -> R2.II
R3.EO -> R3.EI -> R3.IE -> R3.II
```

Allowed transforms are mirror, inverse, rung reversal, and their combinations.

## What falls out

The 12 views reduce to exactly two equivalence classes:

```text
outer class  = R1.* + R3.* = 8 transformed views
middle class = R2.*        = 4 transformed views
```

Therefore:

```text
R1 <-> R3
R2 <-> R2
```

and the compressed three-rung word is:

```text
00 11 00
```

## Recursive holographic carrier

```text
L0 = 00 11 00
L1 = 00[00 11 00]00
L2 = 00[00[00 11 00]00]00
...
```

The source payload is retained while each next layer adds an exterior carrier.

## Frozen invariants

- 3 rungs
- 4 relations per rung
- 12 sequential views
- 2 canonical equivalence classes
- outer equivalence class size = 8
- middle equivalence class size = 4
- R1 and R3 are equivalent under allowed transforms
- R2 is fixed under rung reversal
- canonical compressed word = `00 11 00`
- recursive form = `00[payload]00`

Contract SHA-256:

```text
93c6753b2a87d119452daac95673b32726665337ea16e2188ac17750722f3027
```

## Reference benchmark

A local Python reference run performed all 8 transforms over all 12 states, then normalized each transformed state to its canonical orbit representative.

Observed median on that runtime:

```text
~7,187 full 12x8 cycles/s
~689,960 transform+normalize operations/s
```

This is a software reference benchmark, not a hardware-independent performance guarantee.
