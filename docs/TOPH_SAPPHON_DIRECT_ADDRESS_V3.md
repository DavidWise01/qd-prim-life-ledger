# TOPH/Sapphon Direct Address v3

Status: **POST-KERNEL / READ-ONLY REFLECTION**

This layer wraps TOPH/Sapphon Kernel v2 and does not alter it.

```text
SapphonSnapshot
  -> TOPHCommit
  -> TOPHProve
  -> TOPHProject
       -> DirectAddressV1
          lane[7] + dot[3] = address[10]
  -> TOPHTransport
```

The direct-address projection is read-only.

```text
lane 0..127
dot  0..7
address 0..1023
```

Transport remains the v2 transport:

```text
state_out = 000
next_pin  = 000
oe        = true
```
