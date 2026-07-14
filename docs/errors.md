# Compile errors, explained

Every error is `file:line: message`, shown on the in-engine error screen.
Fix the file and save — the game hot-reloads. The catalogue, A–Z by cause:

| Message (pattern) | Meaning | Fix |
|---|---|---|
| `expected str, got str?` (any types) | using an optional (or wrong type) where a plain value is needed | unwrap with `??` or narrow with `if x != nil { }` |
| `if condition must be bool (wick has no truthiness)` | `if x` on a number/string | write the comparison: `if x > 0`, `if s != ""` |
| `unknown variable 'x' — wick has no implicit globals; use let` | assigned a name never declared (often a typo) | `let x = ...`, or fix the spelling |
| `unknown variable 'x' (declare it with let)` | read of an undeclared name | same |
| `'+' needs num+num or str+str (use str(x))` | mixed-type `+` | convert explicitly: `"n=" + str(n)` |
| `f() argument 3: expected num, got str` | typed call mismatch (engine or your fn) | check the [API table](engine-api.md) |
| `f() needs at least N arguments` / `takes N arguments` | arity mismatch | see signature |
| `unknown function 'f' (wick requires declare-before-use)` | called above its definition | move the `fn` up |
| `can't infer a type from nil; annotate: let x: str? = nil` | bare `nil` initializer | add the annotation |
| `empty [] needs a type: let xs: list<num> = []` | untyped empty literal | annotate the `let` |
| `list elements must share one type` | `[1, "a"]` | homogeneous lists only |
| `comparing non-optional to nil` | `x != nil` on a plain type | it can never be nil; delete the check |
| `'??' left side must be an optional` | `a ?? b` where `a` can't be nil | delete the `??` |
| `'x' already declared in this scope` | duplicate `let` | assign instead, or rename |
| `parenthesize this condition: (a != b) and ...` | narrowing pattern mixed with logic | add parentheses |
| `break outside a loop` / `continue outside a loop` | | |
| `fn declarations can't nest` | `fn` inside `fn` | top level only (v0.1) |
| `return outside a function` / `void function can't return a value` / `this function must return T` | return/type mismatch | align with the declared return type |
| `map keys must be str literals` | computed keys in a literal | build with `m[k] = v` |
| `container elements must be num, bool, or str` | nested containers | see [limits](limits.md) |

## Runtime errors

Static types can't remove these; they stop the frame and show on the
error screen with a line number:

| Message | Cause |
|---|---|
| `list index N out of range (len M)` | out-of-bounds `xs[i]` (read or write) |
| `check failed: <msg>` | your own `check()` assertion |
| `load_texture/mesh/sound failed: <path>` | missing or bad asset |
