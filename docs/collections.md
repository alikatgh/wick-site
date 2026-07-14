# Collections

## Lists

Typed, ordered, **0-based**:

```wick
let xs = [1, 2, 3]            // list<num>, element type inferred
let names = ["a", "b"]        // list<str>
let flags: list<bool> = []    // empty literal REQUIRES the annotation

push(xs, 4)                   // append (type-checked)
let last = pop(xs) ?? 0       // pop returns T? (nil when empty)
xs[0] = 10                    // index assignment
let n = len(xs)               // length
```

Indexing out of range is a **runtime error** (shown on the error screen
with the line number) — not undefined behavior, not a silent nil.

Elements are `num`, `bool`, or `str`; lists of lists are a v0.1
[limit](limits.md). List literals must be homogeneous — `[1, "a"]` does
not compile.

## Maps

String-keyed, value-typed:

```wick
let scores = ["ana": 3, "bo": 5]   // map<num>
scores["cid"] = 1                  // insert / update
let s = scores["dee"] ?? 0         // get is ALWAYS T? — missing key is nil
let n = len(scores)
```

Map lookup returning `T?` is deliberate: the missing-key case is forced
into view at the call site, where `??` handles it in three characters.

## Idioms

**Records via parallel lists** (v0.1 has no structs):

```wick
let lamp_x: list<num> = []
let lamp_z: list<num> = []
let lamp_lit: list<bool> = []
// index i is one lamp across all three lists
```

**Iterate**:

```wick
for i in 0..len(xs) { use(xs[i]) }
```
