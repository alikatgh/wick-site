# Built-ins

Always available, no namespace. Generic built-ins (`len`, `str`, `num`,
`push`, `pop`) are dispatched **by static type at compile time** — using
one on the wrong type is a compile error, not a runtime surprise.

## Generic

| Signature | Notes |
|---|---|
| `len(x: str \| list \| map): num` | characters / elements / entries |
| `str(x: num \| bool \| str): str` | `str(42)` → `"42"`, integers print clean |
| `num(s: str): num?` | parse; `nil` on failure (including `""`) |
| `push(xs: list<T>, v: T)` | append |
| `pop(xs: list<T>): T?` | remove+return last; `nil` when empty |

## Math

| Signature | Notes |
|---|---|
| `floor(x: num): num` · `ceil(x: num): num` | |
| `abs(x: num): num` · `sqrt(x: num): num` | |
| `min(a: num, b: num): num` · `max(a, b)` | |
| `sin(x: num): num` · `cos(x: num): num` | radians |
| `atan(y: num, x: num): num` | two-argument arctangent |
| `pi` | constant |

## Randomness — deterministic by design

| Signature | Notes |
|---|---|
| `rand(): num` | uniform `[0, 1)`, xorshift64\* — the **same sequence on every machine** |
| `srand(seed: num)` | reseed; seed your game once for replayable runs |

There is no "time-seeded" mode: if you want variation between runs, seed
with something you choose (and can log). CI screenshot tests rely on this.

## Environment & testing

| Signature | Notes |
|---|---|
| `env(name: str): str?` | read an environment variable (e.g. your game's own `MYGAME_AUTO` self-play switch) |
| `check(cond: bool, msg: str)` | runtime assertion; failure shows `check failed: msg` on the error screen — the wick test suite is built from these |
