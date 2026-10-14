#!/usr/bin/env python3
"""Assemble the 408 knowledge-point handbook: chapter Markdown -> one XeLaTeX book.

Supported Markdown (deliberately small, so nothing silently degrades):
  ## / ### / #### / #####  headings
  paragraphs, - / * / + / 1. lists (nested by indentation)
  **bold**, *italic*, `code`, [text](url)
  ```lang fenced code blocks
  | pipe | tables |
  $inline$ and $$display$$ math
  > blockquote
  :::key|warn|exam Title ... :::   callout blocks
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

# ---------------------------------------------------------------- book layout

PARTS = [
    ("第一部分", "数据结构", [
        ("D01", "基本概念"),
        ("D02", "线性表"),
        ("D03", "栈、队列和数组"),
        ("D04", "树与二叉树"),
        ("D05", "图"),
        ("D06", "查找"),
        ("D07", "排序"),
    ]),
    ("第二部分", "计算机组成原理", [
        ("C01", "计算机系统概述"),
        ("C02", "数据的表示和运算"),
        ("C03", "存储器层次结构"),
        ("C04", "指令系统"),
        ("C05", "中央处理器"),
        ("C06", "总线和输入/输出系统"),
    ]),
    ("第三部分", "操作系统", [
        ("O01", "操作系统基础"),
        ("O02", "进程管理"),
        ("O03", "内存管理"),
        ("O04", "文件管理"),
        ("O05", "输入/输出管理"),
    ]),
    ("第四部分", "计算机网络", [
        ("N01", "计算机网络概述"),
        ("N02", "物理层"),
        ("N03", "数据链路层"),
        ("N04", "网络层"),
        ("N05", "传输层"),
        ("N06", "应用层"),
    ]),
]

CALLOUTS = {
    "key": ("核心结论", "callkey"),
    "warn": ("易错点", "callwarn"),
    "exam": ("真题考法", "callexam"),
    "note": ("说明", "callnote"),
}

CN_NUM = "零一二三四五六七八九十"

UNNUMBERED = ("本章考纲要求", "本章小结", "易错清单", "速查表", "考点分布",
              "真题分布", "真题考法", "参考文献", "索引", "附录")

NUM_PREFIX = re.compile(
    r"^(?:[一二三四五六七八九十]+\s*[、.．]\s*"
    r"|（\s*[一二三四五六七八九十]+\s*）\s*"
    r"|\(\s*[一二三四五六七八九十]+\s*\)\s*"
    r"|\d+\s*[.、．)）]\s*"
    r"|第\s*[一二三四五六七八九十百\d]+\s*[章节讲部分]\s*)"
)


def norm_numbering(text: str) -> str:
    """Drop the author's own section numbering; LaTeX renumbers consistently."""
    prev = None
    out = text
    while prev != out:
        prev = out
        out = NUM_PREFIX.sub("", out, count=1).strip()
    # trim stray separators left behind
    out = re.sub(r"^[、.．)）:：\s]+", "", out).strip()
    return out


def normalize_chapter(md: str, chapter_title: str) -> str:
    """Remove a heading that merely repeats the chapter title, then lift the
    remaining content headings one level so every chapter starts at \\section."""
    lines = md.replace("\r\n", "\n").split("\n")

    def is_end(txt: str) -> bool:
        t = txt.strip()
        return any(k in t for k in UNNUMBERED)

    # locate a redundant wrapper: first "## 一、<x>" whose <x> is the chapter title
    wrap_idx = None
    for idx, ln in enumerate(lines):
        m = re.match(r"^##\s+([一二三四五六七八九十]+[、.．])\s*(.+?)\s*$", ln)
        if not m:
            continue
        inner = norm_numbering(m.group(2))
        if inner and inner in chapter_title:
            wrap_idx = idx
        break

    if wrap_idx is not None:
        stop = len(lines)
        for idx in range(wrap_idx + 1, len(lines)):
            m = re.match(r"^##\s+(.*?)\s*$", lines[idx])
            if m and is_end(m.group(1)):
                stop = idx
                break
        out_lines = []
        for idx, ln in enumerate(lines):
            if idx == wrap_idx:
                continue
            if wrap_idx < idx < stop:
                m = re.match(r"^(#{2,5})\s+(.*?)\s*$", ln)
                if m and len(m.group(1)) > 1:
                    ln = "#" * (len(m.group(1)) - 1) + " " + m.group(2)
            out_lines.append(ln)
        lines = out_lines

    # strip numbering from every heading + flag unnumbered ones
    res = []
    for ln in lines:
        m = re.match(r"^(#{2,5})\s+(.*?)\s*$", ln)
        if m:
            title_raw = m.group(2)
            if is_end(title_raw):
                unnum = True
                title = title_raw
            else:
                unnum = False
                title = norm_numbering(title_raw)
            if not title:
                continue
            mark = "!" if unnum else ""
            res.append("#" * len(m.group(1)) + mark + " " + title)
        else:
            res.append(ln)
    return "\n".join(res)


