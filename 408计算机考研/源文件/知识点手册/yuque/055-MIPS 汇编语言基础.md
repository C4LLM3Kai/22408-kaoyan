<!-- yuque:hnlngb/tn00n0s4e133qean book_id=48597829 doc_id=274168028 -->

# MIPS 汇编语言基础

## MIPS 体系结构核心特点
+ **<font style="color:rgb(29, 29, 31);">体系结构</font>**<font style="color:rgb(29, 29, 31);">：RISC（精简指令集计算机），指令长度固定为 </font>**<font style="color:rgb(29, 29, 31);">32位</font>**<font style="color:rgb(29, 29, 31);">。</font>
+ **<font style="color:rgb(29, 29, 31);">存储编址</font>**<font style="color:rgb(29, 29, 31);">：按</font>**<font style="color:rgb(29, 29, 31);">字节</font>**<font style="color:rgb(29, 29, 31);">编址。</font>
+ **<font style="color:rgb(29, 29, 31);">数据存放</font>**<font style="color:rgb(29, 29, 31);">：采用</font>**<font style="color:rgb(29, 29, 31);">大端方式</font>**<font style="color:rgb(29, 29, 31);">，即高字节存放在低地址。</font>
+ **<font style="color:rgb(29, 29, 31);">对齐要求</font>**<font style="color:rgb(29, 29, 31);">：要求按</font>**<font style="color:rgb(29, 29, 31);">字边界对齐</font>**<font style="color:rgb(29, 29, 31);">，即字的地址必须是4的倍数。</font>
+ **<font style="color:rgb(29, 29, 31);">访存原则</font>**<font style="color:rgb(29, 29, 31);">：MIPS 是 </font>**<font style="color:#DF2A3F;">Load/Store </font>**<font style="color:rgb(29, 29, 31);">架构，只有 Load/Store 指令可以访问内存，</font>**<u><font style="color:#DF2A3F;">运算指令的操作数必须来自寄存器</font></u>**<font style="color:rgb(29, 29, 31);">。</font>

## MIPS 通用寄存器堆（共 32 个）
MIPS 提供了 32 个 32 位的通用寄存器，寄存器编号为 0~31（占 5 位）。在汇编中以 `$` 符号开头，可用名称或编号表示。

| 寄存器名称 | 寄存器编号 | 核心功能与 408 考点说明 | 过程调用保存规则 |
| :---: | :---: | :---: | :---: |
| `zero` | **0** | **恒为 0**。任何时候读都是 0，写入任何值都会被丢弃。常用于清零、求反或提供常数 0。 | - |
| `at` | 1 | 为**汇编程序保留**的临时寄存器（程序员不应直接使用）。 | - |
| `v0 ~ v1` | 2 ~ 3 | **过程调用返回值**（函数返回值存放处）。 | 调用者保存 (Caller-saved) |
| `**<font style="color:#DF2A3F;">a0 ~ a3</font>**` | 4 ~ 7 | **<font style="color:#DF2A3F;">过程调用参数</font>**（前4个函数入参存放处）。 | 调用者保存 (Caller-saved) |
| `t0 ~ t7` | **8 ~ 15** | **临时变量**。调用子程序时**无需保存**，可直接覆盖。 | 调用者保存 (Caller-saved) |
| `**<font style="color:#DF2A3F;">s0 ~ s7</font>**` | **16 ~ 23** | **<font style="color:#DF2A3F;">全局/保存变量</font>**。子程序中若要使用，**必须先压栈保存**，退出时恢复。 | 被调用者保存 (Callee-saved) |
| `t8 ~ t9` | 24 ~ 25 | 额外的临时变量，规则同 `t0~t7`。 | 调用者保存 (Caller-saved) |
| `k0 ~ k1` | 26 ~ 27 | 为 **OS 内核保留**，处理异常/中断时使用。 | - |
| `gp` | 28 | 全局指针（Global Pointer），指向静态全局数据区。 | - |
| `**<font style="color:#DF2A3F;">sp</font>**` | **29** | **<font style="color:#DF2A3F;">栈指针（Stack Pointer），指向当前栈顶。MIPS 栈通常向下（低地址）增长。</font>** | 被调用者保存 (Callee-saved) |
| `**<font style="color:#DF2A3F;">fp</font>**` | 30 | **<font style="color:#DF2A3F;">帧指针（Frame Pointer），指向当前栈帧的底部。</font>** | 被调用者保存 (Callee-saved) |
| `**<font style="color:#DF2A3F;">ra</font>**` | **31** | **<font style="color:#DF2A3F;">返回地址寄存器。执行 </font>**`jal`**<font style="color:#DF2A3F;">（过程调用）指令时自动保存下一条指令的地址；执行 </font>**`jr $ra`**<font style="color:#DF2A3F;"> 实现子程序返回。</font>** | 调用者保存 (Caller-saved) |


---

**<font style="color:#DF2A3F;">MIPS 三大指令格式与寻址方式</font>**

MIPS 指令长度均为 32 位，通过高 6 位的操作码（OP）来区分格式。

### R-型指令（Register-Register，寄存器-寄存器型）
主要用于算术、逻辑和移位运算。

+ **字段划分**：$ \begin{array}{|c|c|c|c|c|c|}
\hline
\text{OP (6位)} & \text{rs (5位)} & \text{rt (5位)} & \text{rd (5位)} & \text{shamt (5位)} & \text{func (6位)} \\
\hline
\end{array} $
+ **字段含义**：
+ `OP`：操作码，R-型指令的 OP 恒为 `000000`。
+ `func`：具体操作码（功能码），由于 OP 全为 0，实际由 `func` 决定执行什么运算（如 add, sub）。
+ `rs`：第一个源操作数寄存器编号。
+ `rt`：第二个源操作数寄存器编号。
+ `rd`：目的操作数寄存器编号（保存运算结果）。
+ `shamt`：移位量（Shift Amount），逻辑移位指令（如 `sll`, `srl`）中指定移位位数。非移位指令中该字段为 `0`。
+ **寻址方式**：**寄存器寻址**（操作数均来自 CPU 内部寄存器）。

### I-型指令（Immediate，立即数型）
主要用于双目立即数运算、访存指令（Load/Store）以及条件转移指令（Branch）。

+ **字段划分**：$ \begin{array}{|c|c|c|c|}
\hline
\text{OP (6位)} & \text{rs (5位)} & \text{rt (5位)} & \text{立即数 Immediate (16位)} \\
\hline
\end{array} $
+ **字段含义与应用场景**：
1. **双目运算类（如 **`andi`**, **`ori`**）**：将 `rs` 的内容与 16 位立即数（进行符号扩展或零扩展后）进行运算，结果送往 `rt`。
2. **访存指令（如 **`lw`**, **`sw`**）**：**基址寻址**。有效地址 $ EA = (rs) + \text{SignExt}(\text{立即数}) $。
+ `lw`：将内存 $ EA $ 处的数据加载到 `rt`。
+ `sw`：将 `rt` 中的数据存入内存 $ EA $ 处。
3. **条件转移指令（如 **`beq`**, **`bne`**）**：**相对寻址**。若条件成立，目标地址 = $ \text{当前 } PC \text{（或 } PC+4\text{）} + \text{符号扩展后的立即数} \times 4 $。
+ **寻址方式**：寄存器寻址、立即数寻址、基址寻址、相对寻址。

### 3. J-型指令（Jump，跳转型）
主要用于无条件全局跳转（如 `j`, `jal`）。

+ **字段划分**：$ \begin{array}{|c|c|}
\hline
\text{OP (6位)} & \text{直接地址 Target Address (26位)} \\
\hline
\end{array} $
+ **目标地址计算方法（常考）**：
    - 将指令中的 26 位直接地址**左移 2 位**（末尾补两个 `0`，因为指令按字对齐，地址最后两位必为 0），得到 28 位。
    - 拼接上**当前 PC（或下一条指令 PC）的高 4 位**，最终组合成一个 32 位的绝对目标地址。
    - 公式：$ \text{Target\_PC} = PC[31:28] \mathbin{\Vert} (\text{target} \ll 2) $

---

