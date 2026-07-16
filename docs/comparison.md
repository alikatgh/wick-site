# wick vs Lua — the same game, twice

Kora Night ships in both languages, as two deliberately separate projects
that evolve together:
[`games/showcase`](https://github.com/alikatgh/lantern/tree/main/games/showcase) (Lua) ·
[`games/showcase_wick`](https://github.com/alikatgh/lantern/tree/main/games/showcase_wick) (wick).
Highlights from the diff:

## The hi-score bug, before and after

```lua
-- Lua: shipped with a frame-1 crash. A 0-byte save file makes
-- load_save return "" (truthy!), the fallback never fires, and
-- tonumber("") = nil poisons everything downstream.
local best = tonumber(lt.load_save("koranight_best") or "0")
```

```wick
// wick: this is the ONLY version that compiles — both nil cases
// are handled or it's a type error.
let best = num(lt.load_save("koranight_wick_best") ?? "") ?? 0
```

## Records

```lua
-- Lua: a list of tables
local LAMPS = {
  { x = 3.4, z = 3.4, lit = true },
  ...
}
for i, l in ipairs(LAMPS) do ... l.lit ... end
```

```wick
// wick: flat records (admitted when KORA kitchen paid the cost)
record Lamp { x: num, z: num, lit: bool }
let lamps: list<Lamp> = []
push(lamps, Lamp { x: 3.4, z: 3.4, lit: true })
for i in 0..len(lamps) { ... lamps[i].lit ... }
```

Lantern Night still uses parallel lists for four lamps — that's fine.
KORA kitchen props use `list<Prop>`. Prefer records when a third field appears.

Honest score: Lua reads better here today. This is the top of wick's
v0.2 wishlist.

## Multiple returns

```lua
local i, dist2 = nearest_unlit()
```

```wick
let i = nearest_unlit()      // returns the index, or -1
let d = dist2_to(i)          // second query, explicit
```

## What you stop writing entirely

- Defensive `if x ~= nil` chains around every save/parse — the compiler
  tracks it.
- `math.` prefixes (`sin`, `floor`, `rand` are built-ins) and
  `string.format` for integers (`str()` prints them clean).
- Argument-order paranoia on engine calls — arity and types are checked
  with the call name and argument number in the message.

## What stays the same

The engine API is call-for-call identical (`lt.draw(...)` is the same
line in both), the frame contract is the same, hot-reload and the error
screen behave the same, and the games render the same frames.
