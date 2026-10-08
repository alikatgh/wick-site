#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python scripts/build-book.py
python scripts/build-book.py --lang ja
for source in docs book-docs docs-ja book-docs-ja; do
  mkdir -p "$source/assets"
  cp -R theme/assets/. "$source/assets/"
  cp theme.js "$source/assets/theme.js"
done
mkdocs build --strict -f mkdocs.learn.yml
mkdocs build --strict -f mkdocs.book.yml
mkdocs build --strict -f mkdocs.ja.yml
mkdocs build --strict -f mkdocs.book.ja.yml

python scripts/check-content.py
python scripts/check-japanese.py
