# q.d PRIM Final Kernel

Status: **FINAL / FROZEN / APPEND-ONLY**

This file is the terminal architectural declaration for the repository.

## One purpose

> Take one exact append-only event, preserve provenance, derive higher-scale views, and never overwrite source state.

Everything in the kernel belongs to one five-stage contract:

```text
Event -> Commit -> Prove -> Project -> Transport
```

### Event

Create exactly one new append-only state event.

```text
tick[n]
  -> exact state
  -> next append
```

Canonical base:

```text
PRIM = 1 1 2 8
dot = sapphon
base tick = 10^-35 s
tick delta = -1
```

### Commit

Preserve the event and its ancestry.

```text
event
  -> canonical record / leaf
  -> parent provenance
  -> append-only commit
```

Completed lower registers are retained. New information is added to the next register.

### Prove

Provide deterministic evidence that a retained event belongs to the committed history.

```text
event / leaf
   -> digest
   -> Merkle root
   -> inclusion proof / backdraft
```

Proof structures witness source state; they do not replace it.

### Project

Read committed state through a higher-scale interpretation without mutating the source.

Examples include physics-model, chemistry-model, cellular/corpus, mnemonic, hierarchy, and other derived views.

```text
committed source
      |
      +-> view A
      +-> view B
      +-> view C
```

Projection is read-only with respect to the committed source.

### Transport

Move deterministic records, proofs, or projections across a boundary without changing their source semantics.

```text
L0 exact ledger
      -> framing
      -> OSI transport
      -> downstream consumer
```

## Final boundary

The kernel itself is complete.

```text
{{5/3/2/1/1}}
        |
        v
PRIM 1 1 2 8
        |
        v
Event -> Commit -> Prove -> Project -> Transport
        |
        v
FINAL
```

After this declaration, repository development may add only external or derived work such as:

- adapters
- benchmarks
- documentation
- projections
- transport bindings
- verification tooling

It must not silently redefine the frozen kernel primitive, generation boundary, append rule, or source-state semantics.

## Scope

This is a repository-defined symbolic/simulation architecture. Physics, chemistry, biological, corpus, and other overlays are model layers unless independently supported by established evidence.
