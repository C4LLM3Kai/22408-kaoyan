#!/usr/bin/env python3
"""Build + compile the 408 knowledge-point handbook."""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "/Users/shaoyikai/Desktop/考研/408计算机考研/源文件/知识点手册"
OUT = os.path.join(HERE, "book")
TEXBIN = "/Library/TeX/texbin"


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def main() -> int:
    only = sys.argv[1:] or None
    os.makedirs(OUT, exist_ok=True)
    env = dict(os.environ)
    env["PATH"] = TEXBIN + ":" + env.get("PATH", "")

    r = run([sys.executable, os.path.join(HERE, "build_book.py"),
             os.path.join(SRC, "chapters"), os.path.join(OUT, "book.tex")] +
            (["--only"] + only if only else []))
    print(r.stdout.strip())
    if r.returncode:
        print(r.stderr[-3000:])
        return 1

    for i in (1, 2):
        r = run([os.path.join(TEXBIN, "xelatex"),
                 "-interaction=nonstopmode", "-halt-on-error", "book.tex"],
                cwd=OUT, env=env)
        log = os.path.join(OUT, "book.log")
        txt = open(log, encoding="utf-8", errors="replace").read() if os.path.exists(log) else ""
        errs = [l for l in txt.splitlines() if l.startswith("!")]
        print(f"[pass {i}] exit={r.returncode} errors={len(errs)}")
        if errs:
            for l in errs[:10]:
                print("   ", l)
            return 1

    txt = open(os.path.join(OUT, "book.log"), encoding="utf-8", errors="replace").read()
    miss = len(re.findall(r"Missing character", txt))
    over = len(re.findall(r"Overfull", txt))
    under = len(re.findall(r"Underfull", txt))
    pages = 0
    m = re.search(r"Output written on book\.pdf \((\d+) pages", txt)
    if m:
        pages = int(m.group(1))
    print(f"missing_characters={miss} overfull={over} underfull={under} pages={pages}")
    for l in txt.splitlines():
        if "Overfull" in l and "hbox" in l:
            print("   ", l[:150])
    print("PDF:", os.path.join(OUT, "book.pdf"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
