#!/usr/bin/env python3
"""一页纸笔记的编译前检查：在花时间编译前，先挡住会导致失败或超页的问题。

用法：
    python3 check_note.py note.md [--subject 数学二]

检查项：
    1. frontmatter 必填字段（title / subject）
    2. 行内与行间公式的 $ 配对
    3. 常用但本管线不支持的宏（\\begin{align} 等）与缺字风险字符
    4. 篇幅预算：按学科给出字符上限，超出则警告（大概率超一页）
    5. 结构：至少 2 个小节；不允许 TODO/待补

退出码：0 通过；1 有错误；4 仅警告。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BUDGET = {
    "数学一": 3000, "数学二": 3000, "数学三": 3000,
    "408": 3400, "计算机": 3400,
    "英语一": 2600, "英语二": 2600,
    "政治": 3200,
    "default": 3000,
}

UNSUPPORTED = [
    (r"\\begin\{align", "行间公式请用 $$...$$，不要用 align 环境"),
    (r"\\begin\{equation", "行间公式请用 $$...$$，不要用 equation 环境"),
    (r"\\begin\{tikz", "一页纸笔记不放 tikz 图，改用文字/表格表达"),
    (r"\\includegraphics", "一页纸笔记不放外部图片"),
    (r"\\cite\{", "笔记不引用文献，直接写来源名称"),
    (r"\\label\{", "笔记不用交叉引用"),
    (r"\\usepackage", "不要写导言区命令，样式已由模板提供"),
    (r"\\documentclass", "不要写导言区命令"),
    (r"\\begin\{document\}", "不要写导言区命令"),
    (r"\\part\{|\\chapter\{", "一页纸不用 part/chapter，请用 ## 小节"),
]

# 缺字风险字符。注意：≤ ≥ √ ∞ → ①②③ ★ 希腊字母等已由导言区的
# \xeCJKDeclareCharClass 交给中文字体，可以安全使用；这里只列真正渲染不出来的。
RISKY = {
    "✅": "改写成「对」或 $\\checkmark$",
    "❌": "改写成「错」",
    "🔥": "删掉，一页纸不放 emoji",
    "📌": "删掉，一页纸不放 emoji",
    "💡": "删掉，一页纸不放 emoji",
    "⚠️": "改用「注意」两个字",
    "～": "用 \\sim 或改为「到」",
    "㎡": "改用 $\\mathrm{m}^2$",
}


def check(path: Path, subject: str | None) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    meta: dict[str, str] = {}
    body = text
    if text.lstrip().startswith("---"):
        stripped = text.lstrip()
        end = stripped.find("\n---", 3)
        if end == -1:
            errors.append("frontmatter 没有闭合的 ---")
        else:
            for line in stripped[3:end].splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    meta[key.strip()] = value.strip()
            body = stripped[end + 4:]

    if not meta.get("title") and not re.search(r"^#\s+\S", body, re.M):
        errors.append("缺少标题：frontmatter 里写 title，或正文首行写 # 标题")
    if not meta.get("subject") and not subject:
        warnings.append("建议在 frontmatter 写 subject（决定页脚与归档目录）")

    # 公式配对
    inline_math = re.findall(r"(?<!\\)\$", body)
    if len(inline_math) % 2:
        errors.append(f"行内公式 $ 数量为奇数（{len(inline_math)}），存在未闭合的 $")
    if body.count("$$") % 2:
        errors.append("行间公式 $$ 数量为奇数，存在未闭合的 $$")

    for pattern, message in UNSUPPORTED:
        if re.search(pattern, body):
            errors.append(message)

    for char, hint in RISKY.items():
        if char in body:
            warnings.append(f"发现字符「{char}」有缺字风险：{hint}")

    for token in ("TODO", "待补", "XXX", "略"):
        if token in body:
            warnings.append(f"发现占位内容「{token}」，交付前请补全")

    sections = re.findall(r"^##\s+\S", body, re.M)
    if len(sections) < 2:
        warnings.append(f"只有 {len(sections)} 个小节，一页纸通常需要 3–5 个小节")

    key = subject or meta.get("subject", "")
    budget = BUDGET.get("default", 3000)
    for name, limit in BUDGET.items():
        if name != "default" and name in key:
            budget = limit
            break
    length = len(re.sub(r"\s+", "", body))
    if length > budget:
        warnings.append(f"正文约 {length} 字，超过 {key or '默认'} 的 {budget} 字预算，很可能超一页")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="一页纸笔记编译前检查")
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--subject")
    args = parser.parse_args()

    errors, warnings = check(args.markdown, args.subject)
    for item in warnings:
        print(f"[warn] {item}")
    for item in errors:
        print(f"[error] {item}")
    if errors:
        return 1
    if warnings:
        return 4
    print("[ok] 检查通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
