# 内部構造と組み込み { #internals-embedding }

言語全体が Lantern リポジトリ内の 3 つのファイルに収まっています。
C++ 標準ライブラリ以外の依存関係はありません。

```
wick/wick.hpp            the embed API (~120 lines)
wick/wick_front.cpp      lexer + one-pass typed compiler → bytecode
wick/wick_vm.cpp         stack VM, GC, built-ins, signature parser
```

## パイプライン { #pipeline }

**AST はありません。** コンパイラは clox 方式の 1 パスです。Pratt 式パーサは、
すべての式について静的な `Type` を保持しながら、その場でバイトコードを出力します。
型検査とコード生成は同じ走査で行います。
これが使用前の宣言を必要とする理由であり、実装を約 2,000 行に保てる理由です。

出力時に型が分かっているため、オペコードは**専用化**されます。`+` は数値の `ADD` または
文字列の `CONCAT` にコンパイルされ、実行時のタグ検査はありません。比較は数値用の操作になり、
ローカル変数はフレームのスロットに解決されます。実行時にアクセスのたびに名前を検索することはありません。
エンジンのネイティブ関数はコンパイル時に整数 ID に解決されます。
VM の `NCALL` は配列の添字アクセスであり、テーブルの走査ではありません。

## VM { #the-vm }

古典的なスタックマシンです。定数プール、スロットでローカル変数を指定する呼び出しフレーム、
約 40 個のオペコードがあります。実行時エラーにはバイトコードと行番号の対応表を持たせ、
エラー画面でソースの位置を示せるようにしています。意図的に **JIT はありません**。
400×240 のゲームロジックにはインタプリタで十分な速度があり、
エンジンは JIT が禁止されるプラットフォームも対象にしています。

## ガベージコレクション { #garbage-collection }

文字列、リスト、マップ、**レコード**に対してマーク＆スイープを行います。ただし、
コレクタが動くのは**ホストが `wick::collect()` を呼んだときだけ**です。Lantern は画面の提示後、
毎フレームちょうど 1 回呼び出します。描画の途中にコレクションが入ることはありません。
最悪の場合の処理量は、1 フレームに生まれるゴミの量で制限されます。
クロージャや upvalue がないため、オブジェクトグラフは浅く保たれます。ルートはグローバル変数、
定数、そしてフレーム間には空になる VM スタックです。

## Wick を自分で組み込む { #embedding-wick-yourself }

```cpp
#include "wick.hpp"

wick::VM* vm = wick::create();
std::string err;

// typed natives: a signature DSL the compiler enforces
wick::addNative(vm, "game", "spawn(num, num, str): num",
    [](wick::VM& vm, const wick::Value* a, int) {
        int id = mySpawn(a[0].d, a[1].d, wick::getStr(a[2]));
        return wick::Value::num(id);
    }, err);
wick::addConst(vm, "game", "MAX", 64);

wick::load(vm, source, "main.wick", err);       // compile + run top level
wick::call(vm, "update", dt, true, err);        // each frame
wick::collect(vm);                              // at YOUR safe point
wick::reset(vm);                                // hot-reload support
```

シグネチャの文法は `name(type[, type][, type = default]) [: type]` です。
型には `num bool str list`、オプショナルには `?` を使います。既定値を指定すると、
末尾の引数を呼び出し側で省略できます。コンパイラが値を補うため、ネイティブ関数には
常にすべての引数が渡されます。ネイティブ関数は `wick::setError(vm, msg)` で失敗を報告します。
VM はそれを、呼び出し箇所の file:line を伴う実行時エラーに変換します。
