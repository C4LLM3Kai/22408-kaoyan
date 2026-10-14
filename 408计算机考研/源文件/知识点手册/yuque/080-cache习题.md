<!-- yuque:hnlngb/kpfo07kszac3fyrc book_id=48597829 doc_id=272034233 -->

# cache习题

1. 【2009-21】假设某计算机的存储系统由Cache和主存组成。某程序执行过程中访存1000次，其中访问Cache缺失（未命中）50次，则Cache的命中率是（ ）。

A. 5%

B. 9.5%

C. 50%

D. 95%

<details class="lake-collapse"><summary id="u2812ede2"><span class="ne-text">解析</span></summary><p id="u7bf6106f" class="ne-p"><strong><span class="ne-text">答案：D</span></strong><span class="ne-text"><br /></span><span class="ne-text">Cache命中率公式为：</span><span id="Hc0Pc" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/a3fc71943e35d319eaf306a7dc5b97eb.svg"></span></p><p id="u18e1c4e7" class="ne-p"><span class="ne-text">总访存1000次，缺失50次，命中次数=1000-50=950次，因此命中率=950/1000=95%。</span></p></details>


2. 【2014-16】采用指令Cache与数据Cache分离的主要目的是（ ）。

A. 降低Cache的缺失损失

B. 提高Cache的命中率

C. 降低CPU平均访存时间

D. 减少指令流水线资源冲突

<details class="lake-collapse"><summary id="ub3598ba9"><span class="ne-text">解析</span></summary><p id="uc85cd646" class="ne-p"><strong><span class="ne-text">答案：D</span></strong><span class="ne-text"></span></p><p id="udb99cf45" class="ne-p" style="text-indent: 2em"><span class="ne-text">在指令流水线中，IF（取指）阶段访问指令 Cache，MEM（访存）阶段访问数据 Cache。若两者共用同一个 Cache，IF 和 MEM 阶段将产生</span><strong><span class="ne-text">结构冒险（资源冲突）</span></strong><span class="ne-text">，无法并行执行。分离后，IF 和 MEM 可在同一时钟周期内同时访问各自的 Cache，消除结构冲突。</span></p><p id="u9d3ff70c" class="ne-p" style="text-indent: 2em"><span class="ne-text">选项 A/B/C 不是主要目的，命中率和平均访存时间不一定因分离而明显改善。</span></p></details>


3. 【2009-14】某计算机的Cache共有16块，采用2路组相联映射方式（即每组2块）。每个主存块大小为32字节，按字节编址。主存129号单元所在主存块应装入到的Cache组号是（ ）。

A. 0

B. 2

C. 4

D. 6

<details class="lake-collapse"><summary id="u8456bec5"><span class="ne-text">解析</span></summary><p id="u4468013f" class="ne-p"><strong><span class="ne-text">答案：C</span></strong><span class="ne-text"><br /></span><span class="ne-text">组相联映射核心公式：</span><span id="BPn7n" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/ec8df49e6e2705c81dd843a1ebc31ff4.svg"></span></p><ol class="ne-ol"><li id="u2dc065c1" data-lake-index-type="0"><span class="ne-text">计算主存块号：主存块大小32字节，按字节编址，129号单元所在主存块号=⌊129/32⌋=4；</span></li><li id="uc3f1efb1" data-lake-index-type="0"><span class="ne-text">计算Cache组数：Cache共16块，2路组相联，每组2行，组数=16/2=8组；</span></li><li id="ud3311dec" data-lake-index-type="0"><span class="ne-text">计算组号：4 mod 8=4。</span></li></ol><p id="u02d69b2e" class="ne-p"><span class="ne-text">或者这样，</span></p><ul class="ne-ul"><li id="uadb2d35f" data-lake-index-type="0"><span class="ne-text" style="color: rgb(51, 51, 51)">Cache 共 16 块，2 路组相联 → 组数 = 16 / 2 = </span><strong><span class="ne-text" style="color: rgb(51, 51, 51)">8 组</span></strong></li><li id="ue2d9c784" data-lake-index-type="0"><span class="ne-text" style="color: rgb(51, 51, 51)">块大小 = 32 字节 → 块内偏移位数 = log₂(32) = 5 位</span></li><li id="u3a8a8e99" data-lake-index-type="0"><span class="ne-text" style="color: rgb(51, 51, 51)">组索引位数 = log₂(8) = 3 位  因此可知</span></li></ul><p id="u66037595" class="ne-p"><span class="ne-text">主存地址 129 转为二进制为 </span><span class="ne-text" style="background-color: #FBDE28">100 </span><span class="ne-text" style="background-color: #FBE4E7">00001</span><span class="ne-text">，其中 </span><span class="ne-text" style="background-color: #FBE4E7">00001</span><span class="ne-text"> 为块内地址，</span><span class="ne-text" style="background-color: #FBDE28">100 </span><span class="ne-text">为组号，因此组号为 4.</span></p></details>


4. 【2012-17】假设某计算机按字编址，Cache有4个行，Cache和主存之间交换的块大小为1个字。若Cache的内容初始为空，采用2路组相联映射方式和LRU替换策略。访问的主存地址依次为 0,4,8,2,0,6,8,6,4,8 时，命中Cache的次数是（ ）。

A. 1

B. 2

C. 3

D. 4

<details class="lake-collapse"><summary id="ud2237514"><span class="ne-text">解析</span></summary><p id="u33e31653" class="ne-p"><span class="ne-text">本题与 408 现在的映射规则不同，因此跳过不做</span></p></details>


5. 【2015-15】假定主存地址位数为32位，按字节编址，主存和Cache之间采用直接映射方式，主存块大小为4个字，每字32位，写操作时采用回写 (Write Back) 方式，则能存放4K字数据的Cache的总容量的位数至少是（ ）。

A. 146K

B. 147K

C. 148K

D. 158K