def cn_chapter(n: int) -> str:
    if n <= 10:
        return CN_NUM[n]
    if n < 20:
        return "十" + CN_NUM[n - 10]
    if n == 20:
        return "二十"
    return "二十" + CN_NUM[n - 20]


# ---------------------------------------------------------------- inline text

SPECIALS = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "#": r"\#",
            "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\ctilde{}",
            "^": r"\ccaret{}", "$": r"\$"}

# Unicode symbols that the Latin text font does not carry: route them through math.
SYMBOLS = {
    "①": r"$\circled{1}$", "②": r"$\circled{2}$", "③": r"$\circled{3}$",
    "④": r"$\circled{4}$", "⑤": r"$\circled{5}$", "⑥": r"$\circled{6}$",
    "⑦": r"$\circled{7}$", "⑧": r"$\circled{8}$", "⑨": r"$\circled{9}$",
    "⑩": r"$\circled{10}$", "⑪": r"$\circled{11}$", "⑫": r"$\circled{12}$",
    "×": r"$\times$", "÷": r"$\div$", "±": r"$\pm$", "∓": r"$\mp$",
    "≈": r"$\approx$", "≠": r"$\neq$", "≤": r"$\le$", "≥": r"$\ge$",
    "≡": r"$\equiv$", "≪": r"$\ll$", "≫": r"$\gg$", "∝": r"$\propto$",
    "→": r"$\to$", "←": r"$\leftarrow$", "↔": r"$\leftrightarrow$",
    "⇒": r"$\Rightarrow$", "⇔": r"$\Leftrightarrow$", "↑": r"$\uparrow$",
    "↓": r"$\downarrow$", "∞": r"$\infty$", "∈": r"$\in$", "∉": r"$\notin$",
    "⊆": r"$\subseteq$", "⊂": r"$\subset$", "∪": r"$\cup$", "∩": r"$\cap$",
    "∅": r"$\varnothing$", "∧": r"$\land$", "∨": r"$\lor$", "¬": r"$\neg$",
    "∀": r"$\forall$", "∃": r"$\exists$", "∑": r"$\sum$", "∏": r"$\prod$",
    "√": r"$\sqrt{\ }$", "⊥": r"$\perp$", "∥": r"$\parallel$",
    "∠": r"$\angle$", "⋅": r"$\cdot$", "·": r"$\cdot$", "∘": r"$\circ$",
    "⌈": r"$\lceil$", "⌉": r"$\rceil$", "⌊": r"$\lfloor$", "⌋": r"$\rfloor$",
    "α": r"$\alpha$", "β": r"$\beta$", "γ": r"$\gamma$", "δ": r"$\delta$",
    "ε": r"$\varepsilon$", "ζ": r"$\zeta$", "η": r"$\eta$", "θ": r"$\theta$",
    "ι": r"$\iota$", "κ": r"$\kappa$", "λ": r"$\lambda$", "μ": r"$\mu$",
    "ν": r"$\nu$", "ξ": r"$\xi$", "π": r"$\pi$", "ρ": r"$\rho$",
    "σ": r"$\sigma$", "τ": r"$\tau$", "υ": r"$\upsilon$", "φ": r"$\varphi$",
    "χ": r"$\chi$", "ψ": r"$\psi$", "ω": r"$\omega$", "Δ": r"$\Delta$",
    "Σ": r"$\Sigma$", "Ω": r"$\Omega$", "Λ": r"$\Lambda$", "Φ": r"$\Phi$",
    "²": r"$^{2}$", "³": r"$^{3}$", "¹": r"$^{1}$", "⁰": r"$^{0}$",
    "℃": r"$^\circ$C", "℉": r"$^\circ$F",
    "✔": r"$\checkmark$",
    "✓": r"$\checkmark$",
    "✘": r"$\times$",
    "✗": r"$\times$",
    "★": r"$\bigstar$",
    "☆": r"$\star$",
    "●": r"$\bullet$",
    "○": r"$\circ$",
    "■": r"$\blacksquare$",
    "□": r"$\square$",
    "▲": r"$\blacktriangle$",
    "▼": r"$\blacktriangledown$",
    "◆": r"$\blacklozenge$",
    "◇": r"$\lozenge$",
    "⊕": r"$\oplus$",
    "⊗": r"$\otimes$",
    "⊙": r"$\odot$",
    "⊥": r"$\perp$",
    "∅": r"$\varnothing$",
    "∫": r"$\int$",
    "∬": r"$\iint$",
    "♠": r"$\spadesuit$",
    "♥": r"$\heartsuit$",
    "♦": r"$\diamondsuit$",
    "♣": r"$\clubsuit$",
    "⊃": r"$\supset$", "⊇": r"$\supseteq$",
    "⟨": r"$\langle$", "⟩": r"$\rangle$",
    "⟹": r"$\Longrightarrow$",
    "⟸": r"$\Longleftarrow$",
    "⇐": r"$\Leftarrow$",
}

