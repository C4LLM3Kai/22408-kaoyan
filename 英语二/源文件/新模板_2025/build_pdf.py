#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成《英语二小作文 · 十二类文体模板》LaTeX 源文件并编译为 PDF。

用法：python3 build_pdf.py
依赖：XeLaTeX（/Library/TeX/texbin）、ctex、Times New Roman
"""
import os
import re
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from content_front import COVER, RULES, DECIDE, APPENDIX          # noqa: E402
from content_genres_a import GENRES_A                             # noqa: E402
from content_genres_b import GENRES_B                             # noqa: E402

GENRES = GENRES_A + GENRES_B

ACCENT = "0E4D5C"
WARN = "9B2226"
GRAY = "5A5A5A"
RULE = "CBDCDD"
SOFT = "F2F7F7"

# ---------------------------------------------------------------- 工具函数

SPECIAL = {
    "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
    "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def esc(text):
    return "".join(SPECIAL.get(ch, ch) for ch in text)


SLOT_RE = re.compile(r"【([^】]*)】")
CIRCLED = {v: "（%d）" % i for i, v in enumerate("①②③④⑤⑥⑦⑧⑨⑩", 1)}


def fx(text):
    """转义文本，把【槽位】渲染成加粗主题色，圈号改成（1）式。"""
    text = "".join(CIRCLED.get(ch, ch) for ch in text)
    out, pos = [], 0
    for m in SLOT_RE.finditer(text):
        out.append(esc(text[pos:m.start()]))
        out.append(r"{\color{accent}\bfseries 【%s】}" % esc(m.group(1)))
        pos = m.end()
    out.append(esc(text[pos:]))
    return "".join(out)


def romawi_label(no):
    return "g" + no


def count_words(lines, kind):
    """统计正文词数：跳过称呼、结束语、署名、日期与通知标题。"""
    skip_exact = {"Notice", "Yours sincerely,", "Yours faithfully,", "Best wishes,",
                  "With many thanks,", "Yours respectfully,", "Li Ming",
                  "The Student Union", "Oct. 20, 2025"}
    body = []
    for i, line in enumerate(lines):
        s = line.strip()
        if not s:
            continue
        if i == 0 and (s.startswith("Dear") or s == "Notice"):
            continue
        if s in skip_exact:
            continue
        if re.match(r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.\s+\d{1,2},\s+\d{4}$", s):
            continue
        body.append(s)
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", " ".join(body)))


# ---------------------------------------------------------------- 排版片段


def band(no, cn, en, tag):
    return "\n".join([
        r"\noindent\colorbox{accent}{%",
        r"\parbox{\dimexpr\linewidth-2\fboxsep\relax}{%",
        r"\color{white}\vspace{1pt}",
        r"{\LARGE\bfseries %s}\hspace{0.5em}{\Large %s}\hfill{\large\itshape %s}" % (no, esc(cn), esc(en)),
        r"\\[1pt]{\footnotesize %s}\par\vspace{1pt}}}" % esc(tag),
        r"\par",
    ])


def sechead(title):
    return "\n".join([
        r"\vspace{4pt}\noindent{\color{accent}\bfseries %s}\par\nopagebreak" % esc(title),
        r"{\color{rule}\rule{\linewidth}{0.6pt}}\par\nopagebreak",
        r"\vspace{1pt}",
    ])


def signal_box(text):
    return "\n".join([
        r"\vspace{4pt}\noindent\colorbox{soft}{%",
        r"\parbox{\dimexpr\linewidth-2\fboxsep\relax}{\footnotesize{\color{accent}\bfseries 识别信号}\quad %s}}" % fx(text),
        r"\par",
        r"\vspace{2pt}",
    ])


def kv_table(rows, labelw="2.1cm"):
    out = [r"\vspace{2pt}\noindent\begin{tabularx}{\dimexpr\linewidth-1.4pt\relax}{@{}>{\raggedright\arraybackslash}p{%s}X@{}}" % labelw,
           r"\toprule"]
    for i, (k, v) in enumerate(rows):
        if i:
            out.append(r"\midrule")
        out.append(r"\footnotesize{\color{accent}\bfseries %s} & \footnotesize %s \\" % (esc(k), fx(v)))
    out += [r"\bottomrule", r"\end{tabularx}\par", r"\vspace{2pt}"]
    return "\n".join(out)


def data_table(cols, widths, rows):
    spec = "@{}" + "".join(r">{\raggedright\arraybackslash}p{%scm}" % w for w in widths[:-1])
    spec += r">{\raggedright\arraybackslash}X@{}"
    out = [r"\vspace{2pt}\noindent\begingroup\footnotesize\renewcommand{\arraystretch}{1.15}",
           r"\begin{tabularx}{\dimexpr\linewidth-1.4pt\relax}{%s}" % spec,
           r"\toprule",
           " & ".join(r"{\color{accent}\bfseries %s}" % esc(c) for c in cols) + r" \\",
           r"\midrule"]
    for r in rows:
        out.append(" & ".join(fx(c) for c in r) + r" \\")
    out += [r"\bottomrule", r"\end{tabularx}\endgroup\par", r"\vspace{2pt}"]
    return "\n".join(out)


def compact_groups(groups, keep_items=2):
    kept, tone = [], []
    for g in groups:
        if g["label"].startswith("④"):
            tone.extend(it["zh"] for it in g["items"])
            continue
        g2 = dict(g)
        g2["items"] = g["items"][:keep_items]
        kept.append(g2)
    return kept, tone


def groups_block(groups):
    groups, tone = compact_groups(groups)
    out = [r"\vspace{1pt}\begingroup\setlength{\parindent}{0pt}"]
    for g in groups:
        out.append(r"\vspace{2pt}{\footnotesize\bfseries\color{ink}%s}\par\vspace{1pt}" % fx(g["label"]))
        out.append(r"\begin{list}{}{\leftmargin=1.3em\labelwidth=0.95em\labelsep=0.35em\itemindent=0pt\topsep=0pt\partopsep=0pt"
                   r"\parsep=1.5pt\itemsep=0pt}")
        for it in g["items"]:
            out.append(r"\item[{\color{accent}\scriptsize$\blacktriangleright$}]"
                       r"{\footnotesize %s}\par\vspace{0.5pt}"
                       r"{\footnotesize\color{gray}%s}" % (fx(it["en"]), fx(it["zh"])))
        out.append(r"\end{list}")
    if tone:
        out.append(r"\vspace{1pt}{\footnotesize\color{gray}语气与落款：%s}\par" % esc("；".join(tone)))
    out.append(r"\endgroup")
    return "\n".join(out)


def model_block(title, en, zh, wc, kind="letter"):
    lines = [ln for ln in en.split("\n")]
    body = []
    tail = {"The Student Union", "Oct. 20, 2025"}
    for i, ln in enumerate(lines):
        s_ = ln.strip()
        if kind == "notice" and s_ == "Notice":
            body.append(r"\centerline{\footnotesize\bfseries Notice}\par\vspace{2pt}")
        elif kind == "notice" and s_ in tail:
            body.append(r"\par\noindent\hfill\footnotesize %s\par" % esc(s_))
        else:
            body.append(r"\footnotesize %s\par" % esc(s_))
    return "\n".join([
        r"\vspace{2pt}\noindent\colorbox{soft}{\parbox{\dimexpr\linewidth-2\fboxsep\relax}{%",
        r"\vspace{2pt}",
        r"{\footnotesize\bfseries\color{accent}%s}\hfill{\footnotesize\color{gray}正文 %d 词}" % (esc(title), wc),
        r"\par\vspace{2pt}",
        "\n".join(body),
        r"\par\vspace{2pt}{\footnotesize\color{gray}%s}" % fx(zh),
        r"\par\vspace{1pt}}}\par",
        r"\vspace{2pt}",
    ])


def traps_block(items):
    out = [r"\vspace{1pt}\begingroup\setlength{\parindent}{0pt}",
           r"\begin{list}{}{\leftmargin=1.3em\labelwidth=0.95em\labelsep=0.35em\itemindent=0pt\topsep=0pt\partopsep=0pt"
           r"\parsep=1.5pt\itemsep=0pt}"]
    for it in items:
        out.append(r"\item[{\color{warn}\scriptsize$\blacksquare$}]{\footnotesize %s}" % fx(it))
    out += [r"\end{list}", r"\endgroup"]
    return "\n".join(out)


# ---------------------------------------------------------------- 页面装配


def genre_page(g):
    out = [r"\clearpage", r"\label{%s}" % romawi_label(g["no"]), band(g["no"], g["cn"], g["en"], g["tag"])]
    out.append(signal_box(g["signal"]))
    for blk in g["blocks"]:
        t = blk["t"]
        if t == "model":
            wc = count_words(blk["en"].split("\n"), g["kind"])
            out.append(sechead(blk["h"]))
            out.append(model_block(blk["title"], blk["en"], blk["zh"], wc, g["kind"]))
            continue
        out.append(sechead(blk["h"]))
        if t == "kv":
            out.append(kv_table(blk["rows"]))
        elif t == "table":
            out.append(data_table(blk["cols"], blk["widths"], blk["rows"]))
        elif t == "groups":
            out.append(groups_block(blk["groups"]))
        elif t == "traps":
            out.append(traps_block(blk["items"]))
        else:
            raise ValueError(t)
    return "\n".join(out)


def cover_page():
    rows = []
    for g in GENRES:
        rows.append(r"\footnotesize %s\quad %s & \footnotesize\hfill \pageref{%s} \\"
                    % (g["no"], esc(g["cn"]), romawi_label(g["no"])))
    lines = "\n".join(r"\par\vspace{1.5pt}{\small %s}" % esc(x) for x in COVER["lines"])
    return "\n".join([
        r"\clearpage", r"\thispagestyle{empty}",
        r"\vspace*{1.0cm}",
        r"{\color{accent}\footnotesize\bfseries %s}\par" % esc(COVER["kicker"]),
        r"\vspace{8pt}",
        r"{\color{accent}\rule{\linewidth}{2.2pt}}\par\vspace{8pt}",
        r"{\Huge\bfseries %s}\par" % esc(COVER["title"]),
        r"\vspace{6pt}",
        r"{\large\color{gray} %s}\par" % esc(COVER["subtitle"]),
        r"\vspace{8pt}",
        r"{\color{accent}\rule{\linewidth}{0.8pt}}\par\vspace{12pt}",
        lines,
        r"\vspace{14pt}",
        r"\noindent{\color{accent}\bfseries\large 目\quad 录}\par\vspace{3pt}",
        r"{\color{rule}\rule{\linewidth}{0.6pt}}\par\vspace{3pt}",
        r"\noindent\begin{tabularx}{\linewidth}{@{}Xr@{}}",
        "\n".join(rows),
        r"\end{tabularx}\par",
        r"\vfill",
        r"\noindent\colorbox{soft}{\parbox{\dimexpr\linewidth-2\fboxsep\relax}{%",
        r"\footnotesize\color{gray}%s}}\par" % esc(COVER["note"]),
        r"\vspace{4pt}",
        r"\noindent{\footnotesize\color{gray}使用建议：先看第 02 页的决策表定文体，再翻到对应页背“骨架句”，最后用第 03 页的六条自查过一遍。}",
    ])


def rules_page():
    out = [r"\clearpage", r"\label{rules}", r"\vspace*{-6pt}",
           r"{\color{accent}\bfseries\LARGE %s}\par\vspace{4pt}" % esc(RULES["title"]),
           r"{\color{accent}\rule{\linewidth}{1.2pt}}\par"]
    for blk in RULES["blocks"]:
        out.append(sechead(blk["h"]))
        t = blk["t"]
        if t == "table":
            out.append(data_table(blk["cols"], blk["widths"], blk["rows"]))
        elif t == "bullets":
            out.append(r"\vspace{1pt}\begin{list}{}{\leftmargin=1.3em\labelwidth=0.95em\labelsep=0.35em\itemindent=0pt\topsep=0pt"
                       r"\parsep=1.5pt\itemsep=1pt}")
            for it in blk["items"]:
                out.append(r"\item[{\color{accent}\scriptsize$\blacktriangleright$}]{\footnotesize %s}" % fx(it))
            out.append(r"\end{list}\vspace{2pt}")
        elif t == "traps":
            out.append(traps_block(blk["items"]))
    return "\n".join(out)


def decide_page():
    out = [r"\clearpage", r"\label{decide}",
           r"{\color{accent}\bfseries\LARGE %s}\par\vspace{4pt}" % esc(DECIDE["title"]),
           r"{\color{accent}\rule{\linewidth}{1.2pt}}\par",
           r"\vspace{4pt}\noindent{\footnotesize %s}\par\vspace{4pt}" % fx(DECIDE["intro"]),
           data_table(DECIDE["cols"], DECIDE["widths"], DECIDE["rows"])]
    out.append(sechead("三条通用判断"))
    out.append(r"\vspace{1pt}\begin{list}{}{\leftmargin=1.35em\labelwidth=1.0em\labelsep=0.35em\itemindent=0pt\topsep=0pt"
               r"\parsep=2pt\itemsep=2pt}")
    for i, tip in enumerate(DECIDE["tips"], 1):
        out.append(r"\item[{\color{accent}\footnotesize\bfseries %d.}]{\footnotesize %s}" % (i, fx(tip)))
    out.append(r"\end{list}")
    return "\n".join(out)


def appendix_pages():
    out = []
    up = APPENDIX["upgrade"]
    out += [r"\clearpage", r"\label{app:a}",
            r"{\color{accent}\bfseries\LARGE %s}\par\vspace{4pt}" % esc(up["title"]),
            r"{\color{accent}\rule{\linewidth}{1.2pt}}\par",
            r"\vspace{4pt}\noindent{\footnotesize %s}\par\vspace{4pt}" % fx(up["intro"])]
    out.append(data_table(up["cols"], up["widths"], up["rows"]))

    ph = APPENDIX["phrases"]
    out += [r"\clearpage", r"\label{app:b}",
            r"{\color{accent}\bfseries\LARGE %s}\par\vspace{4pt}" % esc(ph["title"]),
            r"{\color{accent}\rule{\linewidth}{1.2pt}}\par\vspace{6pt}"]
    for g in ph["groups"]:
        out.append(r"\noindent{\bfseries\footnotesize\color{accent}%s}\par\vspace{1pt}" % esc(g["label"]))
        out.append(r"\begin{list}{}{\leftmargin=1.3em\labelwidth=0.95em\labelsep=0.35em\itemindent=0pt\topsep=0pt\parsep=2pt\itemsep=2pt}")
        for it in g["items"]:
            out.append(r"\item[{\color{accent}\scriptsize$\blacktriangleright$}]{\small %s}" % fx(it))
        out.append(r"\end{list}\vspace{4pt}")

    ck = APPENDIX["checklist"]
    out += [r"\clearpage", r"\label{app:c}",
            r"{\color{accent}\bfseries\LARGE %s}\par\vspace{4pt}" % esc(ck["title"]),
            r"{\color{accent}\rule{\linewidth}{1.2pt}}\par\vspace{5pt}",
            r"\noindent{\footnotesize\color{gray}逐条打勾；任何一项没法打勾，就回去改那一句，不要改整篇。}\par\vspace{4pt}"]
    for g in ck["groups"]:
        out.append(r"\noindent{\bfseries\small\color{accent}%s}\par\vspace{1pt}" % esc(g["label"]))
        out.append(r"\begin{list}{}{\leftmargin=1.4em\labelwidth=1.0em\labelsep=0.4em\itemindent=0pt\topsep=0pt\parsep=2pt\itemsep=2pt}")
        for it in g["items"]:
            out.append(r"\item[$\square$]{\footnotesize %s}" % fx(it))
        out.append(r"\end{list}\vspace{4pt}")
    out.append(r"\vspace{6pt}\noindent\colorbox{soft}{\parbox{\dimexpr\linewidth-2\fboxsep\relax}{%")
    out.append(r"\footnotesize{\color{accent}\bfseries 最后一句}\quad 小作文的目标不是“写得漂亮”，而是“一件事说清楚、格式不出错、读者不用回头猜”。达到这一点，8 分起。}}")
    return "\n".join(out)


PREAMBLE = r"""
\documentclass[10pt,a4paper]{ctexart}
\usepackage{geometry}
\geometry{left=1.4cm,right=1.4cm,top=1.15cm,bottom=1.0cm,headsep=0.3cm,footskip=0.5cm}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\setsansfont{Helvetica}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{amssymb}
\xeCJKDeclareCharClass{CJK}{"2460 -> "247F}
\usepackage{fancyhdr}
\usepackage[hidelinks]{hyperref}
\definecolor{accent}{HTML}{%ACCENT%}
\definecolor{warn}{HTML}{%WARN%}
\definecolor{gray}{HTML}{%GRAY%}
\definecolor{rule}{HTML}{%RULE%}
\definecolor{soft}{HTML}{%SOFT%}
\definecolor{ink}{HTML}{1C1C1E}
\renewcommand{\familydefault}{\rmdefault}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\linespread{1.0}
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\fancyhead[L]{\footnotesize\color{gray}英语二小作文 · 十二类文体模板}
\fancyhead[R]{\footnotesize\color{gray}Part A · 应用文}
\fancyfoot[C]{\footnotesize\color{gray}\thepage}
\renewcommand{\arraystretch}{1.08}
""".replace("%ACCENT%", ACCENT).replace("%WARN%", WARN).replace("%GRAY%", GRAY) \
   .replace("%RULE%", RULE).replace("%SOFT%", SOFT)


def build_tex():
    parts = [PREAMBLE, r"\begin{document}", cover_page(), rules_page(), decide_page()]
    parts.append(r"\clearpage")
    for g in GENRES:
        parts.append(genre_page(g))
    parts.append(appendix_pages())
    parts.append(r"\end{document}")
    return "\n".join(parts)


def main():
    tex = build_tex()
    tex_path = os.path.join(BASE, "英语二小作文_十二类文体模板.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex)
    print("tex written:", tex_path, len(tex), "chars")

    env = dict(os.environ, PATH="/Library/TeX/texbin:" + os.environ.get("PATH", ""))
    for run in (1, 2):
        p = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error",
                            os.path.basename(tex_path)],
                           cwd=BASE, env=env, capture_output=True, text=True)
        print("xelatex pass", run, "exit", p.returncode)
        if p.returncode != 0:
            print(p.stdout[-4000:])
            return 1

    log = open(os.path.join(BASE, "英语二小作文_十二类文体模板.log"), encoding="utf-8", errors="ignore").read()
    pages = re.findall(r"Output written on .*?\((\d+) pages", log)
    missing = log.count("Missing character")
    ovf_h = log.count("Overfull \\hbox")
    ovf_v = log.count("Overfull \\vbox")
    underfull_v = log.count("Underfull \\vbox")
    print("pages:", pages[-1] if pages else "?", "| missing char:", missing,
          "| overfull hbox:", ovf_h, "| overfull vbox:", ovf_v, "| underfull vbox:", underfull_v)
    if ovf_v:
        for m in re.finditer(r"Overfull \\vbox \(([\d.]+)pt too high\) detected at line (\d+)", log):
            print("  vbox overflow", m.group(1), "pt at tex line", m.group(2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
