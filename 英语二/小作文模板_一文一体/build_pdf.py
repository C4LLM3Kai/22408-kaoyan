#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成《英语二小作文 · 一文一模版》LaTeX 源文件并编译为 PDF。

用法：python3 build_pdf.py
依赖：XeLaTeX（/Library/TeX/texbin）、ctex、Times New Roman
"""
import os
import re
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from content import GENRES, EXAM_MAP  # noqa: E402

TEX_BIN = "/Library/TeX/texbin"
OUT_PDF = "英语二小作文_一文一模版.pdf"
ACCENT = "1F3A5F"
HOT = "A23B2A"
GRAY = "5B5B5B"
RULE = "C9D3DD"
SOFT = "F3F6F9"
SAND = "FBF4E6"

SPECIAL = {
    "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
    "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}
SLOT_RE = re.compile(r"【([^】]*)】")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
MARK_RE = re.compile(r"[①②③④⑤⑥⑦⑧⑨⑩]")


def esc(text):
    return "".join(SPECIAL.get(ch, ch) for ch in text)


def fx(text):
    """转义 + 槽位高亮 + 粗体 + 句号标号着色。"""
    out = esc(text)
    out = SLOT_RE.sub(lambda m: r"{\color{hot}\bfseries 【%s】}" % m.group(1), out)
    out = BOLD_RE.sub(lambda m: r"\textbf{%s}" % m.group(1), out)
    out = MARK_RE.sub(lambda m: r"{\color{accent}\bfseries %s}" % m.group(0), out)
    return out


def plain(text):
    return MARK_RE.sub("", text)


def fill_text(template_paras, fill):
    paras = []
    for para in template_paras:
        s = " ".join(para)
        for k, v in fill.items():
            s = s.replace("【%s】" % k, v)
        paras.append(s)
    return paras


TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*")


def wc(paras, closing=""):
    text = " ".join(paras)
    text = plain(text)
    return len(TOKEN_RE.findall(text))


def letter(paras, closing, sig, salutation="", title=""):
    """把段落渲染成考场信件/通知的样子。"""
    buf = []
    if title:
        buf.append(r"{\centering\bfseries\large %s\par}" % fx(title))
        buf.append(r"\vspace{2pt}")
    if salutation:
        buf.append(r"%s\par" % fx(salutation))
        buf.append(r"\vspace{3pt}")
    for para in paras:
        buf.append(r"%s\par" % fx(para))
        buf.append(r"\vspace{2pt}")
    if closing:
        if title:
            buf.append(r"\begin{flushright}%s\\%s\end{flushright}" % (fx(closing), fx(sig)))
        else:
            buf.append(r"\vspace{2pt}%s\par" % fx(closing))
            buf.append(r"%s\par" % fx(sig))
    return "\n".join(buf)


def boxed(body, bg=SOFT, frame=RULE, pad="3pt"):
    return (r"\noindent\fcolorbox{%s}{%s}{\begin{minipage}{\dimexpr\linewidth-2\fboxsep-2\fboxrule\relax}"
            r"\vspace{%s}\small\linespread{1.03}\selectfont %s\vspace{%s}\end{minipage}}\par"
            % (frame, bg, pad, body, pad))


# ---------------------------------------------------------------- 文档骨架

PREAMBLE = r"""
\documentclass[11pt,a4paper]{ctexart}
\usepackage{geometry}
\geometry{left=1.55cm,right=1.55cm,top=1.35cm,bottom=1.25cm,headsep=0.32cm,footskip=0.5cm}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\setsansfont{Helvetica}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{longtable}
\usepackage{amssymb}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage[hidelinks]{hyperref}
\hypersetup{pdftitle={英语二小作文·一文一模版},pdfauthor={DSH 学习助手},pdfsubject={考研英语二 Part A 应用文}}
\xeCJKDeclareCharClass{CJK}{"2460 -> "247F}
\xeCJKDeclareCharClass{CJK}{"25A0 -> "25FF}
\definecolor{accent}{HTML}{%s}
\definecolor{hot}{HTML}{%s}
\definecolor{gray}{HTML}{%s}
\definecolor{rule}{HTML}{%s}
\definecolor{soft}{HTML}{%s}
\definecolor{sand}{HTML}{%s}
\definecolor{sandline}{HTML}{DCCBA8}
\renewcommand{\familydefault}{\rmdefault}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\linespread{1.02}
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\fancyhead[L]{\footnotesize\color{gray} 英语二小作文 · 一文一模版}
\fancyhead[R]{\footnotesize\color{gray} Part A · 应用文}
\fancyfoot[L]{\footnotesize\color{gray} 12 类 · 每类一整篇}
\fancyfoot[R]{\footnotesize\color{gray} \thepage}
\renewcommand{\arraystretch}{1.12}
\setlength{\LTpre}{0pt}\setlength{\LTpost}{0pt}
""" % (ACCENT, HOT, GRAY, RULE, SOFT, SAND)


def cover():
    return r"""
