from pathlib import Path
import json,re
R=Path(__file__).parent
items=json.loads((R/'templates.json').read_text())
sources=json.loads((R/'sources.json').read_text())
report=json.loads((R/'overlap_report.json').read_text())
OUT=R/'英语二作文_36类融合模板.tex'
def esc(s):
 return ''.join({'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}.get(c,c) for c in s)
def txt(s):
 chunks=re.split(r'(【.*?】)',s)
 return ''.join(r'{\bfseries '+esc(c)+'}' if c.startswith('【') else esc(c) for c in chunks)
def wc(s):return len(re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*|\d+(?:[.,]\d+)*(?:%)?",s))
def para(s):return txt(s)+'\n\n'
def section(title):return r'\clearpage\section*{'+esc(title)+r'}\addcontentsline{toc}{section}{'+esc(title)+'}\n'
def table(headers,rows,cols):
 s=r'\begin{longtable}{'+cols+r'}\toprule'+'\n'+' & '.join(r'\textbf{'+esc(x)+'}' for x in headers)+r'\\\midrule\endhead'+'\n'
 s+='\n'.join(' & '.join(esc(str(v)) for v in row)+r'\\' for row in rows)
 return s+'\n'+r'\bottomrule\end{longtable}'+'\n'
def blocktitle(s):return r'\par\vspace{4pt}{\bfseries '+esc(s)+r'}\par\nopagebreak'+'\n'
def display_header(x,template=False):
 h=x['header']
 if template:
  if x['kind']=='书信':h='Dear 【对方称呼】,'
  elif x['kind']=='纪要':h='Minutes of 【会议名称】\nDate: 【日期】   Place: 【地点】\nPresent: 【与会者】'
  elif x['kind']=='备忘录':h='MEMO\nTo: 【收件对象】   From: 【发件人】\nDate: 【日期】   Subject: 【主题】'
  elif x['kind']=='通知':h='NOTICE\n【具体活动或招募标题】'
  elif x['id']=='A22':h='LOST\n【遗失物品】'
  elif x['id']=='A23':h='FOUND\n【拾得物品】'
  elif x['kind']=='倡议':h='【与倡议目标相符的标题】'
 if not h:return ''
 lines=h.split('\n')
 if x['kind'] in ['通知','告示','倡议']:
  return r'{\centering '+r'\\'.join(txt(z) for z in lines)+r'\par}'+ '\n'
 if x['kind']=='纪要':
  return r'{\centering '+txt(lines[0])+r'\par}'+ '\n'+r'\noindent '+r'\\'.join(txt(z) for z in lines[1:])+r'\par'+'\n'
 ss=r'\noindent '+r'\\'.join(txt(z) for z in lines)+r'\par'+'\n'
 return ss
preamble=r'''% !TEX program = xelatex
\documentclass[11pt,a4paper,fontset=macnew]{ctexart}
\usepackage[left=20mm,right=20mm,top=19mm,bottom=19mm,headsep=5mm]{geometry}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\setsansfont{Arial}
\usepackage{booktabs,longtable,tabularx,array,enumitem,needspace,fancyhdr,xcolor}
\usepackage[hidelinks,bookmarksopen=true,bookmarksnumbered=false]{hyperref}
\hypersetup{pdftitle={英语二作文：36类融合模板},pdfauthor={学习资料整合},pdfsubject={按用户提供的批改指令综合重写；应用文与大作文}}
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\setlength{\parindent}{0pt}
\setlength{\parskip}{3pt}
\linespread{1.10}
\setlength{\emergencystretch}{2em}
\setlength{\tabcolsep}{4pt}
\renewcommand{\arraystretch}{1.18}
\setlist[itemize]{leftmargin=1.35em,itemsep=3pt,topsep=3pt}
\setlist[enumerate]{leftmargin=1.6em,itemsep=3pt,topsep=3pt}
\ctexset{section/format={\Large\bfseries},section/beforeskip=0pt,section/afterskip=8pt,subsection/format={\large\bfseries},subsection/beforeskip=9pt,subsection/afterskip=4pt}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small 英语二作文 \quad 多源融合模板}
\fancyhead[R]{\small\nouppercase{\leftmark}}
\fancyfoot[C]{\small\thepage}
\setlength{\headheight}{15pt}
\renewcommand{\headrulewidth}{0.3pt}
\newenvironment{writing}{\begingroup\fontsize{10.5}{13.5}\selectfont\setlength{\parskip}{3pt}}{\par\endgroup}
\newenvironment{example}{\begingroup\fontsize{11}{14.3}\selectfont\setlength{\parskip}{4pt}}{\par\endgroup}
\begin{document}
\thispagestyle{empty}
\vspace*{25mm}
{\small 2027 考研备考资料 · 英语二专用}\par
\vspace{12mm}
{\fontsize{31}{39}\selectfont\bfseries 英语二作文}\par
\vspace{4mm}
{\fontsize{23}{31}\selectfont\bfseries 36 类融合模板}\par
\vspace{10mm}
\rule{\linewidth}{1pt}\par
\vspace{5mm}
{\Large 26 类应用文 \quad 10 类大作文写法}\par
\vspace{6mm}
可替换模板 · 完整套用示例 · 108 条表达讲解\par
任务核对 · 数据辨析 · 逐篇文字重合检查\par
\vspace{14mm}
\begin{tabularx}{\linewidth}{@{}L{30mm}X@{}}
整理依据 & 用户提供的作文讲义、素材库、方法论笔记及真题配套资料。\\[5pt]
质量标准 & 《考研英语批改指令》第5页、第6页的英语二写作要求。\\[5pt]
词数 & 示例：应用文正文99—109词；大作文147—155词。\\[5pt]
使用原则 & 先答完整题目，再选准确表达；保留文体框架，按情境改写内容。\\
\end{tabularx}
\vfill
{\small 多来源综合新编 \quad 2026年10月25日}\par
{\small 本册的情境与数据均为练习用途；不把模板本身等同于某个确定分数。}
\clearpage
\markboth{目录}{}
\tableofcontents
'''
s=[preamble]
s.append(section('先看这两页：如何使用与如何判定质量'))
s.append(r'\markboth{使用与标准}{}'+'\n')
s.append(para('本册是综合改写后的英语二写作手册。A01—A26 按应用文功能与格式分类；B01—B10 按材料形式及数据关系分类。相近文体有可迁移的表达，但答复信仍须逐项回应来信，混合任务题必须完成题干的每一个动作。'))
s.append(blocktitle('按下面的顺序套用'))
s.append(r'\begin{enumerate}\item 圈出身份、对象、文体和任务动词。先在草稿纸写出任务一、任务二；若有第三项，也要落实到正文。\item 选最接近的模板，把【】中的提示全部换成英文。模板保留固定句法；示例展示同一类任务怎样写具体，不要求与模板逐字对应。\item 优先填写题目明示的信息。题目允许时可以合理补充活动细节；图表数值、比例、时间、单位则必须照材料写。\item 换题后重读整篇：主语、代词、时态、单复数、活动名称和结论要一致。删去与本题无关的句子，再统计词数。\end{enumerate}'+'\n')
s.append(table(['占位提示','该填什么','示例'],[
['动词原形','不带 to 的动词短语','review the draft'],['动名词','doing 短语','reviewing the draft'],['完整分句','主语＋谓语；不自带句末标点','the opening hours are inconvenient'],['完整句','包含主语、谓语及句末标点','The proportion rose to 45%.'],['陈述语序疑问词从句','嵌入问句；不再次倒装','when the course begins']],r'L{28mm}L{60mm}L{65mm}'))
s.append(blocktitle('字数、格式和优先顺序'))
s.append(para('以实际题干为准。常见英语二小作文要求约100词、大作文约150词；“约”不等于固定下限。本册给的是完整示例的统计值，占位模板不标虚假的成文词数。英文缩写及连字符词通常算一词，数值算一词；具体分词方式可能产生少量差异。'))
s.append(para('正文词数不包括称呼、结束语、姓名；通知标题和落款、纪要／备忘录信息栏也另列。各示例另注明这些格式信息的词数，方便核查。考场是否需要日期、标题、邮箱或特定落款，先看题目要求。'))
s.append(para('先练书信常见任务、活动通知和静态／动态图表；然后熟悉纪要、备忘录和复合材料的结构。这是使用顺序，不是对下一次考试题型的预测。'))
s.append(r'\clearpage'+blocktitle('以用户给定批改指令为标准'))
s.append(para('以下档位来自 S09《考研英语批改指令》PDF第5、6页，是该文件整理的练习评分参考，不冒充官方评分细则。采用的是内容、语言、结构和格式的综合评价，不按复杂句数量计分，也不编造“每少10词扣1分”等规则。'))
s.append(table(['小作文／10分','本册落实方式'],[
['8—9；充分优秀可10','完成全部任务；语言准确自然、有变化；格式与双方关系匹配。'],['6—7','主要要点完整；偶有错误；组织清楚、语气适合。'],['4—5','多数要点覆盖；部分语言问题不妨碍整体理解。'],['2—3／1／0','依次对应重要遗漏或语言影响理解、基本未完成、无可评价内容。']],r'L{35mm}L{122mm}'))
s.append(table(['大作文／15分','本册落实方式'],[
['13—15','数据描述准确，任务完整，评论贴题且有展开；语言准确、层次清楚。'],['10—12','主要要点完整，语言较丰富；偶有错误，整体连贯。'],['7—9','多数要点覆盖；描述评论基本合理；错误不妨碍理解。'],['4—6／1—3／0','依次对应重要遗漏或理解偏差、严重偏题且难以表达、无可评价内容。']],r'L{35mm}L{122mm}'))
s.append(blocktitle('本册每篇都按这五项核对'))
s.append(r'\begin{enumerate}\item \textbf{任务：}请求邀请时明确邀请，请求建议时给行动和理由，要求征求意见时写出问题。\item \textbf{语言：}选择常用但准确的动词和搭配；有短句也有适量从句，不为“高级”增加错误风险。\item \textbf{组织：}每一段有任务；句子之间共享具体主题，不靠反复套用 firstly、moreover 撑起逻辑。\item \textbf{图表：}先描述可见事实，再以 may/could 等表达合理解释；静态类别、不同人群、时间趋势分别处理。\item \textbf{格式：}书信有称呼和署名；通知告示有标题和发布者；纪要记录决议与分工；备忘录突出收发信息和行动。\end{enumerate}'+'\n')
s.append(para('本册没有给模板预判“稳拿几分”。实际得分还取决于当场是否切题、信息是否完整、替换后语言是否正确及书写是否清楚。'))

for x in items:
 isbig=x['id'].startswith('B')
 title=x['id']+'  '+x['title']
 s.append(section(title));s.append(r'\markboth{'+esc(x['id']+' '+x['kind'])+'}{}\n')
 s.append(r'{\small '+txt(x['task'])+'}\par\n')
 s.append(r'{\small\textbf{行文路线：}'+txt(x['logic'])+'}\par\n')
 s.append(blocktitle('可替换模板'))
 s.append(r'\begin{writing}'+'\n')
 s.append(display_header(x,True))
 for p in x['template']:s.append(para(p))
 if x['footer']:
  # Honor actual genre rather than displaying a misleading full letter ending everywhere.
  foot=x['footer'] if x['kind']=='书信' else '【题目要求的署名或发布单位】' if x['kind']!='纪要' else 'Recorded by: 【记录人】'
  s.append(r'\noindent '+r'\\'.join(txt(a) for a in foot.split('\n'))+r'\par'+'\n')
 s.append(r'\end{writing}'+'\n')
 s.append(blocktitle('完整套用示例'))
 bcount=wc(' '.join(x['body']));fcount=wc(x['header']+' '+x['footer'])
 note=f'正文 {bcount} 词'
 if fcount:note+=f'；标题／称呼／落款等另 {fcount} 词'
 s.append(r'{\small '+esc(note)+'}\par\n')
 s.append(r'\begin{example}'+'\n');s.append(display_header(x))
 for p in x['body']:s.append(para(p))
 if x['footer']:s.append(r'\noindent '+r'\\'.join(txt(a) for a in x['footer'].split('\n'))+r'\par'+'\n')
 s.append(r'\end{example}'+'\n')
 s.append(blocktitle('好词好句：优先记这三处'))
 for en,zh in x['phrases']:s.append(r'{\small\textbf{'+esc(en)+'} — '+esc(zh)+'}\par\n')
 s.append(r'{\small\textbf{核对重点：}'+txt(x['check'])+'}\par\n')
 s.append(r'{\fontsize{8}{10}\selectfont\textbf{来源线索：}'+esc(x['source'])+'。}\par\n')

s.append(section('表达速查：把好句用在合适的地方'))
s.append(r'\markboth{表达速查}{}'+'\n')
s.append(para('本册每篇的三条表达共108条，既包含实用词组，也包含可迁移句法。下面这些结构优先掌握；每次选与任务有关的两三条，不要把整页连续塞进一篇作文。'))
s.append(table(['用途','可迁移表达','如何用'],[
['建议＋结果','Start by doing ... This will help you ...','先给具体操作，再解释效果。'],['需求匹配','a good match for your interest in ...','推荐理由要对应对方兴趣。'],['邀请角色','have you as our guest speaker','说清对方以什么身份参加。'],['尊重时间','whether this would fit your schedule','向教授求助或协调安排。'],['承担责任','I owe you an apology for doing ...','明确为哪件事道歉。'],['补救办法','Until then, I can ...','给出最终解决前的临时安排。'],['事实核查','check ... against the original records','核查姓名、时间和数据。'],['申请价值','support the team with ...','把技能与岗位需要相连。'],['数据比较','its lead over ... narrowed','写两个指标差距缩小。'],['波动','an uneven upward path','总体上升但中间有回落。'],['群体范围','among the students surveyed','限制在题目调查样本内。'],['条件性判断','where appropriate','在适当条件下，不无条件套用。'],['给出机制','By doing ..., ... can ...','分词逻辑主语必须与主句一致。'],['谨慎解释','One possible explanation is that ...','说明是假设解释，不是图表证明。'],['有依据的推论','The example suggests that ...','先有例子，再给推论。'],['具体改进','collect users’ feedback before ...','先收集反馈，再改变安排。']],r'L{25mm}L{72mm}L{56mm}'))
s.append(blocktitle('从“显得高级”转向“说得准确”'))
s.append(para('increase／rise 通常比不自然的 ascend 或 augment 更好用；the proportion of... 用于比例，the number of... 用于数量；information、advice、equipment 通常不可数。不用为了避重复把所有 people 替换成 individuals 或把 letter 替换成 missive。'))
s.append(section('图表与语言：交卷前的核对表'))
s.append(r'\markboth{核对表}{}'+'\n')
s.append(table(['容易混淆处','准确写法或判断'],[
['30% → 45%','rose by 15 percentage points；相对增长为50%，不是15%。'],['数量120 → 180','rose by 60；相对增长50%；rose to 180 是升至180。'],['45%为最大项','the largest share；未超过50%，不用 a majority。'],['不同群体的数据','18—29岁与50岁以上的对比，不是时间上的增长过程。'],['只有起点终点','能说 increased，不足以证明 steadily／持续平稳。'],['多选合计超过100%','可合理；各类别重叠，不能计算“剩余人群”。'],['份额下跌','不能在未知总体时断言数量下跌。'],['人次与人数','visits 是人次；visitors 是访客人数，两者不互换。'],['两幅图相关','can suggest a possible link，不等于证明因果。'],['过去数据与当前解释','已结束年份的数据用过去时；一般机制可用现在时。'],['副词与形容词','rose sharply；a sharp rise；不要 a sharply rise。'],['两个并列数据','A and B were 20% and 30%, respectively；顺序必须一一对应。'],['建议信动词','suggest doing／suggest that you do；不是 suggest you to do。'],['期待与道歉','look forward to hearing；apologise to somebody for doing。'],['咨询中的从句','Could you tell me when it begins?；从句不用 when does it begin。'],['单复数','the number of students is ...；a number of students are ...。']],r'L{37mm}L{120mm}'))
s.append(blocktitle('60秒终检'))
s.append(para('逐一划去任务清单上的要点；核对图表标题、对象、年份、单位和数字；检查每段是否有具体信息；核对称呼和 Li Ming；检查第三人称单数、时态、冠词、单复数、拼写；最后删去占位提示。'))
s.append(para('同类题复习时可以只背一篇完整示例，但必须另练一次换题：先只看中文任务写出结构，再用新数据或新活动填内容。若某句离开示例就不会改，优先把那一句改成自己能准确写出的短句。'))

s.append(section('文字重合检查：方法、结果与边界'))
s.append(r'\markboth{文字重合检查}{}'+'\n')
s.append(para('为落实“不与任何一个文件相似程度大于50%”，本册采用公开、可复核的文字重合指标。它衡量英文原文复用，不衡量意义相似度，也不能代表某个商业系统的查重结论。以下结果仅适用于本次版本及已经识别出的文本。'))
s.append(blocktitle('比较范围与计算方法'))
s.append(para('处理用户给出的40个PDF，共1164页（含重复文件及408大纲）。可提取的正文使用PDF文字层；扫描正文或乱码文字层经macOS Vision识别。S07使用工作区已保存的完整OCR；S11与S12字节一致，但仍分别纳入比对。S02是计算机考纲，不参与写作内容筛选，仍列入机器比对。图片中的文字和扫描件仍可能存在漏识别或错识别。'))
s.append(para('对每篇模板与每篇示例分别比较，不靠整本文档长度稀释结果。英文转为小写，标点、数字不参与匹配，连字符词拆开；不删除常见虚词。模板的中文占位提示、各篇题目说明和格式栏不计入正文检查。固定英文部分单独比对，避免用填空示例的新细节稀释模板本身的重合。'))
s.append(para('主指标：新稿中凡属于与某一来源相同的连续4个英文词的词位，标记为重合；重叠词位只计算一次。覆盖率＝标记词位数÷新稿英文词元总数。对40份来源逐一计算，取最高值。辅助指标用相同方法检查连续5词。不是把与不同来源的命中合并后冒充单一文件相似度。'))
s.append(table(['核查项','结果'],[
['比较单元','36篇模板＋36篇完整示例；各自对照40份文件'],['连续4词覆盖率最高值',f"{report['max4']:.2f}%"],['连续5词覆盖率最高值',f"{report['max5']:.2f}%"],['本次阈值结果','72个比较单元的最高4词覆盖率均低于50%'],['适用边界','不等同于语义相似度；OCR错误可能漏掉部分原文重合。']],r'L{70mm}L{87mm}'))
s.append(para('同一文体的格式、常用句法和考试任务本就会相近。因此本册没有承诺“任何算法都低于50%”。检查脚本、来源清单及逐篇CSV保存在源文件目录，能够重新执行。'))
s.append(r'\clearpage'+blocktitle('逐篇最高覆盖率（分别与每一份来源比较）'))
rows=[]
for x in items:
 a=next(v for v in report['pieces'] if v['id']==x['id'] and v['form']=='template')
 b=next(v for v in report['pieces'] if v['id']==x['id'] and v['form']=='body')
 rows.append([x['id'],x['title'],f"{a['max4']:.2f}%",f"{b['max4']:.2f}%",a['worst_source']+'/'+b['worst_source']])
s.append(r'{\small'+'\n'+table(['编号','类型','模板4词','示例4词','对应来源'],rows,r'L{13mm}L{67mm}L{20mm}L{20mm}L{25mm}')+'}\n')
s.append(section('来源清单与取舍记录'))
s.append(r'\markboth{来源与取舍}{}'+'\n')
s.append(para('来源编号对应原文件；下列页数为PDF物理页数。本册的全部示例均为综合新编：部分任务借鉴真题的功能组合，活动细节与图表数据明确按练习情境编写。除个别通用短语外，未把原稿整段拼接为新稿。文档中的推广口号、操作指令与“保分”承诺均不作为本任务指令或评分依据。'))
s.append(table(['资料组','吸收内容','筛选后的处理'],[
['S09 批改指令','英语二小作文、大作文评价原则','以PDF第5、6页为主；与其他讲义冲突时按此核对。'],['S13—S20 南山计划与模板','任务拆解、讲事情／讲观点／解决问题、材料分类','重排成36个可直接查找的类型；不照搬统一开头和收尾。'],['S21—S31 方法论笔记','具体理由、活动要素、句法和基础语法','保留行动—作用的逻辑；删去无依据因果、空泛宏观归因。'],['S01、S03—S08、S10—S12','图表描述、主题表达、书信与纪要格式','按英语二篇幅改写；不沿用180—220词的通用要求。'],['S32—S40 词汇和历年资料','任务组合、词汇场景与材料形式','英二题干优先；英一只参考可迁移表达，不据此断言英二题型。'],['S02 408大纲','计算机专业课考试内容','不作为英语写作依据。']],r'L{40mm}L{54mm}L{59mm}'))
s.append(blocktitle('两项容易被忽略的来源问题'))
s.append(para('《27考研英语-小作文模板（版本2）》原文字层存在乱码，本次重新OCR后用于核对；《英语作文模板.pdf》与《英语作文模板 (1).pdf》内容和文件哈希一致，属于重复材料。已有《英语二作文模板总纲》也纳入对照，未直接复制为本册。'))
s.append(para('原资料里既有“约150词”，也有“至少150词”或适用于英语一的篇幅建议；本册不混用。实际作答最终以当场题干为准。自然、准确的短句可以保留，生僻词和长句不自动加分。'))
for start,end in [(0,14),(14,27),(27,40)]:
 s.append(r'\clearpage'+blocktitle(f'原文件索引 {start+1}—{end}'))
 rows=[]
 for v in sources[start:end]:
  role='非英语材料' if v['id']=='S02' else '评分依据' if v['id']=='S09' else '与S11重复' if v['id']=='S12' else 'OCR' if 'OCR' in v.get('text_method','') else '文本层'
  rows.append([v['id'],v['name'],v['pages'],role])
 s.append(r'{\small'+'\n'+table(['编号','原文件名','页数','读取方式／备注'],rows,r'L{13mm}L{104mm}L{11mm}L{25mm}')+'}\n')
 s.append(para('S01—S12 位于工作区“英语二”目录；S13—S40 位于用户指定的“27南山作文模板吃鸡计划4.0（英二）”资料目录。机器清单保留每份原文件的完整路径与SHA-256，便于核对。'))
s.append(r'\end{document}'+'\n')
OUT.write_text(''.join(s))
# A plain-text editable version accompanies the complete TeX source.
md=['# 英语二作文：36类融合模板\n\n完整排版和附录以同名PDF／TeX为准。\n']
for x in items:
 md.append(f"\n## {x['id']} {x['title']}\n\n{x['task']}\n\n行文路线：{x['logic']}\n\n### 可替换模板\n\n")
 md.append(x['header']+'\n\n'+'\n\n'.join(x['template'])+'\n\n'+x['footer'])
 md.append('\n\n### 完整示例\n\n'+x['header']+'\n\n'+'\n\n'.join(x['body'])+'\n\n'+x['footer'])
 md.append('\n\n好词好句：\n\n'+'\n'.join('- '+a+'：'+b for a,b in x['phrases'])+'\n\n核对重点：'+x['check']+'\n\n来源线索：'+x['source']+'\n')
(R/'英语二作文_36类融合模板.md').write_text(''.join(md))
print(OUT)
