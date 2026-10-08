# コレクション { #collections }

## リスト { #lists }

型付きで順序があり、**0 始まり**です。

```wick
let xs = [1, 2, 3]            // list<num>, element type inferred
let names = ["a", "b"]        // list<str>
let flags: list<bool> = []    // empty literal REQUIRES the annotation

push(xs, 4)                   // append (type-checked)
let last = pop(xs) ?? 0       // pop returns T? (nil when empty)
xs[0] = 10                    // index assignment
let n = len(xs)               // length
```

範囲外の添字アクセスは**実行時エラー**になり、行番号とともにエラー画面に表示されます。
未定義の動作になったり、何も知らせず nil を返したりはしません。

要素は `num`、`bool`、`str`、または**レコード**型です。ネストしたリスト
（`list<list<num>>`）は、引き続き[制限](limits.md)の対象です。リストリテラルの要素は
同じ型でなければならず、`[1, "a"]` はコンパイルできません。

## レコードのリスト { #lists-of-records }

```wick
record Pt { x: num, y: num }
let pts: list<Pt> = []
push(pts, Pt { x: 1, y: 2 })
pts[0].x = 9
```

1 つの実体が複数のフィールドを持つ場合は、並列リストよりこちらを使ってください。
詳しい説明: [レコード](records.md)。

## マップ { #maps }

キーは文字列で、値には型があります。

```wick
let scores = ["ana": 3, "bo": 5]   // map<num>
scores["cid"] = 1                  // insert / update
let s = scores["dee"] ?? 0         // get is ALWAYS T? — missing key is nil
let n = len(scores)
```

マップの検索が `T?` を返すのは意図的です。呼び出し側でキーが存在しない場合に必ず向き合う必要があり、
`??` を使えば 3 文字で対処できます。

## 定番の書き方 { #idioms }

**レコード（複数のフィールドを持つ実体に推奨）:**

```wick
record Lamp { x: num, z: num, lit: bool }
let lamps: list<Lamp> = []
push(lamps, Lamp { x: 3.4, z: 3.4, lit: true })
```

**並列リスト**（小さな固定集合や、まだその形式で組み込まれているデータには引き続き使えます）:

```wick
let lamp_x: list<num> = []
let lamp_z: list<num> = []
let lamp_lit: list<bool> = []
// index i is one lamp across all three lists
```

**順に処理する**:

```wick
for i in 0..len(xs) { use(xs[i]) }
```