<details class="lake-collapse"><summary id="uad10900f"><span class="ne-text">解析</span></summary><p id="u22e62521" class="ne-p"><strong><span class="ne-text">答案：C</span></strong><span class="ne-text"></span></p><ul class="ne-ul"><li id="ua1dfcd3d" data-lake-index-type="0"><span class="ne-text">数据容量 = 4K 字 × 32 位/字 = 4K × 4B = </span><strong><span class="ne-text">16KB</span></strong></li><li id="u4082fddd" data-lake-index-type="0"><span class="ne-text">主存块大小 = 4 字 × 4B = </span><strong><span class="ne-text">16B</span></strong></li><li id="uefe89a03" data-lake-index-type="0"><span class="ne-text">Cache 行数 = 16KB / 16B = </span><strong><span class="ne-text">1024 行</span></strong></li><li id="u103aae1a" data-lake-index-type="0"><span class="ne-text">地址位分配（32位，直接映射）：</span></li></ul><ul class="ne-list-wrap"><ul ne-level="1" class="ne-ul"><li id="u70a69388" data-lake-index-type="0"><span class="ne-text">块内偏移 = log₂(16) = </span><strong><span class="ne-text">4 位</span></strong></li><li id="u9b90cdca" data-lake-index-type="0"><span class="ne-text">行索引 = log₂(1024) = </span><strong><span class="ne-text">10 位</span></strong></li><li id="u0fc99f23" data-lake-index-type="0"><span class="ne-text">标记（Tag）= 32 − 4 − 10 = </span><strong><span class="ne-text">18 位</span></strong></li></ul></ul><ul class="ne-ul"><li id="uff3fc3c6" data-lake-index-type="0"><span class="ne-text">每行位数 = 标记(18) + 有效位(1) + 脏位(1，回写需要) + 数据(16B×8=128) = </span><strong><span class="ne-text">148 位</span></strong></li><li id="u47c5cdd2" data-lake-index-type="0"><span class="ne-text">Cache 总容量 = 1024 × 148 = </span><strong><span class="ne-text">148K 位</span></strong></li></ul></details>


6. 【2016-15】有如下 C 语言程序段：

```c
for (k = 0; k < 1000; k++)
    a[k] = a[k] + 32;
```

若数组 a 以及变量 k 均为 int 型，int 型数据占 4B，数据 Cache 采用直接映射方式，数据区大小是 1KB，块大小是 16B，该程序段执行前 Cache 为空，则该程序段执行过程中，访问数组 a 的 Cache 的缺失率是（ ）。

A. 1.25%

B. 2.5%

C. 12.5%

D. 25%

<details class="lake-collapse"><summary id="u0eac9043"><span class="ne-text">解析</span></summary><p id="u71c2f6e4" class="ne-p"><strong><span class="ne-text">答案：C</span></strong><span class="ne-text"></span></p><ul class="ne-ul"><li id="ud0e32dae" data-lake-index-type="0"><span class="ne-text">int = 4B，块大小 = 16B → 每块含 16B / 4B = </span><strong><span class="ne-text">4 个 int</span></strong></li><li id="u12646d8d" data-lake-index-type="0"><span class="ne-text">每次迭代对 a[k] 进行 1 次读 + 1 次写 = 2 次访问</span></li><li id="u0e13eef7" data-lake-index-type="0"><span class="ne-text">总访问次数 = 2 × 1000 = </span><strong><span class="ne-text">2000 次</span></strong></li><li id="u9162a114" data-lake-index-type="0"><span class="ne-text">每 4 个元素（一个块）的第 1 次读为冷缺失，随后的读/写均命中：</span></li></ul><ul class="ne-list-wrap"><ul ne-level="1" class="ne-ul"><li id="ufed9d518" data-lake-index-type="0"><span class="ne-text">缺失次数 = 1000 / 4 = </span><strong><span class="ne-text">250 次</span></strong></li></ul></ul><ul class="ne-ul"><li id="u94a65210" data-lake-index-type="0"><span class="ne-text">缺失率 = 250 / 2000 = </span><strong><span class="ne-text">12.5%</span></strong></li></ul></details>


7. 【2021-16】若计算机主存地址为32位，按字节编址，Cache数据区大小为32KB，主存块大小为32B，采用直接映射方式和回写（Write Back）策略，则Cache行的位数至少是（ ）。

A. 275

B. 274

C. 258

D. 257

<details class="lake-collapse"><summary id="u9bc9d868"><span class="ne-text">解析</span></summary><p id="u2076e689" class="ne-p"><strong><span class="ne-text">答案：A</span></strong><span class="ne-text"><br /></span><strong><span class="ne-text">解析</span></strong><span class="ne-text">：</span></p><ul class="ne-ul"><li id="ubb61f098" data-lake-index-type="0"><span class="ne-text">数据区 = 32KB，块大小 = 32B，直接映射</span></li><li id="uda6f52c0" data-lake-index-type="0"><span class="ne-text">Cache 行数 = 32KB / 32B = </span><strong><span class="ne-text">1024 行</span></strong></li><li id="ue69a609e" data-lake-index-type="0"><span class="ne-text">地址分配（32 位）：</span></li></ul><ul class="ne-list-wrap"><ul ne-level="1" class="ne-ul"><li id="u50ae57f4" data-lake-index-type="0"><span class="ne-text">块内偏移 = log₂(32) = </span><strong><span class="ne-text">5 位</span></strong></li><li id="u9f59b847" data-lake-index-type="0"><span class="ne-text">行索引 = log₂(1024) = </span><strong><span class="ne-text">10 位</span></strong></li><li id="ub07ab62d" data-lake-index-type="0"><span class="ne-text">标记 = 32 − 5 − 10 = </span><strong><span class="ne-text">17 位</span></strong></li></ul></ul><ul class="ne-ul"><li id="ucec111f6" data-lake-index-type="0"><span class="ne-text">每行位数 = 有效位(1) + 脏位(1，回写) + 标记(17) + 数据(32B×8=256) = </span><strong><span class="ne-text">1 + 1 + 17 + 256 = 275 位</span></strong></li></ul></details>


