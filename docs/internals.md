# Internals & embedding

The whole language lives in three files inside the lantern repo — no
dependencies beyond the C++ standard library:

```
wick/wick.hpp            the embed API (~120 lines)
wick/wick_front.cpp      lexer + one-pass typed compiler → bytecode
wick/wick_vm.cpp         stack VM, GC, built-ins, signature parser
```

## Pipeline

**No AST.** The compiler is single-pass, clox-style: the Pratt expression
parser emits bytecode as it goes while carrying a static `Type` for every
expression — the type checker and the code generator are the same walk.
This is why declare-before-use exists, and why the implementation stays
around 2k lines.

Because types are known at emit time, opcodes are **specialized**: `+`
compiles to numeric `ADD` or string `CONCAT` (never a runtime tag check),
comparisons are numeric ops, and locals resolve to frame slots — there is
no per-access name lookup at run time. Engine natives resolve to integer
ids at compile time; the VM's `NCALL` is an array index, not a table walk.

## The VM

A classic stack machine: constants pool, call frames with slot-addressed
locals, ~40 opcodes. Runtime errors carry a bytecode→line table so the
error screen can point at source. There is **no JIT** — deliberately: the
interpreter is fast enough for game logic at 400×240, and the engine
targets platforms where JITs are forbidden.

## Garbage collection

Mark & sweep over strings, lists, maps, and **records** — but the
collector **only runs when the host calls `wick::collect()`**, which
lantern does exactly once per frame, after present. A collection can
never land mid-draw; the worst case is bounded by how much garbage one
frame creates. No closures/upvalues keeps the object graph shallow: roots are
globals, constants, and the (empty-between-frames) VM stack.

## Embedding wick yourself

```cpp
#include "wick.hpp"

wick::VM* vm = wick::create();
std::string err;

// typed natives: a signature DSL the compiler enforces
wick::addNative(vm, "game", "spawn(num, num, str): num",
    [](wick::VM& vm, const wick::Value* a, int) {
        int id = mySpawn(a[0].d, a[1].d, wick::getStr(a[2]));
        return wick::Value::num(id);
    }, err);
wick::addConst(vm, "game", "MAX", 64);

wick::load(vm, source, "main.wick", err);       // compile + run top level
wick::call(vm, "update", dt, true, err);        // each frame
wick::collect(vm);                              // at YOUR safe point
wick::reset(vm);                                // hot-reload support
```

Signature grammar: `name(type[, type][, type = default]) [: type]` with
types `num bool str list` and `?` for optionals. Defaults make trailing
parameters optional at call sites; the compiler fills them in, so natives
always receive full arity. A native reports failure with
`wick::setError(vm, msg)` — the VM turns it into a file:line runtime
error at the call site.
