# Why optionals (a real crash)

*2026-07-14*

Most languages get optionals from type theory fashion. wick got them from
a crash on frame one of a game we had already shown people.

## The Lua bug

Lantern Night stores a hi-score. The Lua build did the usual thing:

```lua
local best = tonumber(lt.load_save("koranight_best") or "0")
```

If the save file is **missing**, `load_save` fails and `or "0"` works.
If the save file is **present but empty** (interrupted write, 0 bytes),
`load_save` returned `""`. In Lua, `""` is truthy. The fallback never
ran. `tonumber("")` is `nil`. The next arithmetic blew up — not in a unit
test, on the title screen of a real session.

That is not a hypothetical. It is why optionals are not optional in wick.

## The wick shape

```wick
let best = num(lt.load_save("koranight_wick_best") ?? "") ?? 0
```

- `lt.load_save` returns `str?` — missing save is `nil`.
- `?? ""` forces a string into `num(...)`.
- `num` returns `num?` — parse failure (including `""`) is `nil`.
- `?? 0` is the only way the type becomes `num`.

There is no other program the compiler accepts for this idea. You cannot
“forget” the empty-string case. That is the whole design.

## What we refused

- Making `load_save` return `""` on missing and empty — hides the two cases.
- Runtime null checks only — we already had those; they were skippable.
- A linter rule — linters are optional; crashes are not.

## Narrowing

```wick
let s = lt.load_save("hi")
if s != nil {
  lt.print(s, 4, 4, 1, 1, 1, 1)  // s: str here
}
```

Narrowing is local-only in the current compiler (one-pass). Globals use
`??`. That is a trade for implementation size, not a philosophical ban.

## Takeaway

Optionals in wick are not “we wanted sum types.” They are **the empty
save file, made unrepresentable as a silent crash**. Every other type
feature will have to clear the same bar.