8. 【2022-16】某计算机主存地址为32位，按字节编址，某Cache的数据区容量为32KB，主存块大小为64B，采用8路组相联映射方式，该Cache中比较器的个数和位数分别为（ ）。

A. 8，20

B. 8，23

C. 64，20

D. 64，23

<details class="lake-collapse"><summary id="ud04f949f"><span class="ne-text">解析</span></summary><p id="u21ab75de" class="ne-p"><strong><span class="ne-text">答案：A</span></strong><span class="ne-text"></span></p><ul class="ne-ul"><li id="u2b366454" data-lake-index-type="0"><span class="ne-text">数据区 = 32KB，块大小 = 64B，8 路组相联</span></li><li id="u93bfeb8f" data-lake-index-type="0"><span class="ne-text">组数 = (32KB / 64B) / 8 = 512 / 8 = </span><strong><span class="ne-text">64 组</span></strong></li><li id="u51858cba" data-lake-index-type="0"><span class="ne-text">地址分配（32 位）：</span></li></ul><ul class="ne-list-wrap"><ul ne-level="1" class="ne-ul"><li id="u150edba3" data-lake-index-type="0"><span class="ne-text">块内偏移 = log₂(64) = </span><strong><span class="ne-text">6 位</span></strong></li><li id="u65972f16" data-lake-index-type="0"><span class="ne-text">组索引 = log₂(64) = </span><strong><span class="ne-text">6 位</span></strong></li><li id="u052aeb82" data-lake-index-type="0"><span class="ne-text">标记 = 32 − 6 − 6 = </span><strong><span class="ne-text">20 位</span></strong></li></ul></ul><ul class="ne-ul"><li id="ub7b77198" data-lake-index-type="0"><span class="ne-text">访问时，用组索引选定一组，将输入标记与该组 </span><strong><span class="ne-text">8 路</span></strong><span class="ne-text">的标记同时比较：</span></li></ul><ul class="ne-list-wrap"><ul ne-level="1" class="ne-ul"><li id="uaf4e27d4" data-lake-index-type="0"><span class="ne-text">比较器个数 = </span><strong><span class="ne-text">8 个</span></strong><span class="ne-text">（每路一个，并行比较）</span></li><li id="u858f9cc6" data-lake-index-type="0"><span class="ne-text">每个比较器宽度 = 标记位数 = </span><strong><span class="ne-text">20 位</span></strong></li></ul></ul></details>


9. **（袁书习题）在主存和 CPU 之间增加 cache 的目的是（ ）。**  
A. 增加内存容量  
B. 提高内存可靠性  
C. 加快信息访问速度  
D. 增加内存容量，同时加快访问速度

<details class="lake-collapse"><summary id="u4a0f95c3"><span class="ne-text">解析</span></summary><p id="ua5aca0f8" class="ne-p"><strong><span class="ne-text">答案：C</span></strong></p><p id="u1640c031" class="ne-p"><strong><span class="ne-text">解析：</span></strong><span class="ne-text"> “Cache（高速缓冲存储器）是CPU与主存之间的小容量高速缓冲存储层级，是现代计算机存储体系中弥补CPU与主存速度鸿沟的核心组件”。Cache 的主要目的是利用局部性原理，让 CPU 尽可能从高速的 Cache 中获取数据，从而</span><strong><span class="ne-text">大幅降低 CPU 的平均访存延迟（即加快信息访问速度）</span></strong><span class="ne-text">，而不是为了增加容量（容量由主存决定）或提高可靠性。</span></p></details>


10. **（袁书习题）以下（ ）情况能很好地发挥 cache 的作用。**  
A. 程序中不含有过多的 I/O 操作  
B. 程序的大小不超过实际的内存容量  
C. 程序具有较好的访问局部性  
D. 程序的指令间相关度不高

<details class="lake-collapse"><summary id="ub8a36144"><span class="ne-text">解析</span></summary><p id="u642e2876" class="ne-p"><strong><span class="ne-text">答案：C</span></strong></p><p id="u7a209a16" class="ne-p"><strong><span class="ne-text">解析：</span></strong><span class="ne-text"> “Cache的高效工作完全依赖程序访问的局部性特征”，包括时间局部性和空间局部性。只有当</span><strong><span class="ne-text">程序具有较好的访问局部性</span></strong><span class="ne-text">时，Cache 才能保持高命中率，从而发挥加速作用。</span></p></details>
11. ** （袁书习题）假定主存地址位数为 32 位，按字节编址，主存和 cache 之间采用直接映射方式，主存块大小为 1 个字，每字 32 位，写操作时采用直写（write through）方式，则能存放 32K 字数据的 cache 的总容量至少应有（ ）位。**  
A. 1504K  
B. 1536K  
C. 1568K  
D. 1600K

