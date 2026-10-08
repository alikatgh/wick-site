# エンジン API — `lt.*` { #the-engine-api-lt }

Lantern の各呼び出しには、**コンパイラが検査する型付きシグネチャ**が登録されています。
引数の個数や型が誤っている場合は、呼び出し名と引数番号を示すコンパイルエラーになります。
省略可能な引数には既定値を記載しています。
ハンドル（メッシュ、テクスチャ、音声）の型は `num` です。

## フレームと画面 { #frame-screen }

| 呼び出し | 補足 |
|---|---|
| `lt.W` · `lt.H` | コンパイル時定数: 400、240 |
| `lt.clear(r, g, b)` | 色と深度をクリアします。`draw()` の最初に呼び出してください |
| `lt.time(): num` | 起動後の秒数（`LANTERN_FIXED_DT` 指定時は固定ステップ） |
| `lt.screenshot(path: str)` | 400×240 のフレームを BMP として保存します |
| `lt.quit()` | 正常終了を要求します |
| `lt.escape_quits(enable: bool)` | 既定では Escape で終了します。ポーズメニュー用には無効にできます |

## 3D シーン { #3d-scene }

| 呼び出し | 補足 |
|---|---|
| `lt.camera(ex,ey,ez, tx,ty,tz, fov=55)` | 位置と注視点 |
| `lt.light(dx,dy,dz, ambient=0.35)` | 平行光源 |
| `lt.point_light(i, x,y,z, radius, r=1,g=1,b=1)` | スロット 0〜3。`radius <= 0` で無効 |
| `lt.fog(start, end, r,g,b)` | 視点からの深度に対して線形。`end <= start` で無効 |

## メッシュ { #meshes }

| 呼び出し | 補足 |
|---|---|
| `lt.cube(): num` | 単位立方体 |
| `lt.plane(segs=1): num` | 分割された単位 XZ 平面 |
| `lt.sphere(seg=12)` · `lt.cylinder(seg=16)` · `lt.cone(seg=16)` | 単位サイズの基本形状 |
| `lt.mesh(verts: list<num>): num` | カスタムメッシュ。頂点ごとに 12 個の浮動小数点数: pos3 normal3 uv2 rgba4 |
| `lt.load_mesh(path: str): num` | Wavefront OBJ（法線がなければ面法線を使用） |
| `lt.draw(m, x,y,z, rx=0,ry=0,rz=0, sx=1,sy=1,sz=1, r=1,g=1,b=1, tex=-1)` | グーローシェーディングで描画 |
| `lt.draw_lerp(a, b, t, x,y,z, ...same..., tex=-1)` | 頂点数が同じ 2 つのメッシュ間のキーフレーム補間 |
| `lt.billboard(tex, x,y,z, w,h, u0=0,v0=0,u1=1,v1=1)` | カメラに向く四角形（スプライトのキャラクター） |
| `lt.shadow(x,y,z, radius, alpha=0.35)` | 接地感を出す丸い影（床の高さに小さなイプシロンを足して渡す） |

## 2D { #2d }

| 呼び出し | 補足 |
|---|---|
| `lt.rect(x,y,w,h, r,g,b, a=1)` | 塗りつぶし、アルファブレンド |
| `lt.load_texture(path: str): num` | BMP。マゼンタ（255,0,255）は透明 |
| `lt.sprite(tex, x,y, sx=1,sy=1)` | 左上を基準に配置 |
| `lt.sprite_ex(tex, cx,cy, sx=1,sy=1, rot=0, r=1,g=1,b=1,a=1)` | 中心、回転、色付け。負の倍率で反転 |
| `lt.sprite_uv(tex, x,y,w,h, u0,v0,u1,v1)` | アトラス内の部分矩形（タイルマップ） |
| `lt.print(text: str, x,y, r=1,g=1,b=1,a=1)` | 内蔵 8×8 フォント。`\n` に対応 |

## 音声 { #audio }

| 呼び出し | 補足 |
|---|---|
| `lt.load_sound(path: str): num` | WAV |
| `lt.play(sound, volume=1, loop=0): num` | チャンネルを返します。16 個すべてが使用中なら −1 |
| `lt.stop(channel)` · `lt.volume(v)` | |

## 入力と保存 { #input-saves }

| 呼び出し | 補足 |
|---|---|
| `lt.key(name: str): bool` | 押されている状態。キーボードとゲームパッドを統合 |
| `lt.pressed(name: str): bool` | このフレームで押されたか |
| `lt.gamepad(): bool` · `lt.rumble(low, high, ms)` | |
| `lt.touch_down(): bool` | 現在画面に触れているか（デスクトップではマウスの左ボタン） |
| `lt.touch_pressed(): bool` | このフレームでタッチが始まったか。状態を保持するので、フレームより短いタップも 1 回検出 |
| `lt.touch_x(): num` · `lt.touch_y(): num` | 400×240 の画面座標。レターボックスの余白を除いて範囲内に制限。離した後も最後の位置を保持 |
| `lt.save(name: str, data: str): bool` | バイナリデータにも安全 |
| `lt.load_save(name: str): str?` | **オプショナル**。読み取れなければ `nil` |

入力名: `left right up down z x c space return escape a s d w`
（ゲームパッド: 十字キー・スティック → 方向、A→`z`、B→`x`、Y→`c`、Start→`return`）。
タッチは 3DS のような単一の点で、意図的にマルチタッチにはしていません。
iPhone/iPad では実際のタッチスクリーンを使い、デスクトップではマウスの左ボタンが指の代わりになります。

## パスとパッケージモード { #paths-package-mode }

すべての `load_*` のパスは**ゲームディレクトリからの相対パス**で、サンドボックス化されています。

- 絶対パス（`/…`）は使えません
- `..` を含むパス要素は使えません
- ドットで始まるパス要素は使えません
- `assets/tileset.bmp` のような階層のある名前は使えます

**パッケージモード**（`.lant` の実行）では、`lt.screenshot` は展開先ディレクトリの下に
安全なベース名でのみ書き込めます。ブログ記事
[ストアの安全性は言語の性質](blog/2026-07-14-store-safety.md)を参照してください。
