<!-- yuque:hnlngb/zxtsfqce5t4dkvdc book_id=48597829 doc_id=272034241 -->

# CISC与RISC

### CISC（复杂指令集计算机，Complex Instruction Set Computer）
#### 1. CISC 的核心理念与代表
CISC 的核心设计思路是通过增强原有指令的功能，设置更为复杂的新指令来实现特定的操作 。它期望**<font style="color:#DF2A3F;">用一条硬件指令来完成复杂的任务</font>**<font style="color:#DF2A3F;">。</font>

> **典型代表**：我们日常使用的 **x86 架构**计算机，例如 Intel 的 Core i5、i7、i9 系列以及 AMD 的 Ryzen 系列处理器，都是典型的 CISC 架构 。
>

#### 2. CISC 是如何演变而来的？
早期计算机面临着“软件危机”：硬件集成电路技术飞速发展使得硬件成本不断下降，但软件的复杂度激增，开发成本不断上升 。为了解决这个问题，设计者们不断向指令系统中添加新指令，主要出于以下需求：

+ **弥补“语义鸿沟”**：增加**语义上更接近高级语言的指令**，这样就能简化编译器的设计，提高编译效率，让软件开发更容易 
+ **向后兼容性**：为了让以前的软件能无缝运行在新机器上，**同一系列的新型和高档计算机只能扩充新指令**，绝对不能删减老指令，导致指令集像滚雪球一样越来越大 。

#### 3. CISC 的核心特征 
+ **指令库极其庞大**：指令数目非常多，一般都在200条以上，甚至多达数百条 。
+ **格式复杂，字长不固定**：指令的长度是不固定的，为了在有限的长度内实现各种功能，设计了**非常多的指令格式和寻址方式**（如基址寻址、相对寻址等） 。
+ **访存极其自由**：不仅是专门的存取指令，**<u><font style="color:#DF2A3F;">CISC 对可以访问主存的指令不加限制，很多运算指令可以直接在内存数据上进行操作 。</font></u>**
+ **<font style="color:#DF2A3F;">微程序控制</font>****为主**：因为指令太复杂，很难用纯硬件逻辑电路直接接线实现，所以**<font style="color:#DF2A3F;">绝大多数 CISC 采用微程序控制器</font>**。这种控制器的控制存储器往往要占据整个 CPU 芯片面积的 50% 以上 。
+ **执行时间参差不齐**：**不同指令的执行时间相差极大**，大多数复杂指令需要多个时钟周期才能完成，这让流水线设计变得非常困难，也难以进行编译优化 。

#### 4. CISC 面临的挑战与“二八定律”
尽管功能极其强大，但人们后来对传统 CISC 程序的运行情况进行了测试，发现了一个惊人的“80-20规律”：

+ 典型的程序在运行中，**大约 80% 的时间仅仅反复使用了指令集中最简单的 20% 的指令 **。
+ 而花费巨大精力设计的剩下 80% 的复杂指令，在程序运行中却极少被用到（约占20%） 。

> 虽然从硬件执行效率和面积利用率上看，RISC（精简指令集）显得更科学，但 CISC 依然不可替代。因为早期绝大部分软件都是基于 CISC 开发的，CISC 在软件兼容性上有着无与伦比的优势，这也是 Intel 至今能在 PC 领域“一统江湖”的关键原因 。
>
> 有趣的是，现代的 CISC 结构 CPU 其实早已不再是纯粹的 CISC，它们在内部大量融合了 RISC 的技术成分（例如在微架构层面将复杂的 CISC 指令打碎成简单的微操作来执行），两者的性能差距正在逐渐缩小 。
>



有了前面 CISC 的基础，理解 RISC（精简指令集计算机，Reduced Instruction Set Computer）就会有一种“豁然开朗”的感觉。**如果说 CISC 是做加法，那么 RISC 就是在做极致的减法。**

### RISC（精简指令集计算机，Reduced Instruction Set Computer）
####  诞生的契机：打破“80-20规律”
正如我们在 CISC 中提到的，设计者对传统程序的测试发现了一个惊人的事实：程序运行中大约 80% 的时间只用到了 20% 最简单的指令 。RISC 正是基于这一规律诞生的：既然 80% 的复杂指令极少被使用，为什么不干脆把它们去掉？

