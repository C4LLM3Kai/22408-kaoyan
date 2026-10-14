#!/usr/bin/env python3
"""把 22408 一页纸笔记的 Markdown 编译成可打印的 A4 单页 PDF。

用法：
    python3 build_note.py note.md out.pdf [--tex out.tex] [--title 弧长公式] \
        [--subject 数学二] [--topic 高等数学·定积分应用] [--footer 文字] \
        [--keep-aux] [--allow-multipage]

行为：
    1. 读取 Markdown，转成自包含 XeLaTeX 文档（导言区来自 assets/note-preamble.tex）
    2. 用 XeLaTeX 编译两遍（ASCII 临时文件名，避免中文日志名问题）
    3. 校验：页数必须为 1；检查缺字（Missing character）与溢出（Overfull）
    4. 渲染每页 PNG 预览，输出 JSON 报告

退出码：0 成功；1 编译失败；2 页数超限（需精简）；3 缺字
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREAMBLE = HERE.parent / "assets" / "note-preamble.tex"

DOC_HEAD = r"""\documentclass[%(size)s,a4paper]{ctexart}
\input{%(preamble)s}
\renewcommand{\NoteFooter}{%(footer)s}
\linespread{%(spread)s}
\begin{document}
"""

DOC_TAIL = r"""
\end{document}
"""

MATH_PLACEHOLDER = "\x00MATH%d\x00"
CODE_PLACEHOLDER = "\x00CODE%d\x00"

LATEX_ESCAPES = [
    ("\\", r"\textbackslash{}"),
    ("&", r"\&"),
    ("%", r"\%"),
    ("$", r"\$"),
    ("#", r"\#"),
    ("_", r"\_"),
    ("{", r"\{"),
    ("}", r"\}"),
    ("~", r"\textasciitilde{}"),
    ("^", r"\textasciicircum{}"),
]

# 允许直接透传的 LaTeX 命令（作者显式书写的排版指令）
RAW_COMMANDS = ("\\sechead", "\\notebox", "\\warnline", "\\notetitle")


def escape_text(text: str) -> str:
    for src, dst in LATEX_ESCAPES:
        text = text.replace(src, dst)
    return text


def inline(text: str) -> str:
    """处理行内标记：`code`、$math$、**bold**、*em*，其余文本转义。"""
    store_math: list[str] = []
    store_code: list[str] = []

    def stash_math(match: re.Match[str]) -> str:
        store_math.append(match.group(1))
        return MATH_PLACEHOLDER % (len(store_math) - 1)

    def stash_code(match: re.Match[str]) -> str:
        store_code.append(match.group(1))
        return CODE_PLACEHOLDER % (len(store_code) - 1)

    # 先取出行内公式与行内代码，避免被转义
    text = re.sub(r"(?<!\\)\$(.+?)(?<!\\)\$", stash_math, text)
    text = re.sub(r"`([^`]+)`", stash_code, text)

    if not any(cmd in text for cmd in RAW_COMMANDS):
        text = escape_text(text)

    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"\\emph{\1}", text)

    for index, value in enumerate(store_code):
        text = text.replace(CODE_PLACEHOLDER % index, r"\texttt{%s}" % escape_text(value))
    for index, value in enumerate(store_math):
        text = text.replace(MATH_PLACEHOLDER % index, "$%s$" % value)
    return text


def render_table(rows: list[str]) -> str:
    """把 Markdown 表格渲染成无竖线的三线表。"""
    def cells(line: str) -> list[str]:
        line = line.strip()
        line = line[1:] if line.startswith("|") else line
        line = line[:-1] if line.endswith("|") else line
        return [c.strip() for c in line.split("|")]

    header = cells(rows[0])
    body = [cells(r) for r in rows[2:]]
    columns = max(len(header), max((len(r) for r in body), default=0))
    spec = "@{}" + "".join(">{\\raggedright\\arraybackslash}X" for _ in range(columns)) + "@{}"

    out = [r"\begin{center}\small", r"\begin{tabularx}{\linewidth}{%s}" % spec, r"\toprule"]
    out.append(" & ".join(inline(c) for c in header) + r" \\")
    out.append(r"\midrule")
    for row in body:
        padded = row + [""] * (columns - len(row))
        out.append(" & ".join(inline(c) for c in padded) + r" \\")
    out += [r"\bottomrule", r"\end{tabularx}", r"\end{center}"]
    return "\n".join(out)


def convert(markdown: str, meta: dict[str, str]) -> str:
    lines = markdown.splitlines()
    body: list[str] = []
    index = 0
    list_mode: str | None = None
    columns_open = False

    def close_list() -> None:
        nonlocal list_mode
        if list_mode:
            body.append(r"\end{%s}" % list_mode)
            list_mode = None

    def open_list(kind: str) -> None:
        nonlocal list_mode
        if list_mode != kind:
            close_list()
            body.append(r"\begin{%s}" % kind)
            list_mode = kind

    while index < len(lines):
        raw = lines[index]
        line = raw.rstrip()
        stripped = line.strip()

        # ---- 空行：结束列表 ----
        if not stripped:
            close_list()
            index += 1
            continue

        # ---- 分栏标记 ----
        if stripped in ("[[cols2]]", "[[columns2]]"):
            close_list()
            body.append(r"\begin{multicols}{2}")
            columns_open = True
            index += 1
            continue
        if stripped in ("[[/cols2]]", "[[/columns2]]"):
            close_list()
            body.append(r"\end{multicols}")
            columns_open = False
            index += 1
            continue

        # ---- 代码块 ----
        if stripped.startswith("```"):
            close_list()
            language = stripped[3:].strip()
            chunk: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                chunk.append(lines[index])
                index += 1
            index += 1  # 跳过结束围栏
            if language and language.lower() not in ("text", "plain", "c"):
                body.append(r"\codecaption{%s}" % escape_text(language))
            body.append("\\begin{codebox}\n%s\n\\end{codebox}"
                        % "\n".join(chunk).rstrip())
            continue

        # ---- 标题 ----
        if stripped.startswith("# "):
            index += 1
            continue  # 标题由 meta 提供
        if stripped.startswith("## "):
            close_list()
            body.append(r"\sechead{%s}" % inline(stripped[3:].strip()))
            index += 1
            continue
        if stripped.startswith("### "):
            close_list()
            body.append(r"\par\addvspace{2pt}\noindent\textbf{%s}\par"
                        % inline(stripped[4:].strip()))
            index += 1
            continue

        # ---- 表格 ----
        if stripped.startswith("|") and index + 1 < len(lines) \
                and re.match(r"^\|[\s:|-]+\|$", lines[index + 1].strip()):
            close_list()
            block = [stripped]
            index += 1
            while index < len(lines) and lines[index].strip().startswith("|"):
                block.append(lines[index].strip())
                index += 1
            body.append(render_table(block))
            continue

        # ---- 结论条 / 提醒 ----
        if stripped.startswith("> "):
            close_list()
            body.append(r"\notebox{%s}" % inline(stripped[2:].strip()))
            index += 1
            continue
        if stripped.startswith("! "):
            close_list()
            body.append(r"\warnline{%s}" % inline(stripped[2:].strip()))
            index += 1
            continue

        # ---- 分隔线 ----
        if re.fullmatch(r"(-{3,}|\*{3,})", stripped):
            close_list()
            body.append(r"\par\addvspace{3pt}\noindent{\color{line}\hrule height 0.4pt}"
                        r"\par\addvspace{3pt}")
            index += 1
            continue

        # ---- 行间公式 ----
        if stripped.startswith("$$"):
            close_list()
            chunk: list[str] = []
            remainder = stripped[2:]
            if remainder.endswith("$$") and len(remainder) > 2:
                chunk.append(remainder[:-2])
            else:
                if remainder:
                    chunk.append(remainder)
                index += 1
                while index < len(lines) and "$$" not in lines[index]:
                    chunk.append(lines[index])
                    index += 1
                if index < len(lines):
                    chunk.append(lines[index].split("$$")[0])
            body.append("\\[\n%s\n\\]" % "\n".join(chunk).strip())
            index += 1
            continue

        # ---- 列表 ----
        bullet = re.match(r"^[-*+]\s+(.*)$", stripped)
        ordered = re.match(r"^(\d+)[.)]\s+(.*)$", stripped)
        if bullet:
            open_list("itemize")
            body.append(r"\item %s" % inline(bullet.group(1)))
            index += 1
            continue
        if ordered:
            open_list("enumerate")
            body.append(r"\item %s" % inline(ordered.group(2)))
            index += 1
            continue

        # ---- 普通段落 ----
        close_list()
        body.append(inline(stripped))
        index += 1

    close_list()
    if columns_open:
        body.append(r"\end{multicols}")

    title = meta.get("title", "22408 笔记")
    subject = meta.get("subject", "")
    topic = meta.get("topic", "")
    header = "\\notetitle{%s}{%s}{%s}" % (
        inline(title), inline(subject), inline(topic))
    return header + "\n" + "\n\n".join(body) + "\n"


def parse_meta(markdown: str) -> tuple[dict[str, str], str]:
    meta: dict[str, str] = {}
    body = markdown
    if markdown.lstrip().startswith("---"):
        text = markdown.lstrip()
        end = text.find("\n---", 3)
        if end != -1:
            front = text[3:end]
            body = text[end + 4:]
            for line in front.splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    meta[key.strip()] = value.strip().strip('"').strip("'")
    if not meta.get("title"):
        for line in body.splitlines():
            if line.strip().startswith("# "):
                meta["title"] = line.strip()[2:].strip()
                break
    return meta, body


def find_compiler() -> str | None:
    for name in ("xelatex", "lualatex"):
        found = shutil.which(name)
        if found:
            return found
    for candidate in (
        "/Library/TeX/texbin/xelatex",
        "/usr/local/texlive/2026basic/bin/universal-darwin/xelatex",
        "/opt/homebrew/bin/xelatex",
    ):
        if Path(candidate).exists():
            return candidate
    return None


def compile_pdf(tex_source: Path, output: Path, keep_aux: bool) -> tuple[bool, str]:
    compiler = find_compiler()
    if compiler is None:
        raise SystemExit("找不到 xelatex/lualatex，PDF 未生成")
    workdir = tex_source.parent if keep_aux else tempfile.mkdtemp(prefix="22408-note-")
    build = Path(workdir)
    build.mkdir(parents=True, exist_ok=True)
    local_tex = build / "note.tex"
    shutil.copyfile(tex_source, local_tex)
    log = ""
    for _ in range(2):
        result = subprocess.run(
            [compiler, "-interaction=nonstopmode", "-halt-on-error", "note.tex"],
            cwd=build, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", check=False)
        log = result.stdout
        if result.returncode:
            return False, log
    pdf = build / "note.pdf"
    if not pdf.is_file() or pdf.stat().st_size == 0:
        return False, log or "编译器没有产出 PDF"
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(pdf, output)
    return True, log


def _load_pymupdf():
    """优先用本机 pymupdf；缺失时回退到 skill 自带的 .venv。"""
    try:
        import pymupdf  # type: ignore
        return pymupdf
    except ImportError:
        pass
    try:
        import fitz as pymupdf  # type: ignore
        return pymupdf
    except ImportError:
        pass
    venv_site = sorted((HERE.parent / ".venv" / "lib").glob("python*/site-packages"))
    for site in venv_site:
        if str(site) not in sys.path:
            sys.path.insert(0, str(site))
        try:
            import pymupdf  # type: ignore
            return pymupdf
        except ImportError:
            continue
    return None


def inspect_pdf(path: Path, log: str) -> dict[str, object]:
    report: dict[str, object] = {"pages": None, "missing_chars": [], "overfull": [],
                                 "fill_ratio": None, "preview": []}
    missing = sorted(set(re.findall(r"Missing character: There is no (.+?) in font", log)))
    report["missing_chars"] = missing
    report["overfull"] = re.findall(r"Overfull \\hbox \(([\d.]+)pt too wide\)", log)
    pymupdf = _load_pymupdf()
    if pymupdf is None:
        report["note"] = "未安装 PyMuPDF，跳过页数与预览检查"
        return report
    doc = pymupdf.open(path)
    report["pages"] = doc.page_count
    preview_dir = path.parent / "preview"
    preview_dir.mkdir(parents=True, exist_ok=True)
    images = []
    for number, page in enumerate(doc, start=1):
        target = preview_dir / f"{path.stem}-p{number}.png"
        page.get_pixmap(dpi=130).save(target)
        images.append(str(target))
    # 版面填充率：正文最后一处墨迹的位置（排除页脚带），用来判断该放大还是缩小字号
    first = doc[0]
    pixmap = first.get_pixmap(dpi=72, colorspace=pymupdf.csGRAY)
    samples = pixmap.samples
    stride = pixmap.stride
    limit = int(pixmap.height * 0.90)  # 页脚所在带，不参与统计
    last_ink = 0
    for y in range(min(limit, pixmap.height - 1), -1, -1):
        row = samples[y * stride:(y + 1) * stride]
        if row and min(row) < 235:
            last_ink = y
            break
    if pixmap.height:
        report["fill_ratio"] = round(last_ink / pixmap.height, 3)
    report["preview"] = images
    doc.close()
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="22408 一页纸笔记编译器")
    parser.add_argument("markdown", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--tex", type=Path, default=None, help="保留的 .tex 路径")
    parser.add_argument("--title")
    parser.add_argument("--subject")
    parser.add_argument("--topic")
    parser.add_argument("--footer")
    parser.add_argument("--keep-aux", action="store_true", help="把 .tex/.log 留在输出目录")
    parser.add_argument("--allow-multipage", action="store_true", help="允许超过一页（默认拒绝）")
    parser.add_argument("--size", default=None, choices=["10pt", "11pt", "12pt"],
                        help="正文字号；一页放不满时加大，溢出时减小")
    parser.add_argument("--auto-fit", action="store_true",
                        help="自动在 11pt/12pt/10pt 中挑最大的、仍能单页排下的字号")
    parser.add_argument("--linespread", type=float, default=None, help="行距倍数，默认 1.14")
    args = parser.parse_args()

    markdown = args.markdown.read_text(encoding="utf-8")
    meta, body = parse_meta(markdown)
    for key in ("title", "subject", "topic", "footer"):
        value = getattr(args, key)
        if value:
            meta[key] = value
    footer = meta.get("footer", "22408 一页纸笔记")
    if meta.get("subject") and "footer" not in meta:
        footer = f"22408 一页纸笔记 · {meta['subject']}"

    content = convert(body, meta)
    spread = args.linespread or float(meta.get("linespread", 1.14))
    tex_path = args.tex or (args.output.parent / "源文件" / (args.output.stem + ".tex"))
    tex_path.parent.mkdir(parents=True, exist_ok=True)

    def write_tex(size: str) -> None:
        tex_path.write_text(DOC_HEAD % {
            "preamble": PREAMBLE,
            "footer": escape_text(footer),
            "size": size,
            "spread": spread,
        } + content + DOC_TAIL, encoding="utf-8")

    if args.auto_fit:
        candidates = ["12pt", "11pt", "10pt"]
    else:
        candidates = [args.size or meta.get("size", "11pt")]

    compiled = False
    log = ""
    report: dict[str, object] = {}
    chosen = candidates[-1]
    for size in candidates:
        chosen = size
        write_tex(size)
        compiled, log = compile_pdf(tex_path, args.output, args.keep_aux)
        if not compiled:
            break
        report = inspect_pdf(args.output, log)
        pages = report.get("pages")
        if pages == 1 or args.allow_multipage or pages is None:
            break
    write_tex(chosen)  # 保证 .tex 与最终 PDF 的字号一致

    log_path = tex_path.with_suffix(".log")
    log_path.write_text(log, encoding="utf-8")
    if not compiled:
        print("编译失败，日志尾部：\n" + "\n".join(log.splitlines()[-25:]), file=sys.stderr)
        return 1

    report = inspect_pdf(args.output, log)
    report.update({"pdf": str(args.output), "tex": str(tex_path), "log": str(log_path),
                   "size": chosen})
    print(json.dumps(report, ensure_ascii=False, indent=2))

    pages = report.get("pages")
    if isinstance(pages, int) and pages > 1 and not args.allow_multipage:
        print(f"页数为 {pages}，超出一页，请精简内容后重编译", file=sys.stderr)
        return 2
    if report.get("missing_chars"):
        print("存在缺字，请更换字体或改写字符", file=sys.stderr)
        return 3
    fill = report.get("fill_ratio")
    if isinstance(fill, float) and fill < 0.80:
        print(f"提示：版面只用到 {fill:.0%}，可加 --auto-fit 放大字号或补充内容",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
