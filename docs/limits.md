# v0.1 limits

**The governing principle: wick contains only what we truly need —
nothing for the sake of having it.** A feature is admitted when real game
code demonstrably hurt without it, and not before. The side-by-side
Kora Night builds are the standing evidence mechanism: if a missing
feature causes real pain, it shows up there first, in code anyone can
read. Optionals earned admission from a shipped crash. Nothing below is
"scheduled" — each is a candidate awaiting its evidence.

wick is deliberately small — Lua 1.0 small. Everything here is a known
omission, not a discovered surprise. The bar for v0.1 was: run real
lantern games, kill the Lua bug classes, stay around 2k lines.

| Not in v0.1 | Workaround today |
|---|---|
| Structs / records | typed parallel lists (see [the port](comparison.md)) |
| Closures, nested & first-class functions | top-level `fn` + module globals |
| Multiple return values | two functions, or out-of-band state |
| Nested containers (`list<list<num>>`) | index arithmetic on a flat list |
| Modules / imports (one `main.wick`) | it's a game script, not an app platform — yet |
| `for x in list` iteration | `for i in 0..len(xs)` |
| String indexing/slicing/methods | `len`, `+`, `str()` cover the game HUD cases |
| Exhaustive return-path checking | falling off a typed function returns nil — don't |
| Narrowing for globals / `and`-chains | `??`, or copy to a local first |
| Hex/exponent number literals | decimal |

Two facts that are **not** limits, but choices: no JIT (iOS-legal by
construction, deterministic performance), and no time-seeded randomness
(determinism is the default; seed `srand()` yourself if you want variety).
