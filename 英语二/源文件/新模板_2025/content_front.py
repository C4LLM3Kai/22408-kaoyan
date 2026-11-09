# -*- coding: utf-8 -*-
"""英语二小作文 · 十二类文体模板 —— 前置内容（封面 / 通用规则 / 文体决策表）"""

COVER = {
    "title": "英语二小作文 · 十二类文体模板",
    "subtitle": "十二类文体 · 每类一页 · 骨架可替换 · 按 10 分档写法组织",
    "kicker": "考研英语（二）Part A · 应用文写作",
    "lines": [
        "覆盖 2010—2025 全部真题文体：邀请 / 回复 / 建议 / 感谢 / 祝贺 / 道歉 / 投诉 / 咨询 / 通知 / 汇报",
        "补充大纲内两类：推荐信、申请信（模拟题高频）",
        "每页固定五块：题型识别 → 结构骨架 → 可替换句型 → 满分范文 → 雷区与得分点",
        "范文均按“正文约 100 词”控制，可直接背诵，也可按【槽位】改写",
    ],
    "note": "编写依据：考研英语（二）考试大纲对 Part A 的要求，以及工作区《批改指令》中的评分档位与批改原则。全部英文为原创句型，与市面通用“万能模板”不重合。",
}

# 通用规则页
RULES = {
    "title": "通用规则：先拿满格式分，再谈语言分",
    "blocks": [
        {"h": "一、分数构成（10 分）",
         "t": "table",
         "cols": ["评分维度", "权重感受", "最容易失分的地方"],
         "widths": [3.2, 3.0, 11.0],
         "rows": [
             ["任务完成", "最高", "漏写时间/地点/联系方式；合并题只答一半"],
             ["语言准确", "高", "主谓一致、时态混用、搭配错（congratulations for）"],
             ["格式语气", "中", "称呼与署名不合身份；公务信写成口语便条"],
             ["连贯与变化", "中", "通篇 I will / you should 单一句式；无衔接手段"],
         ]},
        {"h": "二、格式四要素（书信）",
         "t": "table",
         "cols": ["位置", "写法", "例"],
         "widths": [3.2, 6.4, 7.6],
         "rows": [
             ["称呼", "顶格，逗号结尾；公务用姓，私人用名", "Dear Professor Wang, / Dear Jack,"],
             ["正文", "2—3 段，每段一个功能，段首不空格", "见各文体骨架"],
             ["结束语", "顶格，逗号结尾，与署名同一语气层", "Yours sincerely, / Best wishes,"],
             ["署名", "另起一行，题目指定姓名", "Li Ming"],
         ]},
        {"h": "三、通知类格式（无称呼）",
         "t": "table",
         "cols": ["位置", "写法", "例"],
         "widths": [3.2, 6.4, 7.6],
         "rows": [
             ["标题", "居中，单独一行，首字母大写", "Notice"],
             ["正文", "1—3 段：目的 → 安排 → 号召/联系方式", "见第 09 页"],
             ["落款", "右下角两行：单位 + 日期", "The Student Union / Oct. 20, 2025"],
         ]},
        {"h": "四、词数与时间",
         "t": "bullets",
         "items": [
             "正文约 100 词（不含称呼、结束语、署名）。120 词以内不必担心，超过 150 词会挤占大作文时间并放大错误。",
             "考场建议 18 分钟：审题画要点 3 分钟 → 写作 13 分钟 → 检查 2 分钟（主谓一致、时态、拼写、格式）。",
             "三段最稳：第一段点题、第二段展开、第三段收束。四段也可以，但每段不能只有一句话。",
         ]},
        {"h": "五、评分档位（据《批改指令》，不人为封顶）",
         "t": "table",
         "cols": ["档位", "表现"],
         "widths": [2.2, 15.0],
         "rows": [
             ["8—9 分", "很好完成任务：要点完整，语言准确自然，表达有变化，行文连贯，格式与语气恰当"],
             ["6—7 分", "较好完成任务：主要要点完整，允许遗漏少量次要信息；语言基本准确，偶有错误"],
             ["4—5 分", "基本完成任务：涵盖多数要点；有一些语言错误，但不影响整体理解"],
             ["2—3 分", "遗漏重要要点或夹杂无关内容；语言错误较多，影响理解"],
             ["1 分 / 0 分", "未完成任务，语言错误严重 / 未作答或内容完全无关"],
         ]},
        {"h": "六、六个高频扣分点（自查）",
         "t": "traps",
         "items": [
             "漏要点：邀请信不写时间地点、投诉信不写购买渠道、咨询信不列具体问题。",
             "称呼错：Dear Mr. Jack（名不加 Mr.）、Dear Teacher（不这么说，用 Dear Professor Wang）。",
             "语气错：投诉信全程 angry、trash，或建议信通篇 you must。",
             "搭配错：congratulations for → on；grateful to your help → for；depend of → on。",
             "时态乱：邀请用将来时，感谢用过去时，汇报用现在完成时；同一段内不要来回跳。",
             "字数失衡：正文只有 60 词，或把 Mid-Autumn Festival 展开成三句话 cultural background。",
         ]},
    ],
}

