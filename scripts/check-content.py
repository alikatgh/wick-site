#!/usr/bin/env python3
"""Check every rendered article and compare web book tables/code to TeX source."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

class Article(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.active = False
        self.pre = False
        self.code = None
        self.blocks = []
        self.text = []
        self.tables = 0
        self.feed(html)
    def handle_starttag(self, tag, attrs):
        if tag == 'article': self.active = True
        if not self.active: return
        if tag == 'table': self.tables += 1
        if tag == 'pre': self.pre = True
        if tag == 'code' and self.pre: self.code = []
    def handle_endtag(self, tag):
        if tag == 'article': self.active = False
        if tag == 'code' and self.code is not None:
            self.blocks.append(''.join(self.code).strip())
            self.code = None
        if tag == 'pre': self.pre = False
    def handle_data(self, data):
        if self.code is not None: self.code.append(data)
        if self.active and not self.pre: self.text.append(data)

root = Path(__file__).resolve().parents[1]
errors = []
count = 0
for site in sys.argv[1:] or ['build/book', 'build/reference']:
    for file in (root / site).rglob('*.html'):
        article = Article(file.read_text())
        if not article.text: continue
        count += 1
        text = ''.join(article.text)
        for pattern in [r'\|\s*:?---', r'\\(?:times|rightarrow|begin|end)\b', r'WICKPLACEHOLDER', r'\$`']:
            if re.search(pattern, text): errors.append(f'{file}: raw markup {pattern}')

book = root / 'build/book'
for file in (root / 'book/chapters').glob('*.tex'):
    for n, text in enumerate(re.split(r'(?=\\chapter\{)', file.read_text())):
        if not text.strip(): continue
        slug = file.stem if file.stem != 'appendix' else 'appendix-' + str(n)
        page = Article((book / slug / 'index.html').read_text())
        expected = len(re.findall(r'\\begin\{(?:tabular|longtable)\}', text))
        if page.tables != expected:
            errors.append(f'{slug}: expected {expected} tables, got {page.tables}')
            print((root / 'book-docs' / (slug + '.md')).read_text())
        for code in re.findall(r'\\begin\{lstlisting\}(?:\[[^\n]*\])?\n(.*?)\\end\{lstlisting\}', text, flags=re.S):
            if code.strip() not in page.blocks: errors.append(f'{slug}: changed or missing code: {code[:70]!r}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'Content check passed: {count} articles; all book tables and code listings preserved.')