**核心思路**：**<u><font style="color:#DF2A3F;">只保留那些使用频率最高、最简单的指令，遇到复杂的功能，就通过组合这些常用的简单指令来实现 </font></u>**<u>。</u>

#### RISC 的核心特征 
+ **严格的 LOAD/STORE 架构**：这是极其重要的一点。因为访问内存非常慢，在 RISC 中，**<u><font style="color:#DF2A3F;">只有取数（LOAD）和存数（STORE）指令被允许访问主</font></u>**存 。所有其他的运算操作都必须在 CPU 的寄存器之间进行 。
+ **面向通用寄存器的结构**：既然运算只能在寄存器里做，为了减少频繁访问慢速的主存，RISC 内部配备了数量相当庞大的通用寄存器 。
+ **指令“长相”高度统一**：**指令长度是固定的，指令格式和寻址方式的种类都非常少 **。这大大简化了 CPU 内部译码逻辑的设计
+ **<font style="color:#DF2A3F;">硬布线控制</font>****为主**：因为指令简单规整，不再需要 CISC 那种庞大复杂的微程序控制器，可以直接用**<font style="color:#DF2A3F;">组合逻辑电路（硬布线）</font>**来实现控制部件 。这种硬布线逻辑通常只占 CPU 芯片面积的 10% 左右（而 CISC 的微程序控制往往占 50% 以上），不仅大大提升了速度，还节省了芯片空间 。
+ **流水线的绝对依赖**：绝大多数 RISC 指令极其简单，因此可以完美适配“指令流水线”技术，使得**<u><font style="color:#DF2A3F;">大部分指令都能在一个时钟周期内完成</font></u>**，极大地提高了运算速度 。
+ **极其重视编译优化**：一个在 CISC 上只需一条复杂指令就能完成的操作，在 RISC 上可能需要被拆解成好几条简单指令的组合 。因此，RISC 特别**依赖聪明的“编译器”来选择有效的指令、调整指令顺序**，以保证最终生成的目标代码执行高效 。
+ **兼容性包袱**：由于指令被大刀阔斧地精简，指令条数少且格式不同于老机器，**<u><font style="color:#DF2A3F;">大多数 RISC 计算机无法像 CISC 那样对老款机器的软件做到向下兼容 。</font></u>**

> **典型代表**：我们智能手机和嵌入式设备里几乎 100% 使用的 **ARM** 架构，以及经典的 **MIPS** 和近年来非常火爆的开源架构 **RISC-V**，都是典型的 RISC 计算机 。
>

****

****

**走向融合**：从实用性和结构合理性来看，RISC 代表了处理器更高的效率 。虽然 Intel 靠着 CISC 和庞大的历史软件生态赢得了 PC 时代，但现代的 CISC 处理器其实已经大量融合了 RISC 的成分，两者的性能差距正在缩小 。

**两者的哲学区别：**  
CISC 是“重剑无锋”，试图用强大的硬件（复杂指令）替软件分担工作；  
RISC 是“天下武功唯快不破”，用最轻快的硬件（简单指令+流水线）把复杂的逻辑推给软件（编译器）去处理。