<details class="lake-collapse"><summary id="u121d25d0"><span class="ne-text">解析</span></summary><p id="u618ffa1d" class="ne-p"><strong><span class="ne-text">答案：B</span></strong></p><p id="ua6a4d8b4" class="ne-p"><strong><span class="ne-text">解析：</span></strong></p><ol class="ne-ol"><li id="u5a80cdce" data-lake-index-type="0"><strong><span class="ne-text">计算 Cache 行数：</span></strong><span class="ne-text"> 数据区容量为 32K 字，块大小为 1 字，所以 Cache 行数 = </span><span id="YTExF" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/879ec98d0bfc5a17e6bb04fc8c9cb28f.svg"></span><span class="ne-text"> 行。因此 Index（行索引）占 15 位。</span></li><li id="u3e271602" data-lake-index-type="0"><strong><span class="ne-text">计算地址划分：</span></strong><span class="ne-text"> 主存地址 32 位，按字节编址。块大小 1 字 = 4 字节（32位），所以 Offset（块内偏移）占 </span><span id="nE9Kv" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/15e1eb50ebb3e18eebd25f83990c7305.svg"></span><span class="ne-text"> 位。</span></li><li id="uecaf9839" data-lake-index-type="0"><strong><span class="ne-text">计算 Tag 位数：</span></strong><span class="ne-text"> Tag = 总地址位 - Index位 - Offset位 = </span><span id="M2Oyc" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/9f29dde567f1baea9068a9d09b306bac.svg"></span><span class="ne-text"> 位。</span></li><li id="uc2b4fdd5" data-lake-index-type="0"><strong><span class="ne-text">确定控制位：</span></strong></li></ol><ul class="ne-list-wrap"><ul ne-level="1" class="ne-ul"><li id="u3aa8acac" data-lake-index-type="0"><span class="ne-text">Valid位（有效位）：1 位（必须）。</span></li><li id="u2babe19b" data-lake-index-type="0"><span class="ne-text">Dirty位（脏位）：题目采用直写方式，</span><strong><span class="ne-text">无需脏位</span></strong><span class="ne-text">（dirty bit），因为数据同时写入主存，Cache与主存实时一致。</span></li></ul></ul><ol start="5" class="ne-ol"><li id="u08ed8d71" data-lake-index-type="0"><strong><span class="ne-text">计算总容量：</span></strong></li></ol><ul class="ne-list-wrap"><ul ne-level="1" class="ne-ul"><li id="u568fad30" data-lake-index-type="0"><span class="ne-text">每行位数 = 数据位 + Tag位 + Valid位 = </span><span id="ag1h3" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/152c2bfddf795cd1f3ececc416dc37cc.svg"></span><span class="ne-text"> 位。</span></li><li id="u7b6ad4ea" data-lake-index-type="0"><span class="ne-text">总容量 = 行数 × 每行位数 = </span><span id="P9BKW" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/2387d452165450350b479b96363551d6.svg"></span><span class="ne-text"> 位。</span></li></ul></ul></details>
12. **（袁书习题）假定主存地址位数为 32 位，按字节编址，主存和 cache 之间采用直接映射方式，主存块大小为 1 个字，每字 32 位，写操作时采用回写（write back）方式，则能存放 32K 字数据的 cache 的总容量至少应有（ ）位。**  
A. 1504K  
B. 1536K  
C. 1568K  
D. 1600K

<details class="lake-collapse"><summary id="uec8e6778"><span class="ne-text">解析</span></summary><p id="u8d8c0a03" class="ne-p"><strong><span class="ne-text">答案：C</span></strong></p><p id="u79ba61f2" class="ne-p"><strong><span class="ne-text">解析：</span></strong></p><ol class="ne-ol"><li id="ufb54596c" data-lake-index-type="0"><strong><span class="ne-text">参数同上：</span></strong><span class="ne-text"> 行数 32K，Tag 15 位，数据 32 位。</span></li><li id="u91a2ee42" data-lake-index-type="0"><strong><span class="ne-text">确定控制位：</span></strong><span class="ne-text"> 题目采用回写方式，必须为每个 Cache行设置 1位脏位（Dirty Bit）。</span></li><li id="udbf29a1d" data-lake-index-type="0"><strong><span class="ne-text">计算总容量：</span></strong></li></ol><ul class="ne-list-wrap"><ul ne-level="1" class="ne-ul"><li id="ufdfba7d3" data-lake-index-type="0"><span class="ne-text">每行位数 = 数据位 + Tag位 + Valid位 + Dirty位 = </span><span id="uAngl" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/9a32d39cb7799c11b4a3f74ee22647a5.svg"></span><span class="ne-text"> 位。</span></li><li id="uffac3350" data-lake-index-type="0"><span class="ne-text">总容量 = </span><span id="a6sk8" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/95efe3ad1e2bbada2579891195fbbec7.svg"></span><span class="ne-text"> 位。</span></li></ul></ul></details>
13. **（袁书习题）假定主存地址位数为 32 位，按字节编址，主存和 cache 之间采用全相联映射方式，主存块大小为 1 个字，每字 32 位，采用回写（write Back）方式和随机替换策略，则能存放 32K 字数据的 cache 的总容量至少应有（ ）位。**  
A. 1536K  
B. 1568K  
C. 2016K  
D. 2048K

