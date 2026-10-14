#!/usr/bin/env python3
"""总装并编译《考研数学二 知识点手册》两个分册（高等数学 / 线性代数）。

用法：
    python3 build_m2.py               # 编译两个分册
    python3 build_m2.py 高数          # 只编译高等数学分册
复用 408 手册的 Markdown -> XeLaTeX 转换器（build_book.py）。
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_book as B  # noqa: E402  复用 Markdown -> XeLaTeX 转换器

ROOT = os.path.dirname(HERE)                 # 数学二/
SRC_ROOT = os.path.join(ROOT, "源文件")
BUILD_ROOT = os.path.join(ROOT, "build")
TEXBIN = "/Library/TeX/texbin"

# 补充 408 版未覆盖的数学符号（否则 XeLaTeX 会静默丢字）
EXTRA_SYMBOLS = {
    "∂": r"$\partial$", "∇": r"$\nabla$", "′": r"$'$", "″": r"$''$",
    "⋯": r"$\cdots$", "−": r"$-$", "⊤": r"$\top$", "≃": r"$\simeq$",
    "≅": r"$\cong$", "∮": r"$\oint$", "⇀": r"$\rightharpoonup$", "∗": r"$*$",
    "⩽": r"$\leqslant$", "⩾": r"$\geqslant$", "∶": r"$:$", "∙": r"$\cdot$",
    "∽": r"$\sim$",
}
B.SYMBOLS.update(EXTRA_SYMBOLS)
B.MATH_SYMBOLS.update(
    {k: v[1:-1] for k, v in EXTRA_SYMBOLS.items()
     if v.startswith("$") and v.endswith("$") and v.count("$") == 2})

VOLUMES = {
    "高数": {
        "src": "高数",
        "title": "高等数学",
        "book": "考研数学二 · 高等数学知识点手册",
        "sub": "按《考研数学二考试大纲》编排 · 五星重难点分级",
        "chapters": [
            ("G1", "函数极限连续"),
            ("G2", "一元函数微分学"),
            ("G3", "一元函数积分学"),
            ("G4", "多元函数微积分学"),
            ("G5", "常微分方程"),
            ("A1", "附录一 五星考点冲刺路线"),
            ("A2", "附录二 必背公式与结论速查"),
        ],
        "meta": [
            ("考查科目", "高等数学（数学二不考概率统计）"),
            ("分值占比", "约 80\\%（150 分中约 120 分）"),
            ("本册章节", "5 章，覆盖大纲高等数学全部条目"),
            ("分级方式", "$\\bigstar$ 五级：考频 $\\times$ 难度 $\\times$ 分值"),
            ("主要素材", "高等数学大讲义 · 喻老强化讲义 · 中值定理专题"),
            ("", "考研数学大观知识点 · 反常积分专题 · 数学二真题"),
        ],
    },
    "线代": {
        "src": "线代",
        "title": "线性代数",
        "book": "考研数学二 · 线性代数知识点手册",
        "sub": "按《考研数学二考试大纲》编排 · 五星重难点分级",
        "chapters": [
            ("L1", "行列式"),
            ("L2", "矩阵"),
            ("L3", "向量"),
            ("L4", "线性方程组"),
            ("L5", "特征值和特征向量"),
            ("L6", "二次型"),
            ("A1", "附录一 五星考点冲刺路线"),
            ("A2", "附录二 结论速查与易混对照"),
        ],
        "meta": [
            ("考查科目", "线性代数（数学二不考概率统计）"),
            ("分值占比", "约 20\\%（150 分中约 30 分）"),
            ("本册章节", "6 章，覆盖大纲线性代数全部条目"),
            ("分级方式", "$\\bigstar$ 五级：考频 $\\times$ 难度 $\\times$ 分值"),
            ("主要素材", "线性代数大讲义 · 线代强化/基础讲义"),
            ("", "考研数学大观知识点 · 线代公式 · 数学二真题"),
        ],
    },
}

TITLE_TMPL = r"""
\begin{titlepage}
\centering
\vspace*{2.6cm}
{\Huge\bfseries 考研数学二\par}
\vspace{0.5cm}
{\Huge\bfseries %(title)s知识点手册\par}
\vspace{0.9cm}
{\Large %(sub)s\par}
\vspace{1.8cm}
{\normalsize
\begin{tabular}{rl}
%(rows)s
\end{tabular}\par}
\vfill
{\small 本手册严格按《考研数学二考试大纲》顺序编排，每个考点标注五星重难点等级，供复习检索与精力分配使用。\par}
\vspace{1.0cm}
\end{titlepage}
"""

FRONT_TMPL = r"""
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


