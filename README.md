# wick-site — wick.famemu.aulenor.com

The website for **wick**, the [lantern engine](https://github.com/alikatgh/lantern)'s
own scripting language. The language implementation lives in the engine
repo under [`wick/`](https://github.com/alikatgh/lantern/tree/main/wick);
this repo is only the site.

- `index.html` + `style.css` — the marketing page (root), sharing the
  lantern site's design system
- `docs/` + `mkdocs.yml` — the A–Z language reference, built with
  MkDocs (Material theme) and served under `/docs`
- `.github/workflows/deploy.yml` — builds both and deploys to GitHub Pages

## Local preview

```sh
python3 -m venv .venv && .venv/bin/pip install mkdocs mkdocs-material
.venv/bin/mkdocs build -d _site/docs && cp index.html style.css _site/
python3 -m http.server 8351 -d _site
```

## Go-live (custom domain)

DNS at aulenor.com: CNAME `wick.famemu` → `alikatgh.github.io`, then set
`wick.famemu.aulenor.com` in Settings → Pages and tick Enforce HTTPS.
Until then the site serves at `alikatgh.github.io/wick-site/`.

## Keeping docs honest

The reference documents the implementation as it exists — when the
language changes in the engine repo (`wick/`, `docs/WICK.md`), update the
matching page here in the same sitting.
