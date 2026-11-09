#!/usr/bin/env python3
"""408 应试大题手册 · 多页 LaTeX 编译器

把若干 Markdown 片段按顺序拼成一册 A4 多页 PDF：
    python3 build_handbook.py            # 全量编译

依赖 22408-notes 技能里的转换器（复用其中的 inline / table / codebox 逻辑），
导言区用本目录的 handbook-preamble.tex。
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_SCRIPTS = Path("/Users/shaoyikai/Desktop/考研/.dsh/skills/22408-notes/scripts")
sys.path.insert(0, str(SKILL_SCRIPTS))
import build_note as bn  # noqa: E402

PREAMBLE = HERE / "handbook-preamble.tex"
FRAG_DIR = Path("/tmp/408ext/notes")

# 片段顺序：@@@ 行会切成编页
ORDER = [
    "00-front.md",
    "A-ds01-顺序表与链表基础.md",
    "B-ds02-链表五套路.md",
    "C-ds03-哈夫曼与图应用.md",
    "D-ds04-排序.md",
    "E-co-补码与Cache.md",
    "F-co-指令与流水线.md",
    "G-co-IO方式.md",
    "H-os-PV.md",
    "I-os-分页与请求分页.md",
    "J-os-文件与磁盘.md",
    "K-nw-前三章.md",
    "L-nw-网络层IP.md",
    "M-nw-传输与应用层.md",
]

# 编页：片段前插入 \partpage
PARTS = {
    "E-co-补码与Cache.md": ("第二编", "计算机组成原理",
                        "综合应用题第 43、44 题，共 23 分 ｜ 每年两题，一题算数一题算时间"),
    "H-os-PV.md": ("第三编", "操作系统",
                   "综合应用题第 45、46 题，共 15 分 ｜ PV 与内存/文件，每年一难一易"),
    "K-nw-前三章.md": ("第四编", "计算机网络",
                      "综合应用题第 47 题，共 9 分 ｜ 性价比最低，放最后做，先拿第 1 小问"),
}

DOC_HEAD = r"""\documentclass[10pt,a4paper]{ctexart}
\input{%(preamble)s}
\renewcommand{\BookShort}{%(short)s}
\begin{document}
\handbookcover{%(subtitle)s}{%(line2)s}{%(line3)s}{%(blurb)s}
%(toc)s
"""

DOC_TAIL = "\n\\end{document}\n"


def sanitize(md: str) -> str:
    """把字体里没有的符号换成数学命令；跳过代码块。"""
    out = []
    in_code = False
    table = {"⌈": r"$\lceil$", "⌉": r"$\rceil$",
             "⌊": r"$\lfloor$", "⌋": r"$\rfloor$",
             "⇒": r"$\Rightarrow$", "⇔": r"$\Leftrightarrow$"}
    for ln in md.splitlines():
        if ln.strip().startswith("```"):
            in_code = not in_code
            out.append(ln)
            continue
        if in_code:
            for k, v in {"⇒": "=>", "⇔": "<=>", "⌈": "ceil(", "⌉": ")"}.items():
                ln = ln.replace(k, v)
        else:
            for k, v in table.items():
                ln = ln.replace(k, v)
        out.append(ln)
    res = []
    for ln in out:
        m = re.match(r"^###\s+(.+?)\s*$", ln)
        res.append("\\subhead{%s}" % m.group(1) if m else ln)
    return "\n".join(res)


def disp_width(s: str) -> int:
    w = 0
    for ch in s:
        w += 2 if "\u4e00" <= ch <= "\u9fff" or ch in "，。；：（）「」【】、·—" else 1
    return w


def render_table(rows: list[str]) -> str:
    """自适应三线表：短列用自然宽度，长列用 X 自动折行。"""
    def cells(line: str) -> list[str]:
        line = line.strip().strip("|")
        return [c.strip() for c in line.split("|")]

    header = cells(rows[0])
    body = [cells(r) for r in rows[2:]]
    ncol = max(len(header), max((len(r) for r in body), default=0))
    body = [r + [""] * (ncol - len(r)) for r in body]
    header = header + [""] * (ncol - len(header))

    # 用去掉行内标记后的纯文本估宽
    def plain(c: str) -> str:
        c = re.sub(r"\$[^$]*\$", "xxxxx", c)
        c = re.sub(r"`[^`]*`", "xxxxx", c)
        return re.sub(r"[*\\{}]", "", c)

    widths = []
    for i in range(ncol):
        col = [plain(r[i]) for r in [header] + body]
        widths.append(max(disp_width(c) for c in col))

    long_cols = {i for i, w in enumerate(widths) if w > 16}
    if not long_cols:
        long_cols = {max(range(ncol), key=lambda i: widths[i])}

    if len(body) >= 9:
        total = sum(max(widths[i], 4) for i in range(ncol))
        fracs = [max(widths[i], 4) / total for i in range(ncol)]
        fixed = [max(f, 0.08) for f in fracs]
        scale = sum(fixed)
        # 预留列间距：tabcolsep 5pt，正文宽约 489pt
        shrink = 1.0 - 0.021 * (ncol - 1)
        fixed = [f / scale * shrink for f in fixed]
        colspec = "@{}" + "".join(
            ">{\\raggedright\\arraybackslash}p{%.3f\\linewidth}" % f for f in fixed) + "@{}"
        head = " & ".join(bn.inline(c) for c in header) + r" \\"
        out = [r"\begin{center}\small",
               r"\begin{longtable}{%s}" % colspec,
               r"\toprule", head, r"\midrule", r"\endfirsthead",
               r"\toprule", head, r"\midrule", r"\endhead",
               r"\bottomrule", r"\endlastfoot"]
        for row in body:
            out.append(" & ".join(bn.inline(c) for c in row) + r" \\")
        out += [r"\end{longtable}", r"\end{center}"]
        return "\n".join(out)

    if long_cols == set(range(ncol)) and ncol <= 2:
        spec = "@{}" + "X" * ncol + "@{}"
        env, arg = "tabularx", r"{\linewidth}"
    elif len(long_cols) == ncol:
        spec = "@{}" + "".join(">{\\raggedright\\arraybackslash}X" for _ in range(ncol)) + "@{}"
        env, arg = "tabularx", r"{\linewidth}"
    else:
        parts = []
        for i in range(ncol):
            if i in long_cols:
                parts.append(">{\\raggedright\\arraybackslash}X")
            elif widths[i] <= 5:
                parts.append("c")
            else:
                parts.append("l")
        spec = "@{}" + "".join(parts) + "@{}"
        env, arg = "tabularx", r"{\linewidth}"

    lines = [r"\begin{center}\small", r"\begin{%s}%s{%s}" % (env, arg, spec), r"\toprule"]
    lines.append(" & ".join(bn.inline(c) for c in header) + r" \\")
    lines.append(r"\midrule")
    for row in body:
        lines.append(" & ".join(bn.inline(c) for c in row) + r" \\")
    lines += [r"\bottomrule", r"\end{%s}" % env, r"\end{center}"]
    return "\n".join(lines)


bn.render_table = render_table
bn.RAW_COMMANDS = tuple(bn.RAW_COMMANDS) + ("\\subhead",)


def chunk_to_tex(md: str) -> str:
    tex = bn.convert(sanitize(md), {})
    # convert() 会先塞一个空的 notetitle，去掉
    tex = re.sub(r"^\\notetitle\{[^\n]*\n", "", tex)
    # ## -> 带目录条目的考点标题
    tex = tex.replace("\\sechead{", "\\secheadx{")
    # **考频**：xxx  ->  \kaopin{xxx}
    tex = re.sub(r"^\\textbf\{考频\}：(.*)$", r"\\kaopin{\1}", tex, flags=re.M)
    return tex


def build() -> int:
    missing = [n for n in ORDER if not (FRAG_DIR / n).is_file()]
    if missing:
        print("缺片段：" + ", ".join(missing), file=sys.stderr)
        return 1

    raw = "\n\n".join(
        (("@@@ %s %s %s\n" % PARTS[n] if n in PARTS else "") + (FRAG_DIR / n).read_text(encoding="utf-8"))
        for n in ORDER
    )

    # 逐行扫描：## 之外的 @@@ 行切成编页，其余累积成块后 convert
    body: list[str] = []
    buf: list[str] = []

    def flush() -> None:
        if buf:
            text = "\n".join(buf).strip()
            buf.clear()
            if text:
                body.append(chunk_to_tex(text))

    for line in raw.splitlines():
        m = re.match(r"^@@@[ \t]+(\S+)[ \t]+(\S+)[ \t]*(.*)$", line)
        if m:
            flush()
            body.append("\\partpage{%s}{%s}{%s}" % (
                m.group(1).strip(), m.group(2).strip(), m.group(3).strip()))
        elif line.strip() == "<<<pagebreak>>>":
            flush()
            body.append("\\clearpage")
        else:
            buf.append(line)
    flush()

    tex = DOC_HEAD % {
        "preamble": PREAMBLE,
        "short": "408 应试大题手册",
        "subtitle": "考点 × 暴力解模板 × 真题年份溯源",
        "line2": "数据结构 · 计算机组成原理 · 操作系统 · 计算机网络",
        "line3": "2009--2026 统考真题大题全对齐",
        "blurb": ("只写会考的。数据结构算法题给可直接默写的暴力解模板；"
                  "其余三科每个考点都给可照抄的解题流水线，"
                  "并标注该考点在哪一年的大题里出现过。"),
        "toc": "\\clearpage{\\small\\linespread{1.16}\\selectfont\\tableofcontents}\\clearpage",
    } + "\n".join(body) + DOC_TAIL

    src = HERE / "手册.tex"
    src.write_text(tex, encoding="utf-8")

    compiler = shutil.which("xelatex") or "/Library/TeX/texbin/xelatex"
    work = Path(tempfile.mkdtemp(prefix="408hb-"))
    shutil.copyfile(src, work / "hb.tex")
    shutil.copyfile(PREAMBLE, work / "handbook-preamble.tex")
    log = ""
    for _ in range(3):  # 三遍：目录 + 页码
        r = subprocess.run([compiler, "-interaction=nonstopmode", "-halt-on-error", "hb.tex"],
                           cwd=work, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           text=True, encoding="utf-8", errors="replace", check=False)
        log = r.stdout
        if r.returncode:
            (HERE / "手册.log").write_text(log, encoding="utf-8")
            print("编译失败，日志尾部：\n" + "\n".join(log.splitlines()[-30:]), file=sys.stderr)
            return 1

    pdf = work / "hb.pdf"
    out = HERE.parent / "408应试大题手册.pdf"
    shutil.copyfile(pdf, out)
    (HERE / "手册.log").write_text(log, encoding="utf-8")

    overfull = re.findall(r"Overfull \\hbox \(([\d.]+)pt too wide\)", log)
    missing_chars = sorted(set(re.findall(r"Missing character: There is no (.+?) in font", log)))

    import fitz
    doc = fitz.open(out)
    prev = HERE / "preview"
    prev.mkdir(exist_ok=True)
    for old in prev.glob("*.png"):
        old.unlink()
    for i, page in enumerate(doc, start=1):
        page.get_pixmap(dpi=110).save(prev / f"p{i:03d}.png")
    pages = doc.page_count
    doc.close()

    print(json.dumps({"pdf": str(out), "pages": pages,
                      "overfull": len(overfull), "overfull_max": overfull[:8],
                      "missing_chars": missing_chars}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
