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

The legacy calls remain available:

| Call | Notes |
|---|---|
| `lt.load_sound(path: str): num` | WAV sound ID; explicit load failure raises an error |
| `lt.play(sound, volume=1, loop=0): num` | channel 0–15, or −1 if unavailable |
| `lt.stop(channel)` · `lt.volume(v)` | legacy channel stop and master volume |

The following calls are in [Lantern main source](https://github.com/alikatgh/lantern/pull/4),
not the public 0.8.0 binaries. Build current source to use them.

| Call | Result and behavior |
|---|---|
| `lt.try_load_sound(path: str): num` | sound ID, or −1 for missing, invalid or over-budget WAV; sandbox violations still raise an error |
| `lt.sound_unload(sound): bool` | releases unused decoded data; refuses active or paused users |
| `lt.voice_play(sound, bus=0, volume=1, loop=0, fade_seconds=0): num` | stable positive voice handle, or −1; linear initial fade |
| `lt.voice_stop(voice, fade_seconds=0): bool` | immediate stop or linear fade to silence |
| `lt.voice_pause(voice, paused=1): bool` | 1 pauses, 0 resumes; freezes sample position and voice fade |
| `lt.voice_active(voice): bool` | includes paused and fading voices; false after completion or stop |
| `lt.music(sound, volume=1, loop=1, crossfade_seconds=0.5): num` | stable voice handle, or −1; replaces new music-bus voices with equal-power crossfades |
| `lt.bus_volume(bus, volume, ramp_seconds=0): bool` | independent linear bus-gain ramp |
| `lt.ducking(music_level, attack_seconds=0.08, release_seconds=0.3): bool` | music attenuation while speech contributes audible samples; level 1 disables attenuation |

Buses are `lt.SFX=0`, `lt.MUSIC=1` and `lt.SPEECH=2`. For the new calls, loop
and pause flags are **numeric 0 or 1**, gains are finite 0..1, and times are
finite 0..60 seconds.
All old and new voices share 16 slots. Stable voice handles are never reused;
keep them separate from legacy channel IDs. Legacy playback bypasses the new
buses and speech ducking. A paused voice retains its slot and sound.

```wick
let line = lt.try_load_sound("audio/dialogue/arrival.wav")
let speaking = -1
lt.ducking(0.3, 0.08, 0.3)
if line >= 0 { speaking = lt.voice_play(line, lt.SPEECH) }
// On skip or dialogue close, stop before unloading the sound.
if lt.voice_active(speaking) { lt.voice_stop(speaking) }
if line >= 0 { lt.sound_unload(line) }
```

Playback uses the mixer sample clock. The callback performs no file access,
allocation or asset deallocation. Invalid assets, a full pool or an unavailable
device make `lt.music` return −1 and leave existing music unchanged.
WAV input supports PCM 8/16/24/32 and IEEE float32, mono/stereo, 8–192 kHz,
resampled to 48 kHz stereo. Limits are 64 MiB encoded and decoded per sound,
128 MiB decoded in total and 256 loaded sounds. Streaming and compressed codecs
are not implemented. See [the full audio contract](https://github.com/alikatgh/lantern/blob/main/docs/WICK.md#native-audio-buses-and-stable-voices).

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

## Paths & package mode

Every `load_*` path is **relative to the game directory** and sandboxed:

- no absolute paths (`/…`)
- no `..` segments
- no leading-dot segments
- nested names like `assets/tileset.bmp` are allowed

`lt.screenshot` in **package mode** (running a `.lant`) may only write a
safe basename under the extract directory. See the blog post
[Store safety is a language property](blog/2026-07-14-store-safety.md).