INLINE = re.compile(
    r"(\$\$[\s\S]*?\$\$"          # display math inline (rare)
    r"|\$[^$\n]+?\$"             # inline math
    r"|`[^`\n]+?`"                # code span
    r"|\*\*.+?\*\*"              # bold (may contain a single '*')
    r"|\*[^*\n]+?\*"             # italic
    r"|\[[^\]\n]+?\]\([^)\n]*?\)"  # link
    r")"
)


TAG_RE = re.compile(r"\\tag\*?\{([^{}]*)\}")


MATH_SYMBOLS = {
    ch: val[1:-1] for ch, val in SYMBOLS.items()
    if val.startswith("$") and val.endswith("$") and val.count("$") == 2
}


def fix_math(tex: str) -> str:
    """Render \\tag inline and swap Unicode symbols for math equivalents."""
    tex = TAG_RE.sub(lambda m: "\\qquad (" + m.group(1) + ")", tex)
    if any(ch in tex for ch in MATH_SYMBOLS):
        tex = "".join(MATH_SYMBOLS.get(ch, ch) for ch in tex)
    return tex


def _balanced_single_dollars(line: str) -> bool:
    return len(re.findall(r"(?<!\$)\$(?!\$)", line)) % 2 == 0


def repair_source(md: str) -> str:
    """Undo escape corruption from chapter authoring.

    Chapter files were produced by several different writers; some paths expanded
    backslash escapes, so a mangled '\\times' shows up as TAB+'imes' and a mangled
    '\\right' as a newline followed by 'ight'.  Both are repaired here, together
    with any line break that lands inside an unbalanced inline-math span.
    """
    md = md.replace("\r\n", "\n")
    md = re.sub(r"\times", r"\\times", md)
    md = md.replace("\t", "    ")
    out: list[str] = []
    for line in md.split("\n"):
        if out and re.match(r"^ight(?=[)\]}_,^]|\s*$)", line) and out[-1].rstrip().endswith("}"):
            out[-1] = out[-1].rstrip() + "\\right"
            out.append(re.sub(r"^ight", "", line, count=1))
            continue
        if out and not _balanced_single_dollars(out[-1]) and re.match(r"^[a-zA-Z(]", line):
            out[-1] = out[-1].rstrip() + line.lstrip()
            continue
        out.append(line)
    return "\n".join(out)


TT_BREAK = re.compile(r"([:,;=+/<>\]\)])")


