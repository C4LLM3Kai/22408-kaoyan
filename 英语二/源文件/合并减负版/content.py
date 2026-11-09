from pathlib import Path
import json,re
R=Path(__file__).parent
cores=[
 dict(id='M1',title='活动安排',covers='邀请、介绍、欢迎、活动通知、招募、计划、活动类答复、倡议',route='为什么办 → 何时何地 → 做什么 → 读者怎么参与',
 template=['The 【活动】 will take place 【时间】 at 【地点】. Its aim is to 【目的，动词原形】. I hope you can 【邀请或希望对方做的事，动词原形】.',
 'We plan to start with 【环节一】 and then move on to 【环节二】. During the event, participants can 【动作】, which will help them 【具体收获】. Please 【准备或报名动作】 before 【时间／事件】.',
 'Let me know if you need any further details.'],
 task='例：邀请 Jack 参加校园旧物修理活动；说明安排和准备事项。',
 body=['The repair workshop will take place on Friday afternoon at the student centre. Its aim is to help students reuse old items. I hope you can join us and share your ideas.',
 'We plan to start with a short demonstration and then move on to guided practice. During the event, participants can learn basic repair skills, which will help them make better use of what they own. Please bring a small item that needs repair before the workshop begins.',
 'Let me know if you need any further details. I can reserve a place for you if you are interested.'],
 header='Dear Jack,',footer='Best wishes,\nLi Ming',
 notes=['招募：第二段补职责和要求，见第7页，不另背通知正文。','计划＋征求意见：把 will／plan to 改成 could，把结尾换为 What do you think of this plan?','通知：去掉 I hope you can 和私人回信语，换标题、发布单位及报名方式。','倡议：把活动目的换成行动目标；不必硬填时间地点，直接写两项可执行行动。']),
 dict(id='M2',title='建议与理由',covers='建议、推荐人或物、申请、求职、观点类答复',route='提出选择 → 理由一＋具体作用 → 理由二／证据 → 下一步',
 template=['To 【目标动作，动词原形】, I suggest 【做法，动名词】. There are two practical reasons for this choice.',
 'First, 【做法或对象】 offers 【优势一】. This can help 【受益者】 【具体效果，动词原形】 without 【不必要的代价，动名词】. Second, 【另一特点，完整分句】. For example, 【贴题细节，完整分句】. These features make it suitable for 【具体需要】.',
 'If you decide to try it, start by 【第一步，动名词】.'],
 task='例：朋友 Anna 想提高口语，建议她参加小型讨论组，并说明理由。',
 body=['To improve your spoken English, I suggest joining a small discussion group. There are two practical reasons for this choice.',
 'First, a small group offers regular speaking practice. This can help you express your ideas more confidently without paying for expensive lessons. Second, members can learn from one another. For example, when you cannot explain a point clearly, someone else may suggest a simpler expression. These features make it suitable for learners who need both practice and feedback.',
 'If you decide to try it, start by inviting two classmates to discuss a familiar topic after class. I would be glad to join you.'],
 header='Dear Anna,',footer='Best wishes,\nLi Ming',
 notes=['推荐：只改首句为 For【需求】, I recommend【人或物】；理由必须与对方需求匹配。','直接给建议时，也可把 First 后改成一条行动，再保留 This can help... 解释好处。','申请／求职：用第7页的申请开头；第二段写自己的技能＋具体经历，结尾请求面谈。','推荐他人：补你与此人的关系，给真实情境中的能力证据，不只堆性格形容词。']),
 dict(id='M3',title='问题与补救',covers='道歉、投诉、求助、辞职、婉拒',route='说明目的 → 问题与影响 → 解决或交接 → 确认',
 template=['I am writing about 【事项】. 【从第7页选择一句目的句】',
 'The main difficulty is that 【问题，完整分句】. As a result, 【具体影响，完整分句】. A workable solution would be to 【解决办法】. In the meantime, 【临时安排，完整分句】. This would allow 【受益者】 to 【预期结果】 without 【额外困难，动名词】.',
 'Please tell me whether this arrangement would work for you.'],
 task='例：你借 Alex 的书不慎损坏，说明影响并提出换书和临时借阅方案。',
 body=['I am writing about the book you lent me. I am sorry for damaging it yesterday.',
 'The main difficulty is that several pages are now stained after I spilled water on them. As a result, some of the notes are difficult to read. A workable solution would be to buy you a new copy of the same edition. In the meantime, you can use my copy for your course. This would allow you to continue studying without waiting for the replacement to arrive.',
 'Please tell me whether this arrangement would work for you. I will take better care of borrowed books in future.'],
 header='Dear Alex,',footer='Best wishes,\nLi Ming',
 notes=['道歉要承担责任；投诉是客观说明问题并提出诉求，不能沿用“都是我的错”。','辞职、婉拒必须在开头直接说清决定；补救段换成交接、替代帮助或改期。','求助时写清自己遇到的困难、需要对方做的具体事情和期限。','The main difficulty... 不适合无实际困难的普通咨询；普通咨询直接用第7页问句。']),
 dict(id='M4',title='情感交流',covers='感谢、祝贺、表达感受、分享后追问、私人回复',route='明确情感 → 具体细节 → 为什么有意义 → 合适收尾',
 template=['【感谢／祝贺／回应消息的一句开头】',
 'What stayed with me was 【具体细节】. It showed me how 【观察或感受，完整分句】. I especially valued 【另一细节，名词或动名词】 because 【贴题理由，完整分句】. This experience has encouraged me to 【积极行动，动词原形】.',
 '【按任务选择：再次致谢／祝愿／具体追问】'],
 task='例：Jack 分享了家庭旅行视频；表达具体感受，并询问想进一步了解的旅行细节。',
 body=['Your travel video made me smile, especially the scenes with your family.',
 'What stayed with me was the moment when you learned to make noodles with a local cook. It showed me how food can bring people closer together. I especially valued the conversations with local families because they made the journey feel personal and warm. This experience has encouraged me to learn more about the places you visited.',
 'How did you find the cooking workshop? I would also love to know which place your parents enjoyed most. Please share a few more stories when you have time. I would enjoy hearing them.'],
 header='Dear Jack,',footer='Best wishes,\nLi Ming',
 notes=['感谢：细节写“对方具体帮了什么”，意义写“给我带来的变化”，最后再致谢即可。','祝贺：细节写你看到的努力和成果；不适合写自身收获时删掉 This experience...。','感受＋追问：一定写具体感受和具体问题；不能只用 Thank you／tell me more 凑齐任务。','只有题目要求或情境合理时才写未来行动；这句可删，不必每种情感信都硬套。'])]
