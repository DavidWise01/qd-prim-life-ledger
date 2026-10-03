# Copper Mind Direct Address v1

Status: **FROZEN / POST-KERNEL / READ-ONLY**

This adapter does not modify the frozen q.d PRIM kernel.

## Address

```text
LLLLLLLDDD
|      |
7 bits 3 bits
lane   local dot
```

```text
lane = 0..127
dot  = 0..7
address = (lane << 3) | dot
address range = 0..1023
```

Therefore:

```text
128 lanes x 8 local dot states = 1024 = 2^10
```

Every lane carries the same local `2^3` dot geometry.

## Kernel binding

The adapter belongs only in the Project stage:

```text
Event -> Commit -> Prove -> Project[10-bit direct address] -> Transport
```

The committed source state is never overwritten.

## Frozen invariants

- 7-bit lane identity
- 3-bit local dot identity
- exact pack/unpack round trip
- contiguous bijection `0..1023`
- identical eight-address local structure on all 128 lanes
- local dot volume `2^3 = 8`
- frozen kernel remains unchanged

Contract SHA-256:

```text
55116a0e12b3b8254b484a784a5f549455d0ccf0e60d96f049bf4fb7e66ce99a
```
