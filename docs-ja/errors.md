# コンパイルエラーの解説 { #compile-errors-explained }

すべてのエラーは `file:line: message` の形式で、エンジン内のエラー画面に表示されます。
ファイルを修正して保存すると、ゲームがホットリロードされます。以下は原因別の一覧です。

| メッセージ（パターン） | 意味 | 修正方法 |
|---|---|---|
| `expected str, got str?`（型は任意） | 通常の値が必要な場所で、オプショナルや誤った型を使っている | `??` でアンラップするか、`if x != nil { }` で型を絞り込む |
| `if condition must be bool (wick has no truthiness)` | 数値や文字列に対する `if x` | `if x > 0`、`if s != ""` のように比較を書く |
| `unknown variable 'x' — wick has no implicit globals; use let` | 未宣言の名前に代入した（タイプミスが多い） | `let x = ...` とするか、つづりを修正する |
| `unknown variable 'x' (declare it with let)` | 未宣言の名前を読み取った | 同上 |
| `'+' needs num+num or str+str (use str(x))` | 異なる型を混在させた `+` | `"n=" + str(n)` のように明示的に変換する |
| `f() argument 3: expected num, got str` | 型付き呼び出しの不一致（エンジンまたは自分の fn） | [API 一覧](engine-api.md)を確認する |
| `f() needs at least N arguments` / `takes N arguments` | 引数の個数の不一致 | シグネチャを確認する |
| `unknown function 'f' (wick requires declare-before-use)` | 定義より前で呼び出した | `fn` を上に移動する |
| `can't infer a type from nil; annotate: let x: str? = nil` | 型注釈なしの `nil` 初期化 | 型注釈を追加する |
| `empty [] needs a type: let xs: list<num> = []` | 型のない空のリテラル | `let` に型注釈を付ける |
| `list elements must share one type` | `[1, "a"]` | リストの要素を同じ型にする |
| `comparing non-optional to nil` | 通常の型に対する `x != nil` | nil になることはないので、検査を削除する |
| `'??' left side must be an optional` | `a` が nil にならない `a ?? b` | `??` を削除する |
| `'x' already declared in this scope` | `let` の重複 | 代入にするか、名前を変更する |
| `parenthesize this condition: (a != b) and ...` | 絞り込みのパターンと論理演算の混在 | 括弧を追加する |
| `break outside a loop` / `continue outside a loop` | | |
| `fn declarations can't nest` | `fn` 内の `fn` | トップレベルのみ（v0.1） |
| `return outside a function` / `void function can't return a value` / `this function must return T` | return と型の不一致 | 宣言した戻り値の型に合わせる |
| `map keys must be str literals` | リテラル内で計算されたキーを使用 | `m[k] = v` で構築する |
| `container elements must be num, bool, or str` | ネストしたコンテナ | [制限](limits.md)を参照する |

## 例: オプショナルを使用前に処理する { #example-handle-an-optional-before-using-it }

`lt.load_save` は `str?` を返しますが、`lt.print` は `str` を必要とするため、
次のコードはコンパイルできません。

```wick
let saved = lt.load_save("best")
fn draw() {
  lt.print(saved, 4, 4)
}
```

値を使う前にフォールバックを指定します。

```wick
let saved = lt.load_save("best") ?? "No saved score"
fn draw() {
  lt.clear(0.1, 0.1, 0.2)
  lt.print(saved, 4, 4)
}
```

または、`if saved != nil` の分岐を使います。型の絞り込みの規則は
[型とオプショナル](types.md)を参照してください。これらの検査は、最初のフレームが動く前の、
プログラムのコンパイル時に行われます。

## 実行時エラー { #runtime-errors }

静的な型では防げないエラーです。フレームを停止し、
行番号とともにエラー画面に表示します。

| メッセージ | 原因 |
|---|---|
| `list index N out of range (len M)` | 範囲外の `xs[i]`（読み取りまたは書き込み） |
| `check failed: <msg>` | 自分で記述した `check()` のアサーション |
| `load_texture/mesh/sound failed: <path>` | アセットがない、または不正 |