## 核心常用指令汇编详解
$ \def\arraystretch{1.5}
\begin{array}{|c|l|l|l|l|}
\hline
\text{类别} & \text{指令名称} & \text{汇编举例} & \text{含义} & \text{备注} \\
\hline
\text{算术} & \text{add} & \text{add \$s1, \$s2, \$s3} & \$s1 = \$s2 + \$s3 & \text{三个寄存器操作数} \\
\text{运算} & \text{subtract} & \text{sub \$s1, \$s2, \$s3} & \$s1 = \$s2 - \$s3 & \text{三个寄存器操作数} \\
\hline
\text{存储} & \text{load word} & \text{lw \$s1, 100(\$s2)} & \$s1 = \text{Memory}[\$s2 + 100] & \text{从内存取一个字到寄存器} \\
\text{访问} & \text{store word} & \text{sw \$s1, 100(\$s2)} & \text{Memory}[\$s2 + 100] = \$s1 & \text{从寄存器存一个字到内存} \\
\hline
& \text{and} & \text{and \$s1, \$s2, \$s3} & \$s1 = \$s2 \mathbin{\&} \$s3 & \text{三个寄存器操作数,按位与} \\
& \text{or} & \text{or \$s1, \$s2, \$s3} & \$s1 = \$s2 \mid \$s3 & \text{三个寄存器操作数,按位或} \\
& \text{nor} & \text{nor \$s1, \$s2, \$s3} & \$s1 = \sim(\$s2 \mid \$s3) & \text{三个寄存器操作数,按位或非} \\
\text{逻辑} & \text{and immediate} & \text{andi \$s1, \$s2, 100} & \$s1 = \$s2 \mathbin{\&} 100 & \text{寄存器和常数,按位与} \\
\text{运算} & \text{or immediate} & \text{ori \$s1, \$s2, 100} & \$s1 = \$s2 \mid 100 & \text{寄存器和常数,按位或} \\
& \text{shift left logical} & \text{sll \$s1, \$s2, 10} & \$s1 = \$s2 \ll 10 & \text{按常数对寄存器逻辑左移} \\
& \text{shift right logical}& \text{srl \$s1, \$s2, 10} & \$s1 = \$s2 \gg 10 & \text{按常数对寄存器逻辑右移} \\
\hline
& \text{branch on equal} & \text{beq \$s1, \$s2, L} & \text{if}(\$s1 == \$s2)\ \text{go to L} & \text{相等则转移} \\
\text{条件} & \text{branch on not equal}& \text{bne \$s1, \$s2, L} & \text{if}(\$s1\ !=\ \$s2)\ \text{go to L} & \text{不相等则转移} \\
\text{分支} & \text{set on less than} & \text{slt \$s1, \$s2, \$s3} & \text{if}(\$s2 < \$s3)\ \$s1=1;\ \text{else}\ \$s1=0 & \text{小于则置寄存器为1,否则为0,用于后续指令判0} \\
& \text{set on less than immediate} & \text{slti \$s1, \$s2, 100} & \text{if}(\$s2 < 100)\ \$s1=1;\ \text{else}\ \$s1=0 & \text{小于常数则置寄存器为1,否则为0,用于后续指令判0} \\
\hline
\text{无条件} & \text{jump} & \text{j L} & \text{go to L} & \text{直接跳转至目标地址} \\
\text{跳转} & \text{jump register} & \text{jr \$ra} & \text{go to \$ra} & \text{过程返回} \\
& \text{jump and link} & \text{jal L} & \$ra = \text{PC} + 4;\ \text{go to L} & \text{过程调用} \\
\hline
\end{array} $

### 算术运算指令
1. `add $s1, $s2, $s3`

> 含义：`$s1 = $s2 + $s3`（带溢出检查的加法）。
>

2. `sub $s1, $s2, $s3`

> 含义：`$s1 = $s2 - $s3`（带溢出检查的减法）。
>

### 存储访问指令（仅此两类能访存）
1. `**<font style="color:#DF2A3F;">lw $s1, 100($s2)</font>**`

> 含义：`$s1 = Memory[$s2 + 100]`
>
> 提示：从寄存器 `$s2` 获取基地址，加上偏移量 `100`（符号扩展至 32 位），取出内存中的一个字（4 字节）读入 `$s1`。
>

2. `**<font style="color:#DF2A3F;">sw $s1, 100($s2)</font>**`

> 含义：`Memory[$s2 + 100] = $s1` 
>
> 提示：将寄存器 `$s1` 中的一个字的数据写入到计算出的内存地址中。
>

### 逻辑与移位运算指令
+ `and $s1, $s2, $s3`  $ \rightarrow $ 含义：`$s1 = $s2 & $s3`（按位与）
+ `or $s1, $s2, $s3`   $ \rightarrow $ 含义：`$s1 = $s2 | $s3`（按位或）
+ `nor $s1, $s2, $s3`  $ \rightarrow $ 含义：`$s1 = ~($s2 | $s3)`（按位或非）

> MIPS 没有单独的取反指令 `not`，是用 `nor $s1, $s2, $zero`（与恒 0 寄存器按位或非）来实现按位取反的。
>

+ `andi $s1, $s2, 100` $ \rightarrow $ 含义：`$s1 = $s2 & 100`（立即数按位与，立即数进行**零扩展**）
+ `ori $s1, $s2, 100`  $ \rightarrow $ 含义：`$s1 = $s2 | 100`（立即数按位或）
+ `**<font style="color:#DF2A3F;">sll $s1, $s2, 10</font>**`   $ \rightarrow $ 含义：`$s1 = $s2 << 10`（逻辑左移，空位补 0，利用 `shamt` 字段）
+ `**<font style="color:#DF2A3F;">srl $s1, $s2, 10</font>**`   $ \rightarrow $ 含义：`$s1 = $s2 >> 10`（逻辑右移，高位补 0）

### 条件分支与比较指令
1. `beq $s1, $s2, L`

> 含义：`if ($s1 == $s2) goto L`（相等则跳转至标签 L）。
>

2. `bne $s1, $s2, L`

> 含义：`if ($s1 != $s2) goto L`（不相等则跳转至标签 L）。
>

3. `slt $s1, $s2, $s3`

> 含义：`if ($s2 < $s3) $s1 = 1; else $s1 = 0;`（定小于则置位，常与 `bne`/`beq` 配合实现复合条件判断）。
>

4. `slti $s1, $s2, 100`

> 含义：`if ($s2 < 100) $s1 = 1; else $s1 = 0;`（与立即数比较）。
>

### 无条件跳转指令
1. `j L`

> 含义：`goto L`（直接、无条件长跳转到目标地址 L）。
>

2. `jal L`

> 含义：`$ra = PC + 4; goto L`（**跳转并链接**）。用于函数/过程调用，将下一条指令的地址（返回地址）自动存入 `$ra`（`$31`），然后跳往 L。
>

3. `jr $ra`

> 含义：`goto $ra`（寄存器跳转）。用于函数返回，读取 `$ra` 中的地址并跳转回去。
>

---



## MIPS 中过程(函数)调用的机器级表示
### 核心概念
过程调用（函数调用）是程序模块化的基础。在 MIPS 中，由于寄存器数量有限且所有过程共享，必须遵循严格的**调用约定 **来管理寄存器使用和栈空间。

#### 关键指令
 MIPS 没有像 x86 那样的 `call` 和 `ret`，而是通过以下两条无条件转移指令组合实现函数的调用与返回：  

1. `jal`** (Jump and Link)**：调用指令（J-型）。
+ 功能：① 自动将下一条指令的地址（即 PC + 4）保存到 `$ra` ($31)；②  无条件长跳转到目标标签 `L`（入口地址）处执行 
2. `jr`** (Jump Register)**：返回指令（R-型）。
+ 功能： 无条件跳转到寄存器 `$ra` 中保存的地址处执行，从而无缝返回到调用点（`jal` 的下一条指令）  。

---

#### 寄存器使用约定 
 因为 CPU 中的寄存器是所有过程共用的，为了防止调用者（P）和被调用者（Q）互相覆盖数据，MIPS 制定了严格的**调用约定**：  

| 寄存器类别 | 寄存器编号 | 用途 | 保存责任 | 说明 |
| :---: | :---: | :---: | :---: | :---: |
| **参数寄存器** | `$a0` - `$a3` | 传递前 4 个非浮点参数 | 调用者 (Caller) | 若参数 > 4 个，多余参数压栈 |
| **返回值寄存器** | `$v0` - `$v1` | 传递返回值 | 被调用者 (Callee) | 函数执行完将结果放入此处 |
| **返回地址** | `$ra` ($31) | 存放返回地址 (PC+4) | 被调用者 (Callee) | `jal` 指令自动写入， 非叶子过程（还会调用其他过程的函数）在开头的**第一件事就是必须把 **`**$ra**`** 压栈**，否则后续的 `jal` 会覆盖它导致无法返回。   |
| **临时寄存器** | `$t0` - `$t9` | 临时变量 | **调用者 (Caller)** | 被调用过程可随意修改，**不保证**返回后值不变。若 Caller 需要保留，需自己压栈。 |
| **保存寄存器** | `$s0` - `$s7` | 局部变量/长期数据 | **被调用者 (Callee)** | 若 Callee 使用了这些寄存器，**必须**先压栈保存，返回前恢复。 |
| **栈指针** | `$sp` ($29) | 指向栈顶 | 双方共同维护 | 栈向下生长（高->低），入栈减小，出栈增加 |
| **帧指针** | `$fp` ($30) | 指向当前栈帧底部 | 被调用者 (Callee) | 用于固定访问局部变量和参数（可选，但推荐） |


