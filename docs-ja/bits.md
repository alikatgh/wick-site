# ビット、バイト、ワード { #bits-bytes-and-words }

Wick 0.3 では、プロセッサを作るゲームに必要な基本機能を追加しました。読みやすい
ハードウェア定数、検査付きのビット演算、明示的なレジスタのラップ、2 進数・16 進数のラベルです。
Lantern でも単体の VM でも動作します。

## 定数 { #constants }

```wick
let opcode = 0x76
let mask = 0b10000000
let address = 0xFFFF
```

接頭辞は大文字・小文字を区別しません（`0x`/`0X`、`0b`/`0B`）。値の範囲は 0 から
`0xFFFFFFFF` までで、両端を含みます。数字の欠落、不正な数字、アンダースコア、小数を含む
接頭辞付きリテラル、オーバーフローはコンパイルエラーです。10 進数の構文は変わりません。
指数表記には引き続き対応していません。これらは通常の `num` 値です。

## ビット演算 { #bit-operations }

| 関数 | 意味 |
|---|---|
| `bit_and(a, b)` | AND / マスク |
| `bit_or(a, b)` | OR / ビットを組み合わせる |
| `bit_xor(a, b)` | XOR / ビットを反転する |
| `bit_not(a)` | **32** ビットすべてを反転する |
| `bit_shl(a, count)` | 左シフト。ビット 31 を超えた分は捨てる |
| `bit_shr(a, count)` | 論理右シフト。空いた部分は 0 で埋める |

入力は `0..4294967295` の有限な整数、シフト数は `0..31` の整数でなければなりません。
型や引数の個数が誤っている場合はコンパイル時に失敗します。不正な数値は `file:line` を伴う
実行時エラーになり、黙って切り捨てられたり、未定義の C++ シフトに渡されたりはしません。
結果は符号なし 32 ビットの値で、`num` で正確に表現されます。
これらは関数なので、式の優先順位は変わりません。

## 明示的なレジスタ幅 { #explicit-register-widths }

`u8(n)` は 256 を法として、`u16(n)` は 65536 を法としてラップします。
ビット演算と異なり、負の整数も受け入れます。入力は
`-9007199254740991` から `9007199254740991` まで（両端を含む安全な整数範囲）の
有限な整数でなければなりません。小数は黙って丸めず、拒否します。

```wick
check(u8(0xFF + 1) == 0, "byte carry")
check(u8(-1) == 255, "byte underflow")
check(u16(0xFFFF + 1) == 0, "program counter wrap")
check(u8(bit_not(0x0F)) == 0xF0, "eight-bit complement")
```

`num` 自体に自動的なオーバーフロー処理が加わるわけではありません。
キャリーを計算するまで桁幅の大きい加算結果を保持し、その後レジスタの値をラップしてください。

## 表示 { #display }

`hex(n, width=1)` は接頭辞なしの大文字の 16 進数を返します。
`bin(n, width=1)` は接頭辞なしの 2 進数を返します。値の範囲はビット演算と同じ
符号なし 32 ビットです。幅は切り詰める長さではなく**最小幅**です。
`hex` は 1〜8、`bin` は 1〜32 で、整数のみ指定できます。

```wick
check(hex(10, 2) == "0A", "padded byte")
check(hex(256, 2) == "100", "never hide high bits")
check(bin(5, 8) == "00000101", "bus display")
```

## プロセッサの例 { #processor-example }

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

対話型の [Bit Lab サンプル](https://github.com/alikatgh/lantern/tree/main/games/bitlab)を
`./build/lantern games/bitlab` で実行してください。2 つのレジスタ、ADD/AND/XOR、
ビットの切り替え、フラグ、PC のラップを確認できます。これは言語を試すための作業台であり、
完全な 8080 エミュレータや、完成したプロセッサ制作ゲームではありません。
ADD/ANA/XRA のフラグ規則は、Intel の
[8080/8085 Assembly Language Programming マニュアル](https://st.sdf-eu.org/i8080/Intel%208080-8085%20Assembly%20Language%20Programming%201977%20Intel.pdf)に従います。

## 互換性 { #compatibility }

既存の算術演算、レコード、バイトコードの実行、フレームのコールバックは互換性を維持します。
新しい 10 個の組み込み関数名は予約名になったため、アップグレード時には同名のユーザー定義関数を
改名してください。モジュール、ネストしたレコードやコンテナ、文字列の添字アクセス、第一級関数は
今回のリリースには含まれません。`u8` と `u16` は新しい型ではなく関数です。