# 写手把 LaTeX 代码写进文件时，某些工具会把 "\b" "\a" "\v" 之类当成转义，
# 结果文件里留下 0x08+ "eta"（本该是 \beta）、0x07+"lpha"（本该是 \alpha）这类残留。
CTL_LETTER = {"\x07": "a", "\x08": "b", "\x0b": "v", "\x09": "t",
              "\x0c": "f", "\x0d": "r"}
KNOWN_MACROS = (
    "alpha beta gamma delta varepsilon zeta eta theta iota kappa lambda mu nu xi "
    "pi rho sigma tau upsilon varphi chi psi omega Gamma Delta Theta Lambda Xi Pi "
    "Sigma Phi Psi Omega partial nabla vert Vert lvert rvert left right langle "
    "rangle times frac dfrac tfrac sqrt begin end matrix pmatrix bmatrix vmatrix "
    "cases aligned array text mathbf mathrm mathcal textbf vec bar hat tilde dot "
    "binom forall exists infty cdot cdots ldots ddots vdots quad qquad le ge neq "
    "approx equiv subset supset cup cap varnothing to mapsto Rightarrow Leftarrow "
    "int iint oint sum prod lim ln log sin cos tan cot sec csc arcsin arccos "
    "arctan sinh cosh tanh hline toprule midrule bottomrule item"
).split()