\clearpage
\thispagestyle{empty}
\vspace*{0.55cm}
{\color{accent}\footnotesize\bfseries 考研英语（二）\quad Part A\quad 应用文写作}\par
\vspace{10pt}
{\color{accent}\rule{\linewidth}{2.4pt}}\par
\vspace{14pt}
{\fontsize{40}{44}\selectfont\bfseries 一文一模版}\par
\vspace{8pt}
{\LARGE\bfseries 英语二小作文 · 12 类文体 · 每类一整篇}\par
\vspace{8pt}
{\large\color{gray} 背一篇 → 换五个词 → 直接上考场}\par
\vspace{6pt}
{\color{accent}\rule{\linewidth}{0.9pt}}\par
\vspace{16pt}

\noindent\begin{minipage}[t]{0.32\linewidth}
{\color{accent}\fontsize{30}{32}\selectfont\bfseries 12}\par
{\small\color{gray} 类文体，覆盖 2010—2026\\全部英语二 Part A 真题}
\end{minipage}\hfill
\begin{minipage}[t]{0.32\linewidth}
{\color{accent}\fontsize{30}{32}\selectfont\bfseries 95–105}\par
{\small\color{gray} 词，每篇正文都按考场\\词数控制，逐篇统计}
\end{minipage}\hfill
\begin{minipage}[t]{0.32\linewidth}
{\color{accent}\fontsize{30}{32}\selectfont\bfseries 5}\par
{\small\color{gray} 个空，考场只改活动、\\时间、地点、理由、要求}
\end{minipage}\par

\vspace{22pt}
\noindent\colorbox{soft}{\parbox{\dimexpr\linewidth-2\fboxsep\relax}{%%
\vspace{5pt}
{\small\bfseries 这本书怎么用}\par\vspace{3pt}
{\footnotesize
一、先看第 2 页：分从哪来、格式怎么摆、三段各写几句。\par
二、再按第 3 页的真题地图，找到你要练的那一篇。\par
三、每篇只背“整篇模板”，然后用同一页的真题落地对照，看五个空怎么填。\par
四、写完用第 16 页的 60 秒自评表打勾，再按批改标准给自己定档。\par}
\vspace{5pt}}}

\vspace{12pt}
\noindent{\footnotesize\color{gray}
本书与市面“万能模板”的区别：不给你一堆可替换句型，而是给你 12 篇完整信件；\\每篇的骨架、衔接、语气是固定的，考场上只换信息，不现编句子。\\[3pt]
全部英文为原创；骨架按文体逐篇重写，不照搬南山《小作文万用模版》的万能句。}

\vspace{18pt}
{\color{accent}\bfseries 12 篇目录}\par\vspace{2pt}
{\color{rule}\rule{\linewidth}{0.5pt}}\par\vspace{3pt}
{\footnotesize
\noindent\begin{tabularx}{\linewidth}{@{}XXX@{}}
01\quad 邀请信 & 02\quad 接受邀请 & 03\quad 婉拒邀请 \\
04\quad 建议信 & 05\quad 感谢信 & 06\quad 祝贺信 \\
07\quad 道歉信 & 08\quad 投诉信 & 09\quad 咨询信 \\
10\quad 通知 & 11\quad 介绍·告知 & 12\quad 推荐信 \\
\end{tabularx}}\par
\vspace{2pt}
{\footnotesize\color{gray} 页码见页脚；先练 01、04、11 三篇（近五年高频），再补其余。}\par

