# Wick

Language reference for **Wick 0.3**, included with **Lantern 0.8.0**.
Wick compiles to bytecode; Lantern supplies the game loop and the `lt.*` engine API.

## Where to start

- **Run a program:** [Getting started](getting-started.md) covers installation, a complete example and reload-on-save.
- **Learn in order:** [The Wick Book](https://wick.aulenor.com/book/) introduces the language through game development.
- **Choose the host:** [Lantern](https://wick.aulenor.com/lantern/) covers downloads, builds, examples and platform status.
- **Fix a failure:** [Compile and runtime errors](errors.md) lists messages, causes and corrections.

## Language lookup

| Task | Reference |
|---|---|
| Declare a variable, branch or loop | [Syntax](syntax.md) |
| Handle a missing value | [Types, optionals and narrowing](types.md) |
| Define named fields | [Records](records.md) |
| Store or iterate over values | [Lists and maps](collections.md) |
| Declare or call a function | [Functions](functions.md) |
| Convert, format or check a value | [Built-in functions](builtins.md) |
| Mask bits, wrap registers, display hex | [Bits, bytes and words](bits.md) |
| Draw, read input, play audio or save | [Engine API — `lt.*`](engine-api.md) |

Search accepts function names such as `u8`, `bit_shr` and `lt.rect`, or words
from a diagnostic. Results link to the relevant reference section.

## Common lookups

- [`u8` and `u16`: explicit wrapping](bits.md#explicit-register-widths)
- [`bit_and`, `bit_or`, `bit_xor`, `bit_not`, `bit_shl`, `bit_shr`](bits.md#bit-operations)
- [`hex` and `bin`: formatting](bits.md#display)
- [`lt.rect`, sprites and text](engine-api.md#2d)
- [Input and save data](engine-api.md#input-saves)
- [Supported features and current limits](limits.md)

## Why a new language

Wick uses static types, explicit `T?` optionals, declared variables and boolean
conditions. Calls to the engine are checked for argument types and arity when
a game loads. The runtime uses a bytecode VM with collection between frames.

For specific differences, read [Wick and Lua](comparison.md). For implementation
details, read [Internals and embedding](internals.md) or the
[compiler and VM source](https://github.com/alikatgh/lantern/tree/v0.8.0/wick).

## New in 0.3

[Bits, bytes, and words](bits.md) adds checked bit operations, hex/binary
literals, register wrapping and display functions. `u8` and `u16` are functions,
not new types; ordinary `num` arithmetic does not wrap automatically.

The ten added built-in names are reserved function names. See the
[release notes](blog/2026-10-06-release-0.3.md) for compatibility details and
[the changelog](https://github.com/alikatgh/lantern/blob/v0.8.0/CHANGELOG.md)
for the matching engine release.
