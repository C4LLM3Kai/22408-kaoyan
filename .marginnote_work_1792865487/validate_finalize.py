import json
import pathlib
import plistlib
import re
import sqlite3
import unicodedata
import fitz

WORK = pathlib.Path(__file__).resolve().parent
OUT = WORK.parent / '26考研政治一页纸整合版.pdf'
d = fitz.open(WORK / 'complete_rendered.pdf')
manifest = json.loads((WORK / 'content_manifest.json').read_text())
expected_pages = json.loads((WORK / 'toc_pages.json').read_text())
toc = d.get_toc()
canon = lambda s: ''.join(unicodedata.normalize('NFC', s).replace('\ufeff', '').split())
for _, key, title in manifest['index']:
    found = [t for t in toc if canon(t[1]) == canon(title)]
    assert len(found) == 1 and found[0][2] == expected_pages[key], (key, found)
toclinks = [a for a in d[1].get_links() if a['kind'] in [fitz.LINK_GOTO, fitz.LINK_NAMED]]
assert len(toclinks) == len(expected_pages)
assert sorted(a['page'] + 1 for a in toclinks) == sorted(expected_pages.values())

body = [p.get_text(clip=fitz.Rect(0, 45, p.rect.width, p.rect.height-35)) for p in d]
def alnum(s):
    return ''.join(c for c in unicodedata.normalize('NFKC', s) if c.isalnum() or '\u3400' <= c <= '\u9fff')
alltext = alnum(''.join(body))
for r in manifest['rendered']:
    # These two records contain continued question text that is preserved
    # in the original scanned question image, rather than duplicated as OCR.
    if r['source'] == 'with_answers' and r['title'] in ['2024.21', '2020.29']:
        continue
    for line in r['text'].split('\n'):
        if len(alnum(line)) >= 5:
            assert alnum(line) in alltext, (r['title'], line)

question_pages = {}
for _, title, page in toc:
    if '例题 ' in title:
        question_pages[title.split('例题 ',1)[1]] = page
assert len(question_pages) == 68
conn = sqlite3.connect(next((WORK / 'with_answers').glob('*.marginnotes')))
for title, blob in conn.execute('SELECT ZNOTETITLE,ZNOTES FROM ZBOOKNOTE'):
    if title not in question_pages or not blob:
        continue
    p = plistlib.loads(blob)
    strings = [o['NS.string'] for o in p['$objects'] if isinstance(o, dict) and 'NS.string' in o]
    # LinkNote question continuations are printed as source images. Only the
    # separate answer text must appear in this page's searchable text layer.
    for obj in p['$objects']:
        if not isinstance(obj, dict) or 'NS.keys' not in obj:
            continue
        for key, val in zip(obj['NS.keys'], obj['NS.objects']):
            if p['$objects'][key.data] == 'q_htext':
                question = p['$objects'][val.data]
                question = question['NS.string'] if isinstance(question, dict) else question
                strings = [s for s in strings if s != question]
    # Each answer/analysis text block must be on the same page as its question.
    page_text = alnum(body[question_pages[title]-1])
    for text in strings:
        assert alnum(text) in page_text, ('split answer', title)
conn.close()

assert sum(len(p.get_image_info()) for p in d) == 75
for page in d:
    for block in page.get_text('blocks'):
        assert block[0] >= 25 and block[2] <= page.rect.width-25, ('horizontal overflow', page.number)
    for img in page.get_image_info():
        b = fitz.Rect(img['bbox'])
        assert b.x0 >= 25 and b.y0 >= 45 and b.x1 <= page.rect.width-25 and b.y1 <= page.rect.height-35, ('image outside body', page.number)

d.set_metadata({'title':'26考研政治一页纸整合版', 'author':'原 MarginNote 资料', 'subject':'知识点、解题方法、68 道例题及答案解析', 'keywords':'考研政治, 知识点, 解题方法, 真题解析', 'creator':'MarginNote 资料整合', 'producer':'Chromium / PyMuPDF'})
d.set_toc(toc, collapse=2)
staged = WORK / 'final_checked.pdf'
d.save(staged, garbage=3, deflate=True)
page_count = len(d)
d.close()
staged.replace(OUT)
report = {'output':str(OUT), 'pages':page_count, 'bookmarks':len(toc), 'toc_links':len(toclinks), 'question_answer_pairs':len(question_pages), 'images':75, 'text_coverage':'passed', 'question_answer_same_page':'passed', 'layout_bounds':'passed', 'size_bytes':OUT.stat().st_size}
(WORK / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
# Keep the initial exploration script and previews with the working assets.
initial = WORK.parent / 'build_political_pdf.py'
if initial.exists():
    initial.rename(WORK / 'initial_export.py')
for f in WORK.parent.glob('.pdf_preview-*.png'):
    f.rename(WORK / f.name)
print(json.dumps(report, ensure_ascii=False, indent=2))
