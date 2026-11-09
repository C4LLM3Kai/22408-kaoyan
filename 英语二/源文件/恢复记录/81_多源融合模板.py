from pathlib import Path
p=Path('/Users/shaoyikai/Desktop/考研/英语二/源文件/多源融合模板/extract_ocr.py')
s=p.read_text().replace("parts=root/'ocr_parts'", "parts=root/'ocr_bilingual'").replace("if s['id']=='S07' or not s['sparse_pages']:continue", "if s['id']=='S07' or (not s['sparse_pages'] and s['id'] not in ['S06','S37','S38','S39','S40']):continue")
p.write_text(s)
