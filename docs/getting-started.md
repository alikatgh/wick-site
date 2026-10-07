# Getting started

Run your first Wick program with **Lantern 0.8.0 / Wick 0.3**. Wick is included
with the engine; there is no separate language installation.

## Get the engine

**macOS Apple Silicon:** [download the Lantern bundle](https://wick.aulenor.com/lantern/#downloads),
extract it, and open a terminal in the extracted folder. It contains `lantern`,
`lantern_pack` and the Bit Lab example. The build is ad-hoc signed, not Apple notarized.

**Building from source:** follow the [Lantern build instructions](https://wick.aulenor.com/lantern/#build-from-source).
Commands below assume the downloaded bundle. In a source checkout, replace
`./lantern` with `./build/lantern` and `./lantern_pack` with `./build/lantern_pack`.

## Run your first program

Create a game directory from the folder containing the engine:

```sh
mkdir -p games/first-game
```

Save the following complete program as `games/first-game/main.wick`.
You can also [download main.wick](https://wick.aulenor.com/examples/first-game/main.wick).

```wick
let x = 0

fn update(dt: num) {
  x = (x + 40 * dt) % 400
}

fn draw() {
  lt.clear(0.1, 0.1, 0.2)
  lt.rect(x, 100, 16, 16, 1, 0.8, 0.2, 1)
}
```

Run it from the same terminal:

```sh
./lantern games/first-game
```

**Expected result:** a yellow square moves across a dark 400 × 240 frame.
It wraps to the left when its x position reaches 400. Press Escape to quit.

Change `40` to `80` and save the file while the game is running. The square
restarts and moves twice as fast. If a compile error appears, fix the indicated
line and save again. [Compiler messages and fixes](errors.md) explain common failures.

## A game is a folder

`main.wick` is the entry point. Top-level statements run once when the game
loads; Lantern then calls `update(dt: num)` and `draw()` if they exist.
`dt` is elapsed time in seconds, capped at 0.1. Draw calls use screen coordinates
or the engine's 3D scene; consult the [engine API](engine-api.md) for each signature.

The host prefers `main.wick` when both it and `main.lua` are present. Asset paths
are relative to the game directory, including nested paths such as `assets/tiles.bmp`.

## The dev loop

- Save `main.wick` to recompile and reload. Reloading starts the game's state again.
- Compile and runtime errors appear in-engine with `file:line: message`.
- `LANTERN_FIXED_DT=1` uses a fixed timestep for repeatable runs.
- To save a framebuffer and exit after 60 frames, set `LANTERN_SHOT` to a writable
  output prefix. For example, `LANTERN_SHOT=first-frame ./lantern games/first-game`
  writes a BMP screenshot. `LANTERN_SHOT_FRAME` changes the capture frame.

## Package a game

```sh
./lantern_pack games/first-game first-game.lant
./lantern first-game.lant
```

The `.lant` file contains the game and its assets. Keep the source folder for
editing. [Lantern's packaging guide](https://wick.aulenor.com/lantern/#package-a-game)
covers the folder structure and links to the format specification.

## Two minutes of syntax

```wick
let speed = 120.0            // types are inferred
let name: str = "tenzin"     // ...or written out
let lamps: list<bool> = []   // empty literals need the annotation

record Pt { x: num, y: num }
let p = Pt { x: 1, y: 2 }

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

Read on: [Syntax](syntax.md) · [Types & optionals](types.md) · [Records](records.md) · [Blog](blog/index.md)
