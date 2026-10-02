# TOPH + Sapphon Hierarchical State Space v1

**Address:** `{{Gg.Aa.Ii.Aa}}`  
**Status:** FROZEN / IMMUTABLE / APPEND-ONLY  
**Closure:** `oe`  
**Final q.d kernel modified:** no

## Frozen carrier

```text
000 + {} > 000
```

`000` is frozen state-space. `{}` is event/condition space. The event may
change what is observed, but it may not mutate the carrier.

```text
000 + {-1} > 000
000 + { 0} > 000
000 + {+1} > 000
```

The breathing scalar is therefore:

```text
000
 ↓
{-1, 0, +1}
 ↓
000
 ↓
repeat
```

## Observed state

```text
{{O}{b}{s}{e}{r}{v}{e}{d}}
```

Observation is read-only. A `no::condition` setup can determine which
observation is requested, but any resulting change is written only as an
append-only consequence outside the frozen `000`.

## Derived hierarchical lanes

No new primitive is required. The carrier implies seven routing roles:

```text
state
  ↓
condition
  ↓
observation
  ↓
change
  ↓
provenance
  ↓
return
  ↓
append
```

Every level preserves the same center:

```text
L0  000 + {} > 000

L1  [000 + {} > 000]
        + {}
     > [000 + {} > 000]

L2  [[000 + {} > 000] + {} > [000 + {} > 000]]
        + {}
     > same frozen carrier
```

Thus hierarchy increases lanes/arrows while the state-space invariant remains:

```text
state_in = 000
state_out = 000
```

## Locked address

All projections in this overlay are anchored at:

```text
{{Gg.Aa.Ii.Aa}}
```

Contract SHA-256:

```text
c06158d86bdb5ea2ca5e6eaa2ea32a7cf2770bc2924fd13be5b3b5e70896ef01
```
