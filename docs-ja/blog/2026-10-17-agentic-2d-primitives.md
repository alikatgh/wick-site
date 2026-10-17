# Lanternの接地スプライトとフレームテレメトリ { #grounded-sprites-and-frame-telemetry-in-lantern }

*2026年10月17日 · WickとLanternの技術ノート*

小さな描画機能でも、場面の制作と確認を進めやすくできます。Lanternには接地を保つアトラス描画と放射状のグローがあり、Wickには`clamp`と`lerp`があります。選んだフレームで投入された2Dクアッドを、構造化データとして記録することもできます。

## 足元の帯を固定する { #keep-the-lower-band-fixed }

`lt.sprite_grounded`はアトラスの1セルを、隣接する2つのクアッドに分けて描きます。`baseline`は上側の高さを論理画素単位で指定します。`feet`は下側の帯の上端で、その下端は`feet + h - baseline`です。`lift`を変えると、下側の帯を固定したまま上側を上方に伸ばせます。

```wick
// An illustrative draw fragment; soleY is the lower band's top.
lt.sprite_grounded(atlas, pose, 4, 2, x, soleY, 32, 64, 58,
                   1, 1, 1, 1, lift)
```

原画のセル、分割位置、床との位置合わせは制作者が決めます。記録内の接地フラグが表すのは、この描画方法です。衝突判定や、絵の足元と地面が合うかどうかは別に確認します。

## 光と動きの計算を明示する { #shape-light-and-motion-explicitly }

`lt.glow_radial`は柔らかな放射状テクスチャに色を付け、横と縦の半径を指定して描きます。ランプの周りに円形や楕円形の光を置けます。これは2Dの合成効果で、物体による光の遮蔽は計算しません。

Wickの算術関数を使うと、対応する計算を簡潔に書けます。

```wick
let amount = clamp(progress, 0, 1)
let radius = lerp(12, 24, amount)
lt.glow_radial(lampX, lampY, radius, 10, 1, 0.6, 0.2, 0.25)
```

`clamp`は上下限が逆順でも扱います。`lerp`は`a + (b - a) * t`を計算し、`t`を制限しません。外挿が不要な場合は、明示的に`clamp`を使います。

## 選んだ1フレームを調べる { #inspect-one-selected-frame }

`LANTERN_FRAME_JSON`に出力先の接頭辞を設定し、`LANTERN_SHOT_FRAME`でフレームを選びます。Lanternはそのフレームで`lantern.frame-scene.v1`形式の`<prefix>.json`を出力し、検証用の実行を終了します。記録には2Dクアッドの形状、UV、色、種類、接地フラグ、テクスチャの情報が含まれます。

`lt.draw_count()`は投入された2Dクアッドを数えるため、有効な接地描画では2増えます。`lt.texture_has_alpha()`は明示的なアルファマスクの有無を返し、全画素が不透明でも真になり得ます。どちらも場面全体の物理状態や可視性を表すものではありません。

この記録に加え、描画画像とネイティブ環境での操作も確認します。呼び出し形式は[エンジンAPI](../engine-api.md)と[組み込み関数のリファレンス](../builtins.md)に記載しています。
