#!/usr/bin/env python3
"""把文件列表按体积装箱成批次，规避 GitHub 单次 pack 2 GiB 硬上限。

用法:
    plan_batches.py <listfile(NUL分隔)> <outdir> [cap_mib]

输出:
    <outdir>/b1.nul, b2.nul, ...  每个文件是 NUL 分隔的路径清单
"""
import os
import sys
import shutil


def main():
    if len(sys.argv) < 3:
        print("用法: plan_batches.py <listfile> <outdir> [cap_mib]", file=sys.stderr)
        return 2

    listfile, outdir = sys.argv[1], sys.argv[2]
    cap = int(sys.argv[3]) * 1024 * 1024 if len(sys.argv) > 3 else 900 * 1024 * 1024

    raw = open(listfile, "rb").read()
    names = [n.decode("utf-8", "surrogateescape") for n in raw.split(b"\0") if n]

    files = []
    for n in names:
        try:
            files.append((n, os.path.getsize(n)))
        except OSError:
            files.append((n, 0))

    total = sum(s for _, s in files)

    # 递减首次适应装箱：大文件优先，尽量填满每批
    files.sort(key=lambda x: -x[1])
    batches = []
    for n, s in files:
        for b in batches:
            if b["size"] + s <= cap:
                b["items"].append(n)
                b["size"] += s
                break
        else:
            batches.append({"items": [n], "size": s})

    shutil.rmtree(outdir, ignore_errors=True)
    os.makedirs(outdir, exist_ok=True)

    for i, b in enumerate(batches, 1):
        with open(os.path.join(outdir, "b%d.nul" % i), "wb") as f:
            for n in b["items"]:
                f.write(n.encode("utf-8", "surrogateescape") + b"\0")
        print("  批次 %d: %5d 个文件  %8.1f MiB"
              % (i, len(b["items"]), b["size"] / 2 ** 20))

    print("  共 %d 批，合计 %.2f GiB" % (len(batches), total / 2 ** 30))

    # 自检：每个文件恰好分配一次
    seen = []
    for i in range(1, len(batches) + 1):
        seen += [x for x in open(os.path.join(outdir, "b%d.nul" % i), "rb").read().split(b"\0") if x]
    assert len(seen) == len(files), "覆盖不全: %d vs %d" % (len(seen), len(files))
    assert len(set(seen)) == len(seen), "存在重复分配"
    return 0


if __name__ == "__main__":
    sys.exit(main())
