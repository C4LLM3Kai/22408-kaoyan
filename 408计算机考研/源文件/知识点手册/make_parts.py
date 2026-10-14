#!/usr/bin/env python3
"""Build and compile the four per-subject volumes of the 408 handbook."""
from __future__ import annotations

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "/Users/shaoyikai/Desktop/考研/408计算机考研/源文件/知识点手册"
OUT = os.path.join(HERE, "parts")
TEXBIN = "/Library/TeX/texbin"

VOLUMES = [
    (1, "数据结构"),
    (2, "计算机组成原理"),
    (3, "操作系统"),
    (4, "计算机网络"),
]


def run(cmd, cwd=None, env=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, env=env)


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    env = dict(os.environ)
    env["PATH"] = TEXBIN + ":" + env.get("PATH", "")
    fail = 0
    for idx, subject in VOLUMES:
        work = os.path.join(OUT, f"vol{idx}")
        os.makedirs(work, exist_ok=True)
        tex = os.path.join(work, "book.tex")
        r = run([sys.executable, os.path.join(HERE, "build_book.py"),
                 os.path.join(SRC, "chapters"), tex, "--part", str(idx)])
        print(f"[{idx}] {subject}: {r.stdout.strip().splitlines()[0] if r.stdout else r.stderr[-300:]}")
        if r.returncode:
            print(r.stderr[-2000:])
            fail += 1
            continue
        ok = True
        for i in (1, 2):
            r = run([os.path.join(TEXBIN, "xelatex"),
                     "-interaction=nonstopmode", "-halt-on-error", "book.tex"],
                    cwd=work, env=env)
            log = os.path.join(work, "book.log")
            txt = open(log, encoding="utf-8", errors="replace").read() if os.path.exists(log) else ""
            errs = [l for l in txt.splitlines() if l.startswith("!")]
            if errs:
                print("   ERROR:", errs[0][:160])
                ok = False
                break
        if not ok:
            fail += 1
            continue
        txt = open(os.path.join(work, "book.log"), encoding="utf-8", errors="replace").read()
        miss = len(re.findall(r"Missing character", txt))
        over = len(re.findall(r"Overfull \\hbox", txt))
        m = re.search(r"Output written on book\.pdf \((\d+) pages", txt)
        pages = int(m.group(1)) if m else 0
        dst = os.path.join(OUT, f"408考纲知识点手册-{idx}-{subject}.pdf")
        subprocess.run(["cp", os.path.join(work, "book.pdf"), dst], check=True)
        print(f"   pages={pages} missing_glyphs={miss} overfull_hbox={over} -> {os.path.basename(dst)}")
    return fail


if __name__ == "__main__":
    sys.exit(main())
