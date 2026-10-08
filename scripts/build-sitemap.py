#!/usr/bin/env python3
"""List canonical entry, reference and book pages in both published languages."""
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree, register_namespace
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
namespace = 'http://www.sitemaps.org/schemas/sitemap/0.9'
xhtml = 'http://www.w3.org/1999/xhtml'
register_namespace('', namespace)
register_namespace('xhtml', xhtml)
tree = Element(f'{{{namespace}}}urlset')
for path in sorted(root.rglob('index.html')):
    route = '/' + path.relative_to(root).as_posix().removesuffix('index.html')
    url = SubElement(tree, f'{{{namespace}}}url')
    SubElement(url, f'{{{namespace}}}loc').text = 'https://wick.aulenor.com' + route
    english = route.removeprefix('/ja') if route.startswith('/ja/') else route
    for language, target in [('en', english), ('ja', '/ja' + english), ('x-default', english)]:
        if (root / target.lstrip('/') / 'index.html').is_file():
            SubElement(url, f'{{{xhtml}}}link', rel='alternate', hreflang=language, href='https://wick.aulenor.com' + target)
ElementTree(tree).write(root / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
(root / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://wick.aulenor.com/sitemap.xml\n')
print(f'Published sitemap: {len(tree)} pages.')
