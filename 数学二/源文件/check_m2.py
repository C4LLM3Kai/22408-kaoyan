#!/usr/bin/env python3
"""数学二手册的质检脚本：星标一致性、公式配平、生僻字符、超纲内容。

用法：
    python3 check_m2.py            # 全部章节
    python3 check_m2.py G1 L3      # 只查指定章节
"""
from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_book as B  # noqa: E402

MASTER = os.path.join(HERE, "考点星级总表.md")

CH_MAP = {
    "G1": ("高数", "G1-函数极限连续.md", "### G1"),
    "G2": ("高数", "G2-一元函数微分学.md", "### G2"),
    "G3": ("高数", "G3-一元函数积分学.md", "### G3"),
    "G4": ("高数", "G4-多元函数微积分学.md", "### G4"),
    "G5": ("高数", "G5-常微分方程.md", "### G5"),
    "L1": ("线代", "L1-行列式.md", "### L1"),
    "L2": ("线代", "L2-矩阵.md", "### L2"),
    "L3": ("线代", "L3-向量.md", "### L3"),
    "L4": ("线代", "L4-线性方程组.md", "### L4"),
    "L5": ("线代", "L5-特征值和特征向量.md", "### L5"),
    "L6": ("线代", "L6-二次型.md", "### L6"),
}

BLACKLIST = ["无穷级数", "幂级数", "傅里叶", "三重积分", "曲线积分", "曲面积分",
             "高斯公式", "斯托克斯", "空间解析几何", "欧拉方程", "若尔当", "Jordan",
             "线性变换", "概率论", "数理统计", "方向导数"]

ALLOWED_EXTRA = set("，。、；：？！（）《》“”‘’—…·　－％＋＝［］｛｝【】・～")


def master_stars() -> dict[str, list[tuple[str, int]]]:
    """{chapter_code: [(考点名, 星数)]}"""
    out: dict[str, list[tuple[str, int]]] = {}
    cur = None
    for line in open(MASTER, encoding="utf-8"):
        m = re.match(r"^### ([GL]\d)", line.strip())
        if m:
            cur = m.group(1)
            out[cur] = []
            continue
        if cur and line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 3 and not set(cells[0]) <= set("-: "):
                stars = cells[2].count("★")
                name = cells[1]
                if stars and name not in ("考点", "考纲要求"):
                    out[cur].append((name, stars))
    return out


def check_unicode(path: str) -> list[str]:
    bad: dict[str, int] = {}
    for ch in open(path, encoding="utf-8").read():
        if ch in B.SYMBOLS or ch in ALLOWED_EXTRA or ch == "★":
            continue
        o = ord(ch)
        if o < 128 or 0x3000 <= o <= 0x303F or 0x4E00 <= o <= 0x9FFF or 0xFF00 <= o <= 0xFFEF:
            continue
        bad[ch] = bad.get(ch, 0) + 1
    return ["%s U+%04X ×%d" % (c, ord(c), n) for c, n in sorted(bad.items(), key=lambda x: -x[1])]


def check_dollars(text: str) -> list[str]:
    issues = []
    if len(re.findall(r"(?<!\$)\$\$(?!\$)", text)) % 2:
        issues.append("$$ 数量为奇数")
    for i, line in enumerate(text.split("\n"), 1):
        stripped = re.sub(r"\$\$[^$]*\$\$", "", line)
        # 行内 $ 必须成对（排除表格中的转义）
        if len(re.findall(r"(?<!\$)\$(?!\$)", stripped)) % 2:
            issues.append("第 %d 行行内 $ 不成对: %s" % (i, line.strip()[:70]))
    return issues


def check_tables(text: str) -> list[str]:
    """表格每行的竖线数必须一致，否则说明单元格里出现了裸 | （如 $|A|$）。"""
    import collections
    issues = []
    table: list[tuple[int, str]] = []
    for i, ln in enumerate(text.split("\n"), 1):
        if ln.strip().startswith("|"):
            table.append((i, ln))
            continue
        if table:
            counts = [l.count("|") for _, l in table]
            mode = collections.Counter(counts).most_common(1)[0][0]
            for (li, l), c in zip(table, counts):
                if c != mode:
                    issues.append("第 %d 行竖线数 %d（表格为 %d），单元格里可能有裸 | ：%s"
                                  % (li, c, mode, l.strip()[:70]))
            table = []
    return issues


def check_braces(text: str) -> list[str]:
    issues = []
    for env in ("pmatrix", "vmatrix", "bmatrix", "cases", "aligned", "array"):
        a = len(re.findall(r"\\begin\{%s\}" % env, text))
        b = len(re.findall(r"\\end\{%s\}" % env, text))
        if a != b:
            issues.append("%s 环境不配对 begin=%d end=%d" % (env, a, b))
    for opener, closer in (("{", "}"), ("$", "$")):
        pass
    if text.count("{") != text.count("}"):
        issues.append("花括号不配对 {=%d }=%d" % (text.count("{"), text.count("}")))
    return issues


def check_stars(code: str, text: str, master: dict) -> list[str]:
    issues = []
    want = master.get(code, [])
    heads = []
    for line in text.split("\n"):
        m = re.match(r"^####\s+(.*?)\s*$", line.strip())
        if m:
            heads.append((m.group(1), m.group(1).count("★")))
    if not heads:
        issues.append("没有任何 #### 考点标题")
    got_blob = " | ".join(n.replace(" ", "").replace("★", "").strip() for n, _ in heads)
    missing = [(n, s) for n, s in want if n.replace(" ", "") not in got_blob]
    # 名称对得上但星数不一致
    for name, stars in want:
        key = name.replace(" ", "")
        for hname, hstars in heads:
            if key and key in hname.replace(" ", ""):
                if hstars != stars:
                    issues.append("星数不一致：%s 总表=%d 正文=%d" % (name[:30], stars, hstars))
                break
    if missing:
        issues.append("总表考点未出现或名称不一致 %d 条：%s"
                      % (len(missing), "; ".join(n for n, _ in missing[:8])))
    for n, s in heads:
        if s == 0:
            issues.append("考点缺星标：%s" % n[:50])
    return issues


def check_blacklist(text: str) -> list[str]:
    hits = []
    for kw in BLACKLIST:
        for i, line in enumerate(text.split("\n"), 1):
            if kw in line:
                hits.append("第 %d 行出现「%s」: %s" % (i, kw, line.strip()[:70]))
    return hits


def main() -> int:
    codes = sys.argv[1:] or list(CH_MAP)
    master = master_stars()
    total_issues = 0
    for code in codes:
        sub, fname, key = CH_MAP[code]
        path = os.path.join(HERE, sub, fname)
        print("=" * 70)
        if not os.path.exists(path):
            print(code, "缺失:", path)
            total_issues += 1
            continue
        text = open(path, encoding="utf-8").read()
        chars = len(re.sub(r"\s", "", re.sub(r"\$[^$]*\$", "", text)))
        heads = len(re.findall(r"^####\s", text, re.M))
        print("%s  %s  字符≈%d  考点=%d" % (code, fname, chars, heads))
        groups = [
            ("星标/考点", check_stars(code, text, master)),
            ("公式", check_dollars(text) + check_braces(text) + check_tables(text)),            ("字符", check_unicode(path)),
            ("超纲", check_blacklist(text)),
        ]
        for label, issues in groups:
            for it in issues:
                print("  [%s] %s" % (label, it))
                total_issues += 1
    print("=" * 70)
    print("问题总数:", total_issues)
    return 0


if __name__ == "__main__":
    sys.exit(main())
