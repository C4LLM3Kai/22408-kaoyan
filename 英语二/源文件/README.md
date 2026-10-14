# 源文件说明

本目录保存《考研英语二 作文模板总纲（整合·改进版）》的全部源材料与可重编译的 LaTeX 源码。

## 成品位置

- PDF：`../英语二作文模板总纲.pdf`（126 页，A4，黑白简约排版）

## 文件清单

| 文件 | 说明 |
| --- | --- |
| `英语二作文模板总纲.tex` | **成品源码**，自包含单文件，可直接用 XeLaTeX 重编译 |
| `英语作文模板.txt` | 从 `../英语作文模板.pdf`（御风 yufeng，74 页）提取的文本 |
| `批改指令.txt` | 从 `../考研英语批改指令.pdf`（7 页）提取的文本，本册全部评分标准的唯一依据 |
| `mmg_ocr.txt` | 从 `../mmg作文模板.pdf`（49 页扫描件）用 macOS Vision OCR 识别的文本 |
| `mmg作文模板.txt` | `../mmg作文模板.pdf` 的原始文本层（该 PDF 为扫描件，无文本层，故为空） |
| `assemble.py` | 把分章节片段拼装成自包含 `.tex` 并做版式后处理的脚本（保留备查） |

## 重新编译

```bash
export PATH=/Library/TeX/texbin:$PATH
cd ./
xelatex -interaction=nonstopmode 英语二作文模板总纲.tex
xelatex -interaction=nonstopmode 英语二作文模板总纲.tex   # 第二遍，生成目录页码
```

编译环境：TeX Live 2026（basic）+ ctex + xeCJK + fontspec + tikz + longtable + booktabs。
字体：正文英文 Times New Roman，中文走 ctex 的 macnew 字体集。

## 编辑提示

- 模板块用 `\begin{tpl}{标题} ... \end{tpl}`；批注用 `\rubric{}` `\zone{}` `\impr{}` `\tip{}`。
- 填空占位用 `\fillin{内容}`，会自动渲染成加粗【内容】。
- 长表格一律用 `longtable` + `booktabs`，列宽用已定义的 `L{宽}` / `C{宽}`；
  单表各列宽度之和加上 `2 × 5pt × 列数` 不得超过 17.0cm（A4 纸 2cm 页边距下的版心宽度）。
- 添加新表格后请重编译一次，检查日志里有没有 `Overfull \hbox` 与 `Missing character`。
