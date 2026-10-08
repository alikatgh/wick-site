# レコード { #records }

名前付きフィールドを持つ、フラットなデータの入れ物です。**メソッド、継承、`self` はありません。**
KORA のキッチンの小物データが 5 本の並列な `list<num>` になったことをきっかけに採用しました。
流行ではなく、根拠を記した台帳に基づいて判断しています。

## 宣言 { #declare }

```wick
record Prop {
  slot: num
  x: num
  y: num
  w: num
  h: num
}
```

- フィールドの型は `num`、`bool`、`str` のみです（オプショナルやネストしたレコードは使えません）。
- フィールドはカンマ、改行、またはその両方で区切れます。
- フィールドは最低 1 個、最大 255 個です。
- 宣言はトップレベルのみで、関数内には書けません。

## 構築 { #construct }

名前付きフィールドを任意の順序で指定します。**すべてのフィールドが必須です**。

```wick
let p = Prop { slot: 21, x: 320, y: 208, w: 87, h: 96 }
let q = Prop { y: 0, x: 0, w: 16, h: 16, slot: 0 }   // order free
```

フィールドを省略したり、存在しないフィールドを追加したりすると**コンパイルエラー**になります。

## フィールドの取得と設定 { #field-get-set }

```wick
let s = p.slot
p.x = p.x + 1
```

ローカル変数とグローバル変数で使えます。リストの要素にも使えます。

```wick
let props: list<Prop> = []
push(props, Prop { slot: 0, x: 10, y: 20, w: 8, h: 8 })
props[0].y = 30
lt.sprite_uv(tex[props[0].slot], props[0].x, props[0].y, ...)
```

## レコードのリスト { #lists-of-records }

```wick
let props: list<Prop> = []
// empty list needs the annotation; element type is the record name
```

`list<record>` は、表形式のデータを拡張するために用意された方法です。
2 つ目、3 つ目のフィールドが必要になったら、並列リストよりこちらを使ってください。

## レコードに*含まれない*もの { #what-records-are-not }

| 含まれない機能 | 理由 |
|---|---|
| メソッド / `self` | Wick をデータと関数の言語に保つため |
| ネストしたレコード / `list` フィールド | v0.2 ではプリミティブのフィールドのみ |
| オプショナルのフィールド | 必要性が確認されるまでは、番兵値（`-1`）か並列のフラグリストを使う |
| フィールドの既定値 | 構築時にすべてのフィールドを明示する |

## 採用の根拠 { #evidence }

| ゲームでの困りごと | 採用した機能 |
|---|---|
| KORA のキッチン: `kitchen_prop` / `_px` / `_py` / `_pw` / `_ph` | `list<Prop>` + `draw_prop_list` |
| Lantern Night のランプ（引き続き並列リスト） | 移行は任意で、必須ではない |

[機能台帳](limits.md)と、ブログ記事
[レコードの採用](blog/2026-07-14-admitting-records.md)を参照してください。