<details class="lake-collapse"><summary id="uee64a462"><span class="ne-text">解析</span></summary><p id="u9b64941d" class="ne-p"><strong><span class="ne-text">答案：D</span></strong></p><p id="u3a175bab" class="ne-p"><strong><span class="ne-text">解析：</span></strong></p><ol class="ne-ol"><li id="u1c3b498f" data-lake-index-type="0"><strong><span class="ne-text">计算 Cache 行数：</span></strong><span class="ne-text"> 数据区 32K 字，块大小 1 字，行数 = 32K。</span></li><li id="uc001f501" data-lake-index-type="0"><strong><span class="ne-text">计算地址划分（全相联）：</span></strong><span class="ne-text"> 全相联映射没有 Index（组/行索引），主存块可以放在任意行。</span></li></ol><ul class="ne-list-wrap"><ul ne-level="1" class="ne-ul"><li id="u3e5e813f" data-lake-index-type="0"><span class="ne-text">Offset = 2 位（块大小 4B）。</span></li><li id="ue49cff00" data-lake-index-type="0"><span class="ne-text">Tag = 总地址位 - Offset位 = </span><span id="dp3pg" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/1a702cc8c49f728b800dd2dc091e3c79.svg"></span><span class="ne-text"> 位。</span></li></ul></ul><ol start="3" class="ne-ol"><li id="udeca7492" data-lake-index-type="0"><strong><span class="ne-text">确定控制位：</span></strong></li></ol><ul class="ne-list-wrap"><ul ne-level="1" class="ne-ul"><li id="u2df95885" data-lake-index-type="0"><span class="ne-text">Valid位：1 位。</span></li><li id="u7750b91b" data-lake-index-type="0"><span class="ne-text">Dirty位：1 位（回写方式）。</span></li><li id="u0eab2a08" data-lake-index-type="0"><span class="ne-text">替换策略位：题目采用</span><strong><span class="ne-text">随机替换</span></strong><span class="ne-text">，无需替换策略位</span></li></ul></ul><ol start="4" class="ne-ol"><li id="ud2c21239" data-lake-index-type="0"><strong><span class="ne-text">计算总容量：</span></strong></li></ol><ul class="ne-list-wrap"><ul ne-level="1" class="ne-ul"><li id="ubdc8f6b4" data-lake-index-type="0"><span class="ne-text">每行位数 = 数据位 + Tag位 + Valid位 + Dirty位 = </span><span id="AJNcq" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/391195ec5a0c54cebdf984ce4f338ee2.svg"></span><span class="ne-text"> 位。</span></li><li id="ua5d62b27" data-lake-index-type="0"><span class="ne-text">总容量 = </span><span id="AeyUa" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/cd9df869412a3e6112c4096815c337a1.svg"></span><span class="ne-text"> 位。</span></li></ul></ul></details>
14. **（袁书习题）假定主存按字节编址，cache 共有 64 行，采用直接映射方式，主存块大小为 32B，所有编号都从 0 开始。问主存第 2593 号单元所在主存块对应的 cache 行号是（ ）。**  
A. 1  
B. 17  
C. 34  
D. 81

<details class="lake-collapse"><summary id="u6905a6e8"><span class="ne-text">解析</span></summary><h4 id="JnY0t"><strong><span class="ne-text">答案：B</span></strong></h4><p id="u3ac84f12" class="ne-p"><strong><span class="ne-text">解析：</span></strong></p><ol class="ne-ol"><li id="ub48f00a4" data-lake-index-type="0"><strong><span class="ne-text">计算主存块号：</span></strong><span class="ne-text"> 主存地址 2593，块大小 32B。</span></li></ol><ul class="ne-list-wrap"><ul ne-level="1" class="ne-ul"><li id="uf45fcf7e" data-lake-index-type="0"><span class="ne-text">主存块号 = </span><span id="qlS0j" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/a031a6d49252e1dd15aca21faece81e9.svg"></span><span class="ne-text">。</span></li></ul></ul><ol start="2" class="ne-ol"><li id="u118b1599" data-lake-index-type="0"><strong><span class="ne-text">计算 Cache 行号（直接映射）：</span></strong></li></ol><ul class="ne-list-wrap"><ul ne-level="1" class="ne-ul"><li id="ua3b7295c" data-lake-index-type="0"><span class="ne-text">公式：Cache行号 = 主存块号 mod Cache行数。</span></li><li id="ud40f70bc" data-lake-index-type="0"><span class="ne-text">Cache行数 = 64。</span></li><li id="udeb19d4d" data-lake-index-type="0"><span class="ne-text">行号 = </span><span id="X6Gjd" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/44ba04f09a0cba635234d0cd1f740ea9.svg"></span><span class="ne-text">。</span></li></ul></ul></details>
15. **（袁书习题）假定主存按字节编址，cache 共有 64 行，采用 4 路组相联映射方式，主存块大小为 32B，所有编号都从 0 开始。问主存第 2593 号单元所在主存块对应的 cache 组号是（ ）。**  
A. 1  
B. 17  
C. 34  
D. 81

<details class="lake-collapse"><summary id="u4a39a3e9"><span class="ne-text">解析</span></summary><p id="uee5d4502" class="ne-p"><strong><span class="ne-text">答案：A</span></strong></p><p id="u76089f63" class="ne-p"><strong><span class="ne-text">解析：</span></strong></p><ol class="ne-ol"><li id="u90161b3d" data-lake-index-type="0"><strong><span class="ne-text">计算主存块号：</span></strong><span class="ne-text"> 同上，主存块号 = 81。</span></li><li id="ufdf0613f" data-lake-index-type="0"><strong><span class="ne-text">计算 Cache 组数（组相联）：</span></strong></li></ol><ul class="ne-list-wrap"><ul ne-level="1" class="ne-ul"><li id="u1c514d30" data-lake-index-type="0"><span class="ne-text">Cache 总行数 = 64，路数 = 4。</span></li><li id="udf651a9b" data-lake-index-type="0"><span class="ne-text">组数 = 总行数 / 路数 = </span><span id="mUgfM" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/aaee2d3e03e4374de263a18874e52bb3.svg"></span><span class="ne-text"> 组。</span></li></ul></ul><ol start="3" class="ne-ol"><li id="ub7e78a0e" data-lake-index-type="0"><strong><span class="ne-text">计算 Cache 组号：</span></strong></li></ol><ul class="ne-list-wrap"><ul ne-level="1" class="ne-ul"><li id="uffe7b4f7" data-lake-index-type="0"><span class="ne-text">公式：Cache组号 = 主存块号 mod Cache组数。</span></li><li id="u30060338" data-lake-index-type="0"><span class="ne-text">组号 = </span><span id="cHGqs" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/2d82ce07ef8e823920df86e03ccb2b48.svg"></span><span class="ne-text">。</span></li></ul></ul></details>


16. 【2010-44】（12分）某计算机的主存地址空间大小为256MB，按字节编址，指令Cache和数据Cache分离，均有8个Cache行，每个Cache行大小为64B，数据Cache采用直接映射方式。现有两个功能相同的程序A和B，其伪代码如下所示：

```c
int a[256][256]
...
int sum_array1()
{
    int i, j, sum=0;
    for (i=0; i<256; i++)
        for (j=0; j<256; j++)
            sum += a[i][j]
    return sum;
}
```