\vspace{20pt}
{\color{rule}\rule{\linewidth}{0.5pt}}\par\vspace{8pt}
\noindent\begin{minipage}[t]{0.235\linewidth}
{\color{accent}\bfseries ① 定文体}\par{\scriptsize\color{gray} 第 3 页真题地图\\找动作词}
\end{minipage}\hfill
\begin{minipage}[t]{0.235\linewidth}
{\color{accent}\bfseries ② 背整篇}\par{\scriptsize\color{gray} 每页第一节\\完整信件}
\end{minipage}\hfill
\begin{minipage}[t]{0.235\linewidth}
{\color{accent}\bfseries ③ 换五词}\par{\scriptsize\color{gray} 同页换装表\\只改槽位}
\end{minipage}\hfill
\begin{minipage}[t]{0.235\linewidth}
{\color{accent}\bfseries ④ 自评}\par{\scriptsize\color{gray} 第 16 页\\60 秒清单}
\end{minipage}\par

\vfill
{\footnotesize\color{gray} 编写依据：考研英语（二）考试大纲对 Part A 的要求；评分档位按工作区《批改指令》的民间参考标准整理，不人为封顶。}\par
"""


def rules():
    rows1 = [
        ("任务完成", "题干两个动作都有落点", "动笔前把 1) 2) 抄在草稿纸，写完逐条打勾"),
        ("语言准确", "主谓一致、时态、搭配、拼写", "只用有把握的句型；不确定的词换简单词"),
        ("格式语气", "称呼、结束语、署名、通知标题落款", "按下面两张表套，30 秒能查完"),
        ("连贯变化", "段间有过渡，句式不重复", "每段首句换开头；I 开头不超过四句"),
    ]
    t1 = "\n".join("%s & %s & %s \\\\" % r for r in rows1)
    rows2 = [
        ("称呼", "顶格，逗号结尾；熟人用名，师长用姓", "Dear Jack, / Dear Professor Wang,"),
        ("正文", "2—3 段，每段一个功能，段首不空格", "见各文体页"),
        ("结束语", "顶格，逗号结尾，与署名同一语气层", "Yours sincerely, / Best wishes,"),
        ("署名", "另起一行，写题目指定姓名", "Li Ming / Zhang Wei"),
    ]
    t2 = "\n".join("%s & %s & %s \\\\" % r for r in rows2)
    rows3 = [
        ("标题", "居中，单独一行", "Notice"),
        ("称呼", "不写称呼", "—"),
        ("落款", "右下角两行：单位＋日期", "The Student Union / June 20, 2026"),
    ]
    t3 = "\n".join("%s & %s & %s \\\\" % r for r in rows3)
    return r"""
\clearpage
\vspace*{-4pt}
{\color{accent}\bfseries\LARGE 考场先看这一页}\par\vspace{3pt}
{\color{accent}\rule{\linewidth}{1.1pt}}\par
\vspace{5pt}
{\small\color{gray} 小作文 10 分，15 分钟。先保证“任务完成＋格式正确”，再谈语言漂亮。}\par
\vspace{8pt}

{\color{accent}\bfseries 一、阅卷人按四个维度给分}\par
{\color{rule}\rule{\linewidth}{0.5pt}}\par\vspace{2pt}
{\footnotesize
\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{2.0cm}>{\raggedright\arraybackslash}p{5.4cm}X@{}}
\toprule
{\color{accent}\bfseries 维度} & {\color{accent}\bfseries 卷面上看什么} & {\color{accent}\bfseries 你写的时候怎么做} \\
\midrule
%s
\bottomrule
\end{tabularx}}\par
\vspace{3pt}
{\footnotesize\color{gray} 四维里“任务完成”权重最高：漏一个动作，语言再好也上不了 7 分。}\par