---

#### 栈与栈帧 (Stack & Stack Frame)
1. **栈的基本操作：**MIPS 没有专门的 `push` / `pop` 指令。
+ **入栈**：先减小 `$sp`，再 `sw`。
    - `addi $sp, $sp, -4`
    - `sw $ra, 0($sp)`
+ **出栈**：先 `lw`，再增加 `$sp`。
    - `lw $ra, 0($sp)`
    - `addi $sp, $sp, 4`

例如，要将 `$ra` 和 `$a0` 两个寄存器（共 8 字节）压栈保存：

```plain
addi $sp, $sp, -8    # 1. 调整栈指针，向下开辟 8 字节空间
sw   $ra, 4($sp)     # 2. 将 $ra 存入高地址单元
sw   $a0, 0($sp)     # 3. 将 $a0 存入低地址单元
```

**2. 栈帧结构**

每个过程在栈上分配一块区域，称为**栈帧**。

+ **生长方向**：**从高地址向低地址生长。**
+ **$sp (Stack Pointer)**：始终指向栈顶（当前最低地址）。 在整个函数执行过程中，由于数据的入栈出栈，`$sp` 的值是动态变化的。  
+ **$fp (Frame Pointer)**：指向当前栈帧的起始位置（高地址端）， 在函数执行期间保持不变，用来稳定地通过偏移量访问局部变量。

> _注：若编译器能通过固定的 _`_$sp_`_ 计算出偏移量，为了节省开销，通常不设置 _`_$fp_`_。_
>

---

#### 过程调用详细步骤 
假设过程 P 调用过程 Q。

1. **调用者 P (Caller) 的执行步骤**
    1. **准备参数**：将前 4 个参数放入 `$a0-$a3`。若超过 4 个，将多余参数压入 P 的栈帧。
    2. **保护现场 (可选)**：如果 P 在 Q 返回后还需要用到 `$t0-$t9` 或 `$a0-$a3`，P 必须先将它们压栈保存（因为 Q 可能会覆盖它们）。
    3. **执行调用**：执行 `jal Q`。此时 `$ra` 被自动更新为 P 中 `jal` 的下一条指令地址。
2. 被调用者 Q (Callee) 的执行步骤

Q 的代码分为三段：**开始段 **、**主体段**、**结尾段**。

**(1) 开始段  - 建立栈帧**

    - 调整 `$sp` 申请当前函数的栈帧空间（`addi $sp, $sp, -FrameSize`）。
    - 如果 Q 会调用其他函数（非叶子过程），必须将 `$ra` 压栈。
    - 将 Q 内部需要用到的保存寄存器（`$s0~$s7`）压栈。
    - 如果寄存器不够用，在栈帧内为局部变量分配空间。

**(2) 主体段**

    - 执行 Q 的具体逻辑代码。
    - 通过 `$fp` 访问局部变量和参数（例如 `lw $t0, 4($fp)`）。

**(3) 结尾段  - 恢复并返回**

    - 从栈中读取并恢复之前保存的 `$s0~$s7` 寄存器。
    - 从栈中恢复返回地址到 `$ra`。
    - 调整 `$sp` 释放栈帧（`addi $sp, $sp, FrameSize`）。
    - 执行 `jr $ra` 返回调用者 P。

#### 典型例题分析：叶子过程 vs 非叶子过程
##### 一、 叶子过程
**定义**：函数内部**不再调用任何其他函数**。它是调用树的末端（叶子）。

C 语言实例：一个简单的数学计算函数：

```c
int leaf_calc(int a, int b) {
    int result = (a + b) * 4;
    return result;
}
```

 **MIPS 汇编代码**

+ 输入参数：`a` 存放在 `$a0`，`b` 存放在 `$a1`
+ 返回值：存放在 `$v0`

```plain
leaf_calc:
    # ------------------ 本体段 (Body) ------------------
    add $t0, $a0, $a1    # $t0 = a + b (使用临时寄存器 $t0)
    sll $v0, $t0, 2      # $v0 = $t0 << 2 (利用移位实现乘以 4，并直接写入返回值寄存器)
    
    # ------------------ 结尾段 (Epilogue) --------------
    jr  $ra              # 直接返回调用者
```

**为什么它的栈帧为空?**

1. 无需保护 `$ra`：因为内部没有 `jal` 指令，`$ra`（返回地址）的值绝对不会被篡改，所以不需要压栈保存。
2. **无需保护寄存器**：该函数只使用了临时寄存器 `$t0`。根据 MIPS 调用约定，`$t` 系列寄存器属于 **Caller-saved（调用者保存）**，被调用者（这里是 `leaf_calc`）可以无条件覆盖使用，不需要尽保护义务。

---

##### 二、 非叶子过程
**定义**：函数内部**还会调用其他函数**（例如调用了上面的 `leaf_calc`）。

**C 语言代码示例：** 一个需要嵌套调用的复合计算函数：

```c
int non_leaf_compute(int x, int y, int z) {
    int sum = leaf_calc(x, y); // 第一次嵌套调用
    return sum + z;            // 此时必须保证 z 的值没有被破坏
}
```

**MIPS 汇编代码**

+ 输入参数：`x` 存放在 `$a0`，`y` 存放在 `$a1`，`z` 存放在 `$a2`
+ 返回值：存放在 `$v0`

```plain
non_leaf_compute:
    # ------------------ 开始段， 建立栈帧  ------------------
    addi $sp, $sp, -8      # 1. 在栈上申请 8 字节空间（2个字）
    sw   $ra, 4($sp)       # 2. 必须保护返回地址！因为后面的 jal 会覆盖 $ra
    sw   $s0, 0($sp)       # 3. 必须保护被调用者保存寄存器 $s0

    # ------------------ 本体段 ----------------------
    addu  $s0, $a2, $zero          # 4. 将 z 的值从 $a2 挪到 $s0 中暂存
                           #    (因为调用 leaf_calc 时，依据约定 $a2 随时可能被其破坏)
                           
    # 此时 $a0 和 $a1 已经自动存放了 x 和 y，直接作为参数调用
    jal  leaf_calc         # 5. 调用叶子过程。此时 $ra 改变，结果返回在 $v0 中
    
    add  $v0, $v0, $s0     # 6. 计算最终结果：$v0 = leaf_calc的返回值 + z ($s0)

    # ------------------ 结尾段  ------------------
    lw   $s0, 0($sp)       # 7. 恢复调用前的 $s0 现场
    lw   $ra, 4($sp)       # 8. 恢复正确的返回地址到 $ra
    addi $sp, $sp, 8       # 9. 释放栈帧空间
    jr   $ra               # 10. 成功返回到上一级调用者
```

为什么它必须用栈？

1. `$ra`** 覆盖危机**：当执行第 5 行 `jal leaf_calc` 时，硬件会自动把 `jal` 下一条指令的地址写入 `$ra`。如果不执行第 2 行的 `sw $ra`，本函数原本的返回地址就**永久丢失**了，程序将陷入无限死循环。
2. **寄存器生存期冲突**：参数 `z` 存放在 `$a2`。在 `jal` 调用期间，子函数有权修改 `$a2`。为了在调用结束后还能正确拿到 `z`，我们选择将它存入 **Callee-saved（被调用者保存）** 的 `$s0` 中。但既然用了 `$s0`，本函数就必须履行义务，在开头（第 3 行）压栈保护 `$s0`，在退出前（第 7 行）弹栈恢复。

---

## MIPS 选择结构的机器级表示
### MIPS 条件跳转的核心机制（无状态码架构）
x86 架构依赖于各种条件标志位（如 `ZF`, `SF`, `CF`）来进行跳转，而 MIPS 贯彻了 RISC 的精简理念，**没有状态码寄存器**。MIPS 判定是否跳转只有两种办法：

1. **直接比较跳转**：通过 `beq`（相等则跳）或 `bne`（不等则跳）直接比较两个寄存器的值。
2. **两步法组合跳转**：如果需要比较大小（如 `<`、`>`、`\ge`），必须先用比较指令（如 `slt`）将结果存入一个临时寄存器，再用 `beq` 或 `bne` 判断该临时寄存器是否为 0。

**核心条件指令**

