#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python scripts/build-book.py
mkdir -p docs/assets book-docs/assets
cp theme/assets/reading.css docs/assets/reading.css
cp theme/assets/reading.css book-docs/assets/reading.css
mkdocs build --strict -f mkdocs.learn.yml
mkdocs build --strict -f mkdocs.book.yml
