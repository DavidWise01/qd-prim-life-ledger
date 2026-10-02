# Discrete Time + Place Outcome v1

**Status:** FROZEN / IMMUTABLE / POST-KERNEL USE-CASE  
**Closure:** `oe`  
**Final kernel modified:** no

This adapter formalizes the current model-local discrete time-and-place plotter without changing the frozen q.d kernel.

```text
0{{+implicit::outcome}}0 > {{i}} > 0
```

## Scalar outcome line

```text
 +1 = good outcome timeline
  0 = implicit natural/reference line
 -1 = bad outcome timeline
```

A zero is not an empty record. It represents an implicit natural choice, its natural consequence, and the resulting implicit outcome on the reference line.

```text
0 0 0 0 0 {{1.00}}
```

The explicit marker is the realized append:

```text
1{where, why, time}
```

## Choice/no resolution

```text
choice::no::{{n}}^3
    =
{{choice + consequence + outcome + direction}}
    >
pin to {{xu{}, yd{}, xr{}, yl{}}}
```

Movement primitive:

```text
scalar 0 | xu | yd | xr | yl
```

## Time closure

```text
-1 -> 0 -> +1 -> 0
1/10 x 10 x 0 = 0
```

The completed local cycle has no residual time in this model.

## Universal frame

Each completed record belongs to one total universal frame snapshot. The next frame is append-only and may use the model's `+2` or `{{n}}^{{n^2}}` transition notation.

## Frozen binding

```text
Event -> Commit -> Prove -> Project -> Transport -> oe
```

Contract SHA-256:

```text
e5daffdd92e13e5762fe1ebe2423538e363ca6656aa711a1f6811e4703dac054
```
