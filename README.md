# wick-site — wick.aulenor.com

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

## Public website and custom domain

- Home: https://wick.aulenor.com/
- Reference and blog: https://wick.aulenor.com/docs/
- Book: https://wick.aulenor.com/book/
- PDF: https://wick.aulenor.com/wick-book.pdf

The domain is registered with EuroDNS; authoritative DNS is in Cloudflare.
The DNS-only CNAME `wick` points to `alikatgh.github.io`. GitHub Pages is
configured for `wick.aulenor.com` with HTTPS enforced. The Actions deployment
includes the checked-in CNAME file. The old project Pages address redirects
to the custom domain while retaining paths.

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

## Legacy standalone reference and book deployments

- `https://learn.wick.aulenor.com/` — a separately deployed language reference and design blog.
- `https://wickbook.aulenor.com/` — a separately deployed book. These Worker deployments are not updated by the Pages workflow.

The book's LaTeX stays canonical. `scripts/build-book.py` converts it to ignored
`book-docs/` sources, preserving every listing verbatim. Edition 0.3 updates the existing chapters for records and adds bits, bytes,
and buses. The PDF and both web builds are generated from the same sources.

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-sites.txt
bash scripts/build-pdf.sh # requires pdflatex + lmodern + latex-extra
bash scripts/build-sites.sh
npx wrangler@4 deploy --config wrangler.reference.json
npx wrangler@4 deploy --config wrangler.book.json
```

Both are static Cloudflare Workers custom domains in the existing Aulenor account.
The primary website is the GitHub Pages build at wick.aulenor.com. Shared reading styles and footer
links live under `theme/`.

The Pages workflow generates the current PDF before publishing and serves the
web book at `/book/` as well as the reference at `/docs/`. Custom-domain
Cloudflare deployments still use the two existing Wrangler configs.