\vspace{9pt}
{\color{accent}\bfseries 二、书信格式四要素（30 秒能查完）}\par
{\color{rule}\rule{\linewidth}{0.5pt}}\par\vspace{2pt}
{\footnotesize
\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{1.8cm}>{\raggedright\arraybackslash}p{6.2cm}X@{}}
\toprule
{\color{accent}\bfseries 位置} & {\color{accent}\bfseries 写法} & {\color{accent}\bfseries 例} \\
\midrule
%s
\bottomrule
\end{tabularx}}\par

\vspace{9pt}
{\color{accent}\bfseries 三、通知的三处不同}\par
{\color{rule}\rule{\linewidth}{0.5pt}}\par\vspace{2pt}
{\footnotesize
\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{1.8cm}>{\raggedright\arraybackslash}p{6.2cm}X@{}}
\toprule
{\color{accent}\bfseries 位置} & {\color{accent}\bfseries 写法} & {\color{accent}\bfseries 例} \\
\midrule
%s
\bottomrule
\end{tabularx}}\par

\vspace{9pt}
{\color{accent}\bfseries 四、三段各写几句}\par
{\color{rule}\rule{\linewidth}{0.5pt}}\par\vspace{2pt}
{\footnotesize
\begin{itemize}[leftmargin=1.2em,itemsep=1pt,topsep=1pt,parsep=0pt]
\item {\bfseries 第一段（1—2 句）}：写作目的＋事由。不写“I am a student”，不铺背景。
\item {\bfseries 第二段（3—4 句）}：全部任务要点，一个要点一句。合并题用 As for… / As to… 切开。
\item {\bfseries 第三段（1—2 句）}：期待、感谢、请回复，三选一，不重复第二段。
\end{itemize}}\par

\vspace{7pt}
{\color{accent}\bfseries 五、词数与时间}\par
{\color{rule}\rule{\linewidth}{0.5pt}}\par\vspace{2pt}
{\footnotesize
\begin{itemize}[leftmargin=1.2em,itemsep=1pt,topsep=1pt,parsep=0pt]
\item 正文 95—105 词，7—9 句；{\bfseries 称呼、结束语、署名不算}，也不写地址和日期（通知除外）。
\item 每行 10—12 词，卷面 8—10 行；超过 120 词不加分，只放大错误。
\item 15 分钟：审题画要点 3 分钟 → 写 10 分钟 → 检查 2 分钟。
\end{itemize}}\par

\vspace{7pt}
{\color{accent}\bfseries 六、六条铁律}\par
{\color{rule}\rule{\linewidth}{0.5pt}}\par\vspace{2pt}
{\footnotesize
\begin{enumerate}[leftmargin=1.4em,itemsep=0.5pt,topsep=1pt,parsep=0pt]
\item 落款用题目给的姓名（Li Ming / Zhang Wei），不写自己的名字。
\item 题干给了时间、地点、姓名，一律照抄；没给就补一个具体而不夸张的（next Saturday / Room 203）。
\item 合并题必须两段分明，段首用 As for… / As to… 提示阅卷人“第二个动作在这里”。
\item 不确定的难词一律换简单词；拼写错误比用词普通更扣分。
\item 称呼：熟人 Dear Jack,；师长 Dear Professor Wang,；不知姓名 Dear Sir or Madam,。
\item 通知不写称呼，标题居中，落款单位＋日期在右下角。
\end{enumerate}}\par
""" % (t1, t2, t3)


def exam_map():
    rows = "\n".join(
        "%s & %s & %s & %s \\\\" % (y, g, t, p) for y, g, t, p in EXAM_MAP
    )
    return r"""
\clearpage
\vspace*{-4pt}
{\color{accent}\bfseries\LARGE 真题地图：先定位，再动笔}\par\vspace{3pt}
{\color{accent}\rule{\linewidth}{1.1pt}}\par
\vspace{5pt}
{\small\color{gray} 题干永远给两件事：写什么（事务）＋要你完成什么动作。先找动作词，文体就定了。}\par
\vspace{5pt}
{\scriptsize
\begin{longtable}{@{}>{\raggedright\arraybackslash}p{1.15cm}>{\raggedright\arraybackslash}p{3.05cm}>{\raggedright\arraybackslash}p{7.9cm}>{\raggedright\arraybackslash}p{2.15cm}@{}}
\toprule
{\color{accent}\bfseries 年份} & {\color{accent}\bfseries 文体} & {\color{accent}\bfseries 题干两个动作} & {\color{accent}\bfseries 用哪篇} \\
\midrule
\endfirsthead
\toprule
{\color{accent}\bfseries 年份} & {\color{accent}\bfseries 文体} & {\color{accent}\bfseries 题干两个动作} & {\color{accent}\bfseries 用哪篇} \\
\midrule
\endhead
%s
\bottomrule
\end{longtable}}\par
\vspace{4pt}
{\footnotesize\color{gray} * 2026 为回忆版，以当年正式试题为准。}\par

