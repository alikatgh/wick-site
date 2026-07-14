# Functions

```wick
fn dist(ax: num, az: num, bx: num, bz: num): num {
  let dx = bx - ax
  let dz = bz - az
  return sqrt(dx * dx + dz * dz)
}
```

- Declared with `fn`, at the **top level only** (no nesting, no closures
  in v0.1).
- **Parameter types are required.** The return type follows the parameter
  list after `:`; omit it for a void function.
- **Declare before use** (C-style): a function must appear above its first
  call. `update`/`draw` are called by the host, so their position doesn't
  matter relative to each other.
- Recursion works (`fn fib(k: num): num { ... return fib(k-1) + fib(k-2) }`).
- Calls are checked: wrong arity or argument types are compile errors that
  name the function and the argument number.

## The frame contract

The engine looks up two functions by name each frame:

```wick
fn update(dt: num) { }   // simulation; dt in seconds
fn draw() { }            // rendering; 3D calls then 2D composites on top
```

Both are optional. Top-level statements run once at load — that is where
you create meshes, load textures and sounds, and initialize state.

## Returning values

A function with a declared return type must `return expr` on the paths
that matter; falling off the end of a non-void function returns `nil`
(avoid relying on this — v0.1 does not enforce full path coverage yet;
see [limits](limits.md)).

Multiple return values do not exist; return a value and use out-of-band
state, or split into two functions (the Kora Night port's
`nearest_unlit()` + `dist2_to(i)` pair is the worked example).
