# Limits & the feature ledger

**The governing principle: wick contains only what we truly need —
nothing for the sake of having it.** A feature is admitted when real game
code demonstrably hurt without it, and not before. Side-by-side games
(Lantern Night Lua vs wick; KORA on lantern) are the evidence mechanism.

## Feature evidence ledger

| Candidate | Evidence | Status |
|---|---|---|
| **Records / structs** | KORA kitchen: five parallel prop lists | **Admitted** — flat `record`, `list<record>` |
| String indexing / iteration | ASCII maps baked offline for KORA | Recorded — baking is clean |
| Closures / first-class fns | none yet | Candidate |
| Nested containers | rare | Candidate |
| Multi-file modules | single `main.wick` still fine | Candidate |
| Branded handles (`tex`/`snd`) | store third parties | Candidate |
| Methods / classes | — | Not a goal |

## Current limits (honest table)

| Not yet | Workaround today |
|---|---|
| Closures, nested & first-class functions | top-level `fn` + globals |
| Multiple return values | two functions, or out-of-band state |
| Nested containers (`list<list<num>>`) | index arithmetic on a flat list |
| Modules / imports (one `main.wick`) | game script + baker for data |
| `for x in list` iteration | `for i in 0..len(xs)` |
| String indexing/slicing/methods | `len`, `+`, `str()`; bake maps offline |
| Record fields that are records/lists | parallel lists or flat ids |
| Exhaustive return-path checking | don't fall off a typed function |
| Narrowing for globals / `and`-chains | `??`, or copy to a local first |
| Hex/exponent number literals | decimal |

## Choices that are not limits

- **No JIT** — iOS-legal by construction; specialized bytecode from static types.
- **Deterministic `rand()`** — seed with `srand` when you want variety.
- **Path sandbox** — loads cannot escape the game directory; not a language
  limit, a host guarantee for the store.