| 指令语法 | 全称 | 核心逻辑功能 | 408 考点避坑提示 |
| :---: | :---: | :---: | :---: |
| `beq $s1, $s2, L1` | Branch if Equal | `if ($s1 == $s2) goto L1` | 对应 C 语言的 `==`。但在汇编中往往用 `bne` 来跳过 `if` 块。 |
| `bne $s1, $s2, L1` | Branch if Not Equal | `if ($s1 != $s2) goto L1` | 对应 C 语言的 `!=`。 |
| `slt $t0, $s1, $s2` | Set on Less Than | `if ($s1 < $s2) $t0 = 1; else $t0 = 0;` | 关键：**有符号数**比较。小于则将目标置 1。 |
| `j L2` | Jump | `goto L2` | 无条件跳转，常用于跳出整个 `else` 块。 |


:::color2
在 C 语言中，我们的思维是：“如果条件**满足**，就执行主体代码”。  
但在机器级代码中，编译器的底层逻辑通常是：“如果条件**不满足**，就**跳过**主体代码”。

因此，你在真题中看到的汇编跳转指令，其条件往往与 C 语言的逻辑是**相反**的。

:::

### 示例 1：等值判断分支
**场景**：系统根据当前校验位是否匹配，决定是累计奖励还是扣除惩罚。

C 语言代码

```c
if (check_val == target_val) {
    score = score + bonus;
} else {
    score = score - penalty;
}
```

**机器级寄存器分配**

+ `check_val` $ \rightarrow $ `$s0`
+ `target_val` $ \rightarrow $ `$s1`
+ `score` $ \rightarrow $ `$s2`
+ `bonus` $ \rightarrow $ `$s3`
+ `penalty` $ \rightarrow $ `$s4`

**MIPS 汇编代码表示**

```plain
    # ------------------ 条件判定 ------------------
    bne  $s0, $s1, label_else   # 核心：若 check_val != target_val，则跳过 IF 块去执行 ELSE
    
    # ------------------ IF 分支体 -----------------
    add  $s2, $s2, $s3          # score = score + bonus
    j    label_exit             # 执行完 IF 后，必须无条件跳出整个选择结构
    
    # ------------------ ELSE 分支体 ---------------
label_else:
    sub  $s2, $s2, $s4          # score = score - penalty
    
label_exit:
    # 结构退出点
```

---

### 示例 2：关系大小判断分支（Relational Selection）
**场景**：经典的“求两数最大值”算法。由于硬件原生只提供 `slt`（小于则置位），如何优雅地实现 `>` 或 `\le` 是重点。

 C 语言代码

```c
if (x > y) {
    max = x;
} else {
    max = y;
}
```

**机器级寄存器分配**

+ `x` $ \rightarrow $ `$s0`
+ `y` $ \rightarrow $ `$s1`
+ `max` $ \rightarrow $ `$s2`
+ 临时判定寄存器 $ \rightarrow $ `$t0`

**MIPS 汇编代码表示**

```plain
    # ------------------ 两步法条件判定 ------------------
    # MIPS没有“大于跳转”指令。把 "x > y" 转化为逻辑等价的 "y < x"
    slt  $t0, $s1, $s0          # if (y < x) $t0 = 1; else $t0 = 0;
    
    # 此时，若 x > y 成立，则 $t0 为 1；若不成立（即 x <= y），则 $t0 为 0
    beq  $t0, $zero, label_else # 若 $t0 == 0 (不满足大于条件)，跳转到 ELSE 块
    
    # ------------------ IF 分支体 ----------------------
    add  $s2, $s0, $zero        # max = x (利用与 $zero 相加实现高效的 move 操作)
    j    label_exit             # 跳出选择结构
    
    # ------------------ ELSE 分支体 --------------------
label_else:
    add  $s2, $s1, $zero        # max = y
    
label_exit:
```



---

## MIPS 循环结构的机器级表示 
循环结构在机器级代码中的**<u><font style="color:#DF2A3F;">本质是条件跳转（向后跳）与无条件跳转（向前循环）的组合。</font></u>**

MIPS 实现标准 `while` 循环的通用模板如下：

1. **循环头（Loop Test）**：在循环体开始前，利用条件分支指令（如 `beq`, `bne`）测试循环边界。若不满足条件，则直接跳出循环。
2. **循环体（Loop Body）**：执行核心计算。
3. **步进（Increment）**：更新循环变量（如 `i++`）。
4. **尾部跳转（Back Edge）**：执行无条件跳转指令 `j`，强行将控制流送回循环头，形成闭环。

****

**核心问题：循环中的数组变址访问**

**MIPS 架构没有自动变址寻址方式**。

+ **x86 的做法**：拥有复杂的寻址模式，一条 `mov eax, [ebx + ecx * 4]` 就能自动完成“基地址 + 索引 $ \times $ 4”的计算并访存。
+ **MIPS 的做法**：属于精简指令集（RISC），其访存指令 `lw/sw` 唯一的寻址方式是**基址寻址**，即 `offset(base)`，其中的 `offset` 必须是一个**立即数常数**。



因此，在 MIPS 中访问 C 语言中的数组元素 `A[i]`（假设为 32位 `int` 数组），编译器必须**显式地用多条指令**计算出该元素的绝对内存地址：$ \text{有效地址 } EA = \text{A的首地址} + (i \times 4) $

**关于乘以 4 的底层实现**：**使用逻辑左移指令 **`sll $t0, $s0, 2`**（左移 2 位相当于乘以 4）**，这也是执行效率最高、最常用的手段。



**示例：**

```c
while (i < size) {
    sum = sum + src[i];
    i++;
}
```

**机器级寄存器分配**

+ `i`（循环计数器） $ \rightarrow $ `$s0`
+ `size`（循环上限） $ \rightarrow $ `$s1`
+ `sum`（累加器） $ \rightarrow $ `$s2`
+ `src`（数组 `src` 的首地址） $ \rightarrow $ `$s3`
+ 临时寄存器 $ \rightarrow $ `$t0, $t1, $t2`

**MIPS 汇编代码表示**

```plain
Loop:
    # ------------------ 1. 循环边界检查 ------------------
    slt  $t0, $s0, $s1          # if (i < size) $t0 = 1; else $t0 = 0;
    beq  $t0, $zero, Exit       # 若 $t0 == 0 (即 i >= size)，条件不满足，跳出循环
    
    # ------------------ 2. 核心：显式变址寻址计算 src[i] -------
    sll  $t1, $s0, 2            # $t1 = i * 4 (计算字节偏移量，左移 2 位)
    add  $t1, $t1, $s3          # $t1 = src + i * 4 (计算出 src[i] 的绝对内存地址 EA)
    lw   $t2, 0($t1)            # 将内存地址 EA 处的一个字（4字节）加载到临时寄存器 $t2
    
    # ------------------ 3. 循环体内容与步进 ------------------
    add  $s2, $s2, $t2          # sum = sum + src[i]
    addi $s0, $s0, 1            # i = i + 1 (循环变量自增)
    
    # ------------------ 4. 闭环控制 ----------------------
    j    Loop                   # 无条件跳转回循环头，进入下一次迭代
    
Exit:
    # 循环退出点
```

---

## 真题中出现的 MIPS 指令
1. <font style="color:rgb(25, 27, 31);">【2014-44】（12分）某程序中有如下循环代码段P：“for (int i=0; i＜N; i++) sum += A[i];”。假设编译时变量sum和i分别分配在寄存器R1和R2中。常量N在寄存器R6中，数组A的首地址在寄存器R3中。程序段P起始地址为08048100H，对应的汇编代码和机器代码如下表所示。</font>

$ \begin{array}{cccccc} \text{编号}&\text{地址}&\text{机器代码}&\text{汇编代码}&\text{注释}\\\hline 1&\text{08048100H}&\text{00022080H}&\text{loop: sll R4, R2, 2}&\text{(R2)<<2→R4}\\ 2&\text{08048104H}&\text{00083020H}&\text{add R4, R4, R3}&\text{(R4)+(R3)→R4}\\ 3&\text{08048108H}&\text{8C850000H}&\text{load R5, 0(R4)}&\text{((R4)+0)→R5}\\ 4&\text{0804810CH}&\text{00250820H}&\text{add R1, R1, R5}&\text{(R1)+(R5)→R1}\\ 5&\text{08048110H}&\text{20420001H}&\text{add R2, R2, 1}&\text{(R2)+1→R2}\\ 6&\text{08048114H}&\text{1446FFFAH}&\text{bne R2, R6, loop}&\text{if (R2)!=(R6) goto loop}\\ \end{array} $

<font style="color:rgb(25, 27, 31);">执行上述代码的计算机M采用32位定长指令字，其中分支指令bne采用如下格式。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/42876865/1781633817557-f17232db-c77b-4824-b8b6-c9e63873ef68.png)

<font style="color:rgb(25, 27, 31);">Op为操作码，Rs和Rd为寄存器编号，OFFSET为偏移量，用补码表示。请回答下列问题，并说明理由。</font>