### CISC 与 RISC 的对比
| **<font style="color:rgb(31, 31, 31);">对比项目</font>** | **<font style="color:rgb(31, 31, 31);">CISC (复杂指令集计算机)</font>** | **<font style="color:rgb(31, 31, 31);">RISC (精简指令集计算机)</font>** |
| :---: | :---: | :---: |
| **<font style="color:rgb(31, 31, 31);">指令系统</font>** | <font style="color:rgb(31, 31, 31);">复杂、庞大 </font> | <font style="color:rgb(31, 31, 31);">简单，精简 </font> |
| **<font style="color:rgb(31, 31, 31);">指令数目</font>** | <font style="color:rgb(31, 31, 31);">一般大于 200 条 </font> | <font style="color:rgb(31, 31, 31);">一般小于 100 条 </font> |
| **<font style="color:rgb(31, 31, 31);">指令字长</font>** | <font style="color:rgb(31, 31, 31);">不固定 </font> | <font style="color:rgb(31, 31, 31);">定长 </font> |
| **<font style="color:rgb(31, 31, 31);">可访存指令</font>** | <font style="color:rgb(31, 31, 31);">不加限制 </font> | <font style="color:rgb(31, 31, 31);">只有 LOAD/STORE 指令可以访存 </font> |
| **<font style="color:rgb(31, 31, 31);">各种指令执行时间</font>** | <font style="color:rgb(31, 31, 31);">相差较大 </font> | <font style="color:rgb(31, 31, 31);">绝大多数在一个周期内完成 </font> |
| **<font style="color:rgb(31, 31, 31);">各种指令使用频度</font>** | <font style="color:rgb(31, 31, 31);">相差很大 </font> | <font style="color:rgb(31, 31, 31);">都比较常用 </font> |
| **<font style="color:rgb(31, 31, 31);">通用寄存器数量</font>** | <font style="color:rgb(31, 31, 31);">较少 </font> | <font style="color:rgb(31, 31, 31);">多 </font> |
| **<font style="color:rgb(31, 31, 31);">控制方式</font>** | <font style="color:rgb(31, 31, 31);">绝大多数为</font>**<font style="color:rgb(31, 31, 31);">微程序控制</font>**<font style="color:rgb(31, 31, 31);"> </font> | <font style="color:rgb(31, 31, 31);">绝大多数为组</font>**<font style="color:rgb(31, 31, 31);">合逻辑控制 (硬布线)</font>**<font style="color:rgb(31, 31, 31);"> </font> |
| **<font style="color:rgb(31, 31, 31);">目标代码与编译优化</font>** | <font style="color:rgb(31, 31, 31);">难以用优化编译生成高效的目标代码程序 </font> | <font style="color:rgb(31, 31, 31);">采用优化的编译程序，生成代码较为高效 </font> |


1. 【2009-17】下列关于RISC的叙述中，错误的是（ ）。

A. RISC普遍采用微程序控制器

B. RISC大多数指令在一个时钟周期内完成

C. RISC的内部通用寄存器数量相对CISC多

D. RISC的指令数、寻址方式和指令格式种类相对CISC少

<details class="lake-collapse"><summary id="u393d64f9"><span class="ne-text">解析</span></summary><p id="ue2c17b4c" class="ne-p"><strong><span class="ne-text">答案：A. RISC普遍采用微程序控制器</span></strong><span class="ne-text"><br /></span><span class="ne-text">这是一道概念题，需要找出错误的叙述。</span></p><ul class="ne-ul"><li id="u2cb155b8" data-lake-index-type="0"><strong><span class="ne-text">A选项错误</span></strong><span class="ne-text">：RISC（精简指令集计算机）的特点是指令简单且规整，因此其控制器</span><strong><span class="ne-text">普遍采用硬布线控制器（组合逻辑控制器）</span></strong><strong><span class="ne-text">以追求极致的执行速度；而 CISC（复杂指令集计算机）因为指令复杂、寻址方式多，才普遍采用</span></strong><strong><span class="ne-text">微程序控制器</span></strong><span class="ne-text">。</span></li><li id="u2b13831c" data-lake-index-type="0"><strong><span class="ne-text">B选项正确</span></strong><span class="ne-text">：RISC 指令简单，绝大多数指令可以在一个时钟周期内（单周期）执行完毕，常常结合流水线技术。</span></li><li id="u5ee8e60c" data-lake-index-type="0"><strong><span class="ne-text">C选项正确</span></strong><span class="ne-text">：为了减少访存次数（只有 Load/Store 指令能访问内存），RISC 架构内部会配置大量的通用寄存器。</span></li><li id="ua82a92ed" data-lake-index-type="0"><strong><span class="ne-text">D选项正确</span></strong><span class="ne-text">：RISC 的核心思想就是“精简”，保留最常用的基本指令，寻址方式和指令格式种类都比 CISC 少很多。</span></li></ul></details>
---

2. **<font style="color:rgb(31, 31, 31);">（袁书习题）下列有关 RISC 特征的描述中，错误的是（  ）。  
</font>**<font style="color:rgb(31, 31, 31);">A. 指令格式规整，寻址方式少  
</font><font style="color:rgb(31, 31, 31);">B. 采用硬连线控制和指令流水线  
</font><font style="color:rgb(31, 31, 31);">C. 配置的通用寄存器数目不多  
</font><font style="color:rgb(31, 31, 31);">D. 运算类指令的操作数不访存</font>

