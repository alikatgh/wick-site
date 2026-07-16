# Admitting records

*2026-07-14*

For months the [ledger](../limits.md) said:

> Structs / records — Kora Night uses parallel lists… Recorded, not admitted.

Today they are admitted. This post is the paper trail.

## The pain

KORA on lantern bakes world data into `main.wick`. Kitchen props looked like:

```wick
let kitchen_prop: list<num> = []
let kitchen_px: list<num> = []
let kitchen_py: list<num> = []
let kitchen_pw: list<num> = []
let kitchen_ph: list<num> = []
// draw: prop_tex[kitchen_prop[i]] at (kitchen_px[i], kitchen_py[i], ...)
```

Five lists, one logical entity. Index drift is a class of bug you only find
when a broom draws at the hearth position. Lantern Night's four lamps still
fit parallel lists; eighteen kitchen props did not.

Baking could not fix this: the *runtime* model was wrong, not the authoring
pipeline.

## The smallest language that helps

We did **not** add:

- classes, methods, inheritance
- nested records or list fields
- optional fields or defaults
- pattern matching

We added:

```wick
record Prop {
  slot: num
  x: num
  y: num
  w: num
  h: num
}

let kitchen_props: list<Prop> = []
push(kitchen_props, Prop { slot: 21, x: 320, y: 208, w: 87, h: 96 })
// ...
props[i].x
props[i].y = props[i].y + 1
```

Flat fields only (`num` / `bool` / `str`). Named construction, all fields
required. Field get/set, including on list elements. ~opcodes `OP_REC`,
`OP_FGET`, `OP_FSET` in the existing stack VM.

## Evidence rule, applied

| Question | Answer |
|---|---|
| Is there real game code that hurts? | Yes — KORA kitchen props |
| Is there a clean static workaround? | No — data is already baked; the runtime shape is the issue |
| Smallest fix? | Flat records + `list<record>` |
| Did we update tests + docs in the same change? | Yes |

Lantern Night lamps were **not** a reason to admit records. Four parallel
lists are readable. The constitution is not “make every table a record.”

## What stays out

Closures, modules, and string indexing still wait on scars. Records do not
unlock them. If your proposal is “now that we have records, we should have
methods,” the answer is still: show the game code that dies without them.

## Links

- [Records reference](../records.md)
- KORA lantern build (flagship)
- Engine [CHANGELOG](https://github.com/alikatgh/lantern/blob/main/CHANGELOG.md)
