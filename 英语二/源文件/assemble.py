#!/usr/bin/env python3
"""把 /tmp/build/*.tex 片段拼成自包含的 LaTeX 单文件，并做版式后处理。"""
import re, os

BUILD = "/tmp/build"
ORDER = [
    "00_preamble.tex", "10_rubric.tex", "20_overview.tex", "30_static.tex",
    "40_dynamic.tex", "45_special.tex", "50_body2.tex", "55_body3.tex",
    "60_full.tex", "65_letter_overview.tex", "70_letter_p1.tex",
    "75_letter_p2.tex", "80_letter_p3.tex", "90_arsenal.tex",
    "95_improvements.tex", "98_appendix.tex",
]

s = "\n".join(open(os.path.join(BUILD, n), encoding="utf-8").read() for n in ORDER)

# ---- 1. 带圈数字等符号交给中文字体 ----
if "xeCJKDeclareCharClass" not in s:
    ins = ('% 带圈数字 ①②③ 等：Times New Roman 无此字形，交给中文字体渲染\n'
           '\\xeCJKDeclareCharClass{CJK}{"2460 -> "24FF}\n'
           '\\xeCJKDeclareCharClass{CJK}{"25A0 -> "25FF}\n\n')
    s = s.replace("\\begin{document}", ins + "\\begin{document}", 1)

SPEC_RE = re.compile(r"\{(?:\s*[LC]\{[0-9.]+cm\})+\s*\}?")

# ---- 2. 补全缺右花括号的 longtable 表头 ----
fixed = 0
pos = 0
while True:
    k = s.find("\\begin{longtable}", pos)
    if k < 0:
        break
    bs = k + len("\\begin{longtable}")
    if bs >= len(s) or s[bs] != "{":
        pos = bs
        continue
    m = SPEC_RE.match(s, bs)
    if not m:
        pos = bs + 1
        continue
    if not m.group(0).rstrip().endswith("}"):
        s = s[:m.end()] + "}" + s[m.end():]
        fixed += 1
        pos = m.end() + 1
    else:
        pos = m.end()
print("  补全表头花括号:", fixed)

# ---- 3. longtable 列宽总和不得超过版心 ----
TEXTWIDTH_CM = 17.0
TABCOLSEP_PT = 5.0
CM_PER_PT = 2.54 / 72.0

edits = []
pos = 0
while True:
    k = s.find("\\begin{longtable}", pos)
    if k < 0:
        break
    bs = k + len("\\begin{longtable}")
    m = SPEC_RE.match(s, bs)
    if not m:
        pos = bs + 1
        continue
    spec = m.group(0)[1:-1]          # 去掉外层花括号
    cols = re.findall(r"[LC]\{([0-9.]+)cm\}", spec)
    pos = m.end()
    if not cols:
        continue
    need = sum(float(c) for c in cols) + (2 * TABCOLSEP_PT * len(cols)) * CM_PER_PT
    if need <= TEXTWIDTH_CM:
        continue
    avail = TEXTWIDTH_CM - (2 * TABCOLSEP_PT * len(cols)) * CM_PER_PT
    kk = avail / sum(float(c) for c in cols)
    new = spec
    for c in cols:
        new = re.sub(r"([LC])\{%scm\}" % re.escape(c),
                     lambda mm, nw="%.2f" % (float(c) * kk): mm.group(1) + "{" + nw + "cm}",
                     new, count=1)
    edits.append((bs, m.end(), "{" + new + "}"))
    print("  缩放列宽: %-46s -> %s" % (spec, new))

for st, en, new in reversed(edits):
    s = s[:st] + new + s[en:]

# ---- 4. 空占位符 ----
s = s.replace("\\fillin{}", "\\fillin{此处填写题干事由}")
s = s.replace("并配中文。\\fillin{此处填写题干事由} 中写题干事由。", "并配中文；表中方括号处填写题干事由。")

# ---- 5. 中文正文里的 ASCII 双引号统一为中文弯引号 ----
out_lines = []
for ln in s.split("\n"):
    if "xeCJKDeclareCharClass" in ln:      # "\"2460 是十六进制写法，不能动
        out_lines.append(ln)
        continue
    if '"' in ln:
        buf, opening = [], True
        for ch in ln:
            if ch == '"':
                buf.append("\u201c" if opening else "\u201d")
                opening = not opening
            else:
                buf.append(ch)
        ln = "".join(buf)
    out_lines.append(ln)
s = "\n".join(out_lines)

with open(os.path.join(BUILD, "full.tex"), "w", encoding="utf-8") as f:
    f.write(s)
print("写出 full.tex：", len(s), "字符")

# ---- 5. 自检 ----
bad = [m.group(0) for m in re.finditer(r"\\begin\{longtable\}[^\n]*", s)
       if m.group(0).count("{") != m.group(0).count("}")]
print("表头括号不平衡:", len(bad), bad[:3])
print("空占位符:", s.count("\\fillin{}"))
