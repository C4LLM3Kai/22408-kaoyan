# -*- coding: utf-8 -*-
"""《英语二小作文 · 一文一模版》内容数据。

设计原则：
1. 每类文体只给一篇完整信件（模板），句首用 ①—⑨ 标号；
2. 模板里的【槽位】就是考场上唯一需要改动的部分；
3. 真题范文由同一模板 + 填槽生成，保证“背的”和“写的”是同一篇；
4. 全部英文为原创，句式和市面“万能模板”不重合。
"""

# ---------------------------------------------------------------- 12 类文体

GENRES = [
    # ------------------------------------------------------------ 01 邀请
    dict(
        num="01", cn="邀请信", en="Invitation",
        years="2021 · 2022 · 2025",
        signal="题干出现 invite / 邀请……参加，并要求交代时间、地点或安排",
        identity="活动组织者、班委或社团负责人；落款写题目指定姓名",
        must="①活动名称与目的　②时间与地点　③两个环节　④请对方在某日前回复",
        strategy="第一段一句点题，第二段全部交代安排，第三段只做一件事：促回复",
        closing="Yours sincerely,", sig="Li Ming",
        paras=[
            ["①I am writing to invite you to 【活动名称】, which 【主办方】 is organizing for 【参加对象】."],
            ["②The event will take place 【日期】 at 【地点】.",
             "③It will open with 【环节一】, followed by 【环节二】, and end with 【环节三】.",
             "④There is no charge, and 【附加安排】.",
             "⑤You will also have a chance to 【参与收获】."],
            ["⑥I do hope you can join us.",
             "⑦Would you please let me know by 【回复期限】 whether you are free that day?"],
        ],
        fill={
            "活动名称": "our Campus Food Festival", "主办方": "the Student Union",
            "参加对象": "international students", "日期": "next Saturday",
            "地点": "the Central Square", "环节一": "a short cooking show",
            "环节二": "a tasting session", "环节三": "a vote for the most popular dish",
            "附加安排": "light refreshments will be served",
            "参与收获": "try dishes from over ten provinces", "回复期限": "Wednesday",
        },
        example_label="2022 真题 · 校园美食节",
        swaps=[
            ("【活动名称】", "our Campus Food Festival", "a charity sale / a welcome party"),
            ("【日期】＋【地点】", "next Saturday / the Central Square", "next Friday at 7 p.m. / Room 203"),
            ("【环节一】【环节二】【环节三】", "cooking show → tasting → vote", "opening speech → game → free talk"),
            ("【参与收获】", "try dishes from over ten provinces", "meet students from other majors"),
        ],
        score=[
            "活动名称、时间、地点三样齐全，且都在第二段，阅卷人一眼能找到",
            "两个以上具体环节（不是“interesting activities”这种空话）",
            "结尾有一句明确的回复请求，并给出期限",
        ],
        traps=[
            "只写“下周六”，不写几点、在哪 —— 直接算要点不全",
            "通篇 I will… I will…，把邀请信写成日程表",
        ],
    ),
    # ------------------------------------------------------------ 02 接受邀请
    dict(
        num="02", cn="回复邀请 · 接受", en="Accepting an Invitation",
        years="2017（回复类真题）",
        signal="题干出现 reply to / 回复某封邀请信，第一个动作是接受",
        identity="受邀者；称呼沿用邀请人的身份与姓氏",
        must="①感谢邀请　②明确接受　③讲座/发言要点　④到场准备或需对方配合的事",
        strategy="第一段必须出现 accept 这个词；第二段用“要点＋准备”证明你真的要来",
        closing="Yours sincerely,", sig="Li Ming",
        paras=[
            ["①Thank you for your invitation to 【活动】.",
             "②I am glad to accept it and look forward to 【期待】."],
            ["③As you suggested, I will center my talk on 【要点一】 and 【要点二】.",
             "④I plan to arrive at 【地点】 half an hour early so that I can 【准备工作】.",
             "⑤If you need any materials from me, please tell me before 【日期】."],
            ["⑥Thank you again for thinking of me.",
             "⑦I will do my best to make the talk useful to 【听众】, and I will bring a short handout."],
        ],
        fill={
            "活动": "give a presentation on Chinese culture", "期待": "meeting your students",
            "要点一": "traditional festivals", "要点二": "table manners",
            "地点": "the lecture hall", "准备工作": "test the projector",
            "日期": "Friday", "听众": "the international students",
        },
        example_label="2017 真题 · 接受邀请并介绍讲座要点",
        swaps=[
            ("【活动】", "give a presentation on Chinese culture", "attend the seminar / join the panel"),
            ("【要点一】【要点二】", "traditional festivals / table manners", "food culture / family life"),
            ("【准备工作】", "test the projector", "check the microphone / print handouts"),
            ("【听众】", "the international students", "first-year students / the audience"),
        ],
        score=[
            "第一段有明确态度词（accept / delighted to accept），不拖到第二段",
            "讲座要点具体到两个名词，不是“something about culture”",
            "主动交代到场时间与准备事项，体现“真接受”",
        ],
        traps=[
            "只写 I am glad to accept，后面全是空话，第二个动作没落地",
            "把接受信写成感谢信，通篇 thank you，没有安排",
        ],
    ),
    # ------------------------------------------------------------ 03 婉拒
    dict(
        num="03", cn="回复邀请 · 婉拒", en="Declining an Invitation",
        years="模拟题 · 大纲内文体",
        signal="题干要求 decline / 不能参加，并说明原因或另约",
        identity="受邀者；语气要礼貌，但不能含糊",
        must="①感谢邀请　②明确不能参加　③一句真实原因　④替代时间或替代方案",
        strategy="先谢、再拒、给原因、给替代——四步缺一不可，尤其不能只拒绝",
        closing="Yours sincerely,", sig="Li Ming",
        paras=[
            ["①Thank you for inviting me to 【活动】.",
             "②I am sorry to say that I shall not be able to attend it, though I really wish I could."],
            ["③The problem is that 【冲突原因】 on that very day, and I cannot change the arrangement.",
             "④I feel bad about missing 【期待内容】, which I have been looking forward to.",
             "⑤Could we meet at another time?",
             "⑥I would be free 【备选时间】, and I am happy to 【替代方案】."],
            ["⑦I hope you will understand.",
             "⑧Thank you again for your kindness."],
        ],
        fill={
            "活动": "the seminar on urban planning",
            "冲突原因": "I have to sit for an important exam",
            "期待内容": "your talk", "备选时间": "next Friday afternoon",
            "替代方案": "visit your office then",
        },
        example_label="模拟题 · 与考试冲突，婉拒研讨会",
        swaps=[
            ("【活动】", "the seminar on urban planning", "the conference / the interview"),
            ("【冲突原因】", "I have to sit for an important exam", "I will be away on a field trip"),
            ("【替代方案】", "visit your office then", "read your paper and send comments"),
        ],
        score=[
            "拒绝得明确（shall not be able to attend），不是“可能不行”",
            "原因只有一句，不展开诉苦；替代方案必须具体到时间",
            "语气礼貌但不卑微，不用 sorry 开头连写三句",
        ],
        traps=[
            "只拒绝、不给替代方案 —— 任务只完成一半",
            "原因写成一段故事（家里、身体、天气全上），挤掉替代安排",
        ],
    ),
    # ------------------------------------------------------------ 04 建议
    dict(
        num="04", cn="建议信", en="Advice / Suggestion",
        years="2011 · 2016 · 2019 · 2023 · 2024",
        signal="题干出现 advice / suggestions / which one / 征求意见，要你给主张",
        identity="朋友、同学或下属；同级用商量口气，对师长用 I would suggest",
        must="①明确建议哪一个　②两条理由　③一条附加好处　④把决定权还给对方",
        strategy="第一段一句话给结论，第二段两条理由各一句，第三段客气收尾",
        closing="Yours sincerely,", sig="Li Ming",
        paras=[
            ["①You asked me for my advice on 【咨询事项】.",
             "②I would suggest 【建议对象】."],
            ["③For one thing, 【理由一】.",
             "④For another, 【理由二】.",
             "⑤Besides, 【附加好处】, which 【对方获益】."],
            ["⑥Of course, the final choice is yours.",
             "⑦I have seen the poster, and it looks really attractive.",
             "⑧If you decide to go, I would be happy to 【陪同安排】, and I am sure you will enjoy it."],
        ],
        fill={
            "咨询事项": "which of the two events is worth going to",
            "建议对象": "the robot show",
            "理由一": "it displays the latest home robots, which are close to our daily life",
            "理由二": "visitors can try operating a simple robot themselves",
            "附加好处": "the show is held indoors", "对方获益": "means the weather will not matter",
            "陪同安排": "go with you",
        },
        example_label="2023 真题 · 艺术展还是机器人展",
        swaps=[
            ("【建议对象】", "the robot show", "the art exhibition / the online course"),
            ("【理由一】【理由二】", "close to daily life / hands-on", "free of charge / good for beginners"),
            ("【陪同安排】", "go with you", "help you book the ticket"),
        ],
        score=[
            "第一段就给出明确选择，不写“both are good”这种和稀泥",
            "两条理由不重复：一条讲内容，一条讲体验或成本",
            "结尾把决定权交还对方，语气不命令",
        ],
        traps=[
            "只给建议不给理由 —— 2023、2024 都明确要求 reason(s)",
            "两条理由其实是一条（都说 interesting），等于只有一条",
        ],
    ),
    # ------------------------------------------------------------ 05 感谢
    dict(
        num="05", cn="感谢信", en="Thanks",
        years="2010 · 2016",
        signal="题干出现 thank / grateful / 感谢对方的接待、帮助或祝贺",
        identity="受助者；对师长正式，对朋友可暖一些",
        must="①感谢的具体事项　②一处细节回忆　③这件事对你的影响　④回请或祝福",
        strategy="不要只说 thank you——用“一个细节”证明感谢是真的",
        closing="Yours sincerely,", sig="Li Ming",
        paras=[
            ["①I have been back in 【地点】 for a week, but I still think of the days I spent in 【对方城市】.",
             "②I am writing to thank you for 【感谢事项】."],
            ["③Without your help, 【假设后果】.",
             "④What impressed me most was 【具体细节】.",
             "⑤I have told my family about it, and they all hope to meet you one day."],
            ["⑥By the way, you are welcome to visit 【我的城市】 at any time.",
             "⑦I would be glad to 【接待安排】 and introduce you to my family."],
        ],
        fill={
            "地点": "Beijing", "对方城市": "New York",
            "感谢事项": "your warm reception during my stay",
            "假设后果": "I could hardly have settled down so quickly",
            "具体细节": "the dinner you prepared for me on my first night",
            "我的城市": "China", "接待安排": "show you around Beijing",
        },
        example_label="2010 真题 · 感谢接待并欢迎访华",
        swaps=[
            ("【感谢事项】", "your warm reception during my stay", "your help with my application"),
            ("【具体细节】", "the dinner on my first night", "the books you lent me"),
            ("【接待安排】", "show you around Beijing", "take you to my hometown"),
        ],
        score=[
            "感谢落到具体事上（接待、修改文书、借书），不是空洞的 your help",
            "有一处细节回忆，这是 8 分以上的分水岭",
            "结尾有回请或祝福，完成“礼尚往来”",
        ],
        traps=[
            "全篇 thank you so much，没有一件具体的事",
            "感谢信用了过去时又突然跳到 I will，时态来回跳",
        ],
    ),
    # ------------------------------------------------------------ 06 祝贺
    dict(
        num="06", cn="祝贺信", en="Congratulations",
        years="2011 · 2016（回复祝贺）",
        signal="题干出现 congratulate / 祝贺对方录取、获奖、晋升",
        identity="亲戚、朋友或同学；语气热情但别夸张",
        must="①祝贺的具体事　②为何值得祝贺　③两条建议或祝福　④保持联系",
        strategy="祝贺一句到位，第二段立刻转到“接下来怎么做”，避免整篇客套",
        closing="Yours sincerely,", sig="Li Ming",
        paras=[
            ["①I was delighted to learn that 【祝贺事项】.",
             "②Congratulations on 【具体成就】!"],
            ["③As you are about to 【阶段】, I would like to offer two suggestions.",
             "④First, 【建议一】.",
             "⑤Second, 【建议二】.",
             "⑥These are only my personal views, and you know your own situation best."],
            ["⑦I am sure you will do well.",
             "⑧I wish you a happy and fruitful four years.",
             "⑨Please keep in touch."],
        ],
        fill={
            "祝贺事项": "you have been admitted to Beijing University",
            "具体成就": "this great achievement", "阶段": "start university life",
            "建议一": "join one or two clubs so that you can meet people outside your major",
            "建议二": "plan your time carefully, for no one will remind you of deadlines any more",
        },
        example_label="2011 真题 · 祝贺录取并给大学适应建议",
        swaps=[
            ("【祝贺事项】", "you have been admitted to Beijing University", "you won the translation contest"),
            ("【阶段】", "start university life", "begin your new job"),
            ("【建议一】【建议二】", "join clubs / plan your time", "ask questions in class / save part of your salary"),
        ],
        score=[
            "祝贺的事写得具体（哪所学校、什么奖），不写 good news",
            "建议两条且不重复，每条带一点理由",
            "结尾有祝福，不写“祝你成功”式的中文直译",
        ],
        traps=[
            "Congratulations for → 必须用 on",
            "整篇只有祝贺，没有第二个动作（2011 还要求 suggestions）",
        ],
    ),
    # ------------------------------------------------------------ 07 道歉
    dict(
        num="07", cn="道歉信", en="Apology",
        years="2018",
        signal="题干出现 apologize / 取消、迟到、弄丢、不能赴约，并要求补救",
        identity="失约方；对师长正式，对朋友可少一点公文腔",
        must="①为何道歉　②一句原因　③补救方案　④另约时间或替代办法",
        strategy="道歉—原因—补救—另约，四句四件事，原因绝不超过一句",
        closing="Yours sincerely,", sig="Li Ming",
        paras=[
            ["①I am writing to apologize for 【道歉事项】.",
             "②I am afraid I have to 【取消/推迟】 at such short notice."],
            ["③The reason is that 【原因】.",
             "④I know this will cause you trouble, and I am truly sorry.",
             "⑤To make up for it, I would like to 【补救方案】.",
             "⑥Would 【备选时间】 suit you?",
             "⑦I can also 【替代安排】 if that is more convenient."],
            ["⑧Please accept my apology.",
             "⑨I hope we can meet soon."],
        ],
        fill={
            "道歉事项": "cancelling my visit to you next Monday",
            "取消/推迟": "put it off",
            "原因": "my mother has suddenly fallen ill and I must take her to hospital",
            "补救方案": "visit you the following Friday", "备选时间": "that",
            "替代安排": "send you my questions by email",
        },
        example_label="2018 真题 · 取消拜访并另约",
        swaps=[
            ("【道歉事项】", "cancelling my visit to you next Monday", "missing your lecture yesterday"),
            ("【原因】", "my mother has suddenly fallen ill", "I was sent on an urgent business trip"),
            ("【补救方案】", "visit you the following Friday", "call you this weekend"),
        ],
        score=[
            "道歉信必须同时有“原因”和“补救”，只有 sorry 最多 5 分",
            "原因一句收住，不写成记叙文",
            "另约时间具体（the following Friday），不用 someday / later",
        ],
        traps=[
            "把道歉写成解释，通篇 because，最后没有补救",
            "对教授用太随意的 Sorry about that!，语域不合",
        ],
    ),
    # ------------------------------------------------------------ 08 投诉
    dict(
        num="08", cn="投诉信", en="Complaint",
        years="2012",
        signal="题干出现 complain / 商品或服务有问题，要求解决或赔偿",
        identity="消费者；对商家用 Sir or Madam，对具体人用其姓氏",
        must="①购买渠道与时间　②具体故障　③已尝试的解决办法　④明确要求与期限",
        strategy="事实—故障—影响—要求，全程冷静，不写情绪词",
        closing="Yours sincerely,", sig="Li Ming",
        paras=[
            ["①I am writing to complain about 【商品】, which I bought from 【购买渠道】 【购买日期】."],
            ["②The problem is that 【问题】.",
             "③I have tried 【已采取措施】, but the fault remains.",
             "④This has made it impossible for me to 【受影响的事】."],
            ["⑤I would like you to 【要求一】, and I hope you can 【要求二】 within 【期限】.",
             "⑥If not, I shall have to 【进一步措施】.",
             "⑦I look forward to your reply."],
        ],
        fill={
            "商品": "the electronic dictionary", "购买渠道": "your online store",
            "购买日期": "last Friday",
            "问题": "the screen goes black whenever I turn it on",
            "已采取措施": "changing the batteries and resetting it",
            "受影响的事": "prepare for my exam",
            "要求一": "replace it with a new one", "要求二": "arrange the delivery",
            "期限": "a week", "进一步措施": "ask for a full refund",
        },
        example_label="2012 真题 · 电子词典故障",
        swaps=[
            ("【商品】", "the electronic dictionary", "the laptop / the online course"),
            ("【问题】", "the screen goes black", "the battery lasts only an hour"),
            ("【要求一】【要求二】", "replace it / deliver within a week", "repair it free / refund the shipping fee"),
        ],
        score=[
            "购买渠道＋日期写清楚，这是投诉信的身份证明",
            "故障描述具体到“什么时候、什么现象”，不写 it is broken",
            "要求明确（换、修、退），并给期限",
        ],
        traps=[
            "通篇 angry / terrible / cheat，情绪代替事实",
            "只投诉不要求，任务第二个动作缺失",
        ],
    ),
    # ------------------------------------------------------------ 09 咨询
    dict(
        num="09", cn="咨询信", en="Inquiry",
        years="2014",
        signal="题干出现 ask about / 询问信息，或“告知自己情况并征求意见”",
        identity="即将前往当地的学生或准参与者；对当地人客气",
        must="①自我介绍或背景　②两到三个具体问题　③为什么问　④致谢",
        strategy="问题要具体到“能不能、在哪里、多少钱”，别问“能介绍一下吗”",
        closing="Yours sincerely,", sig="Li Ming",
        paras=[
            ["①I am writing to ask for your advice about 【咨询主题】.",
             "②I will move to 【地点】 next month, and I know little about 【当地情况】."],
            ["③To give you some idea of my habits, I 【习惯一】, and I usually 【习惯二】.",
             "④I wonder whether 【问题一】.",
             "⑤Besides, could you tell me 【问题二】?"],
            ["⑥I am a little worried about the first few weeks, as everything will be new to me.",
             "⑦Your suggestions would be of great help.",
             "⑧Thank you in advance."],
        ],
        fill={
            "咨询主题": "daily life there", "地点": "London", "当地情况": "local customs",
            "习惯一": "get up early and go to bed before eleven",
            "习惯二": "cook my own meals", "问题一": "my schedule will disturb you",
            "问题二": "where I can buy fresh vegetables nearby",
        },
        example_label="2014 真题 · 告知生活习惯并咨询合租",
        swaps=[
            ("【咨询主题】", "daily life there", "the language course / the apartment"),
            ("【问题一】【问题二】", "will my schedule disturb you / where to buy food", "is the deposit refundable / when does the course start"),
            ("【当地情况】", "local customs", "the transport system"),
        ],
        score=[
            "问题两到三个，且每个都能用一句话回答（不是开放式的“介绍一下”）",
            "先给背景再提问，让对方知道你的情况",
            "结尾致谢，不写“等待您的答复”式的中文直译",
        ],
        traps=[
            "只写 I want to know more，没有一个具体问题",
            "把咨询信写成自我介绍，通篇讲自己，问题只有一句",
        ],
    ),
    # ------------------------------------------------------------ 10 通知
    dict(
        num="10", cn="通知", en="Notice",
        years="2013 · 2015",
        signal="题干出现 Notice / 通知同学参加，或“介绍活动并招募志愿者”",
        identity="学生会、社团或班委；以集体名义发布，不写个人称呼",
        must="①标题　②活动名称、时间、地点　③活动内容　④报名方式或招募要求",
        strategy="通知没有称呼；标题居中；落款单位＋日期在右下角",
        closing="", sig="",
        paras=[
            ["①【活动名称】 will be held 【时间】 at 【地点】.",
             "②It is organized by 【主办方】 for 【参加对象】."],
            ["③The program includes 【活动一】, 【活动二】 and 【活动三】.",
             "④【附加安排】.",
             "⑤Those who wish to take part should 【报名方式】 before 【截止日期】."],
            ["⑥We are also looking for 【招募人数】 volunteers to 【志愿工作】.",
             "⑦Anyone interested may contact 【联系人】 at 【联系方式】.",
             "⑧Please apply early, as places are limited."],
        ],
        fill={
            "活动名称": "The Summer Camp for high school students",
            "时间": "from July 10 to July 20", "地点": "our campus",
            "主办方": "the Student Union", "参加对象": "local high school students",
            "活动一": "campus tours", "活动二": "Chinese culture classes",
            "活动三": "a city walk", "附加安排": "Campers will stay in the student dormitory",
            "报名方式": "sign up at the Student Union office", "截止日期": "July 1",
            "招募人数": "twenty", "志愿工作": "help with reception and translation",
            "联系人": "Li Ming", "联系方式": "Room 203",
        },
        example_label="2015 真题 · 夏令营介绍＋招募志愿者",
        swaps=[
            ("【活动名称】", "The Summer Camp", "A Charity Sale / A Campus Concert"),
            ("【报名方式】", "sign up at the Student Union office", "send an email to notice@univ.edu"),
            ("【志愿工作】", "help with reception and translation", "set up the stage / guide the visitors"),
            ("【附加安排】", "Campers will stay in the student dormitory", "Lunch will be provided / Donations are welcome"),
        ],
        score=[
            "标题 Notice 单独居中，落款单位＋日期在右下角",
            "活动信息（名称、时间、地点、内容）齐全",
            "招募类通知要写清人数、工作内容、报名方式与截止日",
        ],
        traps=[
            "通知加了 Dear classmates, —— 格式直接降档",
            "只介绍活动不招募，或只招募不介绍（2015 两个动作）",
        ],
    ),
    # ------------------------------------------------------------ 11 介绍
    dict(
        num="11", cn="介绍 · 告知信", en="Introduction",
        years="2020 · 2022 · 2024",
        signal="题干出现 tell sb. about / introduce / 介绍景点、计划、活动",
        identity="组织者或知情者；对国际学生要放慢语速、少用难词",
        must="①介绍对象　②两三个特点　③一处亮点　④参观或参与提示",
        strategy="第二段讲“是什么”，第三段讲“注意什么”，两段分工清楚",
        closing="Yours sincerely,", sig="Li Ming",
        paras=[
            ["①I am glad to tell you about 【介绍对象】, which we are going to visit 【日期】."],
            ["②It is 【特点一】.",
             "③It is also 【特点二】.",
             "④The part I like best is 【亮点】.",
             "⑤I am sure you will find it interesting."],
            ["⑥Before we set off, I would like to give you two tips.",
             "⑦First, 【贴士一】.",
             "⑧Second, 【贴士二】.",
             "⑨If you have any questions, please let me know."],
        ],
        fill={
            "介绍对象": "Zhouzhuang", "日期": "next Saturday",
            "特点一": "famous for its waterways and stone bridges",
            "特点二": "home to more than nine hundred years of history",
            "亮点": "the old opera stage, where local performers sing every afternoon",
            "贴士一": "wear comfortable shoes, as we will walk a lot",
            "贴士二": "bring some cash, for small shops there do not accept cards",
        },
        example_label="2020 真题 · 介绍古镇并给参观提示",
        swaps=[
            ("【介绍对象】", "Zhouzhuang", "the Palace Museum / the campus library"),
            ("【特点一】【特点二】", "waterways / nine hundred years", "free entry / open until 9 p.m."),
            ("【贴士一】【贴士二】", "comfortable shoes / bring cash", "book online / bring your student card"),
        ],
        score=[
            "介绍对象有“身份”（古镇、博物馆、项目），不是 it is very good",
            "两条提示都是可执行的动作（穿什么、带什么、几点到）",
            "对国际学生避免生僻词，句子短而清楚",
        ],
        traps=[
            "把介绍写成景点广告，全是形容词，没有一条实用信息",
            "提示写成 Again, it is beautiful，等于没写",
        ],
    ),
    # ------------------------------------------------------------ 12 推荐
    dict(
        num="12", cn="推荐信", en="Recommendation",
        years="模拟高频（大纲内）",
        signal="题干出现 recommend / 推荐一本书、一个地方、一个人",
        identity="了解被推荐对象的同学、朋友或同事",
        must="①推荐什么　②两三条理由　③一个具体事例　④获取方式或联系方式",
        strategy="理由要“可验证”：内容、价格、使用体验；不要只写 highly recommend",
        closing="Yours sincerely,", sig="Li Ming",
        paras=[
            ["①I hear that 【推荐缘由】.",
             "②I would like to recommend 【推荐对象】 without hesitation."],
            ["③【对象】 is 【优点一】.",
             "④Besides, 【优点二】.",
             "⑤In my experience, 【具体事例】.",
             "⑥I believe 【结论】."],
            ["⑦It is available in most bookshops for less than fifty yuan.",
             "⑧If you need more information, please contact me.",
             "⑨I am sure you will not regret the choice."],
        ],
        fill={
            "推荐缘由": "you are looking for a book on Chinese history",
            "推荐对象": "A Brief History of China", "对象": "The book",
            "优点一": "a clear guide to five thousand years of Chinese history",
            "优点二": "each chapter ends with a short summary, which makes review easy",
            "具体事例": "it helped me understand the dynasties far better than any other book",
            "结论": "it will suit you too",
        },
        example_label="模拟题 · 向朋友推荐一本中国史读物",
        swaps=[
            ("【推荐对象】", "A Brief History of China", "the City Museum / Professor Wang"),
            ("【优点一】【优点二】", "clear guide / chapter summaries", "free entry / English guide available"),
            ("【具体事例】", "it helped me understand the dynasties", "I visited it twice last year"),
        ],
        score=[
            "第一段一句话说清推荐什么，不铺垫",
            "理由两到三条，每条都能被验证（内容、价格、体验）",
            "有一个“我自己的使用经历”，可信度立刻上来",
        ],
        traps=[
            "通篇 highly recommend / very good，没有一条具体理由",
            "推荐信写成广告，堆形容词，没有一句事实",
        ],
    ),
]