```c
int a[256][256]
...
int sum_array1()
{
    int i, j, sum=0;
    for (j=0; j<256; j++)
        for (i=0; i<256; i++)
            sum += a[i][j]
    return sum;
}
```

假定int类型数据用32位补码表示，程序编译时i、j、sum均分配在寄存器中，数组a按行优先方式存放，首地址320（十进制数）。请回答下列问题，要求说明理由或给出计算过程。

(1) 若不考虑用于Cache一致性维护和替换算法的控制位,则数据Cache的总容量为多少？

(2) 数组数据a[0][31]和a[1][1]各自所在的主存块对应的Cache行号分别是多少（Cache行号从0开始）？

(3) 程序A和B的数据访问命中率各是多少？哪个程序的执行时间更短？

<details class="lake-collapse"><summary id="ue6bb3d1f"><span class="ne-text">解析</span></summary><p id="u92a6bdc5" class="ne-p"><span class="ne-text">基本参数</span></p><ul class="ne-ul"><li id="uf7432828" data-lake-index-type="0"><span class="ne-text">主存地址空间 = 256MB = 2²⁸ 字节 → </span><strong><span class="ne-text">28 位地址</span></strong></li><li id="ubb5b70dc" data-lake-index-type="0"><span class="ne-text">数据 Cache：8 行，每行 64B，</span><strong><span class="ne-text">直接映射</span></strong></li><li id="u4829d12c" data-lake-index-type="0"><span class="ne-text">int 型 = 4B，int a[256][256]，行优先存放，首地址 = 320（十进制）</span></li></ul><p id="udb1b5ad2" class="ne-p"><span class="ne-text">(1) 地址分配：</span></p><ul class="ne-ul"><li id="ud9f7cc78" data-lake-index-type="0"><span class="ne-text">块内偏移 = log₂(64) = </span><strong><span class="ne-text">6 位</span></strong></li><li id="u1ef8bf26" data-lake-index-type="0"><span class="ne-text">行索引 = log₂(8) = </span><strong><span class="ne-text">3 位</span></strong></li><li id="u755789d2" data-lake-index-type="0"><span class="ne-text">标记 = 28 − 6 − 3 = </span><strong><span class="ne-text">19 位</span></strong></li></ul><p id="uc8cee5b3" class="ne-p"><span class="ne-text">不考虑一致性维护和替换算法控制位（包括脏位、LRU 位），但计入有效位：</span></p><ul class="ne-ul"><li id="u6fc965b6" data-lake-index-type="0"><span class="ne-text">每行 = 有效位(1) + 标记(19) + 数据(64×8=512) = </span><strong><span class="ne-text">532 位</span></strong></li><li id="ua9337aef" data-lake-index-type="0"><strong><span class="ne-text">总容量 = 8 × 532 = 4256 位（即 532B 数据区 + 标记区）</span></strong></li></ul><p id="u4b7f9d68" class="ne-p"><span class="ne-text">(2) </span><strong><span class="ne-text">a[0][31]：</span></strong></p><ul class="ne-ul"><li id="u30ad21bf" data-lake-index-type="0"><span class="ne-text">距首地址偏移 = (0×256 + 31) × 4 = 124 字节</span></li><li id="ub82b68f0" data-lake-index-type="0"><span class="ne-text">绝对地址 = 320 + 124 = </span><strong><span class="ne-text">444</span></strong></li><li id="u078a52f1" data-lake-index-type="0"><span class="ne-text">主存块号 = ⌊444 / 64⌋ = </span><strong><span class="ne-text">6</span></strong></li><li id="u9b03e9ff" data-lake-index-type="0"><span class="ne-text">Cache 行号 = 6 mod 8 = </span><strong><span class="ne-text">6</span></strong></li></ul><p id="u6f10f97d" class="ne-p"><strong><span class="ne-text">或者</span></strong><span id="DtlHC" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/75b573efcbf5b1178a739eb98e858e1f.svg"></span><strong><span class="ne-text">，</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">行号为110B=6。</span></p><p id="u33d04d53" class="ne-p"><strong><span class="ne-text">a[1][1]：</span></strong></p><ul class="ne-ul"><li id="u245c140e" data-lake-index-type="0"><span class="ne-text">距首地址偏移 = (1×256 + 1) × 4 = 257 × 4 = 1028 字节</span></li><li id="uafcda9c4" data-lake-index-type="0"><span class="ne-text">绝对地址 = 320 + 1028 = </span><strong><span class="ne-text">1348</span></strong></li><li id="ud66037c4" data-lake-index-type="0"><span class="ne-text">主存块号 = ⌊1348 / 64⌋ = </span><strong><span class="ne-text">21</span></strong></li><li id="u625426b2" data-lake-index-type="0"><span class="ne-text">Cache 行号 = 21 mod 8 = </span><strong><span class="ne-text">5</span></strong></li></ul><p id="u853bce0b" class="ne-p"><strong><span class="ne-text">或者</span></strong><span id="xn6hc" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/1d717cf523f0bb223c80f3586bd79f9a.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)">，行号为101B=5</span></p><p id="u5cde6625" class="ne-p"><span class="ne-text">(3)</span><strong><span class="ne-text">程序 A（按行访问，i 为外循环，j 为内循环）：</span></strong></p><ul class="ne-ul"><li id="ud65e34ef" data-lake-index-type="0"><span class="ne-text">C 语言数组按行优先存储，程序 A 访问顺序：a[0][0], a[0][1], ..., a[0][255], a[1][0], ... → </span><strong><span class="ne-text">顺序访问，空间局部性好</span></strong></li><li id="u6fae439a" data-lake-index-type="0"><span class="ne-text">每块 64B / 4B = </span><strong><span class="ne-text">16 个 int</span></strong></li><li id="u7fbb6fac" data-lake-index-type="0"><span class="ne-text">每 16 次访问，第 1 次缺失，后 15 次命中</span></li><li id="u8284603e" data-lake-index-type="0"><span class="ne-text">总访问次数 = 256 × 256 = 65536</span></li><li id="u747acfab" data-lake-index-type="0"><span class="ne-text">缺失次数 = 65536 / 16 = 4096</span></li><li id="u82d467ed" data-lake-index-type="0"><strong><span class="ne-text">程序 A 命中率 = (65536 − 4096) / 65536 = 61440 / 65536 ≈ 93.75%</span></strong></li></ul><p id="ud472dc62" class="ne-p"><strong><span class="ne-text">程序 B（按列访问，j 为外循环，i 为内循环）：</span></strong></p><ul class="ne-ul"><li id="u66547297" data-lake-index-type="0"><span class="ne-text">访问顺序：a[0][0], a[1][0], a[2][0], ... → 相邻两次访问之间跨度 = 256×4 = </span><strong><span class="ne-text">1024 字节 = 16 块</span></strong></li><li id="uf170a15b" data-lake-index-type="0"><span class="ne-text">8 行 Cache：16 mod 8 = 0 → a[i][j] 与 a[i+1][j] 映射到</span><strong><span class="ne-text">同一 Cache 行</span></strong><span class="ne-text">，产生冲突缺失</span></li><li id="ucf2ac2a7" data-lake-index-type="0"><span class="ne-text">每次访问都会将上一次加载的块淘汰</span></li><li id="ue81ec642" data-lake-index-type="0"><strong><span class="ne-text">程序 B 命中率 ≈ 0%</span></strong></li></ul><p id="udfec07fb" class="ne-p"><strong><span class="ne-text">结论：程序 A 命中率远高于程序 B（93.75% vs 0%），程序 A 执行时间更短。</span></strong></p></details>






