# 組み込み関数 { #built-ins }

名前空間を指定せず、いつでも利用できます。汎用の組み込み関数（`len`、`str`、`num`、
`push`、`pop`）は、**コンパイル時の静的な型に基づいて**呼び出し先が決まります。
誤った型で使うと、実行時の想定外の動作ではなくコンパイルエラーになります。

## 汎用 { #generic }

| シグネチャ | 補足 |
|---|---|
| `len(x: str \| list \| map): num` | 文字数 / 要素数 / エントリ数 |
| `str(x: num \| bool \| str): str` | `str(42)` → `"42"`。整数は小数部分なしで表示します |
| `num(s: str): num?` | 解析します。失敗すると `nil`（`""` も失敗） |
| `push(xs: list<T>, v: T)` | 末尾に追加します |
| `pop(xs: list<T>): T?` | 最後の要素を削除して返します。空なら `nil` |

## 数学 { #math }

| シグネチャ | 補足 |
|---|---|
| `floor(x: num): num` · `ceil(x: num): num` | |
| `abs(x: num): num` · `sqrt(x: num): num` | |
| `min(a: num, b: num): num` · `max(a, b)` | |
| `sin(x: num): num` · `cos(x: num): num` | ラジアン |
| `atan(y: num, x: num): num` | 2 引数の逆正接 |
| `pi` | 定数 |

## 乱数 — 決定的に動作する設計 { #randomness-deterministic-by-design }

| シグネチャ | 補足 |
|---|---|
| `rand(): num` | `[0, 1)` の一様分布、xorshift64\*。**どのマシンでも同じ系列**になります |
| `srand(seed: num)` | シードを再設定します。再現可能な実行のため、ゲームで 1 回設定してください |

「時刻をシードにする」モードはありません。実行ごとに変化させたい場合は、自分で選んだ
（ログに記録できる）値をシードにしてください。CI のスクリーンショットテストは、この性質に依存しています。

## 環境とテスト { #environment-testing }

| シグネチャ | 補足 |
|---|---|
| `env(name: str): str?` | 環境変数を読み取ります（例: ゲーム独自の自動プレイ切り替え `MYGAME_AUTO`） |
| `check(cond: bool, msg: str)` | 実行時のアサーションです。失敗するとエラー画面に `check failed: msg` を表示します。Wick のテストスイートはこれで構成しています |

## ビットとレジスタ幅（0.3） { #bits-and-register-widths-03 }

`bit_and`、`bit_or`、`bit_xor`、`bit_not`、`bit_shl`、`bit_shr`、`u8`、`u16`、
`hex`、`bin` の正確な入力範囲、ラップ、書式設定の規則は、
[ビット、バイト、ワード](bits.md)を参照してください。
