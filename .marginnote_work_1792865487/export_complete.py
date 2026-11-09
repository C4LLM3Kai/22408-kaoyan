"""Reflow every content block and restore MarginNote's mind-map hierarchy."""
import base64
import collections
import hashlib
import html
import io
import json
import pathlib
import plistlib
import re
import sqlite3
import sys
import unicodedata

from lxml import html as LH
from PIL import Image

WORK = pathlib.Path(__file__).resolve().parent
ROOT = WORK.parent
def decode_archive_object(plist, obj):
    if isinstance(obj, plistlib.UID):
        return decode_archive_object(plist, plist['$objects'][obj.data])
    if isinstance(obj, dict):
        if 'NS.string' in obj:
            return obj['NS.string']
        if 'NS.keys' in obj and 'NS.objects' in obj:
            return dict(zip([decode_archive_object(plist, x) for x in obj['NS.keys']], [decode_archive_object(plist, x) for x in obj['NS.objects']]))
        if 'NS.objects' in obj and '$class' in obj:
            return [decode_archive_object(plist, x) for x in obj['NS.objects']]
        return {k: decode_archive_object(plist, v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [decode_archive_object(plist, x) for x in obj]
    return obj


def unarchive(data):
    p = plistlib.loads(data)
    return decode_archive_object(p, p['$top']['root'])


def norm(s):
    return ''.join(unicodedata.normalize('NFC', s or '').replace('\ufeff', '').split())


def esc(s):
    return html.escape(str(s or '').replace('\ufeff', ''))


class Source:
    def __init__(self, kind):
        self.kind = kind
        self.file = next((WORK / kind).glob('*.marginnotes'))
        conn = sqlite3.connect(f'file:{self.file}?mode=ro', uri=True)
        conn.row_factory = sqlite3.Row
        self.rows = {r['ZNOTEID']: dict(r) for r in conn.execute('SELECT * FROM ZBOOKNOTE')}
        self.topic = dict(conn.execute('SELECT * FROM ZTOPIC').fetchone())
        self.media = {}
        self.internal = {}
        for r in conn.execute('SELECT * FROM ZMEDIA'):
            value = unarchive(r['ZDATA'])
            if isinstance(value, dict) and 'NS.data' in value:
                value = value['NS.data']
            if isinstance(value, bytes) and value.startswith(b'\x89PNG'):
                im = Image.open(io.BytesIO(value)); im.verify()
                self.media[r['ZMD5']] = value
            else:
                self.internal[r['ZMD5']] = value
        self.children = {i: [x for x in (r['ZMINDLINKS'] or '').split('|') if x in self.rows] for i, r in self.rows.items()}
        for row in self.rows.values():
            raw = unarchive(row['ZNOTES']) if row['ZNOTES'] else []
            row['blocks'] = raw if isinstance(raw, list) else [raw]
            blocktext = ''.join(b.get('text', b.get('q_htext', '')) for b in row['blocks'])
            assert norm(blocktext) == norm(row['ZNOTES_TEXT']), (kind, row['ZNOTETITLE'], 'text coverage mismatch')
        self.tree = []
        seen = set()
        def walk(i, path):
            if i in seen:
                return
            seen.add(i)
            r = self.rows[i]
            self.tree.append((r, path))
            for j, child in enumerate(self.children[i], 1):
                walk(child, path + [j])
        top = [x for x in (self.topic['ZMINDLINKS'] or '').split('|') if x in self.rows]
        walk(top[0], [])
        self.orphans = [r for i, r in self.rows.items() if i not in seen]
        conn.close()


knowledge, answers, practice = (Source(k) for k in ['knowledge', 'with_answers', 'no_answers'])

# Both exports contain the same question hierarchy and source assets.  Match
# by the hierarchy path so repeated category names cannot cross-wire answers.
practice_path = {tuple(path): row for row, path in practice.tree}
for row, path in answers.tree:
    other = practice_path[tuple(path)]
    assert row['ZNOTETITLE'] == other['ZNOTETITLE']
    assert row['ZHIGHLIGHT_TEXT'] == other['ZHIGHLIGHT_TEXT']
    assert set(filter(None, (row['ZMEDIA_LIST'] or '').split('-'))) == set(filter(None, (other['ZMEDIA_LIST'] or '').split('-')))
assert answers.media == practice.media

assets = WORK / 'assets'
assets.mkdir(exist_ok=True)
for source in [knowledge, answers]:
    for key, data in source.media.items():
        (assets / (key + '.png')).write_bytes(data)

colors = collections.Counter()
fallbacks = []
rendered = []
used_images = collections.defaultdict(set)
index = []


def css_style(value):
    result = []
    for item in value.split(';'):
        if ':' not in item:
            continue
        key, val = map(str.strip, item.split(':', 1))
        if key in ['color', 'background-color'] and re.fullmatch(r'#[\da-fA-F]{3,6}', val):
            val = val.lower()
            if len(val) == 4:
                val = '#' + ''.join(ch * 2 for ch in val[1:])
            if key == 'color':
                rgb = tuple(int(val[i:i+2], 16) for i in (1, 3, 5))
                # Grey text designed for a dark canvas needs higher contrast on paper.
                if max(rgb) - min(rgb) < 12:
                    val = '#30343b'
                elif min(rgb) > 180:
                    val = '#5b6370'
            result.append(f'{key}:{val}')
        elif key == 'font-weight' and val in ['bold', 'normal', '600', '700']:
            result.append(f'{key}:{val}')
        elif key == 'text-decoration' and val.strip() in ['underline', 'line-through']:
            result.append(f'{key}:{val.strip()}')
    return ';'.join(result)


def rich(block):
    rawtext = block.get('text', '')
    content = block.get('html')
    if not content:
        return '<div class="plain">' + esc(rawtext) + '</div>'
    doc = LH.fromstring(content)
    body = doc.find('body')
    body = body if body is not None else doc
    if norm(''.join(body.itertext())) != norm(rawtext):
        fallbacks.append(rawtext[:40])
        return '<div class="plain">' + esc(rawtext) + '</div>'
    styles = {}
    for selector, rules in re.findall(r'\.([\w-]+)\s*\{([^}]*)\}', content):
        styles[selector] = css_style(rules)
    allowed = {'p', 'span', 'b', 'strong', 'i', 'em', 'u', 's', 'sup', 'sub', 'br', 'ul', 'ol', 'li', 'table', 'tbody', 'tr', 'td', 'th', 'div'}
    def node(n):
        if n.tag in ['script', 'style', 'head']:
            return ''
        tag = n.tag if n.tag in allowed else 'span'
        if tag == 'br':
            return '<br>'
        styling = ';'.join(styles.get(c, '') for c in n.get('class', '').split())
        styling += ';' + css_style(n.get('style', ''))
        attrs = f' style="{esc(styling)}"' if styling.strip(';') else ''
        return f'<{tag}{attrs}>' + esc(n.text) + ''.join(node(c) + esc(c.tail) for c in n) + f'</{tag}>'
    return '<div class="rich">' + esc(body.text) + ''.join(node(n) + esc(n.tail) for n in body) + '</div>'


def figure(source, key, seen, title=''):
    if key in seen:
        return ''
    if key not in source.media:
        raise ValueError(('Missing referenced image', source.kind, key))
    seen.add(key)
    used_images[source.kind].add(key)
    return f'<figure><img src="assets/{esc(key)}.png" alt="{esc(title)}"></figure>'


def body_html(source, row, is_question):
    chunks = []
    seen = set()
    img_key = None
    if row['ZHIGHLIGHT_PIC']:
        pic = unarchive(row['ZHIGHLIGHT_PIC'])
        img_key = pic.get('paint')
    if img_key:
        chunks.append(figure(source, img_key, seen, row['ZNOTETITLE']))
    elif row['ZHIGHLIGHT_TEXT']:
        chunks.append('<div class="plain excerpt">' + esc(row['ZHIGHLIGHT_TEXT']) + '</div>')
    answer_started = False
    for block in row['blocks']:
        typ = block['type']
        if typ == 'PaintNote':
            chunks.append(figure(source, block['paint'], seen, row['ZNOTETITLE']))
        elif typ == 'LinkNote':
            pic = block.get('q_hpic', {})
            if pic.get('paint'):
                chunks.append(figure(source, pic['paint'], seen, row['ZNOTETITLE']))
            elif block.get('q_htext'):
                chunks.append('<div class="plain excerpt">' + esc(block['q_htext']) + '</div>')
        elif typ in ['HtmlNote', 'TextNote']:
            if is_question and not answer_started:
                chunks.append('<p class="answer-label">答案与解析</p>')
                answer_started = True
            chunks.append(rich(block))
        elif typ == 'SketchNote':
            chunks.append('<figure class="sketch"><img src="assets/freehand.png" alt="原图中的手绘标记"></figure>')
        elif typ != 'DummyNote':
            raise ValueError(('Unsupported content', typ))
    for key in filter(None, (row['ZMEDIA_LIST'] or '').split('-')):
        if key in source.media and key not in seen:
            chunks.append(figure(source, key, seen, row['ZNOTETITLE']))
    rendered.append({'source': source.kind, 'id': row['ZNOTEID'], 'title': row['ZNOTETITLE'], 'text': row['ZNOTES_TEXT'] or '', 'images': sorted(seen)})
    return '\n'.join(chunks)


sections = []
chapter_names = {'马原': '马克思主义基本原理', '史纲': '中国近现代史纲要', '思修': '思想道德与法治', '新思想': '习近平新时代中国特色社会主义思想', '时政': '时事政治'}

for source, part, part_title in [(knowledge, 1, '知识点汇编'), (answers, 2, '解题方法与真题解析')]:
    sections.append(f'<section class="part"><h1 id="part-{part}">第{part}部分　{part_title}</h1>')
    index.append((0, f'part-{part}', f'第{part}部分　{part_title}'))
    for row, path in source.tree:
        if not path:
            continue
        title = row['ZNOTETITLE'] or '补充笔记'
        key = f"{source.kind}-{row['Z_PK']}"
        is_question = bool(re.match(r'^20\d\d\.', title))
        num = '.'.join(map(str, [part] + path))
        hlevel = min(len(path) + 1, 6)
        if part == 1 and len(path) == 1:
            title = chapter_names.get(title, title)
        if part == 2 and row['ZNOTETITLE'] == '老头命题手法（挖坑点）' and source.children[row['ZNOTEID']]:
            title = '命题陷阱分类与例题'
        if part == 2 and is_question:
            title = '例题 ' + title
        classes = 'node'
        if len(path) == 1 and part == 1:
            classes += ' chapter'
        if is_question:
            classes += ' question'
        sections.append(f'<article class="{classes}"><h{hlevel} id="{key}"><span class="number">{num}</span> {esc(title)}</h{hlevel}>')
        sections.append(body_html(source, row, is_question))
        sections.append('</article>')
        if (part == 1 and (len(path) == 1 or (len(path) == 2 and path[0] != 5))) or (part == 2 and (len(path) == 1 or (len(path) == 2 and not is_question))):
            index.append((len(path), key, f'{num}　{title}'))
    for row in source.orphans:
        substantive = any(b.get('type') not in ['DummyNote'] for b in row['blocks'])
        if substantive:
            sections.append('<article class="node"><h2>附：原图中的手绘标记</h2>')
            sections.append(body_html(source, row, False))
            sections.append('</article>')
    sections.append('</section>')

for source in [knowledge, answers]:
    assert used_images[source.kind] == set(source.media), ('Unused images', source.kind, set(source.media) - used_images[source.kind])

stats = {
    'knowledge_nodes': len(knowledge.rows), 'knowledge_text_blocks': sum(b['type'] == 'HtmlNote' for r in knowledge.rows.values() for b in r['blocks']),
    'method_nodes': len(answers.rows), 'questions': sum(bool(re.match(r'^20\d\d\.', r['ZNOTETITLE'] or '')) for r in answers.rows.values()),
    'knowledge_images': len(knowledge.media), 'method_images': len(answers.media),
    'rich_text_fallbacks': fallbacks,
    'practice_matched': True,
}
(WORK / 'content_manifest.json').write_text(json.dumps({'stats': stats, 'rendered': rendered, 'index': index}, ensure_ascii=False, indent=2))

toc = ''.join(f'<a class="toc-entry toc-{level}" href="#{key}" data-target="{key}"><span>{esc(title)}</span><span class="toc-page"></span></a>' for level, key, title in index)
style = '''
@page {size:A4; margin:20mm 17mm 18mm;}
* {box-sizing:border-box;}
body {font-family:"PingFang SC","Arial",sans-serif; color:#30343b; font-size:10pt; line-height:1.6; margin:0; -webkit-print-color-adjust:exact; print-color-adjust:exact;}
.cover {height:250mm; page-break-after:always; padding:37mm 8mm 0;}
.eyebrow {color:#a26e37; letter-spacing:3px; font-size:11pt;}
.cover h1 {font-size:32pt; color:#163a57; margin:12mm 0 6mm; line-height:1.35;}
.cover .subtitle {font-size:17pt; color:#355d7a; margin-bottom:20mm;}
.cover .rule {width:28mm; height:3px; background:#b88a51; margin-bottom:10mm;}
.cover p {line-height:1.9;}
.cover .source {font-size:8.5pt; color:#697581; margin-top:13mm;}
.toc {page-break-after:always;}
.toc h1 {font-size:23pt; color:#163a57; margin:0 0 5mm;}
.toc-note {color:#697581; font-size:9pt; margin-bottom:7mm;}
.toc-columns {column-count:2; column-gap:9mm;}
.toc-entry {color:#334e64; text-decoration:none; display:flex; align-items:baseline; justify-content:space-between; break-inside:avoid; gap:2mm; padding:1.15mm 0; border-bottom:1px solid #edf0f2; font-size:8.5pt; line-height:1.5;}
.toc-0 {font-size:10pt; font-weight:600; color:#163a57; margin-top:4mm; break-after:avoid;}
.toc-1 {font-weight:600; break-after:avoid;}
.toc-2 {padding-left:3mm;}
.toc-page {width:8mm; flex-shrink:0; text-align:right; font-variant-numeric:tabular-nums; color:#80909d;}
.part {page-break-before:always;}
.part>h1 {font-size:24pt; color:#163a57; border-bottom:2px solid #b88a51; margin:0 0 8mm; padding-bottom:4mm;}
h2,h3,h4,h5,h6 {color:#244e6b; page-break-after:avoid; break-after:avoid; font-weight:600; line-height:1.45;}
h2 {font-size:16pt; margin:8mm 0 4mm; padding-bottom:2mm; border-bottom:1px solid #cbd8e2;}
h3 {font-size:12pt; margin:5mm 0 3mm;}
h4,h5,h6 {font-size:10.5pt; margin:4mm 0 2.5mm;}
.number {font-family:Arial,sans-serif; font-size:.86em; color:#75899b; margin-right:1.5mm;}
.rich {margin-bottom:3mm;}
.rich p {margin:0 0 1.2mm; orphans:2; widows:2;}
.rich p:empty {height:1.5mm;}
.rich span {font-family:inherit;}
sup,sub {font-size:.8em;}
.plain {white-space:pre-wrap; margin-bottom:3mm;}
figure {margin:2.5mm 0 3mm; text-align:center; page-break-inside:avoid;}
figure img {width:auto; height:auto; max-width:100%; max-height:130mm; object-fit:contain;}
.sketch img {height:8mm;}
.answer-label {font-size:9pt; color:#966525; font-weight:600; margin:1mm 0 2mm; padding-top:1.5mm; border-top:1px solid #e1d6c7; break-after:avoid;}
.question {margin-bottom:5mm; break-inside:avoid;}
.question figure img {max-height:115mm;}
table {border-collapse:collapse; width:100%;} td,th {border:1px solid #bfc9d2; padding:1.5mm;}
'''
cover = f'''<section class="cover"><div class="eyebrow">POLITICS · STUDY COMPANION</div><h1>26考研政治<br>一页纸整合版</h1><div class="subtitle">知识点 · 解题方法 · 真题与解析</div><div class="rule"></div><p>依原思维导图的学科与专题结构编排。<br>收录知识点笔记、{stats['questions']} 道例题及原有答案解析，<br>保留重点标记、补充批注与原始题图。</p><p class="source">资料来源<br>《26考研政治知识点一页纸（完整版）》<br>《26考研政治解题方法一页纸（不含答案）》<br>《政治解题方法一页纸（含答案和解析）》</p><p class="source">相同题目合并呈现；内容、答案及年份沿用原资料。<br>可通过目录链接或 PDF 书签定位章节与题目。</p></section>'''
document = '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><title>26考研政治一页纸整合版</title><style>' + style + '</style></head><body>' + cover + '<section class="toc"><h1>目录</h1><p class="toc-note">按学科、专题与解题方法排列；章节标题可点击跳转。</p><div class="toc-columns">' + toc + '</div></section>' + '\n'.join(sections) + '</body></html>'
(WORK / 'complete.html').write_text(document, encoding='utf-8')
print(json.dumps(stats, ensure_ascii=False, indent=2))
