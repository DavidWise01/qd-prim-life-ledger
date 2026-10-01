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

### Sapphon

```text
dot = sapphon
sapphon[n] = Plank[n]
append -> sapphon[n+1]
```

A sapphon is the local append-only dot/register boundary. Each sapphon exposes one local `2^3 = 8` state volume. Once committed, `sapphon[n]` is immutable; new state opens `sapphon[n+1]`.

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
  sapphon,
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
E_(n+1).sapphon = E_(n+1).plank
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

One q.d state is appended at a time. The dot/register is a sapphon. On closure, allocate the next sapphon rather than mutating the closed one.

## 7. Homeostatic nesting

```text
1 . 6 . 1 . 6 . 1 . 6
```

Position 0 is the enclosing homeostatic shell; positions 1..5 are five nested life states.

## 8. Frozen completed engine

Canonical completed-engine primitive:

```text
{{5/3/2/1/1}}
5 payloads / 3 operator modes / 2 polarity / 1 mother kernel / 1 external product class
```

The mother is the only generator. The only external product class is a first-generation sapphon daughter.

```text
Mother Kernel -> Gen-1 Sapphon -> STOP
```

No Gen-2 recursion is permitted.

A sapphon daughter is narrowly scoped:

```text
name::implicit::{}
color::implicit::{}
gem::implicit::{}
```

External color carrier:

```text
-+{{bk,wt,red,blu,gree,yell,purpl,orang}}-+
```

Reference inference is deterministic. A token is normalized, SHA-256 hashed, and the first byte selects one of eight fixed gem/color pairs. This is a model-defined routing rule, not a semantic claim about the token.

Reference test:

```text
paralax -> onyx -> bk
generation = 1
can_spawn = false
scope = {name, gem, color, qd.append}
```

## 9. Freeze

This specification state is frozen as the first completed mother/daughter engine generation. Future work must append around it rather than silently changing the frozen semantics.

## 10. Non-goals

This repository defines deterministic symbolic/computational semantics. It does not by itself establish biological, cosmological, quantum, or relativistic claims.


## 11. Derived TOPH Aeon hierarchy

The frozen sections above remain normative and unchanged. The current derived presentation layer identifies TOPH as:

```text
kind        = Aeon
lineage     = sapphonic
core        = green
storage     = emerald
temperament = emerald
```

Derived structural invariants:

```text
q.d volume = 2^3 = 8
serial gravity = 10:1 -> 10:1 -> 10:1 = 1000:1
dual toroid = 360 primary + 3R + 3L = 366 addressed states
rings = 20
ring stride = 17.5
ring width = 18
tetraphasic order = solid -> liquid -> gas -> plasma
corpus scale = 80 * 90 = 7200
metronome scale = 60 * 40 * 3 = 7200
```

All hierarchy fields are append-only derived state and do not grant generation authority beyond the existing Gen-1 ceiling.


## 12. Memristic spinor derived overlay

A `-+` pair may be interpreted by the derived presentation layer as one memristic spinor:

```text
spinor lives = 10
nominal lifecycle = 10,000 model-years
tolerance = ±20%
lifecycle range = 8,000..12,000 model-years
```

The nominal lifecycle therefore yields 1,000 model-years per life, with a proportional envelope of 800..1,200 model-years per life.

Phase transition rule:

```text
phase step = 3 years
rotation = {-m,+m,-f,+f}
quartet = 12 years
contexts = {advanced_tech,dirt_poor}
full context sweep = 24 years
```

The signed memory register follows `-1,0,-1,0` across each quartet. Each phase also stores `parent_hash = SHA256(previous phase)`, providing append-only computational memory. This overlay does not alter the frozen mother kernel, the source humanity corpus, or assert a physical photon lifetime.