def breakable_tt(tex: str) -> str:
    """Let long identifiers wrap: insert \\allowbreak after safe separators."""
    return TT_BREAK.sub(r"\1\\allowbreak{}", tex)


def esc(text: str) -> str:
    out = []
    for ch in text:
        if ch in SYMBOLS:
            out.append(SYMBOLS[ch])
        else:
            out.append(SPECIALS.get(ch, ch))
    return "".join(out)


def inline(text: str) -> str:
    res, end = [], 0
    for m in INLINE.finditer(text):
        res.append(esc(text[end:m.start()]))
        tok = m.group()
        if tok.startswith("$$"):
            res.append(r"\(" + fix_math(tok[2:-2].strip()) + r"\)")
        elif tok.startswith("$"):
            res.append(tok if len(tok) < 4 else "$" + fix_math(tok[1:-1]) + "$")
        elif tok.startswith("`"):
            res.append(r"\texttt{" + breakable_tt(esc(tok[1:-1])) + "}")
        elif tok.startswith("**"):
            res.append(r"\textbf{" + inline(tok[2:-2]) + "}")
        elif tok.startswith("*"):
            res.append(r"\emph{" + inline(tok[1:-1]) + "}")
        else:
            g = re.fullmatch(r"\[([^\]]+)\]\(([^)]*)\)", tok)
            res.append(r"\href{" + g.group(2) + "}{" + inline(g.group(1)) + "}")
        end = m.end()
    res.append(esc(text[end:]))
    return "".join(res)


# ---------------------------------------------------------------- blocks

HEADING = re.compile(r"^(#{2,5})(!?)\s+(.*?)\s*$")
ULIST = re.compile(r"^(\s*)[-*+]\s+(.*)$")
OLIST = re.compile(r"^(\s*)\d+[.)]\s+(.*)$")
FENCE = re.compile(r"^```(\w*)\s*$")
CALLOUT_OPEN = re.compile(r"^:::(\w+)\s*(.*)$")
TABLE_SEP = re.compile(r"^\s*\|?[\s:|-]+\|[\s:|-]*$")


def split_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    parts, buf, i = [], "", 0
    while i < len(line):
        if line[i] == "\\" and i + 1 < len(line) and line[i + 1] == "|":
            buf += "|"
            i += 2
            continue
        if line[i] == "|":
            parts.append(buf)
            buf = ""
        else:
            buf += line[i]
        i += 1
    parts.append(buf)
    return [p.strip() for p in parts]


def render_table(rows: list[list[str]]) -> str:
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    weights = []
    for c in range(ncol):
        lens = [len(re.sub(r"\$[^$]*\$|[*`]", "", r[c])) for r in rows]
        weights.append(max(4, sum(lens) / len(lens)))
    total = sum(weights)
    # intercolumn space eats real width; account for it before sizing p{} columns
    tabcolsep = 4.0 if ncol <= 6 else (3.0 if ncol <= 9 else (2.0 if ncol <= 12 else 1.5))
    gap_frac = (2 * tabcolsep * ncol) / 466.0
    avail = max(0.32, 0.98 - gap_frac)
    widths = [max(0.008, min(0.5, w / total * avail)) for w in weights]
    scale = avail / sum(widths)
    widths = [w * scale for w in widths]
    fontsize = "\\small" if ncol <= 8 else "\\footnotesize"
    colspec = "".join(f"L{{{w:.4f}\\linewidth}}" for w in widths)
    out = [r"\begingroup" + fontsize +
           f"\\setlength{{\\tabcolsep}}{{{tabcolsep}pt}}",
           f"\\begin{{longtable}}{{@{{}}{colspec}@{{}}}}", r"\toprule"]
    def cell(c: str) -> str:
        t = inline(c).replace(r"\dfrac", r"\frac")
        return t.replace("\\ ", "\\allowbreak\\ ")

    out.append(" & ".join(r"\textbf{" + cell(c) + "}" for c in rows[0]) + r" \\")
    out.append(r"\midrule")
    out.append(r"\endhead")
    for r in rows[1:]:
        out.append(" & ".join(cell(c) for c in r) + r" \\")
    out.append(r"\bottomrule")
    out.append(r"\end{longtable}")
    out.append(r"\endgroup")
    return "\n".join(out)


