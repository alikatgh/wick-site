#!/usr/bin/env python3
"""Check internal URLs in the assembled Pages site, including static entry pages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import sys

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.ids = [], set()
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'): self.ids.add(a['id'])
        if tag == 'a' and a.get('href'): self.links.append(a['href'])
        if tag in ('script', 'img') and a.get('src'): self.links.append(a['src'])
        if tag == 'link' and a.get('rel') == 'stylesheet': self.links.append(a['href'])
        if tag == 'form' and a.get('action'): self.links.append(a['action'])

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site').resolve()
for required in ('index.html', 'tour/index.html', 'lantern/index.html', 'docs/index.html', 'book/index.html', 'examples/first-game/main.wick', 'ja/index.html', 'ja/tour/index.html', 'ja/lantern/index.html', 'ja/docs/index.html', 'ja/book/index.html', 'wick-book-ja.pdf'):
    if not (root / required).is_file(): raise SystemExit(f'Missing published file: {required}')
pages = {p: Page(p.read_text()) for p in root.rglob('*.html')}
errors = set()
for p, page in pages.items():
    relative = p.relative_to(root).as_posix()
    base = 'https://wick.aulenor.com/' + relative
    if relative.endswith('index.html'): base = base[:-len('index.html')]
    for link in page.links:
        u = urlsplit(urljoin(base, link))
        if u.netloc != 'wick.aulenor.com' or u.scheme not in ('http', 'https'): continue
        target = root / unquote(u.path).lstrip('/')
        if u.path.endswith('/') or target.is_dir(): target = target / 'index.html'
        if not target.is_file():
            errors.add(f'{relative}: missing {link}')
        elif u.fragment and target.suffix == '.html' and unquote(u.fragment) not in pages[target].ids:
            errors.add(f'{relative}: missing anchor {link}')
if errors: raise SystemExit('\n'.join(sorted(errors)))
print(f'Pages check passed: internal routes, anchors and assets across {len(pages)} HTML pages.')
