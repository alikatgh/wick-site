# 入門 { #getting-started }

**Lantern 0.8.0 / Wick 0.3** で、最初の Wick プログラムを実行しましょう。Wick はエンジンに
同梱されているため、言語を別途インストールする必要はありません。

## エンジンを入手する { #get-the-engine }

**macOS Apple Silicon:** [Lantern のバンドルをダウンロード](https://wick.aulenor.com/ja/lantern/#downloads)して
展開し、そのフォルダでターミナルを開きます。`lantern`、`lantern_pack`、Bit Lab のサンプルが
含まれています。このビルドはアドホック署名されており、Apple の公証は受けていません。

**ソースからビルドする:** [Lantern のビルド手順](https://wick.aulenor.com/ja/lantern/#build-from-source)に従ってください。
以下のコマンドは、ダウンロードしたバンドルを使うことを前提としています。ソースをチェックアウトした場合は、
`./lantern` を `./build/lantern` に、`./lantern_pack` を `./build/lantern_pack` に置き換えてください。

## 最初のプログラムを実行する { #run-your-first-program }

エンジンがあるフォルダから、ゲーム用のディレクトリを作成します。

```sh
mkdir -p games/first-game
```

次の完全なプログラムを `games/first-game/main.wick` として保存してください。
[main.wick をダウンロード](https://wick.aulenor.com/examples/first-game/main.wick)することもできます。

```wick
let x = 0

fn update(dt: num) {
  x = (x + 40 * dt) % 400
}

fn draw() {
  lt.clear(0.1, 0.1, 0.2)
  lt.rect(x, 100, 16, 16, 1, 0.8, 0.2, 1)
}
```

同じターミナルから実行します。

```sh
./lantern games/first-game
```

**表示される結果:** 暗い 400 × 240 の画面上を黄色い正方形が移動します。
x 座標が 400 に達すると左端に戻ります。終了するには Escape を押してください。

ゲームを実行したまま `40` を `80` に変更し、ファイルを保存してください。正方形は最初から動き出し、
速度が 2 倍になります。コンパイルエラーが表示されたら、示された行を修正して再度保存してください。
[コンパイラのメッセージと修正方法](errors.md)では、よくある不具合を説明しています。

## ゲームは 1 つのフォルダ { #a-game-is-a-folder }

`main.wick` がエントリーポイントです。トップレベルの文はゲームの読み込み時に 1 回だけ実行され、
その後、Lantern は `update(dt: num)` と `draw()` があれば呼び出します。
`dt` は経過時間を秒で表し、上限は 0.1 です。描画呼び出しには画面座標またはエンジンの 3D シーンを使います。
各関数のシグネチャは[エンジン API](engine-api.md)を参照してください。

`main.wick` と `main.lua` が両方ある場合、ホストは `main.wick` を優先します。アセットのパスは
ゲームディレクトリからの相対パスで、`assets/tiles.bmp` のような階層のあるパスも使えます。

## 開発の流れ { #the-dev-loop }

- `main.wick` を保存すると、再コンパイルして再読み込みします。再読み込み時にはゲームの状態が初期化されます。
- コンパイルエラーと実行時エラーは、エンジン内に `file:line: message` の形式で表示されます。
- `LANTERN_FIXED_DT=1` を指定すると、固定タイムステップを使って再現可能な実行を行えます。
- フレームバッファを保存して 60 フレーム後に終了するには、`LANTERN_SHOT` に書き込み可能な
  出力先の接頭辞を指定します。たとえば、`LANTERN_SHOT=first-frame ./lantern games/first-game`
  は BMP のスクリーンショットを書き出します。`LANTERN_SHOT_FRAME` で撮影するフレームを変更できます。

## ゲームをパッケージ化する { #package-a-game }

```sh
./lantern_pack games/first-game first-game.lant
./lantern first-game.lant
```

`.lant` ファイルには、ゲームとそのアセットが含まれます。編集用にソースのフォルダを残してください。
[Lantern のパッケージ化ガイド](https://wick.aulenor.com/ja/lantern/#package-a-game)では、
フォルダ構造を説明し、フォーマット仕様へのリンクを掲載しています。

## 2 分で学ぶ構文 { #two-minutes-of-syntax }

```wick
let speed = 120.0            // types are inferred
let name: str = "tenzin"     // ...or written out
let lamps: list<bool> = []   // empty literals need the annotation

record Pt { x: num, y: num }
let p = Pt { x: 1, y: 2 }

for i in 0..4 {              // 0-based, end-exclusive
  push(lamps, true)
}

fn dim(v: num): num {        // parameter types are required
  if v < 0.5 { return 0 }    // conditions must be bool
  return v * 0.5
}

let saved = lt.load_save("hi")   // saved: str?  (an optional!)
let text = saved ?? "no save"    // ?? unwraps with a default
if saved != nil {
  lt.print(saved, 4, 4, 1, 1, 1, 1)  // narrowed to str inside the block
}
```

次に読む: [構文](syntax.md) · [型とオプショナル](types.md) · [レコード](records.md) · [ブログ](blog/index.md)
