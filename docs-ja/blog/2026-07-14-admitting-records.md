# レコードの採用 { #admitting-records }

*2026-07-14*

数か月にわたり、[台帳](../limits.md)にはこう書いてありました。

> 構造体 / レコード — Kora Night は並列リストを使用… 記録済み、未採用。

今日、採用に至りました。この記事はその判断の記録です。

## 困りごと { #the-pain }

Lantern 上の KORA は、ワールドデータを `main.wick` に事前生成します。キッチンの小物は次のようになっていました。

```wick
let kitchen_prop: list<num> = []
let kitchen_px: list<num> = []
let kitchen_py: list<num> = []
let kitchen_pw: list<num> = []
let kitchen_ph: list<num> = []
// draw: prop_tex[kitchen_prop[i]] at (kitchen_px[i], kitchen_py[i], ...)
```

論理的には 1 つの実体なのに、リストが 5 本あります。添字のずれは、ほうきが暖炉の位置に描かれて
初めて分かる類のバグです。Lantern Night の 4 つのランプなら並列リストで十分でしたが、
18 個のキッチンの小物には向きませんでした。

事前生成では解決できませんでした。問題は制作パイプラインではなく、*実行時*のモデルにあったからです。

## 役に立つ最小限の言語機能 { #the-smallest-language-that-helps }

次のものは追加**しませんでした**。

- クラス、メソッド、継承
- ネストしたレコードやリストのフィールド
- オプショナルのフィールドや既定値
- パターンマッチング

追加したのは、次の機能です。

```wick
record Prop {
  slot: num
  x: num
  y: num
  w: num
  h: num
}

let kitchen_props: list<Prop> = []
push(kitchen_props, Prop { slot: 21, x: 320, y: 208, w: 87, h: 96 })
// ...
props[i].x
props[i].y = props[i].y + 1
```

フラットなフィールドだけ（`num` / `bool` / `str`）です。名前付きで構築し、すべてのフィールドを必須にしました。
リストの要素も含めて、フィールドの取得と設定ができます。既存のスタック VM に
`OP_REC`、`OP_FGET`、`OP_FSET` のオペコードを追加しています。

## 根拠の規則を適用する { #evidence-rule-applied }

| 問い | 答え |
|---|---|
| 実際のゲームコードで困りごとがあるか？ | はい — KORA のキッチンの小物 |
| 事前処理で無理なく回避できるか？ | いいえ — データはすでに事前生成済みで、実行時の形に問題がある |
| 最小の修正は？ | フラットなレコード + `list<record>` |
| 同じ変更でテストとドキュメントも更新したか？ | はい |

Lantern Night のランプは、レコードを採用する理由では**ありませんでした**。
4 本の並列リストは読みやすいからです。基本方針は「すべての表をレコードにする」ではありません。

## 引き続き含めないもの { #what-stays-out }

クロージャ、モジュール、文字列の添字アクセスは、実際の痛い経験が得られるまで待ちます。
レコードを採用したからといって、それらも採用することにはなりません。
「レコードがあるのだから、メソッドも必要」という提案への答えも同じです。
それがないために行き詰まるゲームコードを示してください。

## リンク { #links }

- [レコードのリファレンス](../records.md)
- KORA の Lantern ビルド（代表作）
- エンジンの[変更履歴](https://github.com/alikatgh/lantern/blob/main/CHANGELOG.md)
