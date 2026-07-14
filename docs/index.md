# wick

*The wick is the part of the lantern that carries the flame.*

**wick** is the [lantern engine](https://github.com/alikatgh/lantern)'s own
scripting language: Lua's size and feel, with the sharp edges designed out
at the language level. The whole implementation — lexer, one-pass typed
compiler, bytecode, stack VM, garbage collector — is about 2,000 lines of
dependency-free C++, open source under the zlib license, living in the
engine repo at [`wick/`](https://github.com/alikatgh/lantern/tree/main/wick).

```wick
// a complete lantern game in wick
let best = num(lt.load_save("best") ?? "") ?? 0

fn update(dt: num) {
  if lt.pressed("z") {
    best = best + 1
    lt.save("best", str(best))
  }
}

fn draw() {
  lt.clear(0.1, 0.1, 0.2)
  lt.print("BEST " + str(best), 4, 4, 1, 1, 1, 1)
}
```

## Why a new language

wick exists because we shipped real games in Lua and catalogued what hurt.
Each pain became a design decision, not a lint rule:

| Lua pain | wick answer |
|---|---|
| nil errors at runtime | **Static types + `T?` optionals** — unchecked use doesn't compile |
| typos create silent globals | **Locals only** — undeclared assignment is a compile error |
| 1-based indexing, no `continue` | 0-based `[ ]`, `continue`, `len(x)` |
| `""` and `0` are truthy | Conditions must be `bool` |
| GC pauses mid-frame | Collection runs **between frames only** |
| stack-index C bindings | Engine calls **type-checked at compile time** |
| `math.random` differs by machine | `rand()` is a fixed xorshift — deterministic everywhere |
| JIT forbidden on iOS | No JIT anywhere — specialized bytecode from static types |

The flagship proof: **Kora Night ships in both languages** —
[`games/showcase`](https://github.com/alikatgh/lantern/tree/main/games/showcase)
(Lua) and
[`games/showcase_wick`](https://github.com/alikatgh/lantern/tree/main/games/showcase_wick)
(wick) — deliberately kept as separate, side-by-side projects that evolve
together. Read the pair like a Rosetta stone: [wick vs Lua](comparison.md).

## Where to start

- [Getting started](getting-started.md) — run a wick game in two minutes
- [Types & optionals](types.md) — the heart of the language
- [The engine API](engine-api.md) — every `lt.*` call, typed
- [Compile errors, explained](errors.md) — what each message means
