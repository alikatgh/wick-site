# The engine API — `lt.*`

Every lantern call is registered with a **typed signature the compiler
checks**: wrong arity or a wrong argument type is a compile error with the
call name and argument number. Optional parameters show their defaults.
Handles (meshes, textures, sounds) are `num`.

## Frame & screen

| Call | Notes |
|---|---|
| `lt.W` · `lt.H` | compile-time constants: 400, 240 |
| `lt.clear(r, g, b)` | clear color and depth; call first in `draw()` |
| `lt.time(): num` | seconds since boot (fixed-step under `LANTERN_FIXED_DT`) |
| `lt.screenshot(path: str)` | save the 400×240 frame as BMP |
| `lt.quit()` | request a clean exit |
| `lt.escape_quits(enable: bool)` | Escape quits by default; disable for pause menus |

## 3D scene

| Call | Notes |
|---|---|
| `lt.camera(ex,ey,ez, tx,ty,tz, fov=55)` | position + look-at |
| `lt.light(dx,dy,dz, ambient=0.35)` | the directional light |
| `lt.point_light(i, x,y,z, radius, r=1,g=1,b=1)` | slots 0–3; `radius <= 0` = off |
| `lt.fog(start, end, r,g,b)` | linear by view depth; `end <= start` disables |

## Meshes

| Call | Notes |
|---|---|
| `lt.cube(): num` | unit cube |
| `lt.plane(segs=1): num` | unit XZ plane, tessellated |
| `lt.sphere(seg=12)` · `lt.cylinder(seg=16)` · `lt.cone(seg=16)` | unit primitives |
| `lt.mesh(verts: list<num>): num` | custom mesh, 12 floats/vertex: pos3 normal3 uv2 rgba4 |
| `lt.load_mesh(path: str): num` | Wavefront OBJ (flat-normal fallback) |
| `lt.draw(m, x,y,z, rx=0,ry=0,rz=0, sx=1,sy=1,sz=1, r=1,g=1,b=1, tex=-1)` | gouraud-lit draw |
| `lt.draw_lerp(a, b, t, x,y,z, ...same..., tex=-1)` | keyframe tween between two same-count meshes |
| `lt.billboard(tex, x,y,z, w,h, u0=0,v0=0,u1=1,v1=1)` | camera-facing quad (sprite characters) |
| `lt.shadow(x,y,z, radius, alpha=0.35)` | grounding blob (pass floor height + small epsilon) |

## 2D

| Call | Notes |
|---|---|
| `lt.rect(x,y,w,h, r,g,b, a=1)` | filled, alpha-blended |
| `lt.load_texture(path: str): num` | BMP; magenta (255,0,255) = transparent |
| `lt.sprite(tex, x,y, sx=1,sy=1)` | top-left anchored |
| `lt.sprite_ex(tex, cx,cy, sx=1,sy=1, rot=0, r=1,g=1,b=1,a=1)` | center, rotate, tint; negative scale flips |
| `lt.sprite_uv(tex, x,y,w,h, u0,v0,u1,v1)` | atlas sub-rect (tilemaps) |
| `lt.print(text: str, x,y, r=1,g=1,b=1,a=1)` | built-in 8×8 font, `\n` aware |

## Audio

| Call | Notes |
|---|---|
| `lt.load_sound(path: str): num` | WAV |
| `lt.play(sound, volume=1, loop=0): num` | returns channel, −1 if all 16 busy |
| `lt.stop(channel)` · `lt.volume(v)` | |

## Input & saves

| Call | Notes |
|---|---|
| `lt.key(name: str): bool` | held; keyboard + gamepad merged |
| `lt.pressed(name: str): bool` | went down this frame |
| `lt.gamepad(): bool` · `lt.rumble(low, high, ms)` | |
| `lt.touch_down(): bool` | screen touched now (desktop: left mouse button) |
| `lt.touch_pressed(): bool` | touch began this frame — latched, so a sub-frame tap still fires once |
| `lt.touch_x(): num` · `lt.touch_y(): num` | 400×240 screen coords, letterbox undone, clamped; last position sticks while up |
| `lt.save(name: str, data: str): bool` | binary-safe |
| `lt.load_save(name: str): str?` | **optional** — `nil` when unreadable |

Input names: `left right up down z x c space return escape a s d w`
(pad: d-pad/stick → directions, A→`z`, B→`x`, Y→`c`, Start→`return`).
Touch is a single point, 3DS-style — deliberately not multitouch. On
iPhone/iPad it is the real touchscreen; on desktop the left mouse button
plays the finger.
