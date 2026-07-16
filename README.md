# wick-site — wick.famemu.aulenor.com

The public website for **wick**, the [lantern engine](https://github.com/alikatgh/lantern)'s
own scripting language. The implementation lives in the engine repo under
[`wick/`](https://github.com/alikatgh/lantern/tree/main/wick); this repo is
the site, the language reference, and the **blog**.

## Layout

| Path | Role |
|------|------|
| `index.html` + `style.css` | Marketing page (root) |
| `docs/` + `mkdocs.yml` | A–Z reference **and** Go-style blog under `docs/blog/` |
| `wick-book.pdf` | Optional long-form PDF (regenerate from book/ when needed) |
| `.github/workflows/deploy.yml` | Builds MkDocs + copies marketing page → GitHub Pages |

## Local preview

```sh
python3 -m venv .venv && .venv/bin/pip install mkdocs mkdocs-material
.venv/bin/mkdocs build -d _site/docs && cp index.html style.css wick-book.pdf _site/ 2>/dev/null
python3 -m http.server 8351 -d _site
# open http://127.0.0.1:8351/ and http://127.0.0.1:8351/docs/blog/
```

## Go-live (custom domain)

DNS at aulenor.com: CNAME `wick.famemu` → `alikatgh.github.io`, then set
`wick.famemu.aulenor.com` in Settings → Pages and tick Enforce HTTPS.
Until then the site serves at `alikatgh.github.io/wick-site/`.

## Keeping docs honest (non-negotiable)

When the language changes in the engine repo (`wick/`, `docs/WICK.md`,
`CHANGELOG.md`):

1. Update the matching page under `docs/` (types, records, limits, …).
2. Add or amend a **blog post** under `docs/blog/` if the change is a design
   decision or release — same role as the Go blog.
3. Bump stats on `index.html` if line counts or CI check counts change.
4. Prefer one PR / one sitting: engine + site stay in lockstep.

The blog is not optional marketing. It is the public feature ledger.

## Blog posts (current)

- Welcome · Why optionals · Admitting records · Store safety · How we test · Release 0.2  
  See `docs/blog/index.md`.
