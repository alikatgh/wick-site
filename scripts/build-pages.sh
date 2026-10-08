#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# build-sites.sh and build-pdf.sh supply the book and shared reference assets.
mkdocs build --strict -d _site/docs
mkdir -p _site/book _site/assets _site/lantern _site/examples _site/tour _site/ja/docs _site/ja/book
cp index.html style.css theme.js wick-book.pdf wick-book-ja.pdf CNAME _site/
cp -R build/book/. _site/book/
cp -R theme/assets/. _site/assets/
cp -R lantern/. _site/lantern/
cp -R examples/. _site/examples/
cp -R tour/. _site/tour/
cp -R ja/. _site/ja/
cp -R build/reference-ja/. _site/ja/docs/
cp -R build/book-ja/. _site/ja/book/
python scripts/check-pages.py _site
python scripts/build-sitemap.py _site