# ---------------------------------------------------------------- 真题地图

EXAM_MAP = [
    ("2010", "感谢＋邀请", "感谢接待；欢迎访华", "05"),
    ("2011", "祝贺＋建议", "祝贺录取；适应大学生活的建议", "06"),
    ("2012", "投诉", "电子词典故障；要求尽快解决", "08"),
    ("2013", "通知", "慈善义卖细节；鼓励同学参加", "10"),
    ("2014", "咨询＋告知", "介绍生活习惯；询问当地生活", "09"),
    ("2015", "通知", "夏令营活动；招募志愿者", "10"),
    ("2016", "回复祝贺＋建议", "感谢祝贺；给出翻译学习建议", "06 · 04"),
    ("2017", "回复邀请·接受", "接受邀请；介绍讲座要点", "02"),
    ("2018", "道歉＋另约", "取消拜访；解释并另约", "07"),
    ("2019", "建议＋安排", "辩论题目及理由；告知安排", "04"),
    ("2020", "介绍＋提示", "介绍历史景点；给出参观提示", "11"),
    ("2021", "邀请", "邀请参加线上会议；告知细节", "01"),
    ("2022", "介绍＋邀请", "介绍校园美食节；邀请参加", "11 · 01"),
    ("2023", "建议＋理由", "艺术展与机器人展二选一；给理由", "04"),
    ("2024", "建议＋征询", "提出调查计划；征求对方意见", "04 · 11"),
    ("2025", "介绍＋邀请", "介绍短剧；邀请朋友参加", "11 · 01"),
    ("2026*", "感谢＋询问", "谈对旅行视频的感受；想了解更多", "05 · 09"),
]


