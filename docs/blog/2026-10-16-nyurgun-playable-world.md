# Human scale and mouse input in painted 2D scenes

*16 October 2026 · Wick and Lantern engineering notes*

A painted 2D scene uses two sets of measurements: image pixels and logical scene
units. Desktop input has a similar distinction between a button being held and
one fresh press. Keeping these distinctions explicit makes Wick and Lantern
scenes easier to author and test.

## Set scale from the scene

Start with a standing figure in logical units and use its feet as the ground
reference. Compare doorway height, seats, tables and nearby structures against
that figure on the same ground line. A uniform image scale keeps those
relationships consistent across a painting.

Keep the sprite anchor, collision base and painted floor aligned. Texture
density can change while the logical geometry stays fixed. Review the whole
scene: a plausible doorway in an isolated crop can still belong to an oversized
building when the surrounding people and furniture come into view.

## Separate image density from geometry

Image density is the source width divided by the logical draw width. A
1200-pixel painting drawn across 600 logical units has a density of two. A
2400-pixel original can use the same logical width without changing the scene's
geometry.

Retain original RGB and alpha data through the export pipeline. Make every crop,
mask and resampling step explicit. When joining painted bands, check their
widths, floor references and structural lines before choosing the seam. Matching
dimensions alone cannot establish that two timber beams or wall planes meet.

## Show ground contact and support

Align visible feet, sprite anchors and solid ground first, then add a soft shadow
as a contact cue. Keep the shadow bounded around the contact area. Platforms
read clearly when their ledges connect to beams, masonry or rock forms.

Check foreground and background together. A surface can be physically solid yet
look unsupported, and a painted floor can appear walkable while its collision
lies elsewhere. A small fixture with a reference figure and visible collision
guides helps locate that disagreement.

## Turn fresh presses into logical actions

For sampled button state, a rising edge means down now after being up in the
previous sample. An event-driven input layer can latch a press until an update
consumes it, preserving a brief press and release that arrive between updates.
Keep held state separate for continuous input such as dragging.

When a keyboard key and a mouse button share a command, combine their fresh
edges before dispatching it. One logical command should run once even when both
devices produce a press in the same frame. The input routing should also make
clear which scene or overlay consumes that press.

## Verify each boundary

A compact input fixture can exercise press, hold, release and another press, as
well as simultaneous keyboard and mouse input. Keep button numbering and edge
behavior consistent between the native platform and its test adapter.

A saved raster checks the pixels from a particular render. A native window
check exercises the presentation and input path. Record those as separate pieces
of evidence. When a result disagrees with the intended behavior, narrow the
fixture around the relevant boundary: asset pixels, logical geometry, input
sampling or action dispatch.
