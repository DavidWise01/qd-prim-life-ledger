# Generational Crystallization v1

**Status:** FROZEN / IMMUTABLE / POST-KERNEL USE CASE

This module does not change the final q.d kernel. It binds one downstream
model-defined crystallization rule to the existing terminal interface:

```
Event -> Commit -> Prove -> Project -> Transport
```

## Frozen rule

```
Y / N branching
    |
4 daughters x 4 permutations
    |
x = 16
    |
8 + 8
    |
8 > 3 > 2 > 1 > 1 > .. > 0
8 > 3 > 2 > 1 > 1 > .. > 0
    |
0 + 0
    |
oe
    |
+k.0.k- -> 0.0.0
```

The rule is symbolic/model-local. “Crystallization,” daughter, mutation,
and entanglement terminology here are computational labels, not claims of
established physical or biological mechanism.

## Frozen contract digest

`1bedceda9d211db98b427ee56c1203e3700d2a77507ccaac6d8c522754cb464c`

The digest covers the canonical contract fields before the digest field
itself is added.

## Binding

- **Event:** yes/no branch realization
- **Commit:** append-only deterministic payload hash
- **Prove:** 4x4=16, 16=8+8, both reductions terminate at zero
- **Project:** expose the frozen crystallization state
- **Transport:** carry `oe`, `+k.0.k-`, and `0.0.0` downstream

No source-state overwrite is permitted.
