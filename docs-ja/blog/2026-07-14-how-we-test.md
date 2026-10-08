# 小さな言語をどうテストするか { #how-we-test-a-tiny-language }

*2026-07-14*

Wick は小さな言語です。テストスイートが小さくてもよいのは、**容赦なく厳しい**場合だけです。
見せかけのカバレッジは測りません。言語が防ぐと約束した種類のバグを測ります。

## 3 つの層 { #three-layers }

### 1. 意味論（実行できること） { #1-semantics-must-run }

一時的な `main.wick` に `check(condition, "label")` のアサーションを詰め込みます。
算術演算、真偽値の短絡評価、オプショナル、リスト、マップ、`rand`/`srand` の決定性、
そして今回加わった**レコード**（構築、フィールドの取得と設定、レコードのリスト）を検査します。

ヘッドレスで実行します。

```sh
LANTERN_FIXED_DT=1 LANTERN_SHOT=... LANTERN_SHOT_FRAME=1 ./build/lantern game/
```

### 2. コンパイルが必ず失敗すること（実行*できない*こと） { #2-must-fail-to-compile-must-not-run }

Wick の要点は、**存在してはいけない**プログラムにあります。各ケースは小さなゲームで、
非ゼロの終了コードで終了し、既知の部分文字列を出力しなければなりません。

| ケース | 部分文字列 |
|---|---|
| 未処理の `str?` を `lt.print` に渡す | `str?` |
| `if 1` | `must be bool` |
| 未宣言の名前へ代入する | `no implicit globals` |
| `"score " + 5` | `str(x)` |
| ネイティブ関数の型 / 引数の個数が不正 | `argument` / `at least` |
| `let x = nil` | `annotate` |
| 未知のレコードフィールド | `unknown field` |
| レコードフィールドの型の不一致 | `field` |

失敗すべきケースがコンパイルできるようになったら、スイートを失敗させます。
これが基本方針に対する回帰テストです。

### 3. 実際のゲーム（描画できること） { #3-real-games-must-paint }

- **Lantern Night（Wick）**は、`SHOWCASE_AUTO` の設定で N フレーム自動プレイします。
- **パッケージの往復**: showcase_wick をパッケージ化し、フォルダ版と `.lant` 版を実行して、
  `cmp` でフレームバッファを比較します。1 バイトを破損させ、CRC 検査で拒否されることを確認します。
- **パスのサンドボックス**: `../` と `/etc/...` を試す Wick のテスト用コードを使います。
- **KORA のキッチン**: `KORA_SCENE=3` のフレームは、比較対象のタイトル画面の画像と
  異なっていなければなりません。

## 行わないこと { #what-we-do-not-do }

- テストハーネス内にコンパイラを再実装し、それを相手に検証すること。
- 巨大な AST をゴールデンマスターとして比較すること。
- ゲームが遅くなる前に、見せかけのベンチマークを行うこと。

## 実行する { #run-it }

```sh
cd lantern
cmake --build build -j
bash tests/wick_test.sh ./build/lantern
bash tests/path_sandbox_test.sh ./build/lantern
bash tests/package_test.sh ./build/lantern ./build/lantern_pack .
```

言語を変更したら、コンパイルが失敗すべきケースか意味論の検査を**同じコミットに**追加してください。
バグ記録と同じ規則です。