# ---------------------------------------------------------------- 每篇的段落分工与升级句

EXTRA = {
    "01": dict(
        split="① 点题｜②—⑤ 时间、地点、环节、收获｜⑥—⑦ 促回复",
        upgrade=[
            ("Should you need any further details, please feel free to contact me.",
             "条件倒装，替代 if you need…，结尾更像公务信"),
            ("I would be more than happy to reserve a seat for you.",
             "would be more than happy 比 I am happy 礼貌一档"),
        ],
    ),
    "02": dict(
        split="①—② 感谢＋接受｜③—⑤ 要点与准备｜⑥—⑦ 再谢＋承诺",
        upgrade=[
            ("I have already prepared a short handout for the audience.",
             "现在完成时，证明“我真的准备好了”"),
            ("Please let me know if there is anything else I should bring.",
             "主动询问，显得可靠，不像背模板"),
        ],
    ),
    "03": dict(
        split="①—② 感谢＋拒绝｜③—⑥ 原因＋替代｜⑦—⑧ 致歉收尾",
        upgrade=[
            ("I would be grateful if we could fix another time that suits you.",
             "礼貌请求，替代生硬的 Can we meet again?"),
            ("I hope this will not cause you too much inconvenience.",
             "先顾对方感受，婉拒信的关键一句"),
        ],
    ),
    "04": dict(
        split="①—② 给结论｜③—⑤ 两条理由＋附加好处｜⑥—⑧ 交还决定权",
        upgrade=[
            ("What makes it stand out is the hands-on experience it offers.",
             "what 从句强调，替代 it is very good"),
            ("Either choice would be fine, but this one fits your interest better.",
             "让步＋比较，语气成熟，不武断"),
        ],
    ),
    "05": dict(
        split="①—② 背景＋感谢｜③—⑤ 影响＋细节｜⑥—⑦ 回请",
        upgrade=[
            ("Your kindness made a stranger feel at home.",
             "make sb. feel at home，比 warm reception 更有画面"),
            ("I hope I can return the favour when you come to China.",
             "return the favour 是“还人情”的地道说法"),
        ],
    ),
    "06": dict(
        split="①—② 祝贺｜③—⑥ 两条建议｜⑦—⑨ 祝福＋联系",
        upgrade=[
            ("This is only the beginning of a much longer journey.",
             "比喻收尾，比 Good luck 高一档"),
            ("Do let me know how you settle in.",
             "do 强调＋settle in，口语得体"),
        ],
    ),
    "07": dict(
        split="①—② 道歉＋取消｜③—⑦ 原因＋补救＋另约｜⑧—⑨ 收尾",
        upgrade=[
            ("I fully understand how inconvenient this must be for you.",
             "先共情再解释，比单说 sorry 成熟"),
            ("I will make sure it does not happen again.",
             "承诺具体，补救不止一句空话"),
        ],
    ),
    "08": dict(
        split="① 购买信息｜②—④ 故障＋影响｜⑤—⑦ 要求＋期限",
        upgrade=[
            ("I have kept the receipt and can send you a photo if needed.",
             "证据意识，投诉可信度立刻上来"),
            ("I would appreciate a reply at your earliest convenience.",
             "礼貌催复，不写 I want a reply now"),
        ],
    ),
    "09": dict(
        split="①—② 背景｜③—⑤ 习惯＋两个问题｜⑥—⑧ 致谢",
        upgrade=[
            ("Any advice you could offer would be much appreciated.",
             "被动礼貌请求，比 please tell me 委婉"),
            ("I would also be grateful for a rough idea of the cost.",
             "把问题问得更具体，对方好回答"),
        ],
    ),
    "10": dict(
        split="①—② 活动概况｜③—⑤ 内容＋报名｜⑥—⑧ 招募＋截止",
        upgrade=[
            ("Places will be allocated on a first-come, first-served basis.",
             "先到先得，通知里一句话说清规则"),
            ("For further information, please visit our website.",
             "通知常用收尾，替掉 Thank you for listening"),
        ],
    ),
    "11": dict(
        split="① 点题｜②—⑤ 特点＋亮点｜⑥—⑨ 两条贴士",
        upgrade=[
            ("You will find the trip both relaxing and rewarding.",
             "both…and 并列收束，比 very nice 具体"),
            ("Do remember to charge your phone before we set off.",
             "do 强调提醒，贴士更像贴士"),
        ],
    ),
    "12": dict(
        split="①—② 推荐什么｜③—⑥ 理由＋事例｜⑦—⑨ 获取方式",
        upgrade=[
            ("It is the kind of book you will finish in a weekend.",
             "定语从句，评价具体可感"),
            ("I would be glad to lend you my copy first.",
             "主动提供帮助，结尾更暖"),
        ],
    ),
}

