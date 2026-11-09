import glob
import io
import os
import plistlib
import re
import sqlite3
from collections import defaultdict
from html import escape
from plistlib import UID

from lxml import html as lxml_html
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)


ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = sorted(glob.glob(os.path.join(ROOT, ".marginnote_work_*")))[-1]
OUT = os.path.join(ROOT, "26考研政治一页纸整合版.pdf")


def normalize_text(value):
    """Make common MarginNote emoji markers render cleanly in study PDFs."""
    if value is None:
        return value
    s = str(value)
    s = re.sub(r"([0-9#*])(?:[\ufe0e\ufe0f])?\u20e3", r"\1.", s)
    s = s.replace("✅", "✓").replace("❌", "✗").replace("⚠️", "⚠")
    s = s.replace("➡️", "→").replace("🔴", "●")
    s = s.replace("\ufeff", "").replace("\ufe0e", "").replace("\ufe0f", "").replace("\u200d", "")
    # Strip pictographic emoji that are not present in the embedded CJK font.
    keep_misc = {"✓", "✗", "⚠", "→", "●"}
    s = "".join(
        ch for ch in s
        if not (0x1F000 <= ord(ch) <= 0x1FAFF)
        and (ord(ch) < 0x2600 or ord(ch) > 0x27BF or ch in keep_misc)
    )
    return s


# Arial Unicode is a TrueType font on macOS and covers the Chinese characters
# in these notes.  Registering a second name lets rich text use a bold face
# without falling back to Helvetica, which has no Chinese glyphs.
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
pdfmetrics.registerFont(TTFont("StudySans", FONT_PATH))
pdfmetrics.registerFont(TTFont("StudySansBold", FONT_PATH))


