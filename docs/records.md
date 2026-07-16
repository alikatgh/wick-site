# Records

Flat data bags with named fields. **No methods, no inheritance, no `self`.**
Admitted when KORA's kitchen props became five parallel `list<num>`s — the
evidence ledger is the authority, not fashion.

## Declare

```wick
record Prop {
  slot: num
  x: num
  y: num
  w: num
  h: num
}
```

- Field types are only `num`, `bool`, or `str` (not optional, not nested records).
- Fields may be separated by commas and/or newlines.
- At least one field; max 255 fields.
- Declarations are top-level only (not inside a function).

## Construct

Named fields, any order; **all fields required**:

```wick
let p = Prop { slot: 21, x: 320, y: 208, w: 87, h: 96 }
let q = Prop { y: 0, x: 0, w: 16, h: 16, slot: 0 }   // order free
```

Missing a field or inventing one is a **compile error**.

## Field get / set

```wick
let s = p.slot
p.x = p.x + 1
```

Works on locals and globals. On list elements:

```wick
let props: list<Prop> = []
push(props, Prop { slot: 0, x: 10, y: 20, w: 8, h: 8 })
props[0].y = 30
lt.sprite_uv(tex[props[0].slot], props[0].x, props[0].y, ...)
```

## Lists of records

```wick
let props: list<Prop> = []
// empty list needs the annotation; element type is the record name
```

`list<record>` is the intended way to grow tables. Prefer it over parallel
lists when a second or third field appears.

## What records are *not*

| Not included | Why |
|---|---|
| Methods / `self` | Keep wick a data + functions language |
| Nested records / `list` fields | v0.2: only primitive fields |
| Optionals in fields | Use a sentinel (`-1`) or parallel flag list until evidence |
| Default field values | All fields explicit at construct |

## Evidence

| Game pain | Admission |
|---|---|
| KORA kitchen: `kitchen_prop` / `_px` / `_py` / `_pw` / `_ph` | `list<Prop>` + `draw_prop_list` |
| Lantern Night lamps (still parallel lists) | Optional migrate; not required |

See the [feature ledger](limits.md) and the blog post
[Admitting records](blog/2026-07-14-admitting-records.md).