<font style="color:rgb(25, 27, 31);">(1) M的存储器编址单位是什么？</font>

<font style="color:rgb(25, 27, 31);">(2) 已知sll指令实现左移功能，数组A中每个元素占多少位？</font>

<font style="color:rgb(25, 27, 31);">(3) 题44表中bne指令的OFFSET字段的值是多少？已知bne指令采用相对寻址方式，当前PC内容为bne指令地址，通过分析题44表中指令地址和bne指令内容，推断出bne指令的转移目标地址计算公式。</font>

<font style="color:rgb(25, 27, 31);">(4) 若M采用如下“按序发射、按序完成”的5级指令流水线：IF（取指）、ID（译码及取数）、EXE（执行）、MEM（访存）、WB（写回寄存器），且硬件不采取任何转发措施，分支指令的执行均引起3个时钟周期阻塞，则P中那些指令的执行会由于数据相关而发生流水线阻塞？哪条指令的执行会发生控制冒险？为什么指令1的执行不会因为与指令5的数据相关而发生阻塞？</font>

<details class="lake-collapse"><summary id="u781a6864"><span class="ne-text">解析</span></summary><p id="udb1d98e1" class="ne-p"><span class="ne-text" style="color: rgb(25, 27, 31)">在分析具体问题前，我们先梳理已知条件和寄存器对应关系：</span></p><ul class="ne-ul"><li id="u532fc271" data-lake-index-type="0"><strong><span class="ne-text">循环代码功能</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：对数组 </span><span id="rRCzW" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/de951302f41d4707b9d80ca1af34dd0f.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)"> 进行累加，</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">sum += A[i]</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li><li id="ue44c74fe" data-lake-index-type="0"><strong><span class="ne-text">寄存器分配</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">sum</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> </span><span id="L986T" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/33b44e34aa35b8c4ecd0606453ee68e9.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)"> </span><strong><span class="ne-text">R1</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">，</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">i</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> </span><span id="ieCok" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/33b44e34aa35b8c4ecd0606453ee68e9.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)"> </span><strong><span class="ne-text">R2</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">，</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">A</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">的首地址 </span><span id="Zclt1" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/33b44e34aa35b8c4ecd0606453ee68e9.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)"> </span><strong><span class="ne-text">R3</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">，</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">N</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> </span><span id="flMqx" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/33b44e34aa35b8c4ecd0606453ee68e9.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)"> </span><strong><span class="ne-text">R6</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li><li id="u4c9db234" data-lake-index-type="0"><strong><span class="ne-text">机器特性</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：32位定长指令字，采用 5 级流水线（IF、ID、EXE、MEM、WB），按序发射、按序完成。</span></li></ul><p id="uf8d14230" class="ne-p"><strong><span class="ne-text" style="color: #DF2A3F">(1) 字节编址</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">（或者说编址单位是</span><strong><span class="ne-text">字节/Byte</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">）。</span></p><ol class="ne-ol"><li id="u604e7c41" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">题目中明确指出：计算机M采用 </span><strong><span class="ne-text">32位定长指令字</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">，也就是说每条指令占 32 位（即 </span><strong><span class="ne-text">4 个字节</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">）。</span></li><li id="u0f976dd1" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">观察表中连续指令的地址，例如：</span></li></ol><ul class="ne-ul"><li id="u655795d3" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">指令 1 的地址为 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">08048100H</span></code></li><li id="u23716791" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">指令 2 的地址为 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">08048104H</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"><br /></span><span class="ne-text" style="color: rgb(25, 27, 31)">两个相邻指令的地址差为：</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">08048104H - 08048100H = 4H</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">（即十进制的 4）。</span></li></ul><ol start="3" class="ne-ol"><li id="u3a0f5338" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">因为一条 4 字节的指令占用了 4 个地址单位，所以 </span><strong><span class="ne-text">1 个地址单位 = 1 个字节</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">。因此，该存储器是按字节编址的。</span></li></ol><hr id="hd3Jm" class="ne-hr"><p id="ue315ce98" class="ne-p"><strong><span class="ne-text" style="color: #DF2A3F">(2) 数组A中每个元素占32位（或 4 字节）。</span></strong></p><ol class="ne-ol"><li id="u0dab72ae" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">指令 1 为 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">sll R4, R2, 2</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">，注释为 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">(R2)&lt;&lt;2 -&gt; R4</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">。</span><strong><span class="ne-text">R2</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)"> 中存放的是循环变量 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">i</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">，左移 2 位相当于乘以 </span><span id="VE5ix" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/4b28b6a6ed249c256473c74e51411f64.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)">。也就是说，</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">R4 = i * 4</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li><li id="uee13a537" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">指令 2 为 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">add R4, R4, R3</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">，将刚才计算的偏移量 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">R4</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 与数组首地址 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">R3</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 相加，得到 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">A[i]</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 的内存地址。</span></li><li id="u06400ea2" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">由于计算机是</span><strong><span class="ne-text">字节编址</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">，下标 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">i</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 每增加 1，地址就增加 4 个字节。这说明数组 </span><span id="i28GC" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/de951302f41d4707b9d80ca1af34dd0f.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)"> 中的每一个元素占 </span><strong><span class="ne-text">4 个字节</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li><li id="u083be283" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">换算成位数：</span><span id="HzExU" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/c23dd7b4de747e28aac87c39d71b9c30.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)"> </span><strong><span class="ne-text">32位</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li></ol><hr id="tlWzj" class="ne-hr"><p id="uf1508f19" class="ne-p"><strong><span class="ne-text" style="color: #DF2A3F">(3) bne指令的OFFSET字段的值是</span></strong><code class="ne-code"><strong><span class="ne-text" style="color: #DF2A3F">FFFAH</span></strong></code><strong><span class="ne-text" style="color: #DF2A3F">（或十进制的 </span></strong><span id="ukh88" class="ne-math" style="color: #DF2A3F"><img src="https://cdn.nlark.com/yuque/__latex/7ae2f2c65fc82b49abf101d96f595f7e.svg"></span><strong><span class="ne-text" style="color: #DF2A3F">）。bne指令的转移目标地址计算公式：</span></strong></p><p id="uff64294d" class="ne-p"><span id="UFApi" class="ne-math" style="color: #DF2A3F"><img src="https://cdn.nlark.com/yuque/__latex/63b9e77a0dca605329ebfd74c93bbe61.svg"></span></p><ol class="ne-ol"><li id="u5b7400cc" data-lake-index-type="0"><strong><span class="ne-text">提取 OFFSET 字段</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：观察指令 6（</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">bne</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">）的机器代码为 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">1446FFFAH</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">。根据题目给出的 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">bne</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 指令格式，高 16 位是 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">OP</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">、</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">Rs</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">、</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">Rd</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">，低 16 位（即最后 4 位十六进制数）是 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">OFFSET</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">。因此，</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">OFFSET = FFFAH</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li><li id="ue40aed58" data-lake-index-type="0"><strong><span class="ne-text">计算 OFFSET 的真值</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">FFFAH</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 用补码表示，首位为 1 是个负数。对其求源码（取反加 1）：</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">FFFAH</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 取反得到 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">0005H</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">，再加 1 得到 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">0006H</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">。所以其十进制真值为 </span><span id="ahDE2" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/7ae2f2c65fc82b49abf101d96f595f7e.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li><li id="u0d7dcb26" data-lake-index-type="0"><strong><span class="ne-text">推导目标地址公式</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：</span></li></ol><ul class="ne-ul"><li id="uc4b39bce" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">当前 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">bne</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 指令的地址（即当前 PC）= </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">08048114H</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li><li id="u79f84151" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">跳转的目标地址（</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">loop</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 标签所在指令 1 的地址）= </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">08048100H</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li><li id="u4c6771ad" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">两者的实际地址差为：</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">08048100H - 08048114H = -14H</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">（即十进制的 </span><span id="y3Rad" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/fd2f143b65a9919505bf18ca865e85eb.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)">）。</span></li><li id="u0991ca7d" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">已知 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">OFFSET = -6</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">，如何通过 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">-6</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 和当前 PC 算出 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">-20</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 的地址偏移？</span></li><li id="ubd4da4bb" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">因为指令是定长 4 字节，通常相对寻址会先将 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">PC + 4</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">（指向下一条指令），再在此基础上加上 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">OFFSET * 4</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li><li id="u2557daa8" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">验证：</span><span id="PIBXq" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/f66b45a80095c077b772be39860614a8.svg"></span></li></ul><ul class="ne-ul"><li id="u64ded73b" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">结果完全吻合，因此公式为：</span><span id="uMO3X" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/b4d32881d8e84296014398511507c1e8.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li></ul><hr id="ILM4M" class="ne-hr"><p id="u85576380" class="ne-p"><span class="ne-text" style="color: rgb(25, 27, 31)">(4) ① </span><strong><span class="ne-text" style="color: #DF2A3F">指令 2、指令 3、指令 4、指令 6</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">的执行会由于数据相关而发生流水线阻塞<br /></span><span class="ne-text" style="color: rgb(25, 27, 31)">题目说明“硬件不采取任何转发（旁路）措施”，这意味着后面指令如果需要用到前面指令写入的寄存器，必须等到前面指令执行到 </span><strong><span class="ne-text">WB（写回）</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)"> 阶段将数据切实写入寄存器文件后，后面指令才能在 </span><strong><span class="ne-text">ID（译码/读寄存器）</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)"> 阶段读出。</span></p><ul class="ne-ul"><li id="uff52c620" data-lake-index-type="0"><strong><span class="ne-text">指令 2</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)"> 依赖 </span><strong><span class="ne-text">指令 1</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)"> 写入的 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">R4</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">（第1条写，第2条读，产生RAW相关）。</span></li><li id="u3b5c271d" data-lake-index-type="0"><strong><span class="ne-text">指令 3</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)"> 依赖 </span><strong><span class="ne-text">指令 2</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)"> 写入的 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">R4</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">（第2条写，第3条读，产生RAW相关）。</span></li><li id="u6ce2028e" data-lake-index-type="0"><strong><span class="ne-text">指令 4</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)"> 依赖 </span><strong><span class="ne-text">指令 3</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)"> 写入的 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">R5</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">（第3条写，第4条读，产生RAW相关）。</span></li><li id="ub98fe924" data-lake-index-type="0"><strong><span class="ne-text">指令 6</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)"> 依赖 </span><strong><span class="ne-text">指令 5</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)"> 写入的 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">R2</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">（第5条写，第6条读，产生RAW相关）。<br /></span><span class="ne-text" style="color: rgb(25, 27, 31)">以上这些相邻指令均因为数据未及时写回而导致流水线阻塞。</span></li></ul><p id="u5cf988b1" class="ne-p"><span class="ne-text" style="color: rgb(25, 27, 31)">② </span><strong><span class="ne-text" style="color: #DF2A3F">指令 6（即 </span></strong><code class="ne-code"><strong><span class="ne-text" style="color: #DF2A3F">bne</span></strong></code><strong><span class="ne-text" style="color: #DF2A3F"> 指令）的执行会发生控制冒险</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)"><br /></span><span class="ne-text" style="color: rgb(25, 27, 31)">控制冒险通常由</span><strong><span class="ne-text">分支跳转指令</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">引起。指令 6 是一条条件转移指令（</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">bne</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">），在它执行到确定是否跳转以及跳转到何处之前，流水线无法确定下一条应该取哪里的指令，从而导致控制冒险（题目也明确指出分支指令会引起 3 个时钟周期的阻塞）。</span></p><p id="u9b227034" class="ne-p"><span class="ne-text" style="color: rgb(25, 27, 31)">③ </span><strong><span class="ne-text" style="color: #DF2A3F">因为 指令 6（分支指令）在执行时引入了 3 个时钟周期的控制冒险阻塞。</span></strong></p><ol class="ne-ol"><li id="uc15b8a29" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">虽然指令 5 会修改 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">R2</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">（</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">add R2, R2, 1</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">），而下一轮循环的指令 1 需要读取 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">R2</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">（</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">sll R4, R2, 2</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">），它们之间存在数据相关。</span></li><li id="u985fe9f0" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">但是在指令 5 和下一轮的指令 1 之间，隔着一条</span><strong><span class="ne-text">指令 6（</span></strong><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">bne</span></code><strong><span class="ne-text">）</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li><li id="u03175d3e" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">题目规定：“</span><em><span class="ne-text">分支指令的执行均引起 3 个时钟周期阻塞</span></em><span class="ne-text" style="color: rgb(25, 27, 31)">”。在这 3 个时钟周期的等待时间内，指令 5 有足够的时间流向流水线的深处，并顺利完成它的 </span><strong><span class="ne-text">WB（写回寄存器）</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)"> 阶段。</span></li><li id="u06d67a92" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">当 3 个周期的阻塞结束、下一轮的指令 1 开始进入 </span><strong><span class="ne-text">ID（读寄存器）</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)"> 阶段时，</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">R2</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 的新值已经稳稳地写回到寄存器中了。因此，指令 1 可以直接读到正确的数据，不需要再进行额外的因数据相关导致的阻塞。</span></li></ol></details>