def decode_archive_object(plist, obj):
    """Resolve the small NSKeyedArchiver dictionaries used by MarginNote."""
    if isinstance(obj, UID):
        return decode_archive_object(plist, plist["$objects"][obj.data])
    if isinstance(obj, dict):
        if "NS.string" in obj:
            return obj["NS.string"]
        if "NS.keys" in obj and "NS.objects" in obj:
            keys = [decode_archive_object(plist, x) for x in obj["NS.keys"]]
            values = [decode_archive_object(plist, x) for x in obj["NS.objects"]]
            return dict(zip(keys, values))
        if "NS.objects" in obj and "$class" in obj:
            return [decode_archive_object(plist, x) for x in obj["NS.objects"]]
        return {k: decode_archive_object(plist, v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [decode_archive_object(plist, x) for x in obj]
    return obj


def decode_note_blob(blob):
    if not blob:
        return {}
    try:
        p = plistlib.loads(blob)
        root = decode_archive_object(p, p["$top"]["root"])
        if isinstance(root, list) and len(root) == 1 and isinstance(root[0], dict):
            root = root[0]
        return root if isinstance(root, dict) else {}
    except Exception:
        return {}


def image_from_media_blob(blob):
    """Return raw PNG/JPEG bytes from a ZMEDIA archive, if present."""
    if not blob:
        return None
    try:
        p = plistlib.loads(blob)
        root = p["$objects"][p["$top"]["root"].data]
        if isinstance(root, bytes) and (root.startswith(b"\x89PNG") or root.startswith(b"\xff\xd8")):
            return root
    except Exception:
        pass
    return None


def css_classes(html_text):
    styles = {}
    if not html_text:
        return styles
    for selector, body in re.findall(r"\.([\w-]+)\s*\{([^}]*)\}", html_text):
        st = {}
        m = re.search(r"(?:^|;)\s*color\s*:\s*(#[0-9a-fA-F]{3,8})", body)
        if m:
            st["color"] = m.group(1)
        if re.search(r"font-weight\s*:\s*bold", body, re.I):
            st["bold"] = True
        if re.search(r"text-decoration\s*:\s*underline", body, re.I):
            st["underline"] = True
        styles[selector] = st
    return styles


def rich_html_paragraphs(html_text, style):
    """Convert MarginNote's simple Cocoa HTML into ReportLab paragraphs."""
    if not html_text:
        return []
    html_text = normalize_text(html_text)
    try:
        root = lxml_html.fromstring(html_text)
    except Exception:
        return []
    css = css_classes(html_text)
    paragraphs = root.xpath(".//p")
    if not paragraphs and root.tag == "p":
        paragraphs = [root]
    if not paragraphs:
        paragraphs = [root]

    def render(node, inherited=None):
        inherited = dict(inherited or {})
        if isinstance(node, str):
            return escape(node)
        current = dict(inherited)
        for cls in (node.get("class", "") or "").split():
            current.update(css.get(cls, {}))
        tag = node.tag.lower() if isinstance(node.tag, str) else ""
        if tag == "br":
            return "<br/>"
        content = escape(node.text or "")
        for child in node:
            content += render(child, current)
            if child.tail:
                content += escape(child.tail)
        if tag in ("sub", "sup"):
            return f"<{tag}>{content}</{tag}>"
        if tag in ("b", "strong"):
            current["bold"] = True
        if tag == "u":
            current["underline"] = True
        if tag in ("span", "font", "b", "strong", "u"):
            if current.get("color") or current.get("bold"):
                attrs = ['name="StudySansBold"' if current.get("bold") else 'name="StudySans"']
                if current.get("color"):
                    attrs.append(f'color="{current["color"]}"')
                content = f"<font {' '.join(attrs)}>{content}</font>"
            if current.get("underline"):
                content = f"<u>{content}</u>"
        return content

    out = []
    for p in paragraphs:
        markup = render(p)
        if not markup.replace("<br/>", "").strip():
            out.append(Spacer(1, 3))
            continue
        try:
            out.append(Paragraph(markup, style))
        except Exception:
            # A malformed rich-text fragment should not make the whole export fail.
            plain = "".join(p.itertext())
            out.append(Paragraph(escape(plain), style))
    return out


def plain_paragraphs(text, style):
    if not text:
        return []
    out = []
    for line in normalize_text(text).replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        if line.strip():
            out.append(Paragraph(escape(line), style))
        else:
            out.append(Spacer(1, 3))
    return out


def media_ids(value):
    return [x for x in (value or "").split("-") if x]


def load_db(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def extract_media(conn):
    out = {}
    for row in conn.execute("SELECT ZMD5, ZDATA FROM ZMEDIA"):
        image = image_from_media_blob(row["ZDATA"])
        if image:
            out[row["ZMD5"]] = image
    return out


def media_flowables(ids, media_map, max_width=165 * mm, max_height=95 * mm):
    result = []
    seen = set()
    for mid in ids:
        if mid in seen or mid not in media_map:
            continue
        seen.add(mid)
        data = media_map[mid]
        try:
            with PILImage.open(io.BytesIO(data)) as im:
                width, height = im.size
            scale = min(max_width / width, max_height / height, 1.0)
            img = Image(io.BytesIO(data), width=width * scale, height=height * scale)
            img.hAlign = "CENTER"
            result.append(img)
            result.append(Spacer(1, 4))
        except Exception:
            continue
    return result


class StudyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="main")
        self.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=draw_page)])
        self._outline_level = 0

    def afterFlowable(self, flowable):
        key = getattr(flowable, "_bookmark_name", None)
        if key:
            self.canv.bookmarkPage(key)
            level = getattr(flowable, "_outline_level", 0)
            title = getattr(flowable, "_outline_title", "")
            self.canv.addOutlineEntry(title[:120], key, level=level, closed=False)


def draw_page(canvas, doc):
    page = canvas.getPageNumber()
    canvas.saveState()
    if page > 1:
        canvas.setStrokeColor(colors.HexColor("#D9E2F3"))
        canvas.setLineWidth(0.4)
        canvas.line(doc.leftMargin, A4[1] - 17 * mm, A4[0] - doc.rightMargin, A4[1] - 17 * mm)
        canvas.setFont("StudySans", 7.5)
        canvas.setFillColor(colors.HexColor("#6B7280"))
        canvas.drawString(doc.leftMargin, A4[1] - 13 * mm, "26考研政治一页纸整合版")
    canvas.setFont("StudySans", 8)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.drawCentredString(A4[0] / 2, 10 * mm, str(page))
    canvas.restoreState()


def heading(text, style, level, key):
    text = normalize_text(text)
    p = Paragraph(escape(text), style)
    p._bookmark_name = key
    p._outline_level = level
    p._outline_title = text
    return p