CODE_WIDTH = 96

CODE_SYMBOLS = str.maketrans({
    "★": "*", "☆": "*", "✓": "v", "✔": "v", "✘": "x", "✗": "x",
    "●": "*", "○": "o", "■": "#", "□": "[ ]", "▲": "^", "▼": "v",
    "≤": "<=", "≥": ">=", "≠": "!=", "≈": "~=", "≡": "==",
    "→": "->", "←": "<-", "↔": "<->", "⇒": "=>", "⇔": "<=>",
    "×": "*", "÷": "/", "±": "+/-", "∞": "inf", "√": "sqrt",
    "⊂": "<", "⊃": ">", "⊆": "<=", "⊇": ">=", "∈": "in", "∉": "notin",
    "∪": "U", "∩": "n", "∧": "and", "∨": "or", "¬": "!", "∀": "all", "∃": "exists",
    "∑": "sum", "∏": "prod", "⌈": "ceil(", "⌉": ")", "⌊": "floor(", "⌋": ")",
    "α": "alpha", "β": "beta", "γ": "gamma", "δ": "delta", "ε": "eps",
    "θ": "theta", "λ": "lambda", "μ": "mu", "π": "pi", "ρ": "rho",
    "σ": "sigma", "τ": "tau", "φ": "phi", "ω": "omega", "Δ": "Delta",
    "¹": "1", "²": "2", "³": "3", "⟨": "<", "⟩": ">",
    "Ⅰ": "I", "Ⅱ": "II", "Ⅲ": "III", "Ⅳ": "IV", "Ⅴ": "V", "Ⅵ": "VI",
})


def wrap_code_line(line: str, width: int = CODE_WIDTH) -> list[str]:
    """Hard-wrap long code lines (fancyvrb here has no breaklines support)."""
    if len(line) <= width:
        return [line]
    indent = len(line) - len(line.lstrip(" "))
    pad = " " * min(indent + 4, 24)
    out, cur = [], ""
    for tok in re.split(r"(\s+)", line):
        if not tok:
            continue
        if cur and len(cur) + len(tok) > width:
            out.append(cur.rstrip())
            cur = pad + tok.lstrip()
        else:
            cur += tok
    if cur.strip():
        out.append(cur.rstrip())
    return out


def render_code(lang: str, body: list[str]) -> str:
    lines = []
    for ln in body:
        lines.extend(wrap_code_line(ln.rstrip().translate(CODE_SYMBOLS)))
    return ("\\begin{codebox}\n" + "\n".join(lines) + "\n\\end{codebox}")


