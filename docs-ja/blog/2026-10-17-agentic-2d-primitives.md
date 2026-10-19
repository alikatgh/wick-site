# エージェント開発のための 2D 描画プリミティブとフレームテレメトリ { #agentic-2d-primitives-and-frame-telemetry }

*2026 年 10 月 17 日 · Lantern 0.8.2 に同梱*

2D アクションゲームの開発や AI エージェントとの協調開発（ペアプログラミング）を進める中で、頻繁に直面する 2 つの課題がありました。

1. **キャラクターアニメーションの接地性**: 待機中の呼吸やしゃがみ、被弾時の反動などでスプライトの描画高さを動的に変化させると、足元が地面から浮いてしまったり、スクリプト側で複雑な UV 計算が必要になります。また、手動でテクスチャを分割すると、サブピクセルの境界でテクスチャの滲みや継ぎ目（シーム）が発生しやすくなります。
2. **自律的な検証の可観測性**: 自動エージェントがゲームシーンをテストしたりグラフィックコードをリファクタリングする際、スクリーンショットの画像ピクセルだけを比較するのは壊れやすく不十分です。エージェントには、エンジンが実際に描画した四角形の境界、使用テクスチャ、色変調、描画順序などの構造化された検証情報が必要です。

Lantern 0.8.2 および Wick では、堅牢な 2D 描画とエージェントによる検証作業に特化したプリミティブとフレームシーンテレメトリを導入しました。

## 接地スプライト分割: `lt.sprite_grounded` { #grounded-sprite-slicing }

新設されたネイティブ呼び出し `lt.sprite_grounded` は、キャラクターセルを基準線（ベースライン）に沿って 2 つの連続した四角形に分割して描画します。

```wick
// Draw character with grounded soles:
// Upper torso stretches or lifts by `lift`, while soles remain planted at `feet`.
lt.sprite_grounded(characterTex, frame, cols, rows, x, feet, w, h, baseline, dir, r, g, b, lift)
```

- **上半身クアッド**: アトラスの `v0` から `soleV` までをカバーし、`(x, feet - baseline - lift)` に配置（高さ `baseline + lift`）。
- **靴底クアッド**: アトラスの `soleV` から `v1` までをカバーし、`(x, feet)` に固定配置（高さ `h - baseline`）。

両方のクアッドは C++ エンジン内で直接スクリーンスペースに整数アライメントされて投入されるため、拡大縮小率にかかわらず境界線に継ぎ目が出ず、呼吸や姿勢変化時にも足元が地面から浮き上がることがありません。

## 滑らかな放射状グロー: `lt.glow_radial` { #smooth-radial-glow }

半透明の長方形を重ねて光を近似する代わりに、`lt.glow_radial` は `(cx, cy)` を中心とする滑らかな減衰を持つクアッドを描画します。

```wick
// Soft ambient campfire illumination
lt.glow_radial(campX, campY, 40, 20, 0.98, 0.54, 0.18, 0.25 * flicker)
```

エンジン内のプロシージャル減衰テクスチャを使用するため、たいまつ、炉、魔法効果などの有機的な光表現が、追加のアセット読み込みやバンディングなしで実現できます。

## 算術組み込み関数: `clamp` と `lerp` { #arithmetic-built-ins }

Wick の標準組み込み関数として、`clamp` と `lerp` が VM レベルで追加されました。

```wick
let boundedSpeed = clamp(velocity, -maxSpeed, maxSpeed)
let smoothedCamera = lerp(cameraX, targetX, 0.1)
```

両関数とも引数の妥当性を厳密に検査し、非有限値（`NaN` や無限大）が渡された場合はコンパイル時または実行時に明確なエラーを報告し、シミュレーションの安定性を担保します。

## 構造化フレームテレメトリ: `LANTERN_FRAME_JSON` { #structured-frame-telemetry }

自律エージェントや CI による検証のために、Lantern は `LANTERN_FRAME_JSON=<path_prefix>` 環境変数をサポートしました。

この設定を有効にすると、指定したフレーム（`LANTERN_SHOT_FRAME`）のレンダリング完了時に、エンジンが描画したシーン全体の詳細な構造化データ `<path_prefix>.json` が出力されます（スキーマ: `lantern.frame-scene.v1`）。

```json
{
  "schema": "lantern.frame-scene.v1",
  "frame": 60,
  "render_width": 400,
  "render_height": 240,
  "draw_count": 84,
  "rect_count": 12,
  "sprite_count": 70,
  "glow_count": 2,
  "font_count": 0,
  "draws": [
    {
      "kind": "sprite",
      "tex": 3,
      "x": 180.0,
      "y": 142.0,
      "w": 64.0,
      "h": 58.0,
      "u0": 0.0,
      "v0": 0.0,
      "u1": 0.125,
      "v1": 0.25,
      "r": 1.0,
      "g": 1.0,
      "b": 1.0,
      "a": 1.0,
      "grounded": true,
      "explicit_alpha": true,
      "tex_path": "assets/hero.bmp"
    }
  ]
}
```

このテレメトリにより、エージェントは以下の項目を自動的かつ高精度に検証できます。
- 画面外へのはみ出しや負の寸法がないか（幾何学的な妥当性）。
- レイヤーごとの描画呼び出し数（`lt.draw_count()` と実際の描画数の一致）。
- キャラクター描画における接地フラグ（`grounded: true`）。
- テクスチャのアルファチャンネル有無（`lt.texture_has_alpha()`）。

決定論的な乱数シードやヘッドレススクリーンショットと組み合わせることで、これらの機能は 2D ゲーム開発を最高水準のエージェント指向ワークフローへと引き上げます。
