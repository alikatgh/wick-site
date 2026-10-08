#!/usr/bin/env python3
"""Fail publication when Japanese coverage or executable examples drift."""
from pathlib import Path
from html.parser import HTMLParser
import re

ROOT = Path(__file__).resolve().parents[1]
errors = []


def blocks(text, pattern):
    return re.findall(pattern, text, flags=re.S | re.M)


def compare_tree(source, translated, pattern, code_pattern):
    originals = {p.relative_to(source) for p in source.glob(pattern)}
    copies = {p.relative_to(translated) for p in translated.glob(pattern)}
    if originals != copies:
        errors.append(f'{translated.name}: file coverage mismatch: missing {originals - copies}, extra {copies - originals}')
    for relative in sorted(originals & copies):
        en = (source / relative).read_text()
        ja = (translated / relative).read_text()
        if not re.search(r'[ぁ-んァ-ン一-龯]', ja):
            errors.append(f'{translated / relative}: no Japanese prose')
        if blocks(en, code_pattern) != blocks(ja, code_pattern):
            errors.append(f'{translated / relative}: changed executable code blocks')
    return len(originals)


docs = compare_tree(ROOT / 'docs', ROOT / 'docs-ja', '**/*.md', r'^```[^\n]*\n(.*?)^```\s*$')
chapters = compare_tree(ROOT / 'book/chapters', ROOT / 'book-ja/chapters', '*.tex',
                        r'\\begin\{lstlisting\}(?:\[[^\n]*\])?\n(.*?)\\end\{lstlisting\}')


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.canonical = None
        self.alternates = {}
        self.code = []
        self.pre = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html': self.lang = attrs.get('lang')
        if tag == 'link' and attrs.get('rel') == 'canonical': self.canonical = attrs.get('href')
        if tag == 'link' and attrs.get('rel') == 'alternate':
            self.alternates[attrs.get('hreflang')] = attrs.get('href')
        if tag == 'pre': self.pre = []

    def handle_data(self, data):
        if self.pre is not None: self.pre.append(data)

    def handle_endtag(self, tag):
        if tag == 'pre' and self.pre is not None:
            self.code.append(''.join(self.pre).strip())
            self.pre = None


for relative in ['index.html', 'lantern/index.html', 'tour/index.html']:
    path = ROOT / 'ja' / relative
    if not path.is_file():
        errors.append(f'Missing Japanese static page: {relative}')
        continue
    en, ja = Page((ROOT / relative).read_text()), Page(path.read_text())
    if en.code != ja.code: errors.append(f'{relative}: changed static-page examples')
    if ja.lang != 'ja': errors.append(f'{relative}: missing Japanese language declaration')
    if not ja.canonical or '/ja/' not in ja.canonical: errors.append(f'{relative}: wrong canonical URL')

for source, rendered in [('book/chapters', 'build/book-ja')]:
    for file in (ROOT / source).glob('*.tex'):
        for n, text in enumerate(re.split(r'(?=\\chapter\{)', file.read_text())):
            if not text.strip(): continue
            slug = file.stem if file.stem != 'appendix' else f'appendix-{n}'
            path = ROOT / rendered / slug / 'index.html'
            if not path.is_file():
                errors.append(f'Missing rendered chapter: {slug}')
                continue
            page = Page(path.read_text())
            expected = blocks(text, r'\\begin\{lstlisting\}(?:\[[^\n]*\])?\n(.*?)\\end\{lstlisting\}')
            if [x.strip() for x in expected] != page.code:
                errors.append(f'{slug}: rendered Japanese book changed code listings')

for folder, section in [('build/reference-ja', 'docs'), ('build/book-ja', 'book')]:
    for path in (ROOT / folder).rglob('index.html'):
        page = Page(path.read_text())
        if page.lang != 'ja': errors.append(f'{path}: wrong rendered language')
        route = path.relative_to(ROOT / folder).as_posix().removesuffix('index.html')
        if page.alternates.get('en') != f'https://wick.aulenor.com/{section}/{route}':
            errors.append(f'{path}: language switch does not preserve the page')

if errors: raise SystemExit('\n'.join(errors))
print(f'Japanese coverage passed: {docs} reference/blog sources, {chapters} chapter files, 3 entry pages; source and rendered code preserved.')