2. <font style="color:rgb(25, 27, 31);">【2016-19】在无转发机制的五段基本流水线中，下列指令序列存在数据冒险的指令对是（ ）。</font>

<font style="color:rgb(25, 27, 31);">I1: add R1, R2, R3; (R2)+(R3)→R1</font>

<font style="color:rgb(25, 27, 31);">I2: add R5, R2, R4; (R2)+(R4)→R5</font>

<font style="color:rgb(25, 27, 31);">I3: add R4, R5, R3; (R5)+(R3)→R4</font>

<font style="color:rgb(25, 27, 31);">I4: add R5, R2, R6; (R2)+(R6)→R5</font>

<font style="color:rgb(25, 27, 31);">A. I1 和 I2</font>

<font style="color:rgb(25, 27, 31);">B. I2 和 I3</font>

<font style="color:rgb(25, 27, 31);">C. I2 和 I4</font>

<font style="color:rgb(25, 27, 31);">D. I3 和 I4</font>





3. <font style="color:rgb(25, 27, 31);">【2019-18】在采用“取指、译码/取数、执行、访存、写回”5段</font>[<font style="color:rgb(25, 27, 31);">流水线</font>](https://zhida.zhihu.com/search?content_id=234528162&content_type=Article&match_order=1&q=%E6%B5%81%E6%B0%B4%E7%BA%BF&zhida_source=entity)<font style="color:rgb(25, 27, 31);">的处理器中，执行如下指令序列，其中s0、s1、s2、s3和t2表示寄存器编号。</font>

```c
I1: add s2,s1,s0    // R[s2]←R[s1]+R[s0]
I2: load s3,0(t2)   // R[s3]←M[R[t2]+0]
I3: add s2,s2,s3    // R[s2]←R[s2]+R[s3]
I4: store s2,0(t2)  // M[R[t2]+0]←R[s2]
```

<font style="color:rgb(25, 27, 31);">下列指令对中，不存在数据冒险的是（ ）。</font>

<font style="color:rgb(25, 27, 31);">A. I1和I3</font>

<font style="color:rgb(25, 27, 31);">B. I2和I3</font>

<font style="color:rgb(25, 27, 31);">C. I2和I4</font>

<font style="color:rgb(25, 27, 31);">D. I3和I4</font>

<font style="color:rgb(25, 27, 31);"></font>

4. <font style="color:rgb(25, 27, 31);">【2021-43】假定计算机M字长为16位，按字节编址，连接CPU和主存的系统总线中地址线为20位、数据线为8位，采用16位定长指令字，指令格式及其说明如下：</font>

![](https://cdn.nlark.com/yuque/0/2026/png/42876865/1778350115694-14237b92-4cb7-4768-adfd-f3d77da33878.png?x-oss-process=image%2Fformat%2Cwebp)

<font style="color:rgb(25, 27, 31);">其中，op1~op3为操作码，rs、rt和rd为通用寄存器编号，R[r]表示寄存器r的内容，imm为立即数，target为转移目标的形式地址。请回答下列问题。</font>

<font style="color:rgb(25, 27, 31);">(1) ALU的宽度是多少位？可寻址主存空间大小为多少字节？指令寄存器、主存地址寄存器（MAR）和主存数据寄存器（MDR）分别应有多少位？</font>

<font style="color:rgb(25, 27, 31);">(2) R型格式最多可定义多少种操作？I型和J型格式总共最多可定义多少种操作？通用寄存器最多有多少个？</font>

<font style="color:rgb(25, 27, 31);">(3) 假定op1为0010和0011时，分别表示带符号整数减法和带符号整数乘法指令，则指令01B2H的功能是什么（参考上述指令功能说明的格式进行描述）？若1、2、3号通用寄存器当前内容分别为B052H、0008H、0020H，则分别执行指令01B2H和01B3H后，3号通用寄存器内容各是什么？各自结果是否溢出？</font>

<font style="color:rgb(25, 27, 31);">(4) 若采用I型格式的访存指令中imm（偏移量）为带符号整数，则地址计算时应对imm进行零扩展还是符号扩展？</font>

<font style="color:rgb(25, 27, 31);">(5) 无条件转移指令可以采用上述哪种指令格式？</font>

<details class="lake-collapse"><summary id="uf7113741"><strong><span class="ne-text" style="color: #DF2A3F">解析</span></strong></summary><p id="ud96064b0" class="ne-p"><strong><span class="ne-text">(1) 硬件参数计算</span></strong></p><ul class="ne-ul"><li id="u727fcfc5" data-lake-index-type="0"><strong><span class="ne-text">ALU 的宽度</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：<br /></span><span class="ne-text" style="color: rgb(25, 27, 31)">ALU（算术逻辑单元）的宽度通常与计算机的</span><strong><span class="ne-text">字长</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">一致。题目已知“计算机 M 字长为 16 位”，因此 ALU 的宽度是 </span><strong><span class="ne-text">16 位</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li><li id="uf43b9441" data-lake-index-type="0"><strong><span class="ne-text">可寻址主存空间大小</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：<br /></span><span class="ne-text" style="color: rgb(25, 27, 31)">地址线决定了最大寻址空间。题目给出“地址线为 20 位”，且“按字节编址”，因此可寻址空间为 </span><span id="kREqT" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/87dfa369bba0572dc6d9b7f429548609.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li><li id="u3d2416e8" data-lake-index-type="0"><strong><span class="ne-text">指令寄存器（IR）位数</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：<br /></span><span class="ne-text" style="color: rgb(25, 27, 31)">IR 存放当前正在执行的指令，其位数与</span><strong><span class="ne-text">指令字长</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">一致。题目指明“采用 16 位定长指令字”，故 IR 为 </span><strong><span class="ne-text">16 位</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li><li id="u5e6952d2" data-lake-index-type="0"><strong><span class="ne-text">主存地址寄存器（MAR）位数</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：<br /></span><span class="ne-text" style="color: rgb(25, 27, 31)">MAR 的位数与主存</span><strong><span class="ne-text">地址线</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">的根数一致。地址线为 20 位，故 MAR 为 </span><strong><span class="ne-text">20 位</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li><li id="ua6125437" data-lake-index-type="0"><strong><span class="ne-text">主存数据寄存器（MDR）位数</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：<br /></span><span class="ne-text" style="color: rgb(25, 27, 31)">MDR 用于缓冲 CPU 与主存之间的数据交换，其位数通常与</span><strong><span class="ne-text">数据线</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">的根数一致。题目给出“数据线为 8 位”，故 MDR 为 </span><strong><span class="ne-text">8 位</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">。 </span><em><span class="ne-text">(注：虽然字长是 16 位，但由于外部数据总线瓶颈只有 8 位，CPU 每次访存只能取 8 位数据，需要分两次才能取完一个字，此时 MDR 与外部数据线等宽为 8 位。这也是 408 常考的“陷阱”之一)</span></em><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li></ul><hr id="HqW4F" class="ne-hr"><p id="u01307e2f" class="ne-p"><strong><span class="ne-text">(2) 指令操作空间与寄存器数量</span></strong></p><ul class="ne-ul"><li id="ue8b69d73" data-lake-index-type="0"><strong><span class="ne-text">R 型格式最多可定义的操作数</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：<br /></span><span class="ne-text" style="color: rgb(25, 27, 31)">观察 R 型指令格式，其操作码字段为 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">op1</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">，占 4 位。因此 R 型格式最多可定义 </span><span id="MERDv" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/e744b0236ae74a5c96ed7b7e104ecf48.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)"> </span><strong><span class="ne-text">种</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">操作。</span></li><li id="u2485603e" data-lake-index-type="0"><strong><span class="ne-text">I 型和 J 型格式总共最多可定义的操作数</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：<br /></span><span class="ne-text" style="color: rgb(25, 27, 31)">最高 6 位是决定指令大类的主操作码。R 型指令独占了 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">000000</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 这一种状态。因此，剩余的 </span><span id="lrotW" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/23ae68a7a3bcf8496d0375fbeffce50f.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)"> </span><strong><span class="ne-text">种</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">状态可以全部分配给 I 型（</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">op2</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">）和 J 型（</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">op3</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">）指令使用。</span></li><li id="ua201331f" data-lake-index-type="0"><strong><span class="ne-text">通用寄存器最多数量</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：<br /></span><span class="ne-text" style="color: rgb(25, 27, 31)">观察 R 型或 I 型指令格式，用于表示寄存器编号的字段 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">rs</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">、</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">rt</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">、</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">rd</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 均为 </span><strong><span class="ne-text">2 位</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">。因此，最多只能寻址 </span><span id="lgNMf" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/d17c133448bc4769225754a461a00c28.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)"> </span><strong><span class="ne-text">个</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">通用寄存器。</span></li></ul><hr id="o4GyJ" class="ne-hr"><p id="u7fad8ef4" class="ne-p"><strong><span class="ne-text">(3) 指令解析与执行推演</span></strong></p><p id="ucc60603b" class="ne-p"><strong><span class="ne-text">第一步：翻译指令 </span></strong><code class="ne-code"><strong><span class="ne-text">01B2H</span></strong></code><span class="ne-text" style="color: rgb(25, 27, 31)"><br /></span><span class="ne-text" style="color: rgb(25, 27, 31)">将十六进制 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">01B2H</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 展开为 16 位二进制：</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">0000 0001 1011 0010B</span></code></p><ul class="ne-ul"><li id="uc5fcea16" data-lake-index-type="0"><strong><span class="ne-text">最高 6 位</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">000000</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> </span><span id="tOInV" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/33b44e34aa35b8c4ecd0606453ee68e9.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)"> 这是一个 </span><strong><span class="ne-text">R 型指令</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li><li id="u87255643" data-lake-index-type="0"><strong><span class="ne-text">rs 字段（第 9~8 位）</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">01</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> </span><span id="SlMHR" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/33b44e34aa35b8c4ecd0606453ee68e9.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)"> 源操作数寄存器 1。</span></li><li id="u2ffc1b8c" data-lake-index-type="0"><strong><span class="ne-text">rt 字段（第 7~6 位）</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">10</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> </span><span id="Qmb3p" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/33b44e34aa35b8c4ecd0606453ee68e9.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)"> 源操作数寄存器 2。</span></li><li id="udd0925d7" data-lake-index-type="0"><strong><span class="ne-text">rd 字段（第 5~4 位）</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">11</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> </span><span id="oelMO" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/33b44e34aa35b8c4ecd0606453ee68e9.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)"> 目的操作数寄存器 3。</span></li><li id="u0b8cbe0e" data-lake-index-type="0"><strong><span class="ne-text">op1 字段（第 3~0 位）</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">0010</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> </span><span id="EppVW" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/33b44e34aa35b8c4ecd0606453ee68e9.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)"> 题目已知表示</span><strong><span class="ne-text">带符号整数减法</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li></ul><p id="uc9473cee" class="ne-p"><strong><span class="ne-text">功能描述：</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)"><br /></span><span class="ne-text" style="color: rgb(25, 27, 31)">将 1 号寄存器的内容减去 2 号寄存器的内容，结果保存到 3 号寄存器中。即：</span><code class="ne-code"><strong><span class="ne-text" style="color: #DF2A3F">R[3] &lt;- R[1] - R[2]</span></strong></code><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></p><p id="ua81b7a6e" class="ne-p"><strong><span class="ne-text">第二步：执行 </span></strong><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">01B2H</span></code><strong><span class="ne-text">（减法）</span></strong></p><ul class="ne-ul"><li id="udd8100ce" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">算式：</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">R[3] = B052H - 0008H</span></code></li><li id="ufdb6c0e0" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">由于是减去一个正数 </span><span id="JbFd0" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/f5794288c516a700737ae84b490f2ca9.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)">，相当于 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">B052</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 向下减 </span><span id="YywgU" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/f5794288c516a700737ae84b490f2ca9.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)">，结果为 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">B04AH</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li><li id="u968318fd" data-lake-index-type="0"><strong><span class="ne-text">溢出判断</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">B052H</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 最高位为 1，是负数；</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">0008H</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 为正数。负数减正数，结果本就该是负数。结果 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">B04AH</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">（最高位 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">1011...</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 是 1）依然是负数，没有发生符号突变（即双符号位运算不会出现 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">01</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 或 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">10</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">），因此 </span><strong><span class="ne-text">未发生溢出</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li></ul><p id="u84598a64" class="ne-p"><strong><span class="ne-text">第三步：执行 </span></strong><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">01B3H</span></code><strong><span class="ne-text">（乘法）</span></strong></p><ul class="ne-ul"><li id="ua15ca626" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">指令 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">01B3H</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> （</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">0000 0001 1011 0011B</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">）中 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">op1</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 变为 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">0011</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">，即</span><strong><span class="ne-text">带符号整数乘法</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li><li id="u1bef5454" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">算式：</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">R[3] = B052H * 0008H</span></code></li><li id="u87321d82" data-lake-index-type="0"><span class="ne-text" style="color: rgb(25, 27, 31)">乘以 </span><span id="L4zut" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/f5794288c516a700737ae84b490f2ca9.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)">（即 </span><span id="TElyG" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/b43cf3246cf5a153f973430352bd16b4.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)">）相当于在二进制下</span><strong><span class="ne-text">左移 3 位</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li><li id="uaec693fd" data-lake-index-type="0"><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">B052H</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 二进制为 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">1011 0000 0101 0010</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">。左移 3 位后，低位补 0，舍弃高 3 位（</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">101</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">），截断保留 16 位结果为：</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">1000 0010 1001 0000B</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">，即 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">8290H</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li><li id="u59583d76" data-lake-index-type="0"><strong><span class="ne-text">溢出判断</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">：</span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">B052H</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 作为 16 位带符号整数的真值是负数（约等于 </span><span id="isa6G" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/d55a506ce4f6f62f95e14aa239f56333.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)">），乘以 8 后实际真值约为 </span><span id="aGvLX" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/dca306dfa9f986a7def27e0c35dbb06f.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)">。而 16 位带符号整数能表示的最小负数是 </span><span id="eOSW8" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/4cdeb46da5660081bd7604f1bfcf8c48.svg"></span><span class="ne-text" style="color: rgb(25, 27, 31)">。实际结果远远超出了 16 位补码的表示范围，发生了截断（舍弃的高 3 位 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">101</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 与剩下的最高位 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">1</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 并不全同），因此 </span><strong><span class="ne-text">发生溢出</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">。</span></li></ul><hr id="KLc0F" class="ne-hr"><p id="u032a8e57" class="ne-p"><strong><span class="ne-text">(4) 符号扩展的底层逻辑</span></strong></p><p id="u87819025" class="ne-p"><span class="ne-text" style="color: rgb(25, 27, 31)">在地址计算时，应对 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">imm</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 进行 </span><strong><span class="ne-text">符号扩展</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">。<br /></span><strong><span class="ne-text">原因：</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)"> </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">imm</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 代表的是相对基址（如 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">R[rs]</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">）的</span><strong><span class="ne-text">偏移量</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">。在访存指令中，偏移量既可以向后偏移（正数），也可以向前偏移（负数）。因此 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">imm</span></code><span class="ne-text" style="color: rgb(25, 27, 31)"> 必须作为带符号整数处理，扩展到 16 位时要保持其数值和符号不变，就必须进行符号扩展（如果是负数，高位补 1；正数高位补 0）。</span></p><hr id="ZXVQA" class="ne-hr"><p id="uff2da416" class="ne-p"><strong><span class="ne-text">(5) 无条件转移指令的格式</span></strong></p><p id="u39ea36e4" class="ne-p"><span class="ne-text" style="color: rgb(25, 27, 31)">无条件转移指令可以采用 </span><strong><span class="ne-text">J 型</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)"> 格式。 观察表格中 J 型指令的说明 </span><code class="ne-code"><span class="ne-text" style="color: rgb(25, 27, 31)">PC 的低10位 &lt;- target</span></code><span class="ne-text" style="color: rgb(25, 27, 31)">，这就是典型的</span><strong><span class="ne-text">绝对转移</span></strong><span class="ne-text" style="color: rgb(25, 27, 31)">，直接将目标地址硬编码在指令中。</span></p></details>


