import pymupdf, os, subprocess, sys, glob
SRC = "/Users/shaoyikai/Desktop/考研/408计算机考研/强化笔记"
OUT = "/Users/shaoyikai/Desktop/考研/.work/ocr-strong"
os.makedirs(OUT, exist_ok=True)
OCR = "/Users/shaoyikai/Desktop/考研/.work/ocr"
for pdf in sorted(glob.glob(os.path.join(SRC, "*.pdf"))):
    base = os.path.splitext(os.path.basename(pdf))[0]
    tmp = os.path.join(OUT, "_pages_" + base)
    os.makedirs(tmp, exist_ok=True)
    d = pymupdf.open(pdf)
    n = d.page_count
    print(f"[{base}] {n} pages", flush=True)
    imgs = []
    for i in range(n):
        p = os.path.join(tmp, f"p{i+1:04d}.png")
        imgs.append(p)
        if not os.path.exists(p):
            d[i].get_pixmap(dpi=180).save(p)
    # OCR in chunks to bound argv length
    outfile = os.path.join(OUT, base + ".txt")
    with open(outfile, "w") as fh:
        CH = 40
        for k in range(0, len(imgs), CH):
            chunk = imgs[k:k+CH]
            r = subprocess.run([OCR] + chunk, capture_output=True, text=True)
            fh.write(r.stdout)
            print(f"  {base}: {k+len(chunk)}/{len(imgs)}", flush=True)
    for p in imgs:
        os.remove(p)
    os.rmdir(tmp)
    print(f"  -> {outfile} ({os.path.getsize(outfile)} bytes)", flush=True)
print("ALL DONE", flush=True)
