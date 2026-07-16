# Types & optionals

wick is **statically typed with inference**. Every expression has a type
at compile time; annotations are only needed where inference has nothing
to work with.

## The types

| Type | Values | Notes |
|---|---|---|
| `num` | IEEE-754 double | the only number type, like Lua |
| `bool` | `true`, `false` | the only type conditions accept |
| `str` | immutable text | `+` concatenates str+str only |
| `list<T>` | ordered, 0-based | `T` is `num`, `bool`, `str`, or a **record** |
| `map<T>` | string-keyed | values are `num`, `bool`, or `str` |
| *record* | named fields | see [Records](records.md) |
| `T?` | `T` or `nil` | an **optional** — the headline feature |

`nil` is not a general value: it only inhabits optionals. `let x = nil`
does not compile without an annotation (`let x: str? = nil`).

## Optionals: nil-safety, enforced

Any operation that can fail returns an optional, and the compiler will
not let you touch the value until you have dealt with the `nil` case.

```wick
let s = lt.load_save("hi")     // s: str?
lt.print(s, 4, 4, 1, 1, 1, 1)  // COMPILE ERROR: str? where str expected
```

Two ways to deal with it:

**1. `??` — unwrap with a default**

```wick
let text = s ?? "no save yet"        // text: str
let n = num("maybe") ?? 0            // num() parses str -> num?
```

`??` evaluates its right side only when the left is `nil`, and the result
is the non-optional base type.

**2. Narrowing — `if x != nil`**

```wick
if s != nil {
  // inside this block, s: str (narrowed)
  lt.print(s, 4, 4, 1, 1, 1, 1)
}
```

Narrowing works on **local** variables; module globals must use `??`.
Assigning a new optional value inside the block un-narrows.

## What returns an optional

| Expression | Type | `nil` when |
|---|---|---|
| `lt.load_save(k)` | `str?` | no readable save |
| `num(s)` | `num?` | `s` is not a number (including `""`) |
| `pop(xs)` | `T?` | the list is empty |
| `m[key]` | `T?` | the key is absent |
| `env(name)` | `str?` | the variable is unset |

!!! note "The bug this kills"
    In the Lua build of Lantern Night, an interrupted save left a 0-byte
    file; `lt.load_save` returned `""` (truthy!), the `or "0"` fallback
    never fired, and `tonumber("")` produced a nil that crashed frame 1.
    The wick equivalent — `num(lt.load_save(k) ?? "") ?? 0` — is the only
    version the compiler accepts.

## Assignment compatibility

- `T` may be stored where `T?` is expected (widening is free).
- `T?` may **not** be stored where `T` is expected — unwrap first.
- Containers are invariant: `list<num>` only accepts `num` elements;
  `list<Prop>` only accepts that record type.
- `void` (a function without a return type) cannot be assigned at all;
  calling a void function is a statement, not an expression.

## Handles are still `num`

Mesh, texture, and sound handles from `lt.load_*` are plain `num` today.
Passing a texture id to `lt.play` type-checks; wrong use is a runtime
no-op or error. Branded handle types are a candidate if store games need
them — not yet admitted.