for _g in GENRES:
    _g.update(EXTRA[_g["num"]])


# ---------------------------------------------------------------- 题干变体怎么改

VARIANTS = {
    "01": ["2021 线上会议：地点改 on Zoom，环节改 agenda items，附上会议号。",
           "2025 短剧：主办方改 the Drama Club，参加对象改 your classmates。"],
    "02": ["线上会议变体：准备工作改 test my microphone，日期改 the day before。",
           "要点部分改成两个具体话题，不要写 many interesting things。"],
    "03": ["只用于“被邀请但去不了”；2018 那种“自己取消约定”用 07 道歉信。",
           "婉拒教授时保留 Professor 姓氏，不要用 Dear teacher。"],
    "04": ["2019 辩论：建议对象换成 a specific topic，理由换成 relevance 与 data。",
           "2024 调查计划：建议对象换成 the plan itself，理由讲可行性与时间。"],
    "05": ["2016 回复祝贺：开头改 Thank you for your congratulations，再接建议。",
           "感谢对象是机构时，称呼用 Dear Sir or Madam，落款仍用题目姓名。"],
    "06": ["2016 回复祝贺：第一段感谢对方的祝贺，第二段再给翻译建议。",
           "祝贺教授晋升时，语气收一点，不用感叹号连发。"],
    "07": ["2018 取消拜访；若只是迟到，把取消改成迟到，补救改成改期。",
           "对朋友可删掉 Please accept my apology，换成 I owe you one。"],
    "08": ["投诉服务（课程、快递）时，商品换成 the course / the delivery。",
           "要求部分按“换—修—退”顺序写，期限给具体天数。"],
    "09": ["2024 征求意见：问题改成 Do you think the plan is workable?",
           "咨询住宿时，两个问题分别问价格与距离，不要都问好不好。"],
    "10": ["2013 慈善义卖：标题仍 Notice，第三段改成鼓励参加，不写招募。",
           "线上活动把地点改 on the school website，报名方式给链接。"],
    "11": ["2022 美食节：介绍对象换成 the festival，贴士改成空腹来、带现金。",
           "2025 短剧：介绍对象换成 the play，贴士改成提前入场、保持安静。"],
    "12": ["推荐人：优点换成 works hard / has a good command of English。",
           "推荐地点：优点换成 free entry / easy to reach，事例写自己去过。"],
}

for _g in GENRES:
    _g["variants"] = VARIANTS[_g["num"]]
