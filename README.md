# Wick website

The public programmer website at **https://wick.aulenor.com/**.
The language and engine implementation lives in [alikatgh/lantern](https://github.com/alikatgh/lantern).

## Sources and published routes

| Source | Published content |
|---|---|
| `index.html`, `style.css` | Homepage, search entry and reference index at `/` |
| `tour/` | Five-minute introduction, real Bit Lab capture, language tradeoffs and first-run path at `/tour/` |
| `lantern/index.html` | Engine guide, downloads, builds, examples and packaging at `/lantern/` |
| `examples/first-game/main.wick` | Downloadable example shared with the homepage and tutorial |
| `docs/`, `mkdocs.yml` | Language and engine reference at `/docs/`, blog at `/docs/blog/` |
| `book/chapters/*.tex` | Canonical book source; web at `/book/`, PDF at `/wick-book.pdf` |
| `theme/`, `theme.js` | Shared reading styles, local fonts, navigation and appearance |
| `ja/`, `docs-ja/`, `book-ja/` | Japanese counterparts at `/ja/`, `/ja/docs/`, `/ja/book/`, and `/wick-book-ja.pdf` |

`book-docs/`, `build/` and `_site/` are generated. Fix book conversion in
`scripts/build-book.py`; do not patch its generated Markdown or HTML.

## Build and review

Use an existing Python environment, or create a virtual environment and install
`requirements-sites.txt`. Book conversion needs Pandoc (via the declared Python
dependency). The English PDF uses pdfLaTeX; Japanese uses XeLaTeX and Noto CJK fonts.
On Ubuntu, install `texlive-latex-extra texlive-fonts-recommended lmodern
texlive-xetex texlive-lang-japanese texlive-lang-chinese fonts-noto-cjk`.

```sh
bash scripts/build-pdf.sh
bash scripts/build-sites.sh
node scripts/test-theme.cjs
bash scripts/build-pages.sh
python3 -m http.server 8351 -d _site
```

Open `http://127.0.0.1:8351/`. Some reading-shell links intentionally use the
canonical hostname; inspect those destinations separately when reviewing locally.

`build-pages.sh` assembles the exact Pages output and validates internal routes,
anchors and assets. The content checker compares book table counts and source
listings with generated pages. Neither check proves example execution or visual
quality: review changed pages and interactions in a browser, including search,
code copy controls, narrow layouts, and both appearance modes.

## Publication

`.github/workflows/verify-book.yml` checks pull requests. The `main` push workflow
builds the PDF, reference, book, homepage, Lantern guide and example download,
then deploys `_site/` to GitHub Pages. `CNAME` retains `wick.aulenor.com`.

The existing Cloudflare redirects send `learn.wick.aulenor.com` to `/docs/` and
`wickbook.aulenor.com` to `/book/` on the canonical hostname, retaining paths and
queries. The standalone MkDocs/Worker configurations remain for compatibility;
ordinary website changes publish through Pages, not the old Workers.

The tour's `bitlab.png` is an actual Lantern framebuffer capture from the 0.3
release verification, not a browser implementation. Its source is
`games/bitlab/main.wick` in Lantern v0.8.0. Keep the screenshot and release links
aligned when updating the tour; retain its explicit platform and language limits.

## Keep the content aligned

When the language or engine changes, update the affected reference pages,
examples, book source and release post together. Check installation commands
against actual release files and supported platforms. Distinguish the Wick
language version from the Lantern engine version; do not promise platform
binaries that the release does not contain. Keep the homepage example, its
`main.wick` download and the getting-started listing consistent.
Update the Japanese counterpart in the same change. Preserve code examples,
API names, source revisions and language-switch destinations. The build checks
translation coverage, example parity, links, and PDF overflow or missing glyphs.
