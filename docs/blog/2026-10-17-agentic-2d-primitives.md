# Purpose-built 2D primitives and frame telemetry for agentic development

*17 October 2026 · Ships with Lantern 0.8.2*

When building 2D action games and pair-programming with AI agents, two friction
points frequently recur:

1. **Character animation grounding**: Dynamic vertical offsets (idle breathing,
   crouching, impact recovery) that shift a sprite quad either lift the feet
   off the floor or require complex manual UV math. Slicing textures manually in
   script often introduces single-pixel sampling seams or texture bleeding.
2. **Autonomous verification visibility**: When an automated agent tests a scene
   or refactors visual code, checking raw screenshot pixels alone is brittle.
   The agent needs structured, verifiable insight into what the engine actually
   drew: quad bounds, textures, color modulations, and draw counts.

Lantern 0.8.2 and Wick introduce purpose-built primitives and frame scene telemetry
designed specifically for robust 2D rendering and agentic testability.

## Grounded sprite slicing: `lt.sprite_grounded`

The new native call `lt.sprite_grounded` splits a character cell into two
contiguous quads along an integer baseline:

```wick
// Draw character with grounded soles:
// Upper torso stretches or lifts by `lift`, while soles remain planted at `feet`.
lt.sprite_grounded(characterTex, frame, cols, rows, x, feet, w, h, baseline, dir, r, g, b, lift)
```

- **Torso Quad**: Spans from `v0` to `soleV` on the atlas, placed at `(x, feet - baseline - lift)`
  with height `baseline + lift`.
- **Sole Quad**: Spans from `soleV` to `v1`, placed firmly at `(x, feet)` with height `h - baseline`.

Because both quads are submitted in integer screen space directly by the C++ engine,
the boundary stays seamless across all scaling factors, and soles never float
above ground geometry during breathing or stance transitions.

## Smooth radial glow: `lt.glow_radial`

Instead of approximating ambient light with nested transparent rectangles, `lt.glow_radial`
renders a smooth quadratic falloff quad centered at `(cx, cy)`:

```wick
// Soft ambient campfire illumination
lt.glow_radial(campX, campY, 40, 20, 0.98, 0.54, 0.18, 0.25 * flicker)
```

The engine applies procedural radial falloff, giving organic lighting around
torches, hearths, and magic effects without asset overhead or banded stepping.

## Arithmetic built-ins: `clamp` and `lerp`

Wick now includes `clamp` and `lerp` as standard arithmetic built-ins in the VM:

```wick
let boundedSpeed = clamp(velocity, -maxSpeed, maxSpeed)
let smoothedCamera = lerp(cameraX, targetX, 0.1)
```

Both built-ins validate their operands and throw clear compile or runtime errors
on non-finite values (`NaN` or infinity), ensuring simulation stability.

## Structured frame telemetry: `LANTERN_FRAME_JSON`

For autonomous agents and continuous integration, Lantern now supports
`LANTERN_FRAME_JSON=<path_prefix>`.

When enabled, Lantern outputs a detailed scene description `<path_prefix>.json`
upon reaching `LANTERN_SHOT_FRAME`. Conforming to the `lantern.frame-scene.v1`
schema, the record provides:

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

This telemetry enables agents to verify:
- Exact geometry bounds (preventing out-of-screen drift or negative dimensions).
- Proper layer draw counts (`lt.draw_count()` matches batch submission).
- Grounded flags on character poses.
- Alpha channel detection (`lt.texture_has_alpha()`).

Combined with deterministic random seeds and headless screenshot capture,
these features elevate 2D development into a first-class agentic engineering workflow.