<details class="lake-collapse"><summary id="u6e4aebfa"><span class="ne-text" style="color: rgb(31, 31, 31)">解析</span></summary><p id="uaecb0856" class="ne-p"><strong><span class="ne-text" style="color: rgb(31, 31, 31)">答案：C</span></strong></p><p id="uabffd4ad" class="ne-p"><strong><span class="ne-text" style="color: rgb(31, 31, 31)">选项A：指令格式规整，寻址方式少：</span></strong><span class="ne-text" style="color: rgb(31, 31, 31)">RISC的设计目标是简化指令系统，因此指令长度固定、格式规整，且寻址方式种类少（通常仅支持寄存器寻址、立即数寻址等少数方式），以降低译码复杂度。→ </span><span class="ne-text">A描述正确，不是错误选项</span><span class="ne-text" style="color: rgb(31, 31, 31)">。</span></p><p id="u17c670f3" class="ne-p"><strong><span class="ne-text" style="color: rgb(31, 31, 31)">选项B：采用硬连线控制和指令流水线</span></strong><span class="ne-text" style="color: rgb(31, 31, 31)">：RISC指令格式规整、操作简单，非常适合用</span><span class="ne-text">硬连线控制</span><span class="ne-text" style="color: rgb(31, 31, 31)">（组合逻辑控制）实现，相比微程序控制速度更快；同时，RISC天然支持</span><span class="ne-text">指令流水线</span><span class="ne-text" style="color: rgb(31, 31, 31)">，通过重叠执行指令大幅提升执行效率。→ </span><span class="ne-text">B描述正确，不是错误选项</span><span class="ne-text" style="color: rgb(31, 31, 31)">。</span></p><p id="u4e5f47d9" class="ne-p"><strong><span class="ne-text" style="color: rgb(31, 31, 31)">选项C：配置的通用寄存器数目不多：</span></strong><span class="ne-text" style="color: rgb(31, 31, 31)">RISC的核心设计思想之一是“</span><strong><span class="ne-text" style="color: rgb(31, 31, 31)">以寄存器为中心</span></strong><span class="ne-text" style="color: rgb(31, 31, 31)">”，通过配置</span><span class="ne-text">大量通用寄存器</span><span class="ne-text" style="color: rgb(31, 31, 31)">（通常几十到上百个），让绝大多数操作在寄存器之间完成，减少访存次数（访存速度远慢于寄存器）。因此“通用寄存器数目不多”是CISC（复杂指令集计算机）的特征，而非RISC。→ </span><span class="ne-text">C描述错误，是本题答案</span><span class="ne-text" style="color: rgb(31, 31, 31)">。</span></p><p id="ua6c876fd" class="ne-p"><strong><span class="ne-text" style="color: rgb(31, 31, 31)">选项D：运算类指令的操作数不访存</span></strong><span class="ne-text" style="color: rgb(31, 31, 31)">：RISC中，只有专门的</span><code class="ne-code"><span class="ne-text" style="color: rgb(31, 31, 31)">Load/Store</span></code><span class="ne-text" style="color: rgb(31, 31, 31)">指令可以访问存储器，运算类指令（如加减乘除）的操作数必须来自寄存器，运算结果也直接写回寄存器，不直接访问内存。这一设计大幅简化了运算指令的控制逻辑，也便于流水线实现。→ </span><span class="ne-text">D描述正确，不是错误选项</span><span class="ne-text" style="color: rgb(31, 31, 31)">。</span></p></details>
---

2. **<font style="color:rgb(31, 31, 31);">下列关于复杂指令系统计算机（CISC）的叙述中，错误的是（ ）。</font>**

<font style="color:rgb(31, 31, 31);">A. CISC的指令长度通常是不固定的，指令格式和寻址方式繁多</font>

<font style="color:rgb(31, 31, 31);">B. CISC严格限制只有LOAD/STORE（取数/存数）指令才能访问主存</font>

<font style="color:rgb(31, 31, 31);">C. CISC的各种指令执行时间相差很大，大多数指令需要多个时钟周期</font>

<font style="color:rgb(31, 31, 31);">D. CISC的控制器大多数采用微程序控制</font>

