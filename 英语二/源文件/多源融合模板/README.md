# 英语二作文：36类融合模板

最终成品：`../../英语二作文_36类融合模板.pdf`，49页。

包含26类应用文、10类大作文；每类一页，含可替换模板、完整新编示例、3条表达讲解和核对重点。完整评分说明、使用说明、文字重合检查及40份原文件索引都在同一个PDF内。

## 可编辑内容与复现

- `templates.json`：当前定稿的36类内容。
- `英语二作文_36类融合模板.tex`：自包含LaTeX文件，可直接用XeLaTeX编译。
- `英语二作文_36类融合模板.md`：模板正文的可编辑文本；附录以TeX为准。
- `content.py`：生成初始示例与内容。
- `refine_templates.py`：将初始占位内容细化成通用句法框架。重建时必须在content.py后执行。
- `build_pdf.py`：将当前JSON和检查结果排成完整TeX。

在本目录执行：

```sh
python3 content.py
python3 refine_templates.py
python3 check_overlap.py
python3 -W ignore build_pdf.py
xelatex -interaction=nonstopmode -halt-on-error 英语二作文_36类融合模板.tex
xelatex -interaction=nonstopmode -halt-on-error 英语二作文_36类融合模板.tex
```

只更改JSON后排版时，不要再运行content.py和refine_templates.py，以免覆盖手动修改。

编译使用TeX Live与ctex/macnew字体集，英文Times New Roman。所有PDF均由XeLaTeX实际编译。

## 来源和检查

- `sources.json`：40份PDF的原路径、页数、SHA-256与提取方式。
- `提取文本/`：文字层或OCR文本。
- `ocr.swift` / `extract_ocr.py`：扫描PDF的macOS Vision识别流程；S07复用既有完整OCR。
- `overlap_report.json`：72个正文单元逐一与40份来源比较的完整矩阵，及逐来源整合统计。
- `逐篇重合检查.csv`：逐篇最高重合覆盖率。
- `最终核对.json`：49页、36类、41个书签和全部正文段落的完整性检查。
- `最终预览/`：最终PDF的逐页渲染与联系表，用于视觉检查。

本次连续4个英文词的逐篇最高覆盖率为20.63%，连续5词为10.20%。算法不删除常用虚词、按新稿长度为分母，不用大体量来源稀释分母。模板与完整示例分别核对，格式栏不纳入正文。该指标衡量字面复用，不是商业语义查重保证；OCR仍可能漏识别。

所有正文段落已从最终PDF回读核对；目录链接和页码核对通过；编译无Overfull和Missing character警告。已逐页检查布局。原始资料未改动。
