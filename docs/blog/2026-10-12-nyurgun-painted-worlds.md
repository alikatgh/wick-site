# Nyurgun: painted worlds, characters and story in Wick

*12 October 2026 · Local development report*

Nyurgun is a story-driven Sakha action-exploration game written in Wick. Its
traversal and combat draw on Castlevania; conversations, inventory and decisions
draw on Ultima. The aim is to bring Sakha literature and visual art into a game
whose people, places and choices carry the story.

The narrative follows the Orosin/Ergis 1947 text. The local working game joins
the five-region Aytaly rescue arc of chapters IV–V to source-audited episodes
VI, VII and VIII, including the northern departure. These are parts of a much
larger epic. The characters need room to speak and act as people, with their
own relationships and reasons to help, resist or leave.

![Nyurgun development prototype: painted mountain landscape, trees and characters](../assets/nyurgun/opening-development-2026-10-12.png)

*Development prototype captured through the real Wick VM and Lantern software
renderer with headless presentation. This is not native-window validation;
the art remains unfinished.*

## Paint that survives the renderer

The visual target is the selected painted Yakut epic illustration style:
expressive faces, detailed clothing and metalwork, and landscapes with depth.
The current game remains below that target. Clearer Unicode text, layered
parallax, a regional map, character portraits and action poses are steps toward
making the scenes readable and the people distinct.

The renderer keeps gameplay coordinates at 400×240 while bounding
physical density to 1–4. The native launcher configuration defaults to 2,
giving an 800×480 framebuffer. More pixels preserve available painted detail;
they do not change movement or level geometry.

The art pipeline now distinguishes explicit BMP V4 alpha from the older
magenta colour-key format. Alpha-weighted bilinear filtering retains soft
painted edges, while opaque-pixel arithmetic remains compatible. Export checks
preserve 714,269 partially transparent pixels across 15 alpha atlases.

The world tree comes from a retained, project-generated props painting. An exact
224×224 source crop was copied unchanged into a padded 256×256 atlas cell at
four times the previous atlas density. Its original detail was preserved
exactly; nothing was enlarged or invented. A faint fringe already present in
the source remains a visual review item.

The painted-alpha renderer is now merged into Lantern's main source through
[upstream pull request #2](https://github.com/alikatgh/lantern/pull/2).
The public Lantern download remains 0.8.0.

## Recovering character detail

Eight portrait cells and four preparation poses now recover detail from the
original retained project-generated paintings at four times their previous
atlas density. Character identity, framing and root anchors are preserved.
This increment adds no new artwork or animation.

![Nyurgun character detail comparison: old atlas on the left, recovered detail on the right](../assets/nyurgun/character-detail-comparison-2026-10-12.png)

*Old atlas on the left, recovered detail on the right. Both use the production
draw path from the same fixed headless state after two frames at physical
density 4. Faces and armour details are clearer; native presentation and final
visual quality remain unreviewed.*

## A game that makes the tools answerable

The rescue and later episodes exercise dialogue, inventory, progression,
interaction prompts and saving. The departure adds a paired catch and recovery
sequence followed by four armament poses. Targeted checks run the real Wick
compiler, VM and renderer, rather than substituting game logic in a test mock.

## An agent-facing compiler check

Lantern source now provides `lantern check --json game` for agents and other
tools. It runs the real Wick compiler with the same Lantern API signatures,
without opening a window or executing top-level game code or native calls.
[The compiler-check change](https://github.com/alikatgh/lantern/pull/3) returns
a single structured JSON result with diagnostics. Source input is
capped at 8 MiB and nesting depth at 256; a constant pool that exceeds its
16-bit index range is rejected rather than allowed to wrap.

This is one step toward tools an agent can use directly. Deterministic headless
scripting, runtime-state inspection and runtime instruction budgets remain
future work.

Sakha is the game's language foundation. English and Russian are the immediate
editing focus, while Sakha wording awaits review by a fluent speaker. Native
presentation, the full campaign and cultural accuracy still need review.
This report records implemented engine and game work and the quality we are working
toward, with further character animation and painted-art refinement ahead.