10. 【2014-45】（12分）假设对于计算机M和程序段P的机器代码，M采用页式虚拟存储管理；P开始执行时，(R1)=(R2)=0，(R6)=1000，其机器代码已调入主存但不在Cache中；数组A未调入主存，且所有数组元素在同一页，并存储在磁盘同一个扇区。请回答下列问题并说明理由。  
$ \begin{array}{cccccc} \text{编号}&\text{地址}&\text{机器代码}&\text{汇编代码}&\text{注释}\\\hline 1&\text{08048100H}&\text{00022080H}&\text{loop: sll R4, R2, 2}&\text{(R2)<<2→R4}\\ 2&\text{08048104H}&\text{00083020H}&\text{add R4, R4, R3}&\text{(R4)+(R3)→R4}\\ 3&\text{08048108H}&\text{8C850000H}&\text{load R5, 0(R4)}&\text{((R4)+0)→R5}\\ 4&\text{0804810CH}&\text{00250820H}&\text{add R1, R1, R5}&\text{(R1)+(R5)→R1}\\ 5&\text{08048110H}&\text{20420001H}&\text{add R2, R2, 1}&\text{(R2)+1→R2}\\ 6&\text{08048114H}&\text{1446FFFAH}&\text{bne R2, R6, loop}&\text{if (R2)!=(R6) goto loop}\\ \end{array} $

(1) P执行结束时，R2的内容是多少？

(2) M的指令Cache和数据Cache分离。若指令Cache共有16行，Cache和主存交换的块大小为32字节，则其数据区的容量是多少？若仅考虑程序段P的执行，则指令Cache的命中率为多少？

(3) P在执行过程中，哪条指令的执行可能发生溢出异常？哪条指令的执行可能产生缺页异常？对于数组A的访问，需要读磁盘和TLB至少各多少次？







11. 【2020-44】（10分）假定主存地址为32位，按字节编址，指令Cache和数据Cache与主存之间均采用8路组相联映射方式，直写（WriteThrough）写策略和LRU替换算法，主存块大小为64B，数据区容量各为32KB。开始时Cache均为空。请回答下列问题。

(1) Cache每一行中标记（Tag）、LRU位各占几位？是否有修改位？

(2) 有如下C语言程序段：

```c
 for(k = 0; k < 1024; k++)
     s[k] = 2 * s[k];
```

若数组s及其变量k均为int型，int型数据占4B，变量k分配在寄存器中，数组s在主存中的起始地址为008000C0H，则该程序段执行过程中，访问数组s的数据Cache缺失次数为多少？

(3) 若CPU最先开始的访问操作是读取主存单元00010003H中的指令，简要说明从Cache中访问该指令的过程，包括Cache缺失处理过程。

