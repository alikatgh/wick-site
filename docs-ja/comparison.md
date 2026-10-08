# Wick と Lua — 同じゲームを 2 つの言語で { #wick-vs-lua-the-same-game-twice }

Kora Night は、両方の言語で提供されています。意図的に別々のプロジェクトにし、
一緒に発展させています。
[`games/showcase`](https://github.com/alikatgh/lantern/tree/main/games/showcase)（Lua）·
[`games/showcase_wick`](https://github.com/alikatgh/lantern/tree/main/games/showcase_wick)（Wick）。
差分から、主な点を紹介します。

## ハイスコアのバグ、修正前と修正後 { #the-hi-score-bug-before-and-after }

```lua
-- Lua: shipped with a frame-1 crash. A 0-byte save file makes
-- load_save return "" (truthy!), the fallback never fires, and
-- tonumber("") = nil poisons everything downstream.
local best = tonumber(lt.load_save("koranight_best") or "0")
```

```wick
// wick: this is the ONLY version that compiles — both nil cases
// are handled or it's a type error.
let best = num(lt.load_save("koranight_wick_best") ?? "") ?? 0
```

## レコード { #records }

```lua
-- Lua: a list of tables
local LAMPS = {
  { x = 3.4, z = 3.4, lit = true },
  ...
}
for i, l in ipairs(LAMPS) do ... l.lit ... end
```

```wick
// wick: flat records (admitted when KORA kitchen paid the cost)
record Lamp { x: num, z: num, lit: bool }
let lamps: list<Lamp> = []
push(lamps, Lamp { x: 3.4, z: 3.4, lit: true })
for i in 0..len(lamps) { ... lamps[i].lit ... }
```

Lantern Night は 4 つのランプに引き続き並列リストを使っており、それで問題ありません。
KORA のキッチンの小物には `list<Prop>` を使っています。3 つ目のフィールドが必要になったら、レコードを選んでください。

率直に評価すると、現時点ではこの部分は Lua のほうが読みやすいです。
これは Wick の v0.2 の改善希望リストで最優先の項目です。

## 複数の戻り値 { #multiple-returns }

```lua
local i, dist2 = nearest_unlit()
```

```wick
let i = nearest_unlit()      // returns the index, or -1
let d = dist2_to(i)          // second query, explicit
```

## まったく書かなくてよくなるもの { #what-you-stop-writing-entirely }

- 保存や解析のたびに周囲へ置く、防御的な `if x ~= nil` の連鎖。コンパイラが追跡します。
- `math.` の接頭辞（`sin`、`floor`、`rand` は組み込み関数）と、
  整数用の `string.format`（`str()` が小数部分なしで表示します）。
- エンジン呼び出しで引数の順序を過度に心配すること。個数と型を検査し、
  メッセージに呼び出し名と引数番号を表示します。

## 変わらないもの { #what-stays-the-same }

エンジン API は呼び出しごとに同一です（`lt.draw(...)` は両方で同じ行になります）。
フレームの呼び出し規約も同じで、ホットリロードとエラー画面も同じ動作をし、
ゲームは同じフレームを描画します。