\vspace{12pt}
{\color{accent}\bfseries 三条读表结论}\par
{\color{rule}\rule{\linewidth}{0.5pt}}\par\vspace{4pt}
{\footnotesize
\begin{enumerate}[leftmargin=1.4em,rightmargin=6pt,itemsep=2pt,topsep=1pt,parsep=0pt]
\item {\bfseries 十二类足够覆盖全部真题。}反复考的只有邀请、回复、建议、感谢、祝贺、道歉、投诉、咨询、通知、介绍；推荐与婉拒备作模拟。
\item {\bfseries 一半年份是“合并题”。}2010、2011、2014、2016、2019、2024 都是两个动作；写的时候第二段开头用 As for… 切开，阅卷人找得到第二个要点。
\item {\bfseries 近五年偏爱“介绍＋邀请 / 建议＋理由”。}2021—2025 全部落在 01、04、11 三篇里；这三篇要练到不看模板能写。
\end{enumerate}}\par

\vspace{8pt}
{\color{accent}\bfseries 合并题的五个现成切法}\par
{\color{rule}\rule{\linewidth}{0.5pt}}\par\vspace{4pt}
{\footnotesize
\begin{itemize}[leftmargin=1.2em,itemsep=2pt,topsep=1pt,parsep=0pt]
\item {\bfseries 2010 感谢＋邀请}：第二段接 05 的 By the way, you are welcome to…
\item {\bfseries 2011 祝贺＋建议}：第二段接 06 的 As you are about to… I would like to offer two suggestions.
\item {\bfseries 2014 告知＋咨询}：第二段接 09 的 To give you some idea of my habits…
\item {\bfseries 2019 建议＋安排}：第二段另起 As for the arrangements, the debate will take place…
\item {\bfseries 2024 计划＋征询}：结尾加一句 I wonder what you think of it.
\end{itemize}}\par

