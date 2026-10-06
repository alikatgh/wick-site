# Bits, bytes, and words

Wick 0.3 adds the primitives needed by a processor-building game: readable
hardware constants, checked bit operations, explicit register wrapping, and
binary/hexadecimal labels. They work in the standalone VM as well as Lantern.

## Constants

```wick
let opcode = 0x76
let mask = 0b10000000
let address = 0xFFFF
```

Prefixes are case-insensitive (`0x`/`0X`, `0b`/`0B`). Values range from 0 to
`0xFFFFFFFF` inclusive. Missing digits, invalid digits, underscores, fractional
prefixed literals, and overflow are compile errors. Decimal syntax is unchanged;
exponent notation is still unsupported. These are ordinary `num` values.

## Bit operations

| Function | Meaning |
|---|---|
| `bit_and(a, b)` | AND / mask |
| `bit_or(a, b)` | OR / combine bits |
| `bit_xor(a, b)` | XOR / toggle bits |
| `bit_not(a)` | Complement all **32** bits |
| `bit_shl(a, count)` | Shift left; discard bits beyond bit 31 |
| `bit_shr(a, count)` | Logical right shift; fill with zero |

Inputs must be finite whole numbers in `0..4294967295`; shift counts must be
whole numbers in `0..31`. Wrong types/arity fail at compile time. Invalid numeric
values fail at runtime with `file:line`; they are never silently truncated or
passed to an undefined C++ shift. Results are unsigned 32-bit values represented
exactly as `num`. These are functions, so expression precedence is unchanged.

## Explicit register widths

`u8(n)` wraps modulo 256; `u16(n)` wraps modulo 65536. Unlike bit operations,
they accept negative integers. Inputs must be finite integers between
`-9007199254740991` and `9007199254740991`, inclusive (the safe-integer range).
They reject fractions instead of silently rounding.

```wick
check(u8(0xFF + 1) == 0, "byte carry")
check(u8(-1) == 255, "byte underflow")
check(u16(0xFFFF + 1) == 0, "program counter wrap")
check(u8(bit_not(0x0F)) == 0xF0, "eight-bit complement")
```

`num` itself does not acquire automatic overflow. Keep the wide sum long enough
to compute the carry, then wrap the register value.

## Display

`hex(n, width=1)` returns uppercase hexadecimal without a prefix.
`bin(n, width=1)` returns binary without a prefix. Values use the same unsigned
32-bit domain as bit operations. Width is a **minimum**, not truncation: 1–8
for `hex`, 1–32 for `bin`, whole numbers only.

```wick
check(hex(10, 2) == "0A", "padded byte")
check(hex(256, 2) == "100", "never hide high bits")
check(bin(5, 8) == "00000101", "bus display")
```

## Processor example

```wick
record Register { value: num, name: str }
let a = Register { value: 0xFF, name: "A" }
let wide = a.value + 1
let carry = wide > 0xFF
a.value = u8(wide)
let high = 0x80
let low = 0x00
let address = bit_or(bit_shl(high, 8), low)
check(carry and a.value == 0 and address == 0x8000, "datapath")
```

Run the interactive [Bit Lab example](https://github.com/alikatgh/lantern/tree/main/games/bitlab)
with `./build/lantern games/bitlab`. It shows two registers, ADD/AND/XOR, bit toggles,
flags, and PC wrapping. It is a language workbench, not a complete 8080 emulator
or the finished processor-building game. Its ADD/ANA/XRA flag rules follow Intel's
[8080/8085 Assembly Language Programming manual](https://st.sdf-eu.org/i8080/Intel%208080-8085%20Assembly%20Language%20Programming%201977%20Intel.pdf).

## Compatibility

Existing arithmetic, records, bytecode execution, and the frame callbacks stay
compatible. The ten new built-in names are now reserved function names; rename
any user-defined functions with those names when upgrading. Modules, nested
records/containers, string indexing and first-class functions remain outside
this release. `u8` and `u16` are functions, not new types.
