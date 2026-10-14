# 22408 一页纸打印笔记

把 22408（数学二 + 408 + 英语二 + 政治）的任何知识点，变成一张 **A4 单页、可直接打印、由 XeLaTeX 实际编译**的 PDF 笔记。

## 为什么值得单独做一个 skill

普通回答里的公式表格，复习时既不能带走也不能打印。这个 skill 把"回答"升级成"可归档的纸质资料"：固定版式、强制单页、编译期自动查错、视觉自检后才交付。

## 目录结构

```text
22408-notes-skill/
├── SKILL.md                      # 触发条件与执行流程
├── assets/note-preamble.tex      # 共享导言区（字体、配色、版式、自定义命令）
├── scripts/
│   ├── doctor.py                 # 环境自检：编译器、字体、宏包、PyMuPDF
│   ├── check_note.py             # 编译前检查：公式闭合、超纲宏、篇幅预算
│   └── build_note.py             # 编译成 PDF + 单页/缺字/溢出校验 + 预览渲染
├── references/
│   ├── layout-spec.md            # 版面参数、页面结构、常见排版问题
│   └── subject-notes.md          # 四个学科各写什么、不写什么
└── examples/
    └── N002-循环队列判满.md       # 408 代码块示例（可直接编译试跑）
```

## 快速开始

```bash
python3 scripts/doctor.py                       # 1. 环境自检

python3 scripts/check_note.py note.md --subject 数学二   # 2. 编译前检查

python3 scripts/build_note.py note.md out.pdf \          # 3. 编译
    --title 弧长公式 --subject 数学二 --topic '高等数学·定积分应用' --auto-fit
```

`build_note.py` 退出码：`0` 成功、`1` 编译失败、`2` 超过一页、`3` 有缺字。非 0 一律修复后重跑。

## 硬性约束

- **必须**由 XeLaTeX/LuaLaTeX 实际编译产出 PDF；不允许网页打印、Word 导出、ReportLab 替代。
- **必须**单页；超页就精简内容或降字号，不拆成两页。
- **必须**在交付前打开预览 PNG 目视检查。
- 公式与条件必须自行核对，不确定的内容不进笔记。

## 依赖

TeX Live（含 ctex、xeCJK、fontspec、tabularx、booktabs、fancyvrb、needspace、multicol）、
macOS 自带字体 Songti SC / Heiti SC / Times New Roman、PyMuPDF（用于页数校验与预览渲染，可缺省）。
