# 関数 { #functions }

```wick
fn dist(ax: num, az: num, bx: num, bz: num): num {
  let dx = bx - ax
  let dz = bz - az
  return sqrt(dx * dx + dz * dz)
}
```

- `fn` を使い、**トップレベルでのみ**宣言します（v0.1 にはネストやクロージャがありません）。
- **引数の型は必須です。** 戻り値の型は引数リストの後に `:` を付けて指定します。
  void 関数では省略します。
- **使用する前に宣言します**（C と同じ方式）。関数は最初の呼び出しより前に記述しなければなりません。
  `update`/`draw` はホストが呼び出すため、この 2 つの相対的な位置は問いません。
- 再帰を使えます（`fn fib(k: num): num { ... return fib(k-1) + fib(k-2) }`）。
- 呼び出しを検査します。引数の個数や型が違う場合は、関数名と引数番号を示すコンパイルエラーになります。

## フレームごとの呼び出し規約 { #the-frame-contract }

エンジンは毎フレーム、次の 2 つの関数を名前で探します。

```wick
fn update(dt: num) { }   // simulation; dt in seconds
fn draw() { }            // rendering; 3D calls then 2D composites on top
```

どちらも省略可能です。トップレベルの文は読み込み時に 1 回だけ実行されます。
メッシュの作成、テクスチャと音声の読み込み、状態の初期化はそこで行います。

## 値を返す { #returning-values }

戻り値の型を宣言した関数では、必要な実行経路で `return expr` を実行してください。
void ではない関数の末尾まで到達すると `nil` が返ります
（この動作に依存しないでください。v0.1 では、まだすべての経路での return を強制していません。
[制限](limits.md)を参照してください）。

複数の戻り値はありません。1 つの値を返して別の状態を利用するか、
2 つの関数に分けてください（Kora Night の移植で使う
`nearest_unlit()` + `dist2_to(i)` の組が、その具体例です）。