<details class="lake-collapse"><summary id="ud3ccf37f"><span class="ne-text">解析</span></summary><p id="u143f486a" class="ne-p"><span class="ne-text">基本</span><strong><span class="ne-text">参数</span></strong></p><ul class="ne-ul"><li id="ub83124c2" data-lake-index-type="0"><span class="ne-text">主存地址 = 32 位，按字节编址</span></li><li id="u61fdbfb6" data-lake-index-type="0"><span class="ne-text">指令/数据 Cache：8 路组相联，直写，LRU 替换</span></li><li id="u2381a136" data-lake-index-type="0"><span class="ne-text">块大小 = 64B，数据区各 32KB，初始为空</span></li></ul><p id="uc0c4ddd3" class="ne-p"><strong><span class="ne-text">(1) </span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">Cache采用8路组相联映射方式，组相联映射格式为</span><span id="FzSQL" class="ne-math" style="color: rgb(25, 27, 31)"><img src="https://cdn.nlark.com/yuque/__latex/b0c1e07d24d98cf793a1574cdfceebfc.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></p><ul class="ne-ul"><li id="ud17d40fb" data-lake-index-type="0"><span class="ne-text">组数 = (32KB / 64B) / 8 = 64 组</span></li><li id="ud77925c4" data-lake-index-type="0"><span class="ne-text">块内偏移 = log₂(64) = </span><strong><span class="ne-text">6 位</span></strong></li><li id="u6bb0989a" data-lake-index-type="0"><span class="ne-text">组索引 = log₂(64) = </span><strong><span class="ne-text">6 位</span></strong></li><li id="u546e5f11" data-lake-index-type="0"><strong><span class="ne-text">Tag = 32 − 6 − 6 = 20 位</span></strong></li></ul><p id="ue1d62286" class="ne-p"><strong><span class="ne-text">LRU 位：</span></strong></p><ul class="ne-ul"><li id="uf1d6fcf0" data-lake-index-type="0"><span class="ne-text">8 路 LRU 需对每路维护访问顺序计数，每路需 log₂(8) = </span><strong><span class="ne-text">3 位</span></strong></li><li id="uf5328beb" data-lake-index-type="0"><span class="ne-text">每个 Cache 行的 LRU 位 = </span><strong><span class="ne-text">3 位</span></strong></li></ul><p id="u5fbbab03" class="ne-p"><strong><span class="ne-text">修改位（脏位）：</span></strong></p><ul class="ne-ul"><li id="ued894774" data-lake-index-type="0"><span class="ne-text">采用</span><strong><span class="ne-text">直写策略</span></strong><span class="ne-text">，写操作同时写 Cache 和主存，Cache 内容始终与主存一致</span></li><li id="u2da0ed22" data-lake-index-type="0"><strong><span class="ne-text">无需修改位（没有脏位）</span></strong></li></ul><p id="u86fdd7e5" class="ne-p"><strong><span class="ne-text"></span></strong></p><p id="udea3cf13" class="ne-p"><span class="ne-text">(2)int = 4B，数组 s 起始地址 = 008000C0H</span><span class="ne-text" style="color: rgb(25, 27, 31)">= </span><span id="yo75K" class="ne-math" style="color: rgb(25, 27, 31)"><img src="https://cdn.nlark.com/yuque/__latex/ecee82148ee43d46320cc957069b936c.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)"> ，块内地址为000000B=0，所以</span><strong><span class="ne-text" style="color: rgb(25, 27, 31)">s位于一个主存块开始处</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">；</span></p><ul class="ne-ul"><li id="u1acfb99e" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">需要访问1024个数组元素，</span><span class="ne-text">1024 × 4B = 4096B，共 4096/64 = </span><strong><span class="ne-text">64 块；</span></strong></li></ul><p id="u3e2cc50a" class="ne-p"><span class="ne-text">每次循环：读 s[k]（可能缺失） → 写 s[k]（直写，缺失已加载则命中）</span></p><ul class="ne-ul"><li id="u2e83975c" data-lake-index-type="0"><span class="ne-text">每块 64B / 4B = 16 个元素，</span><strong><span class="ne-text">第 1 次读缺失（冷缺失），随后 15 次读 + 16 次写均命中</span></strong></li><li id="uae3c3558" data-lake-index-type="0"><strong><span class="ne-text">总缺失次数 = 64 次</span></strong><span class="ne-text">（每块冷缺失一次）</span></li></ul><p id="u39a84ccd" class="ne-p"><span class="ne-text"></span></p><p id="u8fe04aa7" class="ne-p"><span class="ne-text">(3) 访问 00010003H 指令的过程（包括缺失处理）</span></p><ul class="ne-ul"><li id="uc2d2e510" data-lake-index-type="0"><span class="ne-text">地址：00010003H = </span><span id="Sc449" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/30d81ca12221c07b429d2babc4624745.svg"></span></li><li id="u7f9f9b70" data-lake-index-type="0"><span class="ne-text">块内偏移（[5:0]）= </span><code class="ne-code"><span class="ne-text">000011</span></code><span class="ne-text"> = </span><strong><span class="ne-text">3</span></strong></li><li id="ue01a2290" data-lake-index-type="0"><span class="ne-text">组索引（[11:6]）= </span><code class="ne-code"><span class="ne-text">000000</span></code><span class="ne-text"> = </span><strong><span class="ne-text">组 0</span></strong></li><li id="ue60787a9" data-lake-index-type="0"><span class="ne-text">标记（[31:12]）= </span><code class="ne-code"><span class="ne-text">00000000000000010000</span></code><span class="ne-text"> = </span><strong><span class="ne-text">0x10</span></strong></li></ul><p id="u607198a9" class="ne-p"><strong><span class="ne-text">访问过程：</span></strong></p><ol class="ne-ol"><li id="u44c6ca3f" data-lake-index-type="0"><span class="ne-text">CPU 发出地址 00010003H，分解得 Tag=0x10，Set=0，Offset=3。</span></li><li id="uda9f2813" data-lake-index-type="0"><span class="ne-text">访问指令 Cache 第 0 组：Cache 初始为空，8 路均无效（Valid=0）→ </span><strong><span class="ne-text">Cache 缺失</span></strong><span class="ne-text">。</span></li><li id="uc3d0d7b8" data-lake-index-type="0"><strong><span class="ne-text">缺失处理：</span></strong></li></ol><ul class="ne-list-wrap"><ul ne-level="1" class="ne-ul"><li id="ud496784b" data-lake-index-type="0"><span class="ne-text">该地址所在主存块起始地址</span><strong><span class="ne-text">00010000H，</span></strong><span class="ne-text">向主存发请求，读取 00010000H ~ 0001003FH 共 64 字节的数据块。</span></li><li id="ueb032091" data-lake-index-type="0"><span class="ne-text">将该数据块填入指令 Cache 组 0 的某一路，置 Valid=1，Tag=0x10，同时更新 LRU 信息。</span></li></ul></ul><ol start="4" class="ne-ol"><li id="u9f15ddda" data-lake-index-type="0"><span class="ne-text">从填入的 Cache 行中，取偏移 3 处的字节（00010003H 处）开始读取 4 字节作为指令，送至 CPU。</span></li></ol></details>
