from pathlib import Path
p=Path('/Users/shaoyikai/Desktop/考研/英语二/源文件/多源融合模板/ocr.swift')
s=p.read_text().replace('["en-US","zh-Hans"]','["zh-Hans","en-US"]').replace('request.usesLanguageCorrection=true','request.usesLanguageCorrection=true\n request.automaticallyDetectsLanguage=true')
p.write_text(s)
