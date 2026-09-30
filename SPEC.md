# q.d PRIM Specification v0.1

## 1. Primitive

`PRIM := 1 1 2 8`

A PRIM contains eight local slots:

1. unary operator mode
2. binary operator mode
3. ternary operator mode
4. operand 1
5. operand 2
6. operand 3
7. operand 4
8. operand 5

Operational law:

```text
read current -> resolve -> append next
```

No committed PRIM is mutated.

## 2. Identity and life-zero

```text
life = i = 0 = -+z+-
```

The zero state is a pinned local identity. `z` participates in a bidirectional choice/consequence/affect relation.

Shadow carrier:

```text
0 = s{{n}}^{{l}}^{{n}}
```

The shadow is life-bearing at its own zero rather than representing absence.

## 3. Movement basis

```text
V10 = {u,d,l,r,x,y,z,-,+,1}
```

A life and its shadow may be related across this ten-vector symbolic basis.

## 4. q.d event

For life `L`, event `E_n` is immutable after append.

```text
E_n = {
  life,
  plank,
  dimension,
  choice,
  consequence,
  affect,
  state,
  parent_hash
}
```

Append transition:

```text
E_n --choice--> E_(n+1)
```

with:

```text
E_(n+1).plank = E_n.plank + 1
E_(n+1).parent_hash = hash(E_n)
```

## 5. Dimensional trajectory

```text
0D 1D 2D 3D 4D 5D 6D 7D 8D 9D 10D 11D
```

A q.d ledger records ordered life trajectory across these dimensions without rewriting earlier states.

## 6. 3D volume

```text
2^3 = 8
(+3 - 2) + (-3 + 2) = 0
1 1 2 {4} 8
```

One q.d state is appended at a time. On closure, allocate the next dot/register rather than mutating the closed one.

## 7. Homeostatic nesting

```text
1 . 6 . 1 . 6 . 1 . 6
```

Position 0 is the enclosing homeostatic shell; positions 1..5 are five nested life states.

## 8. Non-goals

This repository defines deterministic symbolic/computational semantics. It does not by itself establish biological, cosmological, quantum, or relativistic claims.