def convert(md: str) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i, n = 0, len(lines)
    list_stack: list[str] = []    # open list kinds, outermost first
    indent_stack: list[int] = []  # indentation width of each open list level

    def env(kind: str) -> str:
        return "itemize" if kind == "ul" else "enumerate"

    def close_lists(to: int = 0, target=out):
        while len(list_stack) > to:
            k = list_stack.pop()
            indent_stack.pop()
            target.append("\\end{%s}" % env(k))

    def para(buf: list[str]):
        if buf:
            out.append(inline(" ".join(x.strip() for x in buf)))
            out.append("")

    def leading(line: str) -> int:
        return len(line) - len(line.lstrip(" "))

    buf: list[str] = []
    while i < n:
        line = lines[i]
        stripped = line.strip()

        # ---- fenced code
        m = FENCE.match(stripped)
        if m:
            para(buf); buf = []
            close_lists()
            body = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            out.append(render_code(m.group(1) or "text", body))
            out.append("")
            continue

        # ---- display math block
        if stripped.startswith("$$"):
            para(buf); buf = []
            close_lists()
            first = stripped[2:]
            closed = False
            if first.rstrip().endswith("$$") and len(first.rstrip()) >= 2:
                body = [first.rstrip()[:-2]]
                i += 1
                closed = True
            else:
                body = [first] if first.strip() else []
                i += 1
                guard = 0
                while i < n and guard < 500:
                    s2 = lines[i].strip()
                    if s2 == "$$":
                        i += 1
                        closed = True
                        break
                    if s2.endswith("$$"):
                        body.append(s2[:-2])
                        i += 1
                        closed = True
                        break
                    body.append(lines[i])
                    i += 1
                    guard += 1
            if closed:
                out.append("\\[" + fix_math("\n".join(body).strip()) + "\\]")
            else:
                # never closed: keep it as ordinary text rather than eating the chapter
                out.append(inline(" ".join(body)))
            out.append("")
            continue

        # ---- callout
        m = CALLOUT_OPEN.match(stripped)
        if m and m.group(1) in CALLOUTS:
            para(buf); buf = []
            close_lists()
            kind = m.group(1)
            title = m.group(2).strip()
            default_title, environment = CALLOUTS[kind]
            body = []
            i += 1
            depth = 1
            while i < n:
                s = lines[i].strip()
                if CALLOUT_OPEN.match(s) and s != ":::":
                    depth += 1
                if s == ":::":
                    depth -= 1
                    if depth == 0:
                        i += 1
                        break
                body.append(lines[i])
                i += 1
            inner = convert("\n".join(body))
            head = inline(title) if title else default_title
            out.append("\\begin{%s}{%s}" % (environment, head))
            out.append(inner)
            out.append("\\end{%s}" % environment)
            out.append("")
            continue

        # ---- table
        if stripped.startswith("|") and i + 1 < n and TABLE_SEP.match(lines[i + 1]):
            para(buf); buf = []
            close_lists()
            rows = [split_row(lines[i])]
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            out.append(render_table(rows))
            out.append("")
            continue

        # ---- heading
        m = HEADING.match(stripped)
        if m:
            para(buf); buf = []
            close_lists()
            level = len(m.group(1))
            unnum = m.group(2) == "!"
            cmd = {2: "section", 3: "subsection", 4: "subsubsection", 5: "paragraph"}[level]
            txt = inline(m.group(3))
            if unnum:
                out.append("\\%s*{%s}" % (cmd, txt))
                if level <= 4:
                    out.append("\\addcontentsline{toc}{%s}{%s}" % (cmd, txt))
            elif level == 5:
                out.append("\\%s{%s}\\mbox{}{\\par}" % (cmd, txt))
            else:
                out.append("\\%s{%s}" % (cmd, txt))
            out.append("")
            i += 1
            continue

        # ---- list items
        m = ULIST.match(line)
        m2 = OLIST.match(line)
        if m or m2:
            para(buf); buf = []
            mm = m or m2
            kind = "ul" if m else "ol"
            ind = len(mm.group(1).expandtabs(4))
            while list_stack and ind < indent_stack[-1]:
                k = list_stack.pop(); indent_stack.pop()
                out.append("\\end{%s}" % env(k))
            if list_stack and ind == indent_stack[-1] and list_stack[-1] != kind:
                k = list_stack.pop(); indent_stack.pop()
                out.append("\\end{%s}" % env(k))
            if not list_stack or ind > indent_stack[-1]:
                list_stack.append(kind); indent_stack.append(ind)
                out.append("\\begin{%s}" % env(kind))
            out.append("\\item " + inline(mm.group(2)))
            i += 1
            continue

        # ---- blank line: keep lists open so multi-paragraph items survive
        if not stripped:
            para(buf); buf = []
            i += 1
            continue

        # ---- blockquote
        if stripped.startswith(">"):
            para(buf); buf = []
            close_lists()
            body = []
            while i < n and lines[i].strip().startswith(">"):
                body.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append("\\begin{quote}")
            out.append(convert("\n".join(body)))
            out.append("\\end{quote}")
            continue

        # ---- horizontal rule
        if re.fullmatch(r"[-*_]{3,}", stripped):
            para(buf); buf = []
            close_lists()
            i += 1
            continue

        # ---- ordinary text
        if list_stack and leading(line) > indent_stack[-1] and out and out[-1].startswith("\\item"):
            out[-1] = out[-1] + " " + inline(stripped)
            i += 1
            continue
        if list_stack and leading(line) <= indent_stack[0]:
            close_lists()
            para(buf); buf = []
        buf.append(line)
        i += 1

    para(buf)
    close_lists()
    return "\n".join(x for x in out if x is not None)