<details class="lake-collapse"><summary id="u41ffe526"><span class="ne-text">解析</span></summary><p id="u1d252bad" class="ne-p"><strong><span class="ne-text" style="color: rgb(31, 31, 31)">【答案】</span></strong><span class="ne-text" style="color: rgb(31, 31, 31)"> B</span></p><p id="ub771558f" class="ne-p"><strong><span class="ne-text" style="color: rgb(31, 31, 31)">选项A正确</span></strong><span class="ne-text" style="color: rgb(31, 31, 31)">：CISC为了在有限指令长度内实现更多功能，设计了众多格式和寻址方式，导致指令字长不固定 。</span></p><p id="u48244182" class="ne-p"><strong><span class="ne-text" style="color: rgb(31, 31, 31)">选项B错误</span></strong><span class="ne-text" style="color: rgb(31, 31, 31)">：这是RISC的典型特征。在RISC中，为了减少访问慢速主存，只有LOAD和STORE指令被允许访存 。而CISC对可以访存的指令是不加限制的 。</span></p><p id="u000bc7b0" class="ne-p"><strong><span class="ne-text" style="color: rgb(31, 31, 31)">选项C正确</span></strong><span class="ne-text" style="color: rgb(31, 31, 31)">：由于CISC指令功能复杂程度不一，其执行时间参差不齐，很多复杂指令无法在一个时钟周期内完成 。</span></p><p id="u6e907c8a" class="ne-p"><strong><span class="ne-text" style="color: rgb(31, 31, 31)">选项D正确</span></strong><span class="ne-text" style="color: rgb(31, 31, 31)">：CISC指令系统过于复杂，难以用纯组合逻辑电路直接接线实现，因此绝大多数采用微程序控制器 。</span></p></details>
---

3. **<font style="color:rgb(31, 31, 31);">下列关于精简指令系统计算机（RISC）特点的叙述中，错误的是（ ）。</font>**

<font style="color:rgb(31, 31, 31);">A. RISC的控制器以硬布线控制为主，能更充分地利用CPU芯片面积</font>

<font style="color:rgb(31, 31, 31);">B. RISC特别重视编译优化工作，以减少程序执行时间</font>

<font style="color:rgb(31, 31, 31);">C. 为了保证历史软件的运行，大多数RISC架构都能与老机器实现软件兼容</font>

<font style="color:rgb(31, 31, 31);">D. RISC选取使用频率最高的一些简单指令，复杂功能由简单指令组合实现</font>

<details class="lake-collapse"><summary id="u59fe2116"><span class="ne-text">解析</span></summary><p id="u65c7b1da" class="ne-p"><strong><span class="ne-text" style="color: rgb(31, 31, 31)">【答案】</span></strong><span class="ne-text" style="color: rgb(31, 31, 31)"> C</span></p><p id="u824e1b49" class="ne-p"><strong><span class="ne-text" style="color: rgb(31, 31, 31)">选项A正确</span></strong><span class="ne-text" style="color: rgb(31, 31, 31)">：RISC由于指令简单，大多采用硬布线（组合逻辑）控制，其逻辑电路只占CPU芯片面积的10%左右（相比之下CISC的微程序控制存储器占50%以上），因此能更好地利用芯片面积 。</span></p><p id="u89501463" class="ne-p"><strong><span class="ne-text" style="color: rgb(31, 31, 31)">选项B正确</span></strong><span class="ne-text" style="color: rgb(31, 31, 31)">：RISC把硬件简化了，因此将部分复杂操作推给了软件（编译器）。它特别依赖优化的编译程序来调整指令顺序和选择有效指令，从而生成高效的目标代码 。</span></p><p id="ua9f1134c" class="ne-p"><strong><span class="ne-text" style="color: rgb(31, 31, 31)">选项C错误</span></strong><span class="ne-text" style="color: rgb(31, 31, 31)">：CISC大多能实现软件兼容（高档机包含低档机全部指令） 。但RISC因为大刀阔斧地简化了指令系统，指令条数少且格式不同于老机器，因此大多数RISC计算机不能与老机器兼容 。</span></p><p id="uf70dbb88" class="ne-p"><strong><span class="ne-text" style="color: rgb(31, 31, 31)">选项D正确</span></strong><span class="ne-text" style="color: rgb(31, 31, 31)">：这是RISC诞生的基本理念，基于“80-20规律”，即用最常用的简单指令来重组实现那些不常用的复杂指令功能 。</span></p></details>
<font style="color:rgb(31, 31, 31);"></font>