\vspace{8pt}
{\color{accent}\bfseries 文体频次（2010—2026，含合并题）}\par
{\color{rule}\rule{\linewidth}{0.5pt}}\par\vspace{4pt}
{\footnotesize\renewcommand{\arraystretch}{1.0}
\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{2.6cm}>{\raggedright\arraybackslash}p{0.9cm}>{\raggedright\arraybackslash}p{0.9cm}>{\raggedright\arraybackslash}p{6.4cm}X@{}}
\toprule
{\color{accent}\bfseries 文体} & {\color{accent}\bfseries 次数} & {\color{accent}\bfseries 篇} & {\color{accent}\bfseries 年份} & {\color{accent}\bfseries 频次条} \\
\midrule
建议 & 5 & 04 & 2011·2016·2019·2023·2024 & {\color{accent}■■■■■} \\
介绍·告知 & 5 & 11 & 2014·2020·2022·2024·2025 & {\color{accent}■■■■■} \\
邀请 & 4 & 01 & 2010·2021·2022·2025 & {\color{accent}■■■■} \\
感谢 & 3 & 05 & 2010·2016·2026* & {\color{accent}■■■} \\
通知 & 2 & 10 & 2013·2015 & {\color{accent}■■} \\
祝贺 & 2 & 06 & 2011·2016 & {\color{accent}■■} \\
咨询 & 2 & 09 & 2014·2026* & {\color{accent}■■} \\
投诉 & 1 & 08 & 2012 & {\color{accent}■} \\
道歉 & 1 & 07 & 2018 & {\color{accent}■} \\
\bottomrule
\end{tabularx}}\par
""" % rows


def genre_page(g):
    paras = g["paras"]
    filled = fill_text(paras, g["fill"])
    body_words = wc(filled)
    n_sent = sum(len(p) for p in paras)
    if not (88 <= body_words <= 112):
        print("WARN 词数越界：%s %s -> %d" % (g["num"], g["cn"], body_words))

    EX_SAL = {
        "01": "Dear Jack,", "02": "Dear Professor Williams,", "03": "Dear Professor Wang,",
        "04": "Dear David,", "05": "Dear Mr. Smith,", "06": "Dear Li Ming,",
        "07": "Dear Professor Smith,", "08": "Dear Sir or Madam,", "09": "Dear John,",
        "10": "", "11": "Dear friends,", "12": "Dear Jack,",
    }
    EX_SIG = {"05": "Zhang Wei", "06": "Zhang Wei", "08": "Zhang Wei"}

    if g["num"] == "10":
        title = "Notice"
        tpl_closing, tpl_sig = "【主办方】", "【日期】"
        ex_closing, ex_sig = "The Student Union", "June 20, 2026"
        tpl_salutation = ex_salutation = ""
    else:
        title = ""
        tpl_closing, tpl_sig = g["closing"], g["sig"]
        ex_closing, ex_sig = g["closing"], EX_SIG.get(g["num"], g["sig"])
        tpl_salutation = "Dear 【称呼】,"
        ex_salutation = EX_SAL[g["num"]]

    tpl = boxed(letter(paras, tpl_closing, tpl_sig, salutation=tpl_salutation, title=title),
                bg="soft", frame="rule")
    ex = boxed(letter(filled, ex_closing, ex_sig, salutation=ex_salutation, title=title),
               bg="sand", frame="sandline")

    swaps = "\n".join(
        r"%s & %s & %s \\" % (fx(a).replace(r"\color{hot}", r"\color{hot}"), b, c)
        for a, b, c in g["swaps"]
    )
    # 槽位列用普通字号，避免整列发红
    swaps = "\n".join(
        r"%s & %s & %s \\" % (esc(a), b, c) for a, b, c in g["swaps"]
    )

    score = "\n".join(r"\item %s" % s for s in g["score"])
    traps = "\n".join(r"\item %s" % s for s in g["traps"])

    header_note = "正文 %d 词 · %d 句" % (body_words, n_sent)

    return r"""
\clearpage
\phantomsection\label{g%s}
\noindent{\color{accent}\rule{\linewidth}{1.5pt}}\par\vspace{3pt}
\noindent{\fontsize{26}{28}\selectfont\bfseries\color{accent}%s}\hspace{6pt}
{\LARGE\bfseries %s}\hspace{7pt}{\large\color{gray} %s}\hfill
{\footnotesize\color{gray} 真题 %s}\par
\vspace{1pt}
{\color{accent!35}\rule{\linewidth}{0.5pt}}\par\vspace{3pt}
{\footnotesize {\color{accent}\bfseries 题干信号}\quad %s}\par
{\footnotesize {\color{accent}\bfseries 写作身份}\quad %s}\par
{\footnotesize {\color{accent}\bfseries 必须写到}\quad %s}\par
{\footnotesize {\color{accent}\bfseries 一句话策略}\quad %s}\par

\vspace{5pt}
{\color{accent}\bfseries 一、整篇模板（背这一篇）}\hfill{\footnotesize\color{gray} %s}\par
\vspace{2pt}
%s
\vspace{1pt}
{\footnotesize\color{gray} 段落分工｜%s}\par

\vspace{6pt}
{\color{accent}\bfseries 二、真题落地（%s）}\par
\vspace{2pt}
%s

\vspace{6pt}
{\color{accent}\bfseries 三、换装表（只改这几处）}\par
\vspace{2pt}
{\footnotesize
\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{3.5cm}>{\raggedright\arraybackslash}p{5.6cm}X@{}}
\toprule
{\color{accent}\bfseries 槽位} & {\color{accent}\bfseries 本篇真题怎么填} & {\color{accent}\bfseries 可换词块} \\
\midrule
%s
\bottomrule
\end{tabularx}}\par

