#!/usr/bin/env python3
"""Extract every document of the Yuque book 「计算机考研408笔记」 as Markdown.

Uses the running Yuque desktop renderer (via CDP over the devtools pipe) so the
request carries the logged-in session cookies. Writes one .md per doc plus an
index JSON.
"""
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from yuque_cdp import PipeCDP

BOOK_ID = 48597829
BOOK_SLUG = "hnlngb"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yuque-notes")


def safe(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|\n\r\t]', "_", name).strip()
    return name[:80] or "untitled"


def main():
    os.makedirs(OUT, exist_ok=True)
    c = PipeCDP()
    try:
        time.sleep(8)
        pages = [t for t in c.targets() if t["type"] == "page"]
        if not pages:
            raise SystemExit("no page target")
        sid = c.attach(pages[0]["targetId"])
        c.send("Runtime.enable", session_id=sid)
        time.sleep(1)

        # 1) document list
        listing = c.eval(
            f"""(async () => {{
              const r = await fetch('/api/books/{BOOK_ID}/docs?limit=1000', {{credentials:'include'}});
              const j = await r.json();
              return JSON.stringify(j.data.map(d => ({{id:d.id, slug:d.slug, title:d.title,
                 parent:d.parent_uuid||null, uuid:d.uuid||null, depth:d.depth,
                 word:d.word_count, updated:d.content_updated_at}})));
            }})()""",
            sid,
            timeout=120,
        )
        docs = json.loads(listing)
        print(f"docs listed: {len(docs)}", flush=True)
        json.dump(docs, open(os.path.join(OUT, "_index.json"), "w"), ensure_ascii=False, indent=1)

        # 2) each doc as markdown
        manifest = []
        for i, d in enumerate(docs, 1):
            slug, title = d["slug"], d["title"]
            fn = f"{i:03d}-{safe(title)}.md"
            path = os.path.join(OUT, fn)
            if os.path.exists(path) and os.path.getsize(path) > 0:
                manifest.append({"order": i, "id": d["id"], "slug": slug, "title": title,
                                 "file": fn, "bytes": os.path.getsize(path), "cached": True})
                print(f"[{i}/{len(docs)}] cached {title}", flush=True)
                continue
            try:
                body = c.eval(
                    f"""(async () => {{
                      const r = await fetch('/api/docs/{slug}?book_id={BOOK_ID}&mode=markdown',
                                            {{credentials:'include'}});
                      const j = await r.json();
                      const d = (j && j.data) || {{}};
                      return d.sourcecode || d.body || d.body_draft || '';
                    }})()""",
                    sid,
                    timeout=180,
                )
                body = body or ""
            except Exception as e:
                body = ""
                print(f"[{i}/{len(docs)}] FAILED {title}: {e}", flush=True)
            header = f"<!-- yuque:{BOOK_SLUG}/{slug} book_id={BOOK_ID} doc_id={d['id']} -->\n\n"
            open(path, "w").write(header + f"# {title}\n\n" + body)
            manifest.append({"order": i, "id": d["id"], "slug": slug, "title": title,
                             "file": fn, "bytes": len(body), "cached": False})
            print(f"[{i}/{len(docs)}] {title}: {len(body)} chars", flush=True)
            time.sleep(0.25)

        json.dump(manifest, open(os.path.join(OUT, "_manifest.json"), "w"), ensure_ascii=False, indent=1)
        total = sum(m["bytes"] for m in manifest)
        print(f"DONE docs={len(manifest)} total_chars={total}", flush=True)
    finally:
        c.close()


if __name__ == "__main__":
    main()