# ---------------------------------------------------------------- preamble

PREAMBLE = r"""\documentclass[11pt,openany,UTF8]{ctexbook}
\usepackage{amsmath,amssymb}
\usepackage{array,booktabs,longtable}
\usepackage{fancyvrb}
\usepackage{xcolor}
\usepackage[a4paper,top=2.4cm,bottom=2.4cm,left=2.3cm,right=2.3cm,headsep=0.6cm]{geometry}
\usepackage{fancyhdr}
\usepackage{needspace}
\usepackage{enumitem}
\usepackage[hidelinks,bookmarksnumbered=true]{hyperref}

% ---- fonts
\setCJKmainfont{Songti SC}[BoldFont=Heiti SC]
\xeCJKsetup{CJKmath=true}
\xeCJKDeclareCharClass{CJK}{"2500 -> "257F, "25A0 -> "25FF, "2160 -> "2183, "2190 -> "21FF}
\setCJKsansfont{Heiti SC}
\setCJKmonofont{Songti SC}
\setmainfont{Times New Roman}

% ---- colours (restrained)
\definecolor{accent}{HTML}{1A1A1A}
\definecolor{keybar}{HTML}{1F4E79}
\definecolor{warnbar}{HTML}{9C2A20}
\definecolor{exambar}{HTML}{4A4A4A}
\definecolor{notebar}{HTML}{2E6B4F}
\definecolor{codebg}{HTML}{F4F4F4}
\definecolor{rulesep}{HTML}{BFBFBF}

% ---- table column type
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\newcommand{\ccaret}{\ifmmode\hat{}\else\textasciicircum{}\fi}
\newcommand{\circled}[1]{\textcircled{\scriptsize\,#1}}
\newcommand{\ctilde}{\ifmmode\tilde{}\else\textasciitilde{}\fi}

% ---- code blocks
\DefineVerbatimEnvironment{codebox}{Verbatim}%
  {frame=single,framerule=0.3pt,rulecolor=\color{rulesep},%
   framesep=6pt,fontsize=\small,baselinestretch=0.98,%
   xleftmargin=4pt,xrightmargin=4pt}

% ---- callout environments (breakable: only a bar + rule, no box)
\newcommand{\callouthead}[2]{%
  \par\addvspace{7pt}\noindent
  {\color{#1}\rule[-0.15em]{3pt}{1.05em}}\hspace{0.5em}%
  {\bfseries\color{#1}#2}\par\nobreak\vspace{-0.35em}%
  {\color{rulesep}\hrule height 0.4pt}\nobreak\vspace{0.45em}%
  \begingroup\small\setlength{\parindent}{0pt}%
  \leftskip=1.1em\rightskip=0.6em\noindent\ignorespaces}
\newcommand{\calloutend}{\par\endgroup\addvspace{7pt}}

\newenvironment{callkey}[1]{\callouthead{keybar}{#1}}{\calloutend}
\newenvironment{callwarn}[1]{\callouthead{warnbar}{#1}}{\calloutend}
\newenvironment{callexam}[1]{\callouthead{exambar}{#1}}{\calloutend}
\newenvironment{callnote}[1]{\callouthead{notebar}{#1}}{\calloutend}

% ---- headings
\ctexset{
  chapter = {format = \raggedright\Large\bfseries, name = {第,章}, number = \chinese{chapter},
             aftername = {}, beforeskip = 0pt, afterskip = 18pt, pagestyle = plain},
  section = {format = \raggedright\large\bfseries, name = {,、}, number = \chinese{section},
             aftername = {}, beforeskip = 16pt, afterskip = 8pt},
  subsection = {format = \raggedright\normalsize\bfseries, name = {（,）}, number = \chinese{subsection},
             aftername = {}, beforeskip = 11pt, afterskip = 6pt},
  subsubsection = {format = \raggedright\normalsize\itshape, name = {,.}, number = \arabic{subsubsection},
             aftername = {}, beforeskip = 9pt, afterskip = 4pt},
}
\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{2}
\setlist[itemize]{topsep=3pt,itemsep=1.5pt,parsep=0pt,leftmargin=1.5em}
\setlist[enumerate]{topsep=3pt,itemsep=1.5pt,parsep=0pt,leftmargin=1.8em}
\linespread{1.16}
\tolerance=3000
\emergencystretch=3em
\hbadness=10000
\vbadness=10000
\setlength{\parskip}{3.2pt}
\setlength{\parindent}{0pt}
\renewcommand{\arraystretch}{1.25}

% ---- header / footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\color{exambar}408 考纲知识点手册}
\fancyhead[R]{\small\color{exambar}\leftmark}
\fancyfoot[C]{\small\thepage}
\renewcommand{\headrulewidth}{0.3pt}
\renewcommand{\headrule}{\hbox to\headwidth{\color{rulesep}\leaders\hrule height \headrulewidth\hfill}}
\fancypagestyle{plain}{\fancyhf{}\fancyfoot[C]{\small\thepage}\renewcommand{\headrulewidth}{0pt}}

\begin{document}
"""

