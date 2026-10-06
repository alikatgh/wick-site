#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python scripts/build-book.py
mkdir -p docs/assets book-docs/assets
cp -R theme/assets/. docs/assets/
cp theme.js docs/assets/theme.js
cp theme.js book-docs/assets/theme.js
cp -R theme/assets/. book-docs/assets/
mkdocs build --strict -f mkdocs.learn.yml
mkdocs build --strict -f mkdocs.book.yml

python scripts/check-content.py
