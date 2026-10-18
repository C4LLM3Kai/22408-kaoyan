#!/usr/bin/env python3
"""Two-pass build: resolve TOC page numbers, then stamp page numbers."""
import re, subprocess, sys
from pathlib import Path
import pypdfium2 as pdfium
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

HERE = Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

TOC_TARGETS = [
    ("t0", "写在前面：这门课到底在解决什么问题"),
    ("t1", "第一篇 四大基本定理及其证明"),
    ("s11", "罗尔定理：一切微分中值定理的地基"),
    ("s12", "拉格朗日中值定理：把"),
    ("s13", "积分中值定理：开区间版本为什么更好用"),
    ("s14", "柯西中值定理：两个函数的"),
    ("s15", "第一篇综合：2010 年"),
    ("t2", "第二篇 构造辅助函数的三大方法"),
    ("s21", "总纲：为什么"),
    ("s22", "方法一 观察法"),
    ("s23", "方法二 公式法"),
    ("s24", "整体思想：当结论横跨"),
    ("s25", "方法三 微分方程反解常数"),
    ("s26", "找不到两个等值点怎么办"),
    ("t3", "第三篇 多中值定理与泰勒展开"),
    ("s31", "泰勒展开：两种余项与选点原则"),
    ("s32", "泰勒展开的六种典型题"),
    ("s33", "考法五：中值参数"),
    ("s34", "双中值定理（一）"),
    ("s35", "双中值定理（二）"),
    ("s36", "三中值问题：分段点本身就是中值"),
    ("t4", "附录 一页纸速查表"),
]

def build(body_text, out):
    html = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>中值定理证明题 · 完整讲义</title>
<link rel="stylesheet" href="katex/katex.min.css">
<link rel="stylesheet" href="style.css">
<script src="katex/katex.min.js"></script>
</head><body>
{body_text}
<script>
(function(){{
  var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
  var nodes = [], n;
  while (n = walker.nextNode()) nodes.push(n);
  nodes.forEach(function(node){{
    var text = node.nodeValue;
    if (text.indexOf('$') === -1) return;
    var re = /\\$\\$([\\s\\S]+?)\\$\\$|\\$([^$]+?)\\$/g;
    if (!re.test(text)) return;
    re.lastIndex = 0;
    var frag = document.createDocumentFragment(), last = 0, m;
    while ((m = re.exec(text)) !== null) {{
      if (m.index > last) frag.appendChild(document.createTextNode(text.slice(last, m.index)));
      var span = document.createElement('span');
      try {{
        katex.render(m[1] !== undefined ? m[1] : m[2], span,
          {{displayMode: m[1] !== undefined, throwOnError: false, strict: false}});
      }} catch (e) {{ span.textContent = m[0]; }}
      frag.appendChild(span);
      last = re.lastIndex;
    }}
    if (last < text.length) frag.appendChild(document.createTextNode(text.slice(last)));
    node.parentNode.replaceChild(frag, node);
  }});
}})();
</script>
</body></html>"""
    tmp = HERE / "_render.html"
    tmp.write_text(html, encoding="utf-8")
    pdf = HERE / out
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=20000",
                    f"--print-to-pdf={pdf}", tmp.as_uri()],
                   capture_output=True, text=True)
    return pdf

def find_pages(pdf_path):
    """Return dict target-id -> 1-based printed page number."""
    doc = pdfium.PdfDocument(str(pdf_path))
    pages = {}
    texts = []
    for i in range(len(doc)):
        tp = doc[i].get_textpage()
        texts.append(tp.get_text_range())
    # skip cover(0) and toc(1)
    import re as _re
    norm = [ _re.sub(r"\s+", "", t) for t in texts ]
    for key, needle in TOC_TARGETS:
        nd = _re.sub(r"\s+", "", needle)
        for i, t in enumerate(norm):
            if i < 2:
                continue
            if nd in t:
                pages[key] = i - 1
                break
    return pages

def stamp(pdf_path, out_path):
    reader = PdfReader(str(pdf_path))
    n = len(reader.pages)
    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        if i >= 2:  # no number on cover and toc
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=A4)
            w, h = A4
            c.setFont("Times-Roman", 9)
            c.setFillColorRGB(0.55, 0.58, 0.62)
            c.drawCentredString(w/2, 12*2.8346, str(i - 1))
            c.save()
            buf.seek(0)
            overlay = PdfReader(buf).pages[0]
            page.merge_page(overlay)
        writer.add_page(page)
    with open(out_path, "wb") as f:
        writer.write(f)
    return n

if __name__ == "__main__":
    body = (HERE/"body.html").read_text(encoding="utf-8")
    # pass 1: placeholder
    b1 = re.sub(r'(<span class="pg" data-toc="t\d">)\d+(</span>)', r'\g<1>00\g<2>', body)
    (HERE/"body_pass.html").write_text(b1, encoding="utf-8")
    p1 = build(b1, "_pass1.pdf")
    pages = find_pages(p1)
    print("pass1 pages:", pages)
    # pass 2: inject real numbers
    def repl(m):
        key = m.group(1)
        return f'<span class="pg" data-toc="{key}">{pages.get(key,"00")}</span>'
    b2 = re.sub(r'<span class="pg" data-toc="(s?t?\w+)">\d+</span>', repl, body)
    p2 = build(b2, "_pass2.pdf")
    pages2 = find_pages(p2)
    print("pass2 pages:", pages2)
    if pages2 != pages:
        b3 = re.sub(r'<span class="pg" data-toc="(s?t?\w+)">\d+</span>',
                    lambda m: f'<span class="pg" data-toc="{m.group(1)}">{pages2.get(m.group(1),"00")}</span>', body)
        p3 = build(b3, "_pass3.pdf")
        pages3 = find_pages(p3)
        print("pass3 pages:", pages3)
        final = p3
    else:
        final = p2
    n = stamp(final, HERE/"中值定理讲义.pdf")
    print(f"final: {n} pages")
