# How we test a tiny language

*2026-07-14*

wick is small. The test suite is allowed to be small only if it is
**mean**. We do not measure coverage theater. We measure the bug classes
the language claims to kill.

## Three layers

### 1. Semantics (must run)

A temporary `main.wick` full of `check(condition, "label")` assertions:
arithmetic, short-circuit bools, optionals, lists, maps, `rand`/`srand`
determinism, and now **records** (construct, field get/set, list of
records).

Run headless:

```sh
LANTERN_FIXED_DT=1 LANTERN_SHOT=... LANTERN_SHOT_FRAME=1 ./build/lantern game/
```

### 2. Must-fail-to-compile (must *not* run)

The whole point of wick is programs that **should not exist**. Each case
is a tiny game that must exit non-zero and print a known substring:

| Case | Substring |
|---|---|
| unchecked `str?` into `lt.print` | `str?` |
| `if 1` | `must be bool` |
| assignment to undeclared name | `no implicit globals` |
| `"score " + 5` | `str(x)` |
| wrong native type / arity | `argument` / `at least` |
| `let x = nil` | `annotate` |
| unknown record field | `unknown field` |
| record field type mismatch | `field` |

If a must-fail case starts compiling, the suite fails. That is the
regression test for the constitution.

### 3. Real games (must paint)

- **Lantern Night (wick)** self-plays under `SHOWCASE_AUTO` for N frames.
- **Package round-trip**: pack showcase_wick, run folder vs `.lant`,
  `cmp` framebuffers; corrupt one byte, require CRC refusal.
- **Path sandbox**: wick fixtures that attempt `../` and `/etc/...`.
- **KORA kitchen**: `KORA_SCENE=3` frame must differ from the title
  screen control shot.

## What we do not do

- Re-implement the compiler in the test harness and assert against that.
- Golden-master huge ASTs.
- Benchmark theater before a game is slow.

## Run it

```sh
cd lantern
cmake --build build -j
bash tests/wick_test.sh ./build/lantern
bash tests/path_sandbox_test.sh ./build/lantern
bash tests/package_test.sh ./build/lantern ./build/lantern_pack .
```

If you change the language, add a must-fail or a semantics check **in the
same commit**. Same rule as the bug journal.