def get_rows(conn):
    return list(conn.execute("""
        SELECT Z_PK, ZNOTETITLE, ZHIGHLIGHT_TEXT, ZNOTES_TEXT, ZNOTES,
               ZMEDIA_LIST, ZHIGHLIGHTS
        FROM ZBOOKNOTE ORDER BY Z_PK
    """))


def build_story():
    knowledge_path = glob.glob(os.path.join(WORK, "knowledge", "*.marginnotes"))[0]
    answer_path = glob.glob(os.path.join(WORK, "with_answers", "*.marginnotes"))[0]
    no_answer_path = glob.glob(os.path.join(WORK, "no_answers", "*.marginnotes"))[0]
    knowledge_conn = load_db(knowledge_path)
    answer_conn = load_db(answer_path)
    no_answer_conn = load_db(no_answer_path)
    knowledge_rows = get_rows(knowledge_conn)
    answer_rows = get_rows(answer_conn)
    no_answer_rows = get_rows(no_answer_conn)
    knowledge_media = extract_media(knowledge_conn)
    answer_media = extract_media(answer_conn)
    no_answer_media = extract_media(no_answer_conn)
    answer_media.update(no_answer_media)

    styles = getSampleStyleSheet()
    cover_title = ParagraphStyle(
        "CoverTitle", parent=styles["Title"], fontName="StudySansBold", fontSize=27,
        leading=38, textColor=colors.HexColor("#17365D"), alignment=TA_CENTER,
        spaceAfter=15 * mm,
    )
    cover_subtitle = ParagraphStyle(
        "CoverSubtitle", parent=styles["Normal"], fontName="StudySans", fontSize=12,
        leading=20, textColor=colors.HexColor("#4B5563"), alignment=TA_CENTER,
    )
    section_style = ParagraphStyle(
        "Section", parent=styles["Heading1"], fontName="StudySansBold", fontSize=20,
        leading=28, textColor=colors.HexColor("#1F4E79"), spaceBefore=8, spaceAfter=12,
    )
    note_title_style = ParagraphStyle(
        "NoteTitle", parent=styles["Heading2"], fontName="StudySansBold", fontSize=12.2,
        leading=17, textColor=colors.HexColor("#244A73"), spaceBefore=8, spaceAfter=4,
        keepWithNext=1,
    )
    body_style = ParagraphStyle(
        "Body", parent=styles["BodyText"], fontName="StudySans", fontSize=9.2,
        leading=13.2, textColor=colors.HexColor("#202124"), spaceAfter=2,
        wordWrap="CJK",
    )
    question_style = ParagraphStyle(
        "Question", parent=body_style, fontName="StudySans", fontSize=8.9,
        leading=12.5, leftIndent=6, rightIndent=6, borderColor=colors.HexColor("#C9D7EA"),
        borderWidth=0.5, borderPadding=5, backColor=colors.HexColor("#F6F9FD"),
        spaceBefore=3, spaceAfter=6,
    )
    label_style = ParagraphStyle(
        "Label", parent=body_style, fontName="StudySansBold", fontSize=9.2,
        leading=13, textColor=colors.HexColor("#1F4E79"), spaceBefore=3, spaceAfter=2,
    )
    small_style = ParagraphStyle(
        "Small", parent=body_style, fontSize=8.2, leading=12, textColor=colors.HexColor("#6B7280"),
    )
    empty_style = ParagraphStyle(
        "Empty", parent=small_style, textColor=colors.HexColor("#9CA3AF"), italic=True,
    )

    story = []
    story.append(Spacer(1, 35 * mm))
    story.append(Paragraph("26考研政治一页纸", cover_title))
    story.append(Paragraph("知识点、解题方法、题目答案与解析整合版", cover_subtitle))
    story.append(Spacer(1, 12 * mm))
    story.append(Paragraph("根据 3 份 MarginNote 文件整理生成", cover_subtitle))
    story.append(Paragraph("内容顺序保留原始笔记顺序；解题方法部分将题面、题图与答案解析合并。", cover_subtitle))
    story.append(PageBreak())

    story.append(heading("目录与说明", section_style, 0, "toc"))
    story.append(Paragraph("一、政治知识点一页纸（262 条原始笔记）", body_style))
    story.append(Paragraph("二、政治解题方法一页纸（87 条题目记录，含题面/题图与答案解析）", body_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("说明：空白分类节点仍保留标题；题图以原始 PNG 形式嵌入。附件中的文字仅作为学习资料内容整理。", small_style))
    story.append(PageBreak())

    # Knowledge section.
    story.append(heading("第一部分　政治知识点一页纸", section_style, 0, "knowledge-section"))
    story.append(Paragraph(f"共 {len(knowledge_rows)} 条，按 MarginNote 原始顺序排列。", small_style))
    for idx, row in enumerate(knowledge_rows, 1):
        title = row["ZNOTETITLE"] or f"未命名节点 {idx}"
        story.append(heading(f"{idx}. {title}", note_title_style, 1, f"knowledge-{idx}"))
        data = decode_note_blob(row["ZNOTES"])
        html_text = data.get("html") if isinstance(data, dict) else None
        text = row["ZNOTES_TEXT"] or (data.get("text") if isinstance(data, dict) else None)
        if html_text:
            story.extend(rich_html_paragraphs(html_text, body_style))
        elif text:
            story.extend(plain_paragraphs(text, body_style))
        else:
            story.append(Paragraph("（原笔记为分类节点，未包含可提取正文）", empty_style))
        story.extend(media_flowables(media_ids(row["ZMEDIA_LIST"]), knowledge_media))

    story.append(PageBreak())
    story.append(heading("第二部分　政治解题方法一页纸", section_style, 0, "methods-section"))
    story.append(Paragraph(f"共 {len(answer_rows)} 条题目记录。答案解析来自“含答案和解析”文件；题目文字和题图按可提取内容合并。", small_style))

    # The no-answer export has the same 87 records and is used as a fallback
    # for question text/media when a field is missing in the answer export.
    no_by_title = defaultdict(list)
    for r in no_answer_rows:
        no_by_title[r["ZNOTETITLE"]].append(r)
    no_seen = defaultdict(int)

    for idx, row in enumerate(answer_rows, 1):
        title = row["ZNOTETITLE"] or f"未命名题目 {idx}"
        story.append(heading(f"{idx}. {title}", note_title_style, 1, f"method-{idx}"))
        fallback_list = no_by_title.get(row["ZNOTETITLE"], [])
        fallback = fallback_list[no_seen[row["ZNOTETITLE"]]] if no_seen[row["ZNOTETITLE"]] < len(fallback_list) else None
        no_seen[row["ZNOTETITLE"]] += 1
        highlight = row["ZHIGHLIGHT_TEXT"] or (fallback["ZHIGHLIGHT_TEXT"] if fallback else None)
        ids = media_ids(row["ZMEDIA_LIST"])
        if fallback:
            ids += [x for x in media_ids(fallback["ZMEDIA_LIST"]) if x not in ids]
        if highlight:
            story.append(Paragraph("题目原文", label_style))
            story.append(Paragraph(escape(normalize_text(highlight)), question_style))
        image_parts = media_flowables(ids, answer_media, max_height=88 * mm)
        if image_parts:
            if not highlight:
                story.append(Paragraph("题目原图", label_style))
            story.extend(image_parts)
        data = decode_note_blob(row["ZNOTES"])
        html_text = data.get("html") if isinstance(data, dict) else None
        text = row["ZNOTES_TEXT"] or (data.get("text") if isinstance(data, dict) else None)
        if html_text:
            story.append(Paragraph("答案与解析", label_style))
            story.extend(rich_html_paragraphs(html_text, body_style))
        elif text:
            story.append(Paragraph("答案与解析", label_style))
            story.extend(plain_paragraphs(text, body_style))
        elif not image_parts and not highlight:
            story.append(Paragraph("（该节点未包含可提取的题面、题图或解析正文）", empty_style))

    return story


if __name__ == "__main__":
    doc = StudyDocTemplate(
        OUT,
        pagesize=A4,
        leftMargin=17 * mm,
        rightMargin=17 * mm,
        topMargin=22 * mm,
        bottomMargin=17 * mm,
        title="26考研政治一页纸整合版",
        author="MarginNote content integration",
    )
    doc.build(build_story())
    print(OUT)
