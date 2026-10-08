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
if grep -q 'Overfull' "$OUT/main.log"; then
  echo "PDF layout overflow; inspect $OUT/main.log" >&2
  exit 1
fi
cp "$OUT/main.pdf" "$ROOT/wick-book.pdf"
cp "$OUT/main.pdf" "$ROOT/book/main.pdf"

# Japanese requires a Unicode typesetter and embedded Japanese fonts.
JA_OUT="$OUT/ja"
mkdir -p "$JA_OUT/chapters"
cd "$ROOT/book-ja"
for pass in 1 2; do
  xelatex -interaction=nonstopmode -halt-on-error -output-directory "$JA_OUT" main.tex
done
if grep -Eq 'Overfull|Missing character:' "$JA_OUT/main.log"; then
  echo "Japanese PDF has overflow or missing glyphs; inspect $JA_OUT/main.log" >&2
  exit 1
fi
cp "$JA_OUT/main.pdf" "$ROOT/wick-book-ja.pdf"