chart=dict(id='M5',title='图表作文',covers='静态构成、多选柱图、群体表格、单指标趋势、多指标变化、波动、双图表',
 static='The 【图表类型】 compares 【调查对象】 in terms of 【指标】. 【A】 records the highest figure, at 【数值】, while 【B】 stands at 【数值】. 【另一关键对比，完整句】',
 dynamic='Between 【起年】 and 【止年】, 【指标】 【rose/fell】 from 【起值】 to 【终值】. Over the same period, 【另一个指标或阶段的关键变化，完整分句】. 【可由数据支持的总趋势，完整句】',
 shared=['Two practical factors may help explain 【这种分布或变化，名词短语】. First, 【原因一，完整分句】. This can make it easier for 【群体】 to 【行为，动词原形】. Second, 【原因二，完整分句】. When 【具体情境，完整分句】, people may 【选择或行动，动词原形】. These are possible explanations, rather than causes established by the chart.',
 'For 【有关主体】, a useful next step would be to 【具体措施，动词原形】. The aim should be to 【贴题目标】 while 【兼顾事项，动名词】.'],
 task='新编数据：某市公共交通出行占比，2020年30%、2022年36%、2024年45%；描述趋势并评论。',
 body=['Between 2020 and 2024, the share of journeys made by public transport rose from 30% to 45%. Over the same period, the increase was larger after 2022, when the figure stood at 36%. Overall, public transport gained fifteen percentage points.',
 'Two practical factors may help explain this growth. First, better connections may have reduced the inconvenience of changing buses. This can make it easier for commuters to plan their journeys. Second, reliable arrival information may reduce uncertainty. When waiting times are clear, people may feel more comfortable leaving their cars at home. These are possible explanations, rather than causes established by the chart.',
 'For city transport planners, a useful next step would be to improve connections and access. The aim should be to make daily travel easier while keeping fares affordable. Such improvements could also help people with different schedules benefit from the service.'])
# English chunks used for very short functional substitutions. These are not 26 new essays.
cards=[
 ('邀请／介绍／欢迎','M1','I hope you can join us. / The main arrangements are as follows.','填活动名称、时间地点、两项安排；关系亲近时直接进入正题。'),
 ('招募要求','M1','Volunteers will 【职责】. Applicants should 【条件】.','职责和要求各写一句；招募文不要只写活动意义。'),
 ('推荐／申请','M2','I recommend 【对象】. / I would like to apply for 【岗位】.','申请主体改为 my experience / my skills，并给具体过去经历。'),
 ('道歉／投诉','M3','I am sorry for 【过失，动名词】. / I would like 【解决诉求】.','同用补救结构；道歉承担责任，投诉提出合理要求。'),
 ('求助／辞职／婉拒','M3','Could you help me 【动作】? / I have decided to leave 【岗位】. / I cannot attend 【活动】.','解释原因后写帮法、交接或替代安排；辞职补离职日期。'),
 ('感谢／祝贺','M4','Thank you for 【帮助】. / Congratulations on 【成就】.','主体共用“具体细节＋意义”；结尾致谢或祝愿即可。'),
 ('感受／追问','M4','Your 【分享内容】 made me feel 【感受】. / Could you tell me 【疑问词＋陈述语序从句】?','只背这一问句结构，换 when / where / how / why；确保询问与题目有关。'),
 ('计划征求意见／申请面谈','M1／M2','What do you think of this plan? / I would welcome an interview.','各保留一句专用结尾，不能用期待回信代替征求意见。')]
# Mapping checks account for every former section, without retaining 36 independent essays.
map36={
 'M1':['A01','A05','A06','A07','A17','A20','A21','A24'],
 'M2':['A02','A03','A04','A14','A15'],
 'M3':['A10','A11','A13','A18','A19'],
 'M4':['A08','A09','A16'],
 '问句与格式卡':['A12','A22','A23','A25','A26'],
 'M5':['B01','B02','B03','B04','B05','B06','B07'],
 '备用首段':['B08','B09','B10']}
def count(s):return len(re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*|\d+(?:[.,]\d+)*(?:%)?",s))
def fixed(s):return count(re.sub(r'【.*?】','',s))
core_words=sum(fixed(' '.join(x['template'])) for x in cores)+fixed(chart['static']+' '+chart['dynamic']+' '+' '.join(chart['shared']))
result=dict(cores=cores,chart=chart,cards=cards,mapping=map36,fixed_core_words=core_words)
(R/'content.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print('CORE FIXED WORDS',core_words)
for x in cores+[chart]:print(x['id'],'example words',count(' '.join(x['body'])))
assert len([i for arr in map36.values() for i in arr])==36