\vspace{5pt}
\noindent\begin{minipage}[t]{0.555\linewidth}
{\color{accent}\bfseries 四、阅卷人找什么}\par
{\footnotesize\begin{itemize}[leftmargin=1.2em,itemsep=1pt,topsep=1pt,parsep=0pt]\setlength{\leftmargin}{1.1em}
%s
\end{itemize}}
\end{minipage}\hfill
\begin{minipage}[t]{0.415\linewidth}
{\color{hot}\bfseries 别踩这两个坑}\par
{\footnotesize\begin{itemize}[leftmargin=1.2em,itemsep=1pt,topsep=1pt,parsep=0pt]\setlength{\leftmargin}{1.1em}
%s
\end{itemize}}
\end{minipage}\par

\vspace{6pt}
{\color{accent}\bfseries 五、想上 9 分，从这两句里挑一句加在结尾}\par
\vspace{2pt}
{\footnotesize
\begin{itemize}[leftmargin=1.2em,itemsep=1.5pt,topsep=1pt,parsep=0pt]
\item %s\quad{\color{gray}（%s）}
\item %s\quad{\color{gray}（%s）}
\end{itemize}}\par

\vspace{6pt}
{\color{accent}\bfseries 六、题干变体怎么改（同一篇，换两个词）}\par
\vspace{2pt}
{\footnotesize
\begin{itemize}[leftmargin=1.2em,itemsep=1.5pt,topsep=1pt,parsep=0pt]
\item %s
\item %s
\end{itemize}}\par
""" % (g["num"], g["num"], esc(g["cn"]), esc(g["en"]), esc(g["years"]),
       esc(g["signal"]), esc(g["identity"]), esc(g["must"]),
       esc(g["strategy"]), header_note, tpl, g["split"], esc(g["example_label"]), ex,
       swaps, score, traps,
       fx(g["upgrade"][0][0]), esc(g["upgrade"][0][1]),
       fx(g["upgrade"][1][0]), esc(g["upgrade"][1][1]),
       esc(g["variants"][0]), esc(g["variants"][1]))


def appendix():
    checks = [
        "两个任务动作都写了吗（题干的 1) 2)）",
        "时间、地点、数字写了吗",
        "称呼有逗号，结束语有逗号，署名顶格吗",
        "通知有标题和右下角落款吗",
        "时态统一吗（邀请/安排用将来，感谢/投诉用过去）",
        "主谓一致吗（there are / it is / people are）",
        "拼写检查了吗（receive, convenient, sincerely）",
        "正文 95—105 词吗（不含称呼与落款）",
        "每段都有连接词吗（As for / Besides / Therefore）",
        "有没有写“I am a student”这类无关背景",
        "有没有把题目姓名写成自己的名字",
        "有没有空行分三段（通知可分两段）",
    ]
    ck = "\n".join(r"\item[$\square$] %s" % c for c in checks)

    errors = [
        ("congratulations for", "congratulations on"),
        ("look forward to meet you", "look forward to meeting you"),
        ("I would appreciate if", "I would appreciate it if"),
        ("grateful to your help", "grateful for your help"),
        ("suggest you to go", "suggest that you go"),
        ("There will have a meeting", "There will be a meeting"),
        ("I look forward to hear from you", "I look forward to hearing from you"),
        ("a lot of informations", "a lot of information"),
        ("take part in the meeting", "attend the meeting"),
        ("I am agree with you", "I agree with you"),
        ("pay attention on", "pay attention to"),
        ("It is high time we start", "It is high time we started"),
    ]
    err_rows = "\n".join("%s & %s \\\\" % (a, b) for a, b in errors)

    return r"""
\clearpage
\vspace*{-4pt}
{\color{accent}\bfseries\LARGE 交卷前 60 秒：自评与自查}\par\vspace{3pt}
{\color{accent}\rule{\linewidth}{1.1pt}}\par
\vspace{6pt}

