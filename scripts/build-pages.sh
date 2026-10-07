#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# build-sites.sh and build-pdf.sh supply the book and shared reference assets.
mkdocs build --strict -d _site/docs
mkdir -p _site/book _site/assets _site/lantern _site/examples
cp index.html style.css theme.js wick-book.pdf CNAME _site/
cp -R build/book/. _site/book/
cp -R theme/assets/. _site/assets/
cp -R lantern/. _site/lantern/
cp -R examples/. _site/examples/
python scripts/check-pages.py _site
