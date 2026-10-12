# Nyurgun: painted worlds, characters and story in Wick

*12 October 2026 · Local development report*

Nyurgun is a story-driven Sakha action-exploration game written in Wick. Its
traversal and combat draw on Castlevania; conversations, inventory and decisions
draw on Ultima. The aim is to bring Sakha literature and visual art into a game
whose people, places and choices carry the story. The production vision is a
fully AI-authored game held to the craft expected of human-made work: coherent
art direction, distinct characters, purposeful animation and carefully edited
story and sound.

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

## Recovering main-character poses

All 32 main-character poses now recover twice their previous atlas detail from
the original R4 and roll paintings. The 2048×512 texture retains the same logical
grid, foot roots, frame IDs and timing. Every source scale stays below one.
Historical crop losses and ownership exclusions remain recorded; this is source
recovery, not anatomy repair or additional animation.

![Idle pose: old atlas on the left, recovered source detail on the right](../assets/nyurgun/hero-idle-detail-comparison-2026-10-12.png)

![Walking pose: old atlas on the left, recovered source detail on the right](../assets/nyurgun/hero-walk-detail-comparison-2026-10-12.png)

*Actual production-draw comparisons at physical density 2, with unchanged
framing. These fixed poses do not establish native animation quality.*

Independent checks reconstruct the earlier atlases exactly, compare all
4,194,304 RGBA channels per export, and reject 35 importer mutations. Sixteen
renderer comparisons cover eight pose classes in both directions; every
shifted-root control is rejected. Fresh independent review and a primary
renderer rerun pass. [The source/art update is merged into main](https://github.com/alikatgh/nyurgun/pull/8).
The preserved 0.4.5 app predates it; native and overall visual approval remain open.

## Recovering painted sword and whip poses

Chapter VI now retains twice the previous atlas detail in its sword and sacred-whip
poses. Fifteen original painted poses supply sixteen 512×192 physical cells;
the logical canvas, foot roots, frame indices and animation timing stay the same.
The new atlas is recovered from the original generated paintings at scales below
one, without enlarging the old packed sheet.

![Sword pose: old atlas on the left, recovered source detail on the right](../assets/nyurgun/sword-detail-comparison-2026-10-12.png)

![Sacred-whip pose: old atlas on the left, recovered source detail on the right](../assets/nyurgun/whip-detail-comparison-2026-10-12.png)

*These fixed-state comparisons use the actual game draw path at physical density 2.
They show recovered detail, not an approved animation or native play session.*

Exact source reconstruction checks all 6,291,456 atlas RGBA channels. Twenty-one
importer rejection controls, eight renderer comparisons and eight shifted-root
controls pass. Fresh independent review found no defects.
[The source/art change is merged into main](https://github.com/alikatgh/nyurgun/pull/7).
The preserved 0.4.5 app predates it; overall character quality still needs work.

## Recovering the painted worlds

All ten panoramas now retain exact crops from the original project-generated
paintings, instead of being reduced to 800×240 during import. Their textures
are 960×288, 1320×396 or 1600×480. Every crop keeps its original RGB pixels;
the old exports were not enlarged. Logical framing, camera motion, terrain
and character positions remain unchanged.

Independent checks compare 5,469,600 source pixels and preserve every original
and non-world export. The selected inputs total 13,033,476 bytes within the
unchanged 30 MiB bound. Old/new scenes were compared through the real renderer
at physical density 2, with actors, interface and both camera-pan endpoints.
This recovers visible brushwork and cliff detail. Further character animation,
world composition and native presentation still need work.

## A continuous fresh-save campaign

The implemented rescue → VI → VII → VIII route now passes in one continuous
11,934-frame run from empty private saves. Ordinary keyboard inputs drive the
unchanged Wick controllers, combat and traversal; all four chapters write their
normal saves with no save warnings. The verifier checks canonical assembled
source, contiguous chapter order and sixteen required scene captures.

This is headless gameplay evidence using the real VM, renderer and audio mixer
with synthetic OS input, presentation and audio output. It does not establish
native play or an adaptation of the whole epic.

The new local 0.4.5 review app packages Lantern main's audio and compiler checks
with the recovered worlds. It passed exact resource, ARM64/macOS 15, signature
and extracted-archive verification. Runtime preparation rebuilds 37 hash-verified
source inputs before probing the typed audio API. Older apps remain preserved.
An automated launch attempt stopped during macOS application registration,
before Wick/game initialization. Successful native play remains unverified;
this is not a public executable release.

## A game that makes the tools answerable

The rescue and later episodes exercise dialogue, inventory, progression,
interaction prompts and saving. The departure adds a paired catch and recovery
sequence followed by four armament poses. Targeted checks run the real Wick
compiler, VM and renderer, rather than substituting game logic in a test mock.

A later Chapter VI source repair gives Nyurgun's hurt and death poses priority
when a sword or whip swing was active. Twenty-four painted fixture cases cover
both directions, held death, ordinary retry and attacks during later invulnerability.
The same regression rejects the earlier source, and the final assembled campaign
again passes from empty saves in 11,934 frames. These are headless checks; the
preserved 0.4.5 app predates this repair.

## Voices and music belong to the game

[Native audio is now merged into Lantern main](https://github.com/alikatgh/lantern/pull/4).
Wick can address sound effects, music and speech separately, keep stable voice
handles, pause a line, fade it out and crossfade music on the mixer sample clock.
Audible speech can lower the music and release it after the line ends. The
callback performs no file access, allocation or asset deallocation.

Nyurgun's source now routes dialogue by its exact subtitle key, character and
selected language. Advancing or skipping a line retires the old voice; pause and
journal screens suspend playback, and a language change cancels the previous
language. The audio controller also follows the later cinematic sequences and
scene music. Missing optional recordings leave text and progression available.

[VoiceStudio](https://github.com/debpalash/VoiceStudio) is the required voice
production tool, and [YuE](https://github.com/multimodal-art-projection/YuE) is the
required music tool. The production plan covers eight character and narrator
directions, 219 speech entries across Sakha, Russian and English, and seven music
cues. These are plans, not finished performances. Versioned command-line adapters
prepare bounded, inspectable jobs and provenance records; they do not install
models, start inference or silently substitute another generator. The initial
music contract pins the original YuE-v1 source and models separately from YuE2.

Recordings must pass listening, editorial, cultural and rights review before the
asset manifest admits them. Packaging checks the approved file hashes, current
subtitles and generated loaders, and rejects a runtime without the native audio
capability. No approved AI voice or music takes are bundled yet. The public
Lantern 0.8.0 download and retained Nyurgun review apps remain unchanged.

The real engine tests passed 594 assertions and all 12 CTest targets. Nyurgun's
source passed 22 audio integration assertions, 154 episode-entry cases and a
5,425-frame production self-play run. These checks use synthetic audio or
headless presentation; hardware playback, listening quality and final character
performances remain unverified. WAVs are decoded into bounded memory;
streaming and compressed codecs remain future work.

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
presentation, native campaign play and cultural accuracy still need review.
This report records implemented engine and game work and the quality we are working
toward, with further character animation and painted-art refinement ahead.
