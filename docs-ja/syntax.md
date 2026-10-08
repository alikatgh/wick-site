# 構文 { #syntax }

## 字句構造 { #lexical-structure }

- **コメント**: `// to end of line`。行末までがコメントです。ブロックコメントはありません。
- **識別子**: `[A-Za-z_][A-Za-z0-9_]*`。
- **数値**: 型は `num`（IEEE 倍精度）の 1 種類です。例: `42`、`3.5`、`0.25`。16 進数・2 進数の整数は `0xFF`、`0b1010`（0..0xFFFFFFFF）。指数表記はありません。`1..5` は常に範囲として字句解析され、`1.` と `.5` にはなりません。
- **文字列**: `"double quotes"` のように二重引用符で囲み、エスケープとして `\n`、`\t`、`\"`、`\\` が使えます。
- **キーワード**: `let fn if elif else while for in break continue return
  true false nil and or not record`。

## 変数 { #variables }

すべての変数は `let` で宣言し、そのブロックをスコープとします。

```wick
let x = 10          // num, inferred
let y: num = 10     // same, explicit
let s = "hi"        // str
```

**暗黙のグローバル変数はありません**。未宣言の名前への代入はコンパイルエラーになるため、
この種のタイプミスによるバグは生じません。
トップレベルの `let` はプログラムのグローバル変数を、関数内の `let` はローカル変数を作ります。
内側のブロックで外側と同じ名前を使うシャドーイングは可能ですが、
*同じ*スコープ内での再宣言はエラーです。

## 文 { #statements }

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

ブロックには常に波括弧を使います。セミコロンはありません。
文の終わりは文法によって決まり、改行に意味はありません。

### `if` / `elif` / `else` { #if-elif-else }

条件は `bool` でなければなりません。`if 1 { }` や `if name { }` はコンパイルできません。
Wick には**値を暗黙に真偽値として扱う仕組みはありません**。

### `for` の範囲 { #for-ranges }

`for i in a..b` は `i` を `[a, b)` の範囲で順に処理します。
添字と同様に 0 始まりで、終端の値は含みません。

```wick
for i in 0..len(xs) {
  lt.print(str(xs[i]), 4, 4 + i * 10, 1, 1, 1, 1)
}
```

## 演算子の優先順位（低い順） { #operator-precedence-loosest-to-tightest }

| レベル | 演算子 |
|---|---|
| 1 | `or` |
| 2 | `and` |
| 3 | `??`（nil 合体演算子） |
| 4 | `==` `!=` |
| 5 | `<` `<=` `>` `>=` |
| 6 | `+` `-` |
| 7 | `*` `/` `%` |
| 8 | 単項 `-`、`not` |
| 9 | 呼び出し `f(x)`、添字アクセス `a[i]` |

補足:

- `+` は数値の加算、**または** `str + str` の連結です。型を混在させることはできません。
  `"score " + 5` はコンパイルエラーになるため、`"score " + str(5)` と書きます。
- `and` / `or` は短絡評価を行い、オペランドは `bool` でなければなりません。
- `==` / `!=` は同じ型の値を比較します（`str` は内容を比較します）。
  オプショナルを `nil` と比較するのは型の絞り込みの定番です。
  [型とオプショナル](types.md)を参照してください。
- `x != nil` と `and`/`or` を組み合わせた複雑な条件には、括弧を付けてください。
  必要な場合はコンパイラが知らせます。
