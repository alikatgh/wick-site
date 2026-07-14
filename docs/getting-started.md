# Getting started

wick ships inside the lantern engine — there is nothing separate to
install.

```sh
git clone https://github.com/alikatgh/lantern && cd lantern
brew install sdl2 lua cmake pkg-config    # macOS; Linux: same packages
cmake -B build && cmake --build build -j8

./build/lantern games/wicklab             # the first wick program
./build/lantern games/showcase_wick      # Kora Night, in wick
```

## A game is a folder

A wick game is a directory containing `main.wick`. The host runs it when
present (falling back to `main.lua` otherwise):

```sh
mkdir games/mygame
$EDITOR games/mygame/main.wick
./build/lantern games/mygame
```

Define two functions. The engine calls them at 60 fps:

```wick
fn update(dt: num) {   // dt = seconds since last frame (capped at 0.1)
}

fn draw() {            // 3D first, then 2D composites on top
  lt.clear(0.1, 0.1, 0.2)
  lt.print("HELLO 400X240", 4, 4, 1, 1, 1, 1)
}
```

Both are optional — a `main.wick` with only top-level statements is legal.
Top-level statements run once, at load.

## The dev loop

- **Hot reload**: save `main.wick` while the engine runs; it recompiles and
  reloads live (all previous resources are freed first — reloading never
  leaks).
- **Error screen**: a compile error (or runtime error, like an
  out-of-range index) renders in-engine with `file:line: message`. Fix the
  file, save, keep playing.
- **CI screenshots**: `LANTERN_SHOT=/tmp/x ./build/lantern games/mygame`
  captures frame 60 as BMP and exits. Add `LANTERN_FIXED_DT=1` and the
  capture is byte-identical on every machine — wick's `rand()` is
  deterministic too, so whole gameplay sessions replay exactly.

## Two minutes of syntax

```wick
let speed = 120.0            // types are inferred
let name: str = "tenzin"     // ...or written out
let lamps: list<bool> = []   // empty literals need the annotation

for i in 0..4 {              // 0-based, end-exclusive
  push(lamps, true)
}

fn dim(v: num): num {        // parameter types are required
  if v < 0.5 { return 0 }    // conditions must be bool
  return v * 0.5
}

let saved = lt.load_save("hi")   // saved: str?  (an optional!)
let text = saved ?? "no save"    // ?? unwraps with a default
if saved != nil {
  lt.print(saved, 4, 4, 1, 1, 1, 1)  // narrowed to str inside the block
}
```

Read on: [Syntax](syntax.md) · [Types & optionals](types.md)
