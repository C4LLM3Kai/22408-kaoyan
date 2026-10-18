# 中值定理讲义 · 构建说明

本目录是中值定理讲义 PDF 的可重建源码。

## 产物

- `../中值定理证明题·完整讲义（P2+P3）.pdf` — 最终 54 页 A4 成品

## 源文件

| 文件 | 内容 |
|---|---|
| `part1.html` | 封面、目录、前言（课程地图、定理速查、三步总纲） |
| `part2.html` | 第一篇：四大基本定理的证明 + 2010 真题 |
| `part3.html` | 第二篇：辅助函数三大方法（观察法、公式法、整体思想、微分方程法） |
| `part4.html` | 第三篇：泰勒展开、中值参数 θ、双中值、三中值 |
| `part5.html` | 附录：速查表、信号对照、十大易错点、方法总图 |
| `style.css` | A4 打印样式（字体、配色、分页控制） |
| `build.py` | HTML → PDF（KaTeX 渲染数学公式 + Chrome 无头打印） |
| `finish.py` | 两遍编译：解析真实页码 → 回填目录 → 叠加页码 |
| `katex/` | KaTeX 0.16.9 本地副本（含 woff2 字体，离线可用） |

## 重建

```bash
cat part1.html part2.html part3.html part4.html part5.html > body.html
python3 finish.py          # 输出 中值定理讲义.pdf（含页码与目录）
```

依赖：macOS + Google Chrome、Python 3.10+、`pypdfium2`、`pypdf`、`reportlab`。

## 注意

- 数学公式用 `$...$`（行内）与 `$$...$$`（独立行）书写，由 `build.py` 预切分为
  `data-tex` 属性后交给 KaTeX 渲染。
- `finish.py` 会做两遍编译：第一遍算出各章节的真实页码，第二遍回填目录，
  因此目录页码与正文始终一致。改动内容后务必用它重建，不要直接 `build.py`。
- KaTeX 字体必须完整（20 个 woff2）。缺少 `KaTeX_Main-Regular.woff2` 会导致
  `≠` 等符号显示成方框。
