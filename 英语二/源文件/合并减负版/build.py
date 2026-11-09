from pathlib import Path
import json,re
R=Path(__file__).parent
D=json.loads((R/'content.json').read_text());Q=json.loads((R/'重合检查.json').read_text())
def e(s):return ''.join({'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}'}.get(c,c) for c in s)
def f(s):return ''.join(r'\textbf{'+e(p)+'}' if p.startswith('【') else e(p) for p in re.split(r'(【.*?】)',s))
def p(s):return f(s)+'\n\n'
def count(s):return len(re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*|\d+(?:[.,]\d+)*(?:%)?",s))
def title(s,tag):return r'\clearpage\section*{'+e(s)+r'}\addcontentsline{toc}{section}{'+e(s)+r'}\markboth{'+e(tag)+'}{}\n'
def label(s):return r'\par\vspace{5pt}\noindent\textbf{'+e(s)+r'}\par\nopagebreak'+'\n'
def table(headers,rows,widths):
 t=r'\begin{longtable}{'+''.join(f'L{{{a}mm}}' for a in widths)+r'}\toprule'+'\n'
 t+=' & '.join(r'\textbf{'+e(a)+'}' for a in headers)+r'\\\midrule\endhead'+'\n'
 t+='\n'.join(' & '.join(f(str(v)) for v in row)+r'\\' for row in rows)
 return t+'\n'+r'\bottomrule\end{longtable}'+'\n'
s=[r'''% !TEX program = xelatex
\documentclass[11pt,a4paper,fontset=macnew]{ctexart}
\usepackage[left=20mm,right=20mm,top=18mm,bottom=18mm,headsep=5mm]{geometry}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\usepackage{booktabs,longtable,array,enumitem,fancyhdr,needspace}
\usepackage[hidelinks,bookmarksopen=true]{hyperref}
\hypersetup{pdftitle={英语二作文：5套核心合并版},pdfsubject={合并同类文体，减少背诵负担；按用户给定批改标准}}
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\setlength{\parindent}{0pt}
\setlength{\parskip}{4pt}
\setlength{\tabcolsep}{4pt}
\setlength{\emergencystretch}{2em}
\renewcommand{\arraystretch}{1.18}
\linespread{1.12}
\ctexset{section/format={\Large\bfseries},section/beforeskip=0pt,section/afterskip=8pt}
\setlist[itemize]{leftmargin=1.25em,itemsep=3pt,topsep=3pt}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small 英语二作文 · 5套核心合并版}
\fancyhead[R]{\small\leftmark}
\fancyfoot[C]{\small\thepage}
\setlength{\headheight}{15pt}
\renewcommand{\headrulewidth}{0.3pt}
\newenvironment{english}{\begingroup\fontsize{11}{15}\selectfont\setlength{\parskip}{4pt}}{\par\endgroup}
\newenvironment{example}{\begingroup\fontsize{10.5}{14}\selectfont\setlength{\parskip}{4pt}}{\par\endgroup}
\begin{document}
\section*{英语二作文：5套核心合并版}
\addcontentsline{toc}{section}{背诵范围与合并关系}
\markboth{先明确背什么}{}
{\large\bfseries 主背第2—6页的5块框架，示例不用另背。}\par
\vspace{4pt}
''']
s.append(p('上一版按36个类型分别写，重复的句子太多。本版把相似正文直接合并：开头只表达本题目的，中间只保留共用逻辑，格式与少数专用句另列查表。'))
s.append(table(['只背这5块','合并后的用途','页码'],[
['M1 活动安排','邀请、介绍、欢迎、通知、招募、计划、活动答复、倡议','2'],
['M2 建议与理由','建议、推荐人或物、申请、求职、观点答复','3'],
['M3 问题与补救','道歉、投诉、求助、辞职、婉拒','4'],
['M4 情感交流','感谢、祝贺、表达感受、分享后追问','5'],
['M5 图表作文','静态／动态共用后两段；多选、表格、双图只调整数据段','6']], [34,107,12]))
s.append(label('背诵量到底减少多少'))
s.append(p(f'五块框架共约{D["fixed_core_words"]}个固定英文词，已包含静态、动态两种开头；不含中文填空、称呼、署名和功能卡。第7页的功能卡是短句替换，不再扩成整篇。完整示例用来理解填什么，不增加一套背诵任务。'))
s.append(label('其余类型怎么处理'))
s.append(p('咨询信只用问句结构；寻物与招领共用“物品—特征—联系”；纪要、备忘录保留各自格式，见第8页。图画、文字与复合材料只留备用开头，见第9页。原来36类都有去向，不再各写一篇。'))
s.append(label('同一套怎么变成不同文章'))
s.append(p('邀请和介绍用M1同一个主体，只改变写作目的；道歉和投诉用M3同一个补救段，只改变责任与诉求；静态图和动态图用M5同一个解释段和结尾，只改变数据段。遇到“介绍＋邀请”“感受＋追问”时，把两个任务都写出来。'))
s.append(label('记住这三条就开始背'))
s.append(r'\begin{itemize}\item \textbf{先背框架，再换内容：}【】全部换成英文。动作通常用动词原形；doing提示处填动名词；“完整分句”要有主语和谓语。\item \textbf{正文仍按题目长度：}小作文常见约100词，大作文约150词。固定词少，是给具体信息留空间；填完后要核对总词数。\item \textbf{不能合并掉任务：}招募保留职责和要求，申请保留能力证据，道歉保留补救，图表保留准确数据。\end{itemize}'+'\n')
s.append(r'{\small 判断标准仍采用《考研英语批改指令》英语二部分：任务完整、语言准确、结构清楚、格式得体；大作文另核对数据和评论。}\par'+'\n')
for x in D['cores']:
 s.append(title(x['id']+' '+x['title']+'｜同类只背这一块','核心背诵'))
 s.append(r'{\small\textbf{合并：}'+e(x['covers'])+r'\par\textbf{思路：}'+e(x['route'])+'}\par\n')
 s.append(label('要背：固定框架'))
 s.append(r'\begin{english}'+'\n')
 for q in x['template']:s.append(p(q))
 s.append(r'\end{english}'+'\n')
 s.append(label('只看懂：填好后的同框架示例'))
 s.append(r'{\small '+e(x['task'])+r'\quad 正文'+str(count(' '.join(x['body'])))+'词。}\par\n')
 s.append(r'\begin{example}'+'\n'+e(x['header'])+'\par\n')
 for q in x['body']:s.append(p(q))
 s.append(r'\\'.join(e(a) for a in x['footer'].split('\n'))+'\par\n'+r'\end{example}'+'\n')
 s.append(label('换文体时，只改这些地方'))
 s.append(r'{\small\begin{itemize}'+'\n')
 for n in x['notes']:s.append(r'\item '+e(n)+'\n')
 s.append(r'\end{itemize}}'+'\n')
x=D['chart']
s.append(title('M5 图表作文｜两种开头，共用后两段','核心背诵'))
s.append(r'{\small\textbf{合并：}'+e(x['covers'])+'}\par\n')
s.append(label('要背：第一段二选一'))
s.append(r'\begin{example}\textbf{静态：类别／群体对比。}\par'+'\n'+p(x['static']))
s.append(r'\textbf{动态：同一指标随时间变化。}\par'+'\n'+p(x['dynamic'])+r'\end{example}'+'\n')
s.append(label('要背：第二、三段只保留这一套'))
s.append(r'\begin{example}'+'\n')
for q in x['shared']:s.append(p(q))
s.append(r'\end{example}'+'\n')
s.append(label('只看懂：动态示例，正文144词'))
s.append(r'{\small '+e(x['task'])+'}\par\n'+r'\begin{example}'+'\n')
for q in x['body']:s.append(p(q))
s.append(r'\end{example}'+'\n')
s.append(r'{\small\textbf{只需调整：}表格和多选用静态开头；有转折时写关键升降，不能硬写steadily；双图各写一句核心信息。只有两个时间点时删掉“另一阶段”槽，改写整体增量。原因要能解释本图，不能一律填经济发展。}\par'+'\n')
s.append(title('功能卡｜换文体，不新增整篇','需要时查阅'))
s.append(p('先选M1—M4，再从对应行选真正需要的一句。斜线表示选其一，不是把所有句子一起背、一起写。正式邮件和朋友邮件都可以直接进入主题。'))
s.append(r'{\small'+'\n'+table(['任务','主干','只换这个短句／短语'],[(a,b,c) for a,b,c,d in D['cards']],[30,17,106])+'}\n')
s.append(label('三处不能只换一个单词'))
s.append(p('申请／求职：M2保留“理由＋证据”，把“推荐对象的优势”改成“我能带来的技能”，并加一句具体过去经历；结尾用面谈意愿。你是在证明自己适合岗位，不是在劝招聘者尝试一项活动。'))
s.append(p('道歉／投诉：M3相同的是问题、影响和解决办法。道歉须说明自己的过失；投诉须说明对方产品或服务的问题并提出诉求。不要把道歉的责任句带进投诉信。'))
s.append(p('计划／通知／招募：M1相同的是安排。共同计划用could并征求意见；通知直接发布事实；招募另外写“做什么工作、需要什么条件、如何报名”。'))
s.append(label('书信格式统一处理'))
s.append(p('称呼：Dear【姓名／职务】,；朋友可用Best wishes,，正式信件可用Yours sincerely,；署名依题干，常用Li Ming。读者不认识你且身份影响任务时，加一句I am【题目给定身份】。不要凭空给自己加头衔。'))
s.append(r'{\small\textbf{词句只留够用的一组：}make it easier to...（使……更容易）；be suitable for...（适合……）；a workable solution（可行办法）；in the meantime（在此期间）；practical factors（实际因素）。都已出现在框架中，无须另背108条。}\par'+'\n')
s.append(title('格式卡｜低频类型只记区别','需要时查阅'))
s.append(label('1. 通知／招募／倡议：主体借用M1'))
s.append(p('标题居中写NOTICE或具体倡议标题；正文直接写活动、行动或招募内容；结尾写报名办法和期限；落款按题目写组织或指定姓名。去掉Dear和Yours，不把通知写成私人邮件。'))
s.append(label('2. 咨询：同一问句结构，问两件具体的事'))
s.append(r'\begin{example}'+p('I am considering 【项目】. Could you tell me 【疑问词＋陈述语序从句】? I would also like to know whether 【完整分句】. This would help me 【信息的用途，动词原形】.')+r'\end{example}'+'\n')
s.append(p('每个问题补一句相关背景或用途即可展开，按题目要求写到合适长度。例：Could you tell me when the course begins? 从句不用when does the course begin。'))
s.append(label('3. 寻物／招领：共用一条信息链'))
s.append(r'\begin{example}'+p('I 【lost/found】 【物品】 【时间和地点】. It has 【可辨认的外观】. Please 【联系或领取动作】 【联系方式／地点】.')+r'\end{example}'+'\n')
s.append(p('寻物标题LOST，说明对自己的用途与联系办法；招领标题FOUND，说明保管、领取和认领核实办法。根据题目补足细节，不把这三句短框架直接当100词成文。'))
s.append(label('4. 纪要：会议信息＋决定＋谁何时完成'))
s.append(r'\begin{example}\textbf{Minutes of 【会议】}\par Date: 【日期】 \quad Place: 【地点】\par Present: 【与会者】\par'+'\n')
s.append(p('Members discussed 【议题】 and agreed to 【决定】. 【负责人】 will 【任务】 by 【期限】. Progress will be reviewed 【时间】.')+r'Recorded by: 【记录人】\par\end{example}'+'\n')
s.append(p('只记录会议实际讨论和决定的内容，按题目补充原因或分工。已发生的讨论用过去时，未来待办可用will；不能把纪要改成活动邀请。'))
s.append(label('5. 备忘录：只换信息栏，安排逻辑借用M1'))
s.append(r'\begin{example}\textbf{MEMO}\par To: 【对象】\quad From: 【发件人】\par Date: 【日期】\quad Subject: 【主题】\par'+p('【变更或安排的事实】 Please 【要完成的动作】 by 【期限】. Confirm completion when the task is finished.')+r'\end{example}'+'\n')
s.append(p('正文补充原因、负责人及具体动作。纪要记“会上决定了什么”；备忘录告诉同事“现在需要做什么”。两者都不用再背一篇信。'))
s.append(title('备用与核对｜不用增加背诵篇数','需要时查阅'))
s.append(label('图画／文字／复合材料：保留入口，改掉图表专用句'))
s.append(r'{\small'+'\n'+table(['材料','备用开头'],[
['图画','The picture shows 【人物】 【动作，动名词】. The contrast highlights 【主题】.'],
['文字材料','The author argues that 【原观点】. I agree with 【合理点】, but 【自己的限制或不同意见】.'],
['图画＋图表','The drawing shows 【场景】, while the chart reports 【数据主题】. 【核心数据，完整句】']], [26,131])+'}\n')
s.append(p('图画只在存在对比时用contrast。后面沿用“观点—理由—具体作用—例子—结论”的顺序；M5中的First、This can...、Second可以复用，但必须删掉causes established by the chart等图表专用句。文字题要回应是否同意，不能硬改成原因分析；复合材料要两部分都描述。'))
s.append(label('图表只保留六项核对'))
s.append(r'{\small'+'\n'+table(['看什么','怎么避免写错'],[
['对象、年份、单位','人次用visits，不是visitors；过去数据用过去时。'],['静态／动态','不同年龄组之间的差异，不等于同一群体随时间变化。'],['百分比／百分点','30%到45%：增加15个百分点；相对增长50%。'],['最大／多数','45%可为最大项；majority通常要求超过50%。'],['多选／双图','多选不相加成总人数；双图并存不直接证明因果。'],['任务与词数','小作文约100词、大作文约150词，最终服从题干。']], [32,125])+'}\n')
s.append(label('合并后的质量与文字重合检查'))
s.append(p('仍按你提供的《考研英语批改指令》第5—6页核对：不为难词牺牲准确性，不漏任务，不编图表数据，原因推测与可见事实分开。示例情境和数据为新编，不保证套上框架就有固定分数。'))
s.append(p(f'新版固定框架、示例和功能卡已分别对照原40份PDF的已提取文本检查。连续4词覆盖率最高{Q["max4"]:.2f}%，低于50%；这是字面复用指标，不是语义查重保证。计算以新稿英文词数为分母，命中的词位只计一次；中文占位和格式栏不计，扫描识别仍可能漏字。详细结果与源码保存在“源文件／合并减负版”。'))
s.append(r'{\small\textbf{来源取舍：}沿用上一版对南山任务拆解、各讲义功能句和英语二真题任务的整理；将重复表达归为5块，不再附36篇。完整原文件索引见上一版附录。原36类的逐项合并去向保存在本版content.json；408大纲仍不作为英语依据。}\par'+'\n')
s.append(r'\end{document}'+'\n')
(R/'英语二作文_5套核心合并版.tex').write_text(''.join(s))
print('fixed words',D['fixed_core_words'])
