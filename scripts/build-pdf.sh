#!/usr/bin/env bash
# Generate the release PDF from canonical LaTeX; keep intermediates out of book/.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${WICK_TEX_OUT:-$ROOT/build/tex}"
mkdir -p "$OUT/chapters"
OUT="$(cd "$OUT" && pwd)"
cd "$ROOT/book"
for pass in 1 2; do
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory "$OUT" main.tex
done
cp "$OUT/main.pdf" "$ROOT/wick-book.pdf"
cp "$OUT/main.pdf" "$ROOT/book/main.pdf"