TITLE = r"""
\begin{titlepage}
\centering
\vspace*{3.2cm}
{\Huge\bfseries 408 考纲知识点手册\par}
\vspace{0.9cm}
{\Large 计算机学科专业基础综合\par}
\vspace{0.35cm}
{\large 按 2027 年全国硕士研究生招生考试大纲编排\par}
\vspace{1.6cm}
{\large 数据结构 \quad$\cdot$\quad 计算机组成原理 \quad$\cdot$\quad 操作系统 \quad$\cdot$\quad 计算机网络\par}
\vspace{2.2cm}
{\normalsize
\begin{tabular}{rl}
考查科目数 & 4 \\
知识点条目 & 覆盖大纲全部条目 \\
主要素材 & 语雀「计算机考研408笔记」知识库 \\
           & 王道 2027 系列教材与课件 \\
           & 工作区历年真题与强化笔记 \\
\end{tabular}\par}
\vfill
{\small 本手册为依据 2027 年考试大纲整理的知识点汇编，供复习检索使用。\par}
\vspace{1.2cm}
\end{titlepage}
"""

FRONT = r"""
\frontmatter
\pagestyle{fancy}
\chapter*{使用说明}
\addcontentsline{toc}{chapter}{使用说明}
\markboth{使用说明}{使用说明}
\input{使用说明.tex}
\cleardoublepage
\tableofcontents
\mainmatter
"""


def build(chapter_dir: str, out_tex: str, only: list[str] | None = None):
    body = [PREAMBLE, TITLE, FRONT]
    chap_no = 0
    missing = []
    for part_label, part_name, chapters in PARTS:
        body.append("\\part{%s\\quad %s}" % (part_label, part_name))
        for code, title in chapters:
            if only and code not in only:
                continue
            path = os.path.join(chapter_dir, f"{code}-{title.replace('/', '_')}.md")
            if not os.path.exists(path):
                # tolerate filename differences
                cands = [f for f in os.listdir(chapter_dir) if f.startswith(code)]
                if cands:
                    path = os.path.join(chapter_dir, cands[0])
            chap_no += 1
            if not os.path.exists(path):
                missing.append((code, title, path))
                continue
            md = normalize_chapter(repair_source(open(path, encoding="utf-8").read()), title)
            body.append("\\chapter{%s}" % inline(title))
            body.append("\\markboth{%s}{%s}" % (inline(title), inline(title)))
            body.append(convert(md))
    body.append("\\end{document}\n")
    open(out_tex, "w", encoding="utf-8").write("\n".join(body))
    # the front-matter file is \input by the preamble; keep it beside the .tex
    src_intro = os.path.join(chapter_dir, "使用说明.tex")
    if os.path.exists(src_intro):
        dst = os.path.join(os.path.dirname(os.path.abspath(out_tex)), "使用说明.tex")
        if os.path.abspath(src_intro) != os.path.abspath(dst):
            import shutil
            shutil.copyfile(src_intro, dst)
    return missing, chap_no


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter_dir")
    ap.add_argument("out_tex")
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    miss, n = build(a.chapter_dir, a.out_tex, a.only)
    print(f"chapters built: {n}")
    for m in miss:
        print("MISSING:", m)
