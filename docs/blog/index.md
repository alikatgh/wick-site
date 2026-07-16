# The wick blog

Design notes, release posts, and evidence for language decisions — the same
role the [Go blog](https://go.dev/blog/) plays for Go: not marketing fluff,
but a durable public record of *why* the language looks the way it does.

wick grows only when a real game pays for a feature. The posts below are
that history.

## Posts

| Date | Title |
|---|---|
| 2026-07-14 | [wick 0.2 — Release notes](2026-07-14-release-0.2.md) |
| 2026-07-14 | [Admitting records](2026-07-14-admitting-records.md) |
| 2026-07-14 | [Store safety is a language property](2026-07-14-store-safety.md) |
| 2026-07-14 | [How we test a tiny language](2026-07-14-how-we-test.md) |
| 2026-07-14 | [Why optionals (a real crash)](2026-07-14-why-optionals.md) |
| 2026-07-14 | [Welcome to the wick blog](2026-07-14-welcome.md) |

## Also read

- [Language overview](../index.md)
- [Feature ledger / limits](../limits.md)
- Engine [CHANGELOG](https://github.com/alikatgh/lantern/blob/main/CHANGELOG.md)
- Engine [WICK.md](https://github.com/alikatgh/lantern/blob/main/docs/WICK.md) (in-repo source of truth)

## How to propose a language change

1. Show **code that hurts** in a shipped or in-progress lantern game.
2. Show that a static workaround (bake offline, parallel lists, etc.) is
   no longer clean.
3. Propose the smallest surface that removes the pain — not “feature parity
   with X.”
4. If admitted, land **language + tests + docs + this blog** in one change.

That is the whole process. There is no roadmap committee.
