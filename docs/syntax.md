# Syntax

## Lexical structure

- **Comments**: `// to end of line`. No block comments.
- **Identifiers**: `[A-Za-z_][A-Za-z0-9_]*`.
- **Numbers**: one type, `num` (IEEE double): `42`, `3.5`, `0.25`. No hex,
  no exponents in v0.1. `1..5` lexes as a range, never as `1.` `.5`.
- **Strings**: `"double quotes"` with escapes `\n`, `\t`, `\"`, `\\`.
- **Keywords**: `let fn if elif else while for in break continue return
  true false nil and or not record`.

## Variables

Every variable is introduced by `let` and is scoped to its block:

```wick
let x = 10          // num, inferred
let y: num = 10     // same, explicit
let s = "hi"        // str
```

There are **no implicit globals**: assigning a name that was never
declared is a compile error — the typo class of bug does not exist.
A `let` at top level creates a program global; inside a function it
creates a local. Shadowing an outer name in an inner block is allowed;
redeclaring in the *same* scope is an error.

## Statements

```wick
x = expr             // assignment (declared names only)
xs[i] = expr         // list element / map value assignment
p.field = expr       // record field assignment
xs[i].field = expr   // record element field assignment
f(a, b)              // call statement (non-void results are discarded)
record Name { ... }  // top-level type declaration (see Records)
if c { } elif c2 { } else { }
while c { }
for i in a..b { }    // i: num, from a to b-1
break                // innermost loop
continue             // innermost loop
return expr          // or bare `return` in a void function
```

Blocks always use braces. There are no semicolons; statements end where
the grammar says they do (newlines are not significant).

### `if` / `elif` / `else`

Conditions must be `bool` — `if 1 { }` and `if name { }` do not compile.
There is **no truthiness** in wick.

### `for` ranges

`for i in a..b` iterates `i` over `[a, b)` — 0-based and end-exclusive,
matching indexing:

```wick
for i in 0..len(xs) {
  lt.print(str(xs[i]), 4, 4 + i * 10, 1, 1, 1, 1)
}
```

## Operator precedence (loosest to tightest)

| Level | Operators |
|---|---|
| 1 | `or` |
| 2 | `and` |
| 3 | `??` (nil-coalesce) |
| 4 | `==` `!=` |
| 5 | `<` `<=` `>` `>=` |
| 6 | `+` `-` |
| 7 | `*` `/` `%` |
| 8 | unary `-`, `not` |
| 9 | calls `f(x)`, indexing `a[i]` |

Notes:

- `+` is numeric addition **or** `str + str` concatenation — never mixed.
  `"score " + 5` is a compile error; write `"score " + str(5)`.
- `and` / `or` are short-circuit and require `bool` operands.
- `==` / `!=` compare values of the same type (`str` compares contents).
  Comparing an optional to `nil` is the narrowing idiom — see
  [Types & optionals](types.md).
- Complex conditions mixing `x != nil` with `and`/`or` should be
  parenthesized; the compiler will tell you when.
