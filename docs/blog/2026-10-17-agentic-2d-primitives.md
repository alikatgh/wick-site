# Grounded sprites and frame telemetry in Lantern

*17 October 2026 · Wick and Lantern engineering notes*

Small rendering primitives can make a scene easier to author and inspect.
Lantern provides a grounded atlas draw and a radial glow, while Wick supplies
`clamp` and `lerp`. A selected frame can also produce a structured record of
its submitted 2D quads.

## Keep the lower band fixed

`lt.sprite_grounded` draws an atlas cell as two adjoining quads. `baseline`
sets the upper section's height in logical pixels. `feet` places the top of
the lower band; its bottom is `feet + h - baseline`. Changing `lift` stretches
the upper section upward while keeping that lower band fixed.

```wick
// An illustrative draw fragment; soleY is the lower band's top.
lt.sprite_grounded(atlas, pose, 4, 2, x, soleY, 32, 64, 58,
                   1, 1, 1, 1, lift)
```

The author still chooses the source cell, baseline and floor alignment. A
grounded draw flag describes this rendering operation; collision and painted
ground contact need their own checks.

## Shape light and motion explicitly

`lt.glow_radial` draws a tinted soft radial texture with separate horizontal
and vertical radii. It can form a circular or elliptical glow around a lamp.
This is a blended 2D effect; it does not calculate light occlusion.

Wick's arithmetic helpers keep the corresponding calculations readable:

```wick
let amount = clamp(progress, 0, 1)
let radius = lerp(12, 24, amount)
lt.glow_radial(lampX, lampY, radius, 10, 1, 0.6, 0.2, 0.25)
```

`clamp` accepts reversed bounds. `lerp` computes `a + (b - a) * t` without
clamping `t`; clamp it explicitly when extrapolation is unwanted.

## Inspect one selected frame

Set `LANTERN_FRAME_JSON` to a path prefix and select `LANTERN_SHOT_FRAME`.
Lantern writes `<prefix>.json` with schema `lantern.frame-scene.v1` at that
frame, then ends the verification run. The record contains 2D quad geometry,
UVs, tint, kinds, grounding flags and texture metadata.

`lt.draw_count()` counts submitted 2D quads, so a valid grounded draw adds
two. `lt.texture_has_alpha()` reports an explicit texture alpha mask, even
when every pixel is opaque. Neither reports whole-scene physics or visibility.

Use these records alongside raster captures and native interaction checks.
The [engine API](../engine-api.md) and [built-ins reference](../builtins.md)
describe the callable interfaces.