# 文体决策表
DECIDE = {
    "title": "看到题干，先归到哪一类",
    "intro": "英语二 Part A 的题干通常给两件事：写什么（事务）+ 要你完成什么动作（邀请、说明、请求）。先把“动作词”找出来，文体就定了；再看有没有“合并任务”，合并题必须两个动作都落地。",
    "cols": ["题干里的信号词", "文体", "页码", "最容易漏的要点"],
    "widths": [7.6, 3.6, 1.6, 4.4],
    "rows": [
        ["invite / 邀请……参加……", "邀请信", "01", "时间地点 + 请对方确认"],
        ["reply to / 回复……的来信", "回复信（接受·婉拒）", "02", "第一段必须有明确态度"],
        ["advice / suggestions / 就……提建议", "建议信", "03", "建议要带理由，两条不重复"],
        ["thank / grateful / 感谢", "感谢信", "04", "帮助的具体内容与影响"],
        ["congratulate / 祝贺", "祝贺信", "05", "祝贺什么 + 为何值得"],
        ["apologize / 为……道歉", "道歉信", "06", "原因一句 + 补救方案"],
        ["complain / 投诉", "投诉信", "07", "购买渠道 + 明确要求与期限"],
        ["information / ask about / 询问", "咨询信", "08", "2—3 个具体问题"],
        ["Notice / 通知……参加……", "通知", "09", "标题 + 落款 + 联系方式"],
        ["report / tell sb. about / 汇报", "汇报·告知信", "10", "时间节点与分工"],
        ["recommend / 推荐", "推荐信", "11", "关系交代 + 具体事例"],
        ["apply for / 申请", "申请·求职信", "12", "信息来源 + 可量化成果"],
    ],
    "tips": [
        "合并题（如 2010 感谢＋邀请、2011 祝贺＋建议、2014 告知＋咨询、2019/2024 汇报＋建议）：两件事各写一段，段首用 As for… / Besides… 明确切换，阅卷人一眼能看到两个要点。",
        "题干给了姓名、职位、日期、地点，一律照抄进正文，不要自创；题干没给的时间地点，用 next Saturday / Room 203 这类具体而安全的信息补齐。",
        "落款永远用题目指定姓名（通常是 Li Ming），不要写自己的名字。",
    ],
}