\noindent\begin{minipage}[t]{0.49\linewidth}\raggedright
{\color{accent}\bfseries 一、十二条打勾清单}\par
{\footnotesize\begin{itemize}[leftmargin=1.2em,itemsep=1.5pt,topsep=1pt,parsep=0pt]
%s
\end{itemize}}
\end{minipage}\hfill
\begin{minipage}[t]{0.49\linewidth}\raggedright
{\color{accent}\bfseries 二、按档位给自己定位}\par
{\footnotesize
漏一个任务动作 → 最高 6 分档；漏两个 → 4 分档以下。\par\vspace{3pt}
格式错一处（称呼/落款/通知标题）→ 6—7 分档；错两处以上 → 5 分档。\par\vspace{3pt}
语言偶有小错但意思清楚 → 6—7 分；错误影响理解 → 4—5 分。\par\vspace{3pt}
要点全、格式对、有两处自然衔接、无明显错误 → 8—9 分。\par\vspace{3pt}
以上都对，且句式有变化、用词准确 → 可以到 10 分，不人为封顶。\par}
\end{minipage}\par

\vspace{12pt}
{\color{accent}\bfseries 三、十二组高频错误（左边一律改成右边）}\par
{\color{rule}\rule{\linewidth}{0.5pt}}\par\vspace{3pt}
{\footnotesize
\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}X>{\raggedright\arraybackslash}X@{}}
\toprule
{\color{hot}\bfseries 错误写法} & {\color{accent}\bfseries 正确写法} \\
\midrule
%s
\bottomrule
\end{tabularx}}\par

\vspace{12pt}
{\color{accent}\bfseries 四、通用零件（不够用时从这里取，别再另背一套）}\par
{\color{rule}\rule{\linewidth}{0.5pt}}\par\vspace{4pt}
{\footnotesize
\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{2.1cm}X@{}}
\toprule
{\color{accent}\bfseries 功能} & {\color{accent}\bfseries 现成表达} \\
\midrule
开头 & I am writing to invite / thank / complain about…；I was delighted to learn that… \\
收尾 & I look forward to your reply. / Thank you for your time and consideration. \\
理由 & For one thing… For another…；The main reason is that… \\
请求 & I would be grateful if you could…；Would it be possible for you to…? \\
时间地点 & next Saturday at 3 p.m. in Room 203；from July 10 to July 20；by Friday \\
人数与费用 & twenty volunteers；free of charge；a deposit of 200 yuan \\
\bottomrule
\end{tabularx}}\par

\vspace{10pt}
\noindent\colorbox{sand}{\parbox{\dimexpr\linewidth-2\fboxsep\relax}{%%
\vspace{4pt}{\footnotesize
{\bfseries 最后一句：}小作文不是比谁句子长，是比谁把两个动作写全、把格式写对、把话说清楚。\\
背完整篇之后，一定要掐 15 分钟在答题卡上默写一遍；模板只有落到纸上，才是你的。}
\vspace{4pt}}}
""" % (ck, err_rows)


def build():
    parts = [PREAMBLE, r"\begin{document}", cover(), rules(), exam_map()]
    for g in GENRES:
        parts.append(genre_page(g))
    parts.append(appendix())
    parts.append(r"\end{document}")

    tex = "\n".join(parts)
    tex_path = os.path.join(BASE, "英语二小作文_一文一模版.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex)

    env = dict(os.environ)
    env["PATH"] = TEX_BIN + ":" + env.get("PATH", "")
    for _ in range(2):
        r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error",
                            os.path.basename(tex_path)],
                           cwd=BASE, env=env, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
        if r.returncode != 0:
            print(r.stdout.decode("utf-8", "replace")[-4000:])
            raise SystemExit("XeLaTeX 编译失败")
    print("PDF 已生成：", os.path.join(BASE, OUT_PDF))

    # 页数与预览
    import fitz
    doc = fitz.open(os.path.join(BASE, OUT_PDF))
    print("页数：", doc.page_count)
    os.makedirs(os.path.join(BASE, "preview"), exist_ok=True)
    for i in range(doc.page_count):
        pix = doc[i].get_pixmap(dpi=110)
        pix.save(os.path.join(BASE, "preview", "p%02d.png" % (i + 1)))
    for g in GENRES:
        filled = fill_text(g["paras"], g["fill"])
        print("%s %s 正文 %d 词" % (g["num"], g["cn"], wc(filled)))


if __name__ == "__main__":
    build()
