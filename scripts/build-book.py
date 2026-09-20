#!/usr/bin/env python3
"""Build MkDocs chapters from the original LaTeX book, preserving code verbatim."""
from pathlib import Path
import re, shutil
import pypandoc
ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'book-docs'
out.mkdir(exist_ok=True)
nav = []
for path in sorted((ROOT / 'book/chapters').glob('*.tex')):
    chunks = re.split(r'(?=\\chapter\{)', path.read_text())
    for n, text in enumerate(chunks):
        if not text.strip(): continue
        title = re.search(r'\\chapter\{([^}]+)\}', text).group(1)
        slug = path.stem if path.stem != 'appendix' else 'appendix-' + str(n)
        saved = {}
        def keep(content):
            token = 'WICKPLACEHOLDER' + str(len(saved)) + 'END'
            saved[token] = content
            return token
        def listing(m):
            lang = re.search(r'language=(\w+)', m[1] or '')
            language = lang[1] if lang else 'text'
            language = {'luatwin':'lua'}.get(language, language)
            return '\n\n' + keep('```' + language + '\n' + m[2].strip('\n') + '\n```') + '\n\n'
        text = re.sub(r'\\begin\{lstlisting\}(\[[^\n]*\])?\n(.*?)\\end\{lstlisting\}', listing, text, flags=re.S)
        text = re.sub(r'(?<!`)`([^`\n]+)`(?!`)', lambda m: keep('`' + m[1] + '`'), text)
        text = text.replace('\\chapter{', '\\section{').replace('\\section{', '\\WICKHEADING{',1)
        text = text.replace('\\subsection{','\\subsubsection{').replace('\\section{','\\subsection{').replace('\\WICKHEADING{','\\section{')
        text = re.sub(r'\\endfirsthead.*?\\endlastfoot', '', text, flags=re.S)
        md = pypandoc.convert_text(text, 'gfm', format='latex', extra_args=['--wrap=none'])
        # TeX treats straight apostrophes as closing quotes, including texttt.
        md = re.sub(r'`[^`]+`|<code>.*?</code>', lambda m: m[0].replace('’', chr(39)), md, flags=re.S)
        for token, content in saved.items(): md = md.replace(token, content)
        if 'WICKPLACEHOLDER' in md: raise RuntimeError('Unresolved code placeholder')
        (out / (slug + '.md')).write_text(md)
        nav.append((title, slug + '.md'))
shutil.copy(ROOT / 'wick-book.pdf', out / 'wick-book.pdf')
(out / 'index.md').write_text('''# The Wick Programming Language

<div class="book-intro"><p class="edition">THE ONLINE BOOK · VERSION 0.1</p><p>A small, typed scripting language for the Lantern engine.</p><p>Start with a complete game, then work through the language, its engine interface, and the compiler behind it.</p></div>

[Start reading →](01-introduction.md){ .md-button .md-button--primary }
[Download the PDF](wick-book.pdf){ .md-button }

## Inside the book

''' + '\n'.join(f'{i+1}. [{title}]({file})' for i,(title,file) in enumerate(nav)) + '''

## About this edition

By the Lantern engine authors. This is the web edition of the repository's version 0.1 book, converted from its original LaTeX chapters. The [language reference](https://learn.wick.aulenor.com/) includes later changes, including records.

Copyright © 2026 The Lantern engine authors. Distributed under the same zlib terms as the engine; the original authorship and source are preserved.
''')
print(f'Converted {len(nav)} chapters and appendices to {out}')