CTL_BYTES = {0x07: b"a", 0x08: b"b", 0x0B: b"v", 0x09: b"t", 0x0C: b"f", 0x0D: b"r"}
_LETTER = set(b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")


def match_macro(cand: str) -> bool:
    for macro in KNOWN_MACROS:
        if cand == macro or cand.startswith(macro) or macro.startswith(cand):
            return True
    return False


def repair_ctl_bytes(raw: bytes) -> bytes:
    """在字节层面还原被当成转义序列吃掉的反斜杠（如 0x0D+"ight" -> "\\right"）。"""
    out = bytearray()
    i, n = 0, len(raw)
    while i < n:
        c = raw[i]
        if c in CTL_BYTES:
            j = i + 1
            while j < n and raw[j] in _LETTER:
                j += 1
            word = raw[i + 1:j].decode("ascii", "ignore")
            cand = CTL_BYTES[c].decode() + word
            if word and match_macro(cand):
                out += b"\\" + cand.encode()
                i = j
                continue
        out.append(c)
        i += 1
    return bytes(out)


def repair_right(md: str) -> str:
    """0x0D 被当成换行吃掉后，\right 会变成行首的 "ight"。"""
    out: list[str] = []
    for ln in md.split("\n"):
        if out and re.match(r"^\s*ight\b", ln) and "\\left" in "".join(out[-3:]):
            out[-1] = out[-1].rstrip() + "\\right" + re.sub(r"^\s*ight", "", ln)
            continue
        out.append(ln)
    return "\n".join(out)


def read_md(path: str) -> str:
    raw = open(path, "rb").read()
    return repair_right(repair_ctl_bytes(raw).decode("utf-8").replace("\r\n", "\n").replace("\r", "\n"))


def repair_ctl(md: str) -> str:
    def sub(m):
        ctl, word = m.group(1), m.group(2)
        cand = CTL_LETTER[ctl] + word
        for macro in KNOWN_MACROS:
            if cand == macro or cand.startswith(macro) or macro.startswith(cand):
                return "\\" + cand
        return ctl + word
    return re.sub(r"([\x07\x08\x09\x0b\x0c\x0d])([A-Za-z]+)", sub, md)


def normalize_m2(md: str) -> str:
    """去掉作者手写编号并标记不编号标题。

    与 408 版 build_book.normalize_chapter 的区别：**不做**"包装标题提升层级"的处理。
    本项目的章文件里 `## 一、函数` 是正常板块，若被提升会把 `##` 降成 `#`（渲染成乱码文本）。
    """
    out = []
    for ln in md.split("\n"):
        m = re.match(r"^(#{1,5})\s+(.*?)\s*$", ln)
        if m:
            level = max(2, len(m.group(1)))          # 误写的 # 一律当 ## 处理
            title = m.group(2)
            if any(k in title for k in B.UNNUMBERED):
                mark, title = "!", title
            else:
                mark, title = "", B.norm_numbering(title)
            if not title:
                continue
            out.append("#" * level + mark + " " + title)
        else:
            out.append(ln)
    return "\n".join(out)


def make_preamble(vol: dict) -> str:
    pre = B.PREAMBLE
    pre = pre.replace("408 考纲知识点手册", vol["book"])
    # 章标题 "第二章 一元函数微分学" 需要间距；408 版是 aftername={}
    pre = pre.replace(
        "aftername = {}, beforeskip = 0pt, afterskip = 18pt, pagestyle = plain",
        "aftername = {\\quad}, beforeskip = 0pt, afterskip = 18pt, pagestyle = plain")
    # 补几个写作中可能用到、但基础宏包没有的符号
    extra = r"""
\usepackage{graphicx}
\providecommand{\iddots}{\reflectbox{$\ddots$}}
\providecommand{\xlongequal}[1]{\xrightarrow{\ #1\ }}
\providecommand{\rank}{\operatorname{rank}}
\providecommand{\tr}{\operatorname{tr}}
"""
    pre = pre.replace("\\usepackage[hidelinks,bookmarksnumbered=true]{hyperref}",
                      "\\usepackage[hidelinks,bookmarksnumbered=true]{hyperref}" + extra)
    return pre


def make_title(vol: dict) -> str:
    rows = " \\\\\n".join(
        ("%s & %s" % (k, v)) if k else (" & %s" % v) for k, v in vol["meta"]
    )
    return TITLE_TMPL % {"title": vol["title"], "sub": vol["sub"], "rows": rows}


def build_volume(name: str) -> int:
    vol = VOLUMES[name]
    chapter_dir = os.path.join(SRC_ROOT, vol["src"])
    out_dir = os.path.join(BUILD_ROOT, name)
    os.makedirs(out_dir, exist_ok=True)
    out_tex = os.path.join(out_dir, "book.tex")

    B.UNNUMBERED = tuple(B.UNNUMBERED) + ("星级总表", "速查", "考点分布")
    body = [make_preamble(vol), make_title(vol), FRONT_TMPL]
    missing = []
    for code, title in vol["chapters"]:
        path = os.path.join(chapter_dir, "%s-%s.md" % (code, title))
        if not os.path.exists(path):
            cands = [f for f in sorted(os.listdir(chapter_dir)) if f.startswith(code)] \
                if os.path.isdir(chapter_dir) else []
            if cands:
                path = os.path.join(chapter_dir, cands[0])
        if not os.path.exists(path):
            missing.append(path)
            continue
        md = read_md(path)
        md = normalize_m2(repair_ctl(B.repair_source(md)))
        if code.startswith("A"):
            # 附录：不参与章节编号
            body.append("\\chapter*{%s}" % B.inline(title))
            body.append("\\addcontentsline{toc}{chapter}{%s}" % B.inline(title))
            body.append("\\markboth{%s}{%s}" % (B.inline(title), B.inline(title)))
        else:
            body.append("\\chapter{%s}" % B.inline(title))
            body.append("\\markboth{%s}{%s}" % (B.inline(title), B.inline(title)))
        body.append(B.convert(md))
    body.append("\\end{document}\n")
    open(out_tex, "w", encoding="utf-8").write("\n".join(body))

    if missing:
        print("[%s] 缺少章节文件：" % name)
        for m in missing:
            print("   ", m)
        return 1

    # 使用说明.tex 已由人工准备在 out_dir
    env = dict(os.environ)
    env["PATH"] = TEXBIN + ":" + env.get("PATH", "")
    for i in (1, 2, 3):
        r = subprocess.run(
            [os.path.join(TEXBIN, "xelatex"), "-interaction=nonstopmode",
             "-halt-on-error", "book.tex"],
            cwd=out_dir, env=env, capture_output=True, text=True)
    log_path = os.path.join(out_dir, "book.log")
    log = open(log_path, encoding="utf-8", errors="replace").read() if os.path.exists(log_path) else ""
    errs = [l for l in log.splitlines() if l.startswith("!")]
    miss = len(re.findall(r"Missing character", log))
    over = len(re.findall(r"Overfull", log))
    pages = 0
    m = re.search(r"Output written on book\.pdf \((\d+) pages", log)
    if m:
        pages = int(m.group(1))
    print("[%s] errors=%d missing_char=%d overfull=%d pages=%d"
          % (name, len(errs), miss, over, pages))
    for l in errs[:12]:
        print("    ", l)
    for l in log.splitlines():
        if "Missing character" in l:
            print("    ", l[:160])
    if errs:
        return 1
    print("     PDF:", os.path.join(out_dir, "book.pdf"))
    # 交付副本：与 408 手册同一种命名风格
    idx = 1 if name == "高数" else 2
    final = os.path.join(ROOT, "数学二考纲知识点手册-%d-%s.pdf" % (idx, vol["title"]))
    shutil.copyfile(os.path.join(out_dir, "book.pdf"), final)
    print("     交付:", os.path.basename(final))
    return 0


def main() -> int:
    names = sys.argv[1:] or list(VOLUMES)
    rc = 0
    for n in names:
        if n not in VOLUMES:
            print("未知分册:", n)
            return 2
        rc |= build_volume(n)
    return rc


if __name__ == "__main__":
    sys.exit(main())