5. <font style="color:rgb(25, 27, 31);">【2024-43】（严格来说不属于 mips，是 RISC-V 指令系统）假定计算机M字长32位，按字节编址，采用32位定长指令字。指令 add、slli 和 lw 的格式、编码和功能说明如题 43 图 (a) 所示。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/42876865/1781547618489-9f07e032-49d7-4e52-8b62-4c06d6ead208.png)

<font style="color:rgb(25, 27, 31);">其中，R[x] 表示通用寄存器 x 的内容，M[x] 表示地址为 x 的存储单元内容，shamt 为移位位数，imm 为补码表示的偏移量。题 43 图 (b) 给出了计算机 M 的部分数据通路及控制信号（用带箭头虚线表示），其中，A 和 B 分别表示从通用寄存器 rs1 和 rs2 中读出的内容；IR[31:20] 表示指令寄存器中的高 12 位；控制信号 Ext 为 0、1 时扩展器分别实现零扩展、符号扩展，ALUctr 为 000、001、010 时 ALU 分别实现加、减、逻辑左移运算。</font>

![](https://cdn.nlark.com/yuque/0/2026/png/42876865/1781601164361-eb259790-f1ee-4ba9-ad35-466922f5334c.png)

<font style="color:rgb(25, 27, 31);">请回答下列问题。</font>

<font style="color:rgb(25, 27, 31);">(1) 计算机 M 最多有几个通用寄存器？为什么 shamt 占 5 位？（2 分）</font>

<font style="color:rgb(25, 27, 31);">(2) 执行 add 指令时，控制信号 ALUBsrc 的取值应是什么？若 rs1 和 rs2 寄存器内容分别是 8765 4321 H 和 9876 5432 H，则 add 指令执行后，ALU 输出端 F、OF 和 CF 的结果分别是什么？若该 add 指令处理的是无符号整数，则应该根据哪个标志位判断是否溢出？（5 分）</font>

<font style="color:rgb(25, 27, 31);">(3) 执行 slli 指令时，控制信号 Ext 的取值可以是 0 也可以是 1，为什么？（2 分）</font>

<font style="color:rgb(25, 27, 31);">(4) 执行 lw 指令时，控制信号 Ext、ALUctr 的取值分别是什么？（2 分）</font>

<font style="color:rgb(25, 27, 31);">(5) 若一条指令的机器码是 A040 A103 H，则该指令一定是 lw 指令，为什么？若执行该指令时，R[01H] = FFFF A2D0 H，则所读取数据的存储地址是什么？（2 分）</font>

### 
6. <font style="color:rgb(25, 27, 31);">【2024-44】（本题10 分）对于题 43 中的计算机 M，C 语言程序 P 包含的语句 “sum += a[i];” 在 M 中对应的指令序列 S 如下。</font>

```plain
slli r4, r2, 2 // R[r4]←R[r2]<<2
add r4, r3, r4 // R[r4]←R[r3]+R[r4]
lw r5, 0(r4) // R[r5]←M[R[r4]+0]
add r1, r1, r5 // R[r1]←R[r1]+R[r5]
```

<font style="color:rgb(25, 27, 31);">已知变量 i、sum 和数组 a 都为 int 型，通用寄存器 r1~r5 的编号为 01 H ~ 05 H。</font>

<font style="color:rgb(25, 27, 31);">请回答下列问题。</font>

<font style="color:rgb(25, 27, 31);">(1) 根据指令序列 S 中每条指令的功能，写出存放数组 a 的首地址、变量 i、变量 sum 的通用寄存器编号。（3 分）</font>

<font style="color:rgb(25, 27, 31);">(2) 已知 M 为小端方式计算机，采用页式存储管理方式，页大小为 4 KB。若执行到指令序列 S 中第一条指令时，i=5，且 r1 和 r3 的内容分别为 0000 1332 H 和 0013 DFF0 H，从地址 0013 DFF0 H 开始的存储单元内容如题 44 图所示，则执行 “sum+=a[i];” 语句后，a[i] 的地址、a[i] 和 sum 的机器数分别是什么（用十六进制表示）？a[i] 所在页的页号是多少？此次执行中，数组 a 至少存放在几页中？（5 分）</font>

$ \begin{array}{|c|c|c|c|c|c|c|c|c|}
\hline
\text{地址} & 0 & 1 & 2 & 3 & 4 & 5 & 6 & 7 \\ \hline
\text{0013 DFF0} & \text{FF} & \text{FF} & \text{FF} & \text{7C} & \text{70} & \text{FE} & \text{FF} & \text{FF} \\ \hline
\text{0013 DFF8} & \text{00} & \text{00} & \text{00} & \text{0C} & \text{3C} & \text{02} & \text{01} & \text{FF} \\ \hline
\text{0013 E000} & \text{F0} & \text{F1} & \text{00} & \text{00} & \text{DC} & \text{EC} & \text{FF} & \text{FF} \\ \hline
\text{0013 E008} & \text{FF} & \text{FF} & \text{01} & \text{02} & \text{00} & \text{00} & \text{01} & \text{02} \\ \hline
\end{array} $

<font style="color:rgb(25, 27, 31);">(3) 指令 “slli r4, r2, 2” 的机器码是什么（用十六进制表示）？若数组 a 改为 short 类型，则指令序列 S 中 slli 指令的汇编形式应是什么？（2 分）</font>

<font style="color:rgb(25, 27, 31);"></font>

<font style="color:rgb(25, 27, 31);"></font>

<font style="color:rgb(25, 27, 31);"></font>