# 附录
APPENDIX = {
    "upgrade": {
        "title": "附录 A · 低分句 → 修改句 → 为什么",
        "intro": "下面 10 组是最常见的学生写法。左边是“能看懂但拿不到 8 分”的句子，右边是同一意思的达标写法。批改时按“必须改 / 可选优化”标注。",
        "cols": ["原句（常见写法）", "修改句", "说明"],
        "widths": [6.2, 7.0, 4.0],
        "rows": [
            ["I am a student. I want to invite you to join our activity.",
             "I am writing to invite you to our English speech contest, which will be held next Friday.",
             "两句并成一句主从句；点题句必须带活动名与时间，[必须改]。"],
            ["I very like this activity.",
             "I am really fond of this activity. / I enjoy this activity very much.",
             "like 是及物动词，不能用 very 直接修饰；程度副词位置也错，[必须改]。"],
            ["Thank you for your help, I finished my research.",
             "Thanks to your help, I was able to finish my research on time.",
             "两个完整句不能用逗号连接（逗号粘连）；thanks to 更贴合致谢语境，[必须改]。"],
            ["Please tell me the information about the camp.",
             "Could you tell me when the camp begins and how much it costs?",
             "information 太笼统，阅卷人看不到“问了什么”；改为两个具体问题，[必须改]。"],
            ["I am sorry for I can't come.",
             "I am sorry that I cannot come. / I apologize for being unable to come.",
             "sorry for 后接名词或动名词，不接句子；cannot 在正式信中不缩写，[必须改]。"],
            ["The activity will hold on next Monday.",
             "The activity will be held next Monday. / We will hold the activity next Monday.",
             "hold 是及物动词，活动不能自己 hold；用被动或换主语，[必须改]。"],
            ["I hope you can give me a reply as soon as possible.",
             "I would appreciate it if you could reply at your earliest convenience.",
             "原句不算错，但 as soon as possible 偏催促；公务信改客气句式，[可选优化]。"],
            ["You should read more books and practise more.",
             "It might be a good idea to read more widely and to write one passage a day.",
             "建议信忌用 should 命令对方；给出可执行的具体做法，[必须改]。"],
            ["There are many students take part in it.",
             "Many students take part in it. / There are many students who take part in it.",
             "there be 句型后不能直接跟动词原形，缺关系代词，[必须改]。"],
            ["I am looking forward to meet you.",
             "I am looking forward to meeting you.",
             "look forward to 中 to 是介词，后接动名词，[必须改]。"],
        ],
    },
    "phrases": {
        "title": "附录 B · 功能句速查（按动作取用）",
        "groups": [
            {"label": "点题（第一段）", "items": [
                "I am writing to invite you to… / to apply for… / to complain about…",
                "I am writing in reply to your letter of May 10, in which you asked about…",
                "I was delighted to learn that… / I regret to say that…",
                "On behalf of the Student Union, I would like to…",
            ]},
            {"label": "展开（第二段）", "items": [
                "The activity will start at 9 a.m. and last until 4 p.m. in Room 203.",
                "For one thing… For another… / First… Besides… More importantly…",
                "What impressed me most was… / What I would do in your position is…",
                "Those who wish to join should sign up before Friday.",
            ]},
            {"label": "请求与催促", "items": [
                "I would be grateful if you could…",
                "I would appreciate it if you could reply at your earliest convenience.",
                "Please let me know by Thursday whether you are available.",
                "Could you please send me some details about…?",
            ]},
            {"label": "感谢与道歉", "items": [
                "I am writing to express my sincere gratitude for…",
                "Without your help, I could hardly have…",
                "Please accept my sincere apologies for…",
                "I am sorry for any inconvenience I have caused.",
            ]},
            {"label": "收尾", "items": [
                "I look forward to your early reply. / I am looking forward to meeting you.",
                "I hope you will find these suggestions helpful.",
                "Once again, thank you for your kindness.",
                "Please feel free to contact me if you need further information.",
            ]},
            {"label": "衔接与过渡", "items": [
                "To be specific, … / As for…, … / As you suggested, …",
                "Unfortunately, … / To make up for it, …",
                "In addition, … / What is more, … / On the other hand, …",
                "Therefore, … / As a result, … / In this way, …",
            ]},
        ],
    },
    "checklist": {
        "title": "附录 C · 交卷前 60 秒自检清单",
        "groups": [
            {"label": "格式", "items": [
                "称呼顶格且有逗号；结束语与署名各占一行、顶格。",
                "通知类有居中标题 Notice，右下角有单位与日期。",
                "署名是题目指定姓名，不是自己名字，也不是 Li Ming 加学号。",
            ]},
            {"label": "要点", "items": [
                "题干每个提示点都能在正文找到对应句（时间、地点、原因、要求、联系方式）。",
                "若是合并题（感谢＋邀请、祝贺＋建议、汇报＋征求意见），两件事各有一段或明确一句。",
                "咨询信有 2—3 个具体问题；投诉信有明确要求与期限。",
            ]},
            {"label": "语言", "items": [
                "主谓一致：The activity will be held…（不是 will hold）。",
                "时态成组：邀请用将来时，感谢用过去时，汇报用现在完成时。",
                "搭配清单：congratulations on / grateful for / apologize for / look forward to doing / be interested in。",
                "没有逗号粘连（两个完整句之间必须有连词或分号）。",
                "同一个句型不连续出现三次（I will… / I hope…）。",
            ]},
            {"label": "词数", "items": [
                "正文 90—120 词；不足 80 词要补一个细节句，超过 150 词删掉重复的客套。",
                "不把活动背景、节日来历写成流水账——这类内容不加分，还挤掉要点。",
            ]},
        ],
    },
}
