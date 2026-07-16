# Store safety is a language property

*2026-07-14*

The lantern store ships games as `.lant` packages. The pitch is simple:

> The worst a store game can do is render rude pixels.

That sentence is only true if the **language + host** make it true. This
post is what we closed so the sentence is not aspirational.

## wick-only packages

`lantern_pack` refuses folders without `main.wick`. Lua ships `os` and
`io` — fine for local development, not for strangers' code. wick's only
exits are typed `lt.*` natives registered by the host. There is no open
file API, no shell, no sockets in the language.

That is necessary and not sufficient.

## Path sandbox

Until this release, loads did:

```text
path = gameDir + "/" + userString
```

A wick program could pass `../` or an absolute path and read outside the
game folder (and, with `lt.screenshot`, write outside it).

Now every load (`load_texture`, `load_mesh`, `load_sound`) — wick and Lua —
goes through `pathResolveUnder`:

- no absolute paths
- no `..` segments
- no hidden (leading-dot) segments
- multi-segment relative paths like `assets/tileset.bmp` are allowed

Refusals surface as host errors (`path refused: …`) on the error screen /
stderr. CI: `tests/path_sandbox_test.sh`.

## Screenshots in package mode

When the host extracts a `.lant` to a temp dir, it enters **package mode**.
`lt.screenshot` may only write a basename under that extract directory.
Folder-mode development still writes under the game dir with the same
relative-path rules.

## Nested package names

KORA's assets live under `assets/`. The packer used to skip subdirectories
silently — a KORA `.lant` would ship without textures. Packages now store
relative paths with `/`; extract creates parent directories. Flat games
(Lantern Night) are unchanged.

Folder kitchen frames and package kitchen frames are **byte-identical**
under `LANTERN_FIXED_DT` — the same determinism bar as everything else.

## What “safe by construction” means now

| Guarantee | Mechanism |
|---|---|
| No network / shell | language has no APIs |
| No arbitrary file read | path sandbox on loads |
| No arbitrary file write | screenshot policy + no other write natives except named saves |
| Saves are scoped | `lt.save` name charset filter under app support |
| Reviewable surface | wick-only store packages |

We still review store submissions. The host now matches the brochure.

## Links

- [PACKAGE.md](https://github.com/alikatgh/lantern/blob/main/docs/PACKAGE.md)
- `src/path_sandbox.cpp` in the lantern tree
