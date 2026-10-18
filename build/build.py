#!/usr/bin/env python3
"""Build body.html -> A4 PDF via headless Chrome, with KaTeX math pre-tokenized."""
import re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

DISPLAY = re.compile(r'\$\$(.+?)\$\$', re.S)
INLINE  = re.compile(r'(?<!\$)\$(?!\$)([^$\n]+?)\$(?!\$)')

import html as _html

def unesc(s):
    """Undo HTML entities so KaTeX sees real <, >, & ."""
    return _html.unescape(s)

def esc_attr(s):
    return (s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
             .replace('"','&quot;'))

def tokenize(html):
    """Replace $$..$$ and $..$ with data-tex elements, skipping <script>/<style>."""
    parts = re.split(r'(<script[\s\S]*?</script>|<style[\s\S]*?</style>)', html)
    out = []
    for part in parts:
        if part.startswith('<script') or part.startswith('<style'):
            out.append(part); continue
        part = DISPLAY.sub(lambda m: f'<span class="mathd" data-tex="{esc_attr(unesc(m.group(1).strip()))}"></span>', part)
        part = INLINE.sub(lambda m: f'<span class="mathi" data-tex="{esc_attr(unesc(m.group(1).strip()))}"></span>', part)
        out.append(part)
    return ''.join(out)

SCRIPT = r"""
document.querySelectorAll('.mathd').forEach(function(el){
  var d=document.createElement('div'); d.className='math-display';
  try { katex.render(el.dataset.tex, d, {displayMode:true, throwOnError:false, strict:false}); }
  catch(e){ d.textContent = el.dataset.tex; }
  el.parentNode.replaceChild(d, el);
});
document.querySelectorAll('.mathi').forEach(function(el){
  var s=document.createElement('span');
  try { katex.render(el.dataset.tex, s, {displayMode:false, throwOnError:false, strict:false}); }
  catch(e){ s.textContent = el.dataset.tex; }
  el.parentNode.replaceChild(s, el);
});
"""

def build(body_text, out, title="中值定理证明题 · 完整讲义"):
    body = tokenize(body_text)
    html = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="katex/katex.min.css">
<link rel="stylesheet" href="style.css">
<script src="katex/katex.min.js"></script>
</head><body>
{body}
<script>{SCRIPT}</script>
</body></html>"""
    tmp = HERE / "_render.html"
    tmp.write_text(html, encoding="utf-8")
    pdf = HERE / out
    r = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        "--virtual-time-budget=30000",
                        f"--print-to-pdf={pdf}", tmp.as_uri()],
                       capture_output=True, text=True)
    if not pdf.exists():
        print(r.stderr[-1500:]); sys.exit(1)
    return pdf

if __name__ == "__main__":
    body = Path(sys.argv[1] if len(sys.argv)>1 else "body.html").read_text(encoding="utf-8")
    p = build(body, sys.argv[2] if len(sys.argv)>2 else "中值定理讲义.pdf")
    print("OK", p, f"{p.stat().st_size/1024:.0f} KB")
