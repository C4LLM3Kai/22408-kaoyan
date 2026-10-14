#!/usr/bin/env python3
"""一页纸笔记的环境自检：编译器、中文字体、依赖包、预览渲染。

用法：
    python3 doctor.py [--fix-hint]

任何一项 fail 都会给出可执行的修复建议。退出码 0 表示全绿。
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREAMBLE = HERE.parent / "assets" / "note-preamble.tex"

COMPILER_CANDIDATES = [
    "/Library/TeX/texbin/xelatex",
    "/usr/local/texlive/2026basic/bin/universal-darwin/xelatex",
    "/opt/homebrew/bin/xelatex",
    "/usr/local/bin/xelatex",
]

PACKAGES = [
    "ctexart.cls", "xeCJK.sty", "fontspec.sty", "geometry.sty",
    "amsmath.sty", "amssymb.sty", "array.sty", "booktabs.sty",
    "tabularx.sty", "xcolor.sty", "enumitem.sty", "needspace.sty",
    "fancyhdr.sty", "multicol.sty", "graphicx.sty", "hyperref.sty",
]

FONTS = ["Songti SC", "Heiti SC", "Times New Roman"]


def find_compiler() -> str | None:
    found = shutil.which("xelatex") or shutil.which("lualatex")
    if found:
        return found
    for candidate in COMPILER_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    return None


def main() -> int:
    failures: list[str] = []

    compiler = find_compiler()
    if compiler:
        version = subprocess.run([compiler, "--version"], capture_output=True, text=True).stdout
        print(f"[ok]   编译器：{compiler}")
        print(f"       {version.splitlines()[0] if version else ''}")
    else:
        print("[fail] 找不到 xelatex / lualatex")
        print("       修复：安装 TeX Live（brew install --cask mactex-no-gui），"
              "或把 /Library/TeX/texbin 加入 PATH")
        failures.append("compiler")

    kpsewhich = shutil.which("kpsewhich")
    if kpsewhich is None and compiler:
        candidate = Path(compiler).parent / "kpsewhich"
        kpsewhich = str(candidate) if candidate.exists() else None
    if compiler and kpsewhich is None:
        print("[warn] 找不到 kpsewhich，跳过宏包检查")
    elif kpsewhich:
        for package in PACKAGES:
            result = subprocess.run([kpsewhich, package], capture_output=True, text=True)
            if result.stdout.strip():
                print(f"[ok]   {package}")
            else:
                print(f"[fail] {package} 缺失")
                print(f"       修复：tlmgr install {package.rsplit('.', 1)[0]}")
                failures.append(package)

    font_check = subprocess.run(
        ["system_profiler", "SPFontsDataType"], capture_output=True, text=True).stdout
    for font in FONTS:
        if font in font_check:
            print(f"[ok]   字体：{font}")
        else:
            print(f"[fail] 字体缺失：{font}")
            print("       修复：在「字体册」中启用该字体，或改用系统已有字体并同步修改 "
                  "assets/note-preamble.tex")
            failures.append(font)

    try:
        import pymupdf  # noqa: F401
        print("[ok]   PyMuPDF（用于页数校验与预览渲染）")
    except ImportError:
        try:
            import fitz  # noqa: F401
            print("[ok]   PyMuPDF（fitz 兼容名）")
        except ImportError:
            print("[warn] 未安装 PyMuPDF：仍可编译 PDF，但无法自动校验页数与渲染预览")
            print("       修复：pip3 install pymupdf")

    if not PREAMBLE.is_file():
        print(f"[fail] 缺少导言区模板：{PREAMBLE}")
        failures.append("preamble")

    if failures:
        print(f"\n{len(failures)} 项未通过，先修复再产出 PDF。")
        return 1
    print("\n环境就绪，可以编译一页纸笔记。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
