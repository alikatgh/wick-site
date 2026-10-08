# Wick { #wick }

**Lantern 0.8.0** に同梱されている **Wick 0.3** の言語リファレンスです。
Wick はバイトコードにコンパイルされ、Lantern がゲームループと `lt.*` エンジン API を提供します。

## はじめに { #where-to-start }

- **プログラムを実行する:** [入門](getting-started.md)では、インストール、完全なサンプル、保存時の再読み込みを説明します。
- **順を追って学ぶ:** [The Wick Book](https://wick.aulenor.com/ja/book/)では、ゲーム開発を通して言語を学べます。
- **ホストを選ぶ:** [Lantern](https://wick.aulenor.com/ja/lantern/)には、ダウンロード、ビルド、サンプル、プラットフォームの対応状況をまとめています。
- **不具合を直す:** [コンパイルエラーと実行時エラー](errors.md)には、メッセージ、原因、修正方法をまとめています。

## 言語の項目を探す { #language-lookup }

| やりたいこと | リファレンス |
|---|---|
| 変数、分岐、ループを宣言する | [構文](syntax.md) |
| 値が存在しない場合に対処する | [型、オプショナル、型の絞り込み](types.md) |
| 名前付きフィールドを定義する | [レコード](records.md) |
| 値を格納する、または順に処理する | [リストとマップ](collections.md) |
| 関数を宣言する、または呼び出す | [関数](functions.md) |
| 値を変換、書式設定、検証する | [組み込み関数](builtins.md) |
| ビットをマスクし、レジスタをラップし、16 進数を表示する | [ビット、バイト、ワード](bits.md) |
| 描画、入力の読み取り、音声の再生、保存を行う | [エンジン API — `lt.*`](engine-api.md) |

検索には `u8`、`bit_shr`、`lt.rect` などの関数名や、診断メッセージに含まれる語句を使えます。
検索結果から、該当するリファレンスの節へ移動できます。

## よく参照する項目 { #common-lookups }

- [`u8` と `u16`: 明示的なラップ](bits.md#explicit-register-widths)
- [`bit_and`、`bit_or`、`bit_xor`、`bit_not`、`bit_shl`、`bit_shr`](bits.md#bit-operations)
- [`hex` と `bin`: 書式設定](bits.md#display)
- [`lt.rect`、スプライト、テキスト](engine-api.md#2d)
- [入力とセーブデータ](engine-api.md#input-saves)
- [対応機能と現在の制限](limits.md)

## 新しい言語を作った理由 { #why-a-new-language }

Wick は静的型、明示的な `T?` オプショナル、変数宣言、真偽値の条件式を採用しています。
ゲームの読み込み時には、エンジン呼び出しの引数の型と個数を検査します。
ランタイムはバイトコード VM を使い、フレーム間でガベージコレクションを行います。

具体的な違いは [Wick と Lua](comparison.md)を参照してください。実装の詳細は
[内部構造と組み込み](internals.md)、または
[コンパイラと VM のソース](https://github.com/alikatgh/lantern/tree/v0.8.0/wick)を参照してください。

## 0.3 の新機能 { #new-in-03 }

[ビット、バイト、ワード](bits.md)では、検査付きのビット演算、16 進数・2 進数リテラル、
レジスタのラップ、表示関数を追加しました。`u8` と `u16` は新しい型ではなく関数です。
通常の `num` の算術演算が自動的にラップすることはありません。

追加された 10 個の組み込み関数名は予約されています。互換性の詳細は
[リリースノート](blog/2026-10-06-release-0.3.md)、対応するエンジンのリリースは
[変更履歴](https://github.com/alikatgh/lantern/blob/v0.8.0/CHANGELOG.md)を参照してください。
