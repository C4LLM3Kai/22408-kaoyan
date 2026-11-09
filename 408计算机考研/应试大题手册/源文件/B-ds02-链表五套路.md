## 链表题五套路总览
**考频**：2009/2012/2015/2019｜链表算法题固定 13–15 分，四个年份四道题，五套路全覆盖
**必背结论**
- 动笔前先确认两件事：带不带头结点（大题默认带）、题干的域名与数据域类型（`link` 还是 `next`，`int` 还是 `char`），照抄不改。
- 五套路按「改什么」分类：双指针改速度与间距、长度差对齐改起点、头插法改链接方向、前驱删除改指针停位、拆分合并改表的条数。
- 复杂度写两行就够：时间扫几遍就是几个 $O(n)$；没开辅助数组或辅助链表就是 $O(1)$，开了就是 $O(n)$，求表长的那一趟也要算进时间。
- 空间 $O(1)$ 是隐藏评分点：题目出现「空间复杂度为 O(1)」「尽可能高效」，就不许开等长数组。
- 兜底第 0 档：转数组（求长 → 存数组 → 按下标做 → 倒着重建成链表），思路分先拿到，绝不空着。
- 答题四步固定：结点定义 → 设计思想 → 代码（10 到 15 行量级）→ 时空复杂度，四段各占分。
- 得分口径：这四道题满分 13 分或 15 分（按年份），思路对且代码写出来约 10 分；只写思路不写代码分数很低；结点定义单独有分。

| 套路 | 识别特征 | 真题年份 | 代码骨架一句话 |
|---|---|---|---|
| 双指针 | 倒数第 k 个、中点、判环、两条链表 | 2009 / 2019 | 快指针先走 k 步，再与慢指针同步走 |
| 头插法逆置 | 逆序、反转、后半段翻转 | 2019 | 先断链，再逐个摘下往哨兵后面插 |
| 长度差对齐 | 两条链表求第一个公共结点 | 2012 | 长的先走长度差步，再同时走 |
| 前驱删除 | 去重、删满足条件的结点 | 2015 | cur 停在前驱，删时不动、留时才走 |
| 拆分+重排+合并 | 要求 O(1) 空间重排、判回文 | 2019 | 找中点 → 逆后半段 → 交替合并 |

**模板/流水线**
本章零件代码共用这一份结点定义；四道真题的题干域名与类型各不相同（2009 用 `link`、2012 用 `next` 且 `data` 为 `char`、2015 用 `link`），那三段各自带一份题干版定义，照抄即可：
```c
typedef struct LNode {
    int data;                    /* 题干是 char 就写 char */
    struct LNode *next;          /* 题干叫 link 就写 link */
} LNode, *LinkList;
```
! 返回值类型按题干定：2009 返回 int、2012 返回结点指针、2015 无返回值·题目说「不改变链表」时不许逆置、不许新建结点·「尽可能高效」既管时间也管空间，开数组前先看有没有 O(1) 字样

## 双指针 · 倒数第 k 个
**考频**：2009（15分）｜双指针母题，2012、2019 都是它的变体，不会它后面全崩
**必背结论**
- 识别特征：题面出现「倒数第 k 个」「中间位置」「环」这类位置词，而不是「第几个值」。
- 推进规则：fast 先走 k 步，之后 fast、slow 一起走；fast 到 NULL 时 slow 正好落后 k 步，落在倒数第 k 个。
- 快指针先走的那一轮必须带 `fast != NULL`：k 大于表长时提前停，否则越界。
- 判「不存在」写 `if (slow == list) return 0`：慢指针一步都没动，就是 k 超过了表长，不是 `!=`。
- 表长 n 的链表从头结点到 NULL 共 n+1 步，所以 k 只能取 1 到 n；k 取 n 时 slow 最后停在第一个数据结点。
- 写法二：把两轮合成一轮 `while (fast != NULL) { fast = fast->link; if (k-- <= 0) slow = slow->link; }`，时空复杂度与写法一完全相同，考场挑顺手的写。
**模板/流水线**
```c
/* 2009：带头结点单链表，求倒数第 k 个结点；成功输出 data 返回 1，否则返回 0 */
typedef struct LNode {
    int data;
    struct LNode *link;                    /* 注：题干域名就是 link，不是 next */
} LNode, *LinkList;

int FindKth(LinkList list, int k) {
    LNode *fast = list, *slow = list;      /* 两个都从头结点出发 */
    while (k > 0 && fast != NULL) {        /* 注：fast != NULL 不能省 */
        fast = fast->link;
        k--;
    }
    while (fast != NULL) {                 /* 同步走：fast 到 NULL 时 slow 即答案 */
        fast = fast->link;
        slow = slow->link;
    }
    if (slow == list) return 0;            /* 注：慢指针没动 → 倒数第 k 个不存在 */
    printf("%d\n", slow->data);
    return 1;
}
```
> 复杂度：时间 $O(n)$，只扫一遍；空间 $O(1)$，只有两个指针。

! 漏写 `fast != NULL` 是这道题第一大坑，k 超长直接崩·判不存在写成 `if (slow != list)` 逻辑正好反，找到答案时反而返回 0·k 等于表长时 slow 停在第一个数据结点，不是头结点

## 快慢指针 · 求中点
**考频**：2019（13分）｜重排链表三步里的第一步，丢了中点整道题 13 分归零
**必背结论**
- 识别特征：要把链表「从中间劈开」「分前后两半」「判断回文」，第一步都是求中点。
- 循环条件必须写两个：`fast != NULL && fast->next != NULL`；少了后一个，`fast->next->next` 在最后一轮越界。
- 奇数个结点：slow 停在正中间；偶数个结点：slow 停在前半段的最后一个。奇偶都不含头结点。
- 起点取 `head` 本身而不是 `head->next`，否则上面的奇偶结论整体偏移一格。
- 求中点只走一遍链表，与后面的逆置、合并加起来仍是 $O(n)$，不要写成 $O(n\log n)$。
- 要「后半段」则起点是 `slow->next`；要「前半段含中点」则终点是 slow 本身。
**模板/流水线**
```c
/* 求中点：奇数个停正中间，偶数个停前半段最后一个 */
LNode *FindMid(LinkList head) {            /* head 是头结点 */
    LNode *fast = head, *slow = head;
    while (fast != NULL && fast->next != NULL) {   /* 注：两个条件都要 */
        fast = fast->next->next;                   /* 快指针一次两步 */
        slow = slow->next;                         /* 慢指针一次一步 */
    }
    return slow;
}
```
> 复杂度：时间 $O(n)$，快指针走完半程即结束；空间 $O(1)$。

! 只写 `fast != NULL` 是最高频错误，偶数个时 `fast->next` 为空再取 next 就越界·求中点后若还要判「slow 是不是最后一个」，偶数个时 slow 后面还有结点·中点用返回值传出去，别用全局量

## 双指针 · 判环与入环点
**考频**：选择常考，大题未考｜服务于 2019 那类快慢指针推理，是双指针的第三种推进规则
**必背结论**
- 有环必相遇：fast 每轮 2 步、slow 每轮 1 步，环内相对速度是 1，最迟一圈内追上。
- 无环的退出条件是两个：`fast == NULL || fast->next == NULL`，判断顺序不能反，先判 fast 再判 fast->next。
- 入环点公式：相遇后把一个指针放回起点，两者都改成每轮 1 步，再次相遇处就是入环点。
- 只需记住结论：起点到入环点的距离，等于相遇点到入环点的距离（按环长取模）。
- 复杂度：时间 $O(n)$，无环时快指针走约 n/2 轮就出界；空间 $O(1)$。
- 同型延伸「删除环」：先按上式找到入环点，再从入环点绕一圈回到它自己，把那个尾结点的 next 置空。
**模板/流水线**
```c
/* 判环：有环返回 1 */
int HasCycle(LinkList head) {              /* head 是头结点 */
    LNode *fast = head, *slow = head;
    while (fast != NULL && fast->next != NULL) {
        fast = fast->next->next;
        slow = slow->next;
        if (fast == slow) return 1;
    }
    return 0;
}
/* 求入环点：无环返回 NULL */
LNode *CycleEntry(LinkList head) {
    LNode *fast = head, *slow = head;
    while (fast != NULL && fast->next != NULL) {
        fast = fast->next->next;
        slow = slow->next;
        if (fast == slow) break;           /* 第一次相遇 */
    }
    if (fast == NULL || fast->next == NULL) return NULL;   /* 无环 */
    slow = head;                           /* 一个指针回头结点 */
    while (slow != fast) {                 /* 同步走，再遇即入环点 */
        slow = slow->next;
        fast = fast->next;
    }
    return slow;
}
```
! 相遇后忘记把指针放回起点，直接返回相遇点（那是环内某点，不是入环点）·无环时 break 后 fast 为 NULL，要先判空再进第二段·先判 `fast->next` 后判 `fast` 会先解引用空指针

## 头插法 · 整体逆置
**考频**：2019（13分）｜重排链表的核心零件，也是「逆序输出、逆置」的通杀模板
**必背结论**
- 识别特征：要「逆序」「反转」「从尾往头」，或题目要求 $O(1)$ 空间重排。
- 五步固定顺序：断头 `head->next = NULL` → 存后继 `temp = cur->next` → 前插 `cur->next = head->next` → 挂回 `head->next = cur` → 推进 `cur = temp`。
- 第一步最容易漏：不断头，头插就变成在原串上打转，直接死循环。
- 逆置后原来的第一个结点变成最后一个，它的 next 由第一步置空来保证。
- 适用面：凡要「反向访问」又限空间 $O(1)$（逆序输出、判回文、两数相加、重排），第一刀都是它。
- 递归写法也能逆置，但递归栈会让空间变成 $O(n)$；题干要 $O(1)$ 就只认迭代版。
**模板/流水线**
```c
/* 头插法整体逆置：空间 O(1)，不新建结点 */
void ReverseAll(LinkList head) {           /* head 是头结点，本身不参与逆置 */
    LNode *cur = head->next;               /* cur 指向第一个数据结点 */
    head->next = NULL;                     /* 注：第一步先断开，它成了已逆置串的哨兵 */
    while (cur != NULL) {
        LNode *temp = cur->next;           /* ① 先存后继，不存就断链 */
        cur->next = head->next;            /* ② cur 插到已逆置串最前面 */
        head->next = cur;                  /* ③ 头结点接上 cur */
        cur = temp;                        /* ④ 推进，不推进就死循环 */
    }
}
```
> 复杂度：时间 $O(n)$，每个结点摘下再插入一次；空间 $O(1)$，只借用 temp。

! `head->next = NULL` 漏掉，逆置后表尾不空、遍历停不下来·不存 temp 直接改 `cur->next`，后半段整条丢失·把 head 也当成要逆置的结点，头结点被插进数据结点中间

## 头插法 · 局部逆置
**考频**：2019（13分）｜同一段头插代码，把 head 换成子链前驱就是局部逆置
**必背结论**
- 三段式：切（找到子链前驱 pre、子链第一个 cur）→ 逆（对 cur 之后的结点做头插）→ 接（pre->next 已自动指向新子链头）。
- 局部逆置时 cur 固定不动，它就是逆置后的子链尾；真正在动的是 cur->next 之后的结点。
- 接回不需要额外指针：pre->next 始终跟着最新插入的结点走。
- m 等于 1 或 n 等于表长时同样成立，不用特判（再加哑结点就彻底统一）。
- 下笔前先画四个指针：pre（子链前驱）、cur（子链首，逆置后成尾）、temp（临时）、以及不动的表头 L。
- 与整体逆置的差别只有一个：插入位置从「表头之后」改成「pre 之后」，其余四步一模一样。
**模板/流水线**
```c
/* 逆置第 m 到第 n 个数据结点（1 <= m <= n <= 表长），返回表头 */
LNode *ReverseRange(LinkList L, int m, int n) {
    LNode *pre = L;                        /* pre 最终停在 m-1 号位置 */
    int i;
    for (i = 1; i < m && pre != NULL; i++) pre = pre->next;
    if (pre == NULL || pre->next == NULL) return L;   /* m 越界，原样返回 */
    LNode *cur = pre->next;                /* 子链第一个：逆置后它变成子链尾 */
    for (i = 0; i < n - m; i++) {
        LNode *temp = cur->next;
        if (temp == NULL) break;           /* n 超过表长就提前停 */
        cur->next = temp->next;            /* 把 temp 从 cur 后面摘下来 */
        temp->next = pre->next;            /* 头插到 pre 后面 */
        pre->next = temp;
    }
    return L;
}
```
> 复杂度：时间 $O(n)$（找 pre 用 $O(m)$，逆置用 $O(n-m)$）；空间 $O(1)$。

! 忘记先保存子链尾（cur）就逆置，接不回后半段·m 越界时不返回原表而继续走，野指针崩溃·内层用 `n-m` 而不是 `n-m+1` 计数，会多逆一个结点

## 长度差对齐 · 公共结点
**考频**：2012（13分）｜双指针的第二种推进规则，改的是起点而不是速度
**必背结论**
- 识别特征：两条链表、求「第一个公共结点」「交点」「共同后缀的起始位置」。
- 交点之后两表完全重合，所以长度差就等于交点之前那段的结点数差；长的先走差值步，两指针距表尾就等距了。
- 求表长要走两趟，必须算进复杂度：时间 $O(m+n)$，不是 $O(n)$。
- 循环写 `while (p != q)` 一起走，退出即交点；无交点时两者同时为 NULL，天然返回 NULL，不用特判。
- 长度差比较用严格大于：写成 `>=` 会多走一步（7 和 5 时走 3 步而不是 2 步）。
- 命名用 p、q，不用 fast、slow——谁长谁短事先不知道。
- 两表等长时长度差为 0，两个 while 都不执行，直接进入同步走，代码不用改。
- 备选：用 map 或哈希表存第一条链表的结点地址再扫第二条，时间 $O(m+n)$、空间 $O(n)$；硬性要求 $O(1)$ 空间时不能用。
**模板/流水线**
```c
/* 2012：两条带头结点单链表（data 为 char），求共同后缀起始结点；无公共结点返回 NULL */
typedef struct LNode {
    char data;                             /* 注：题干是字符类型，不是 int */
    struct LNode *next;                    /* 注：题干域名是 next */
} LNode, *LinkList;

int Length(LinkList L) {
    int n = 0;
    LNode *cur = L->next;                  /* 头结点不计入长度 */
    while (cur != NULL) { n++; cur = cur->next; }
    return n;
}
LNode *FindCommon(LinkList str1, LinkList str2) {
    int len1 = Length(str1), len2 = Length(str2);
    LNode *p = str1, *q = str2;            /* 注：用 p、q，不用 fast、slow */
    while (len1 > len2) { p = p->next; len1--; }   /* 注：严格大于，不是大于等于 */
    while (len2 > len1) { q = q->next; len2--; }
    while (p != q) { p = p->next; q = q->next; }
    return p;                              /* 无交点时 p、q 同时为 NULL */
}
```
> 复杂度：时间 $O(m+n)$，两趟求长加一趟同步走；空间 $O(1)$，两个指针。

! 返回结点的值而不是结点指针，题目要的是「起始位置 p」·长度差写成 `>=` 多走一步，交点永远差一格·data 定义成 int 而题干是 char，结点定义分直接丢

## 前驱删除 · 绝对值去重
**考频**：2015（15分）｜删结点类题的唯一起手式，「去重、删满足条件」全套它
**必背结论**
- 单链表删结点必须停在前驱：cur 从头结点出发，判断的永远是 `cur->link` 指向的那个结点，这样第一个数据结点也在删除范围内。
- 删分支里 cur 不动：`cur->link` 已被改写成下下个结点，此时再后移就漏判它。
- 留分支里才写 `cur = cur->link`。
- 辅助数组开 n+1 个（题干给 `|data| <= n`，下标最大取到 n），并且必须显式清零。
- 题干说「时间复杂度尽可能高效」等于允许用 $O(n)$ 空间换 $O(n)$ 时间。
- 判定用的是绝对值：-15 与 15 算同一个值，保留先出现的那个，顺序按原表，不许排序。
**模板/流水线**
```c
/* 2015：删除绝对值相等的多余结点，仅保留第一次出现；题干给 |data| <= n */
typedef struct LNode {
    int data;
    struct LNode *link;                    /* 注：题干域名是 link */
} LNode, *LinkList;

void DeleteDup(LinkList head, int n) {
    int *a = (int *)malloc(sizeof(int) * (n + 1));   /* 注：下标取到 n，开 n+1 个 */
    int i;
    for (i = 0; i <= n; i++) a[i] = 0;               /* 注：必须清零，malloc 不清零 */
    LNode *cur = head;                               /* 注：从头结点出发：删除要停在前驱 */
    while (cur->link != NULL) {
        int v = cur->link->data;
        if (v < 0) v = -v;                           /* 取绝对值，判定用的是绝对值 */
        if (a[v]) {                                  /* 出现过 → 删掉它 */
            LNode *q = cur->link;
            cur->link = q->link;                     /* 注：cur 不动 */
            free(q);
        } else {                                     /* 第一次出现 → 留下 */
            a[v] = 1;
            cur = cur->link;                         /* 注：只有这里才后移 */
        }
    }
    free(a);                                         /* 辅助数组记得还 */
}
```
> 复杂度：时间 $O(n)$，每个结点只判一次；空间 $O(n)$，一个 n+1 的标记数组。

! 数组开 n 个，下标 n 越界（题目给的界是小于等于 n，这是送分点也是送命题）·删完还让 cur 后移，连续两个重复值时漏删第二个·用原值当数组下标，负数直接越界（必须先取绝对值）

## 拆分 · 重排 · 合并
**考频**：2019（13分）｜全书代码最长的一道，三步拼装，考的是零件熟不熟
**必背结论**
- 三步：找中点 → 后半段头插逆置 → 两半交替合并；空间 $O(1)$，时间 $O(n)$。
- 拆链先取后断：先 `q = slow->next`，再 `slow->next = NULL`；顺序反了就永远找不到后半段。
- 合并循环以后半段为准：`while (q != NULL)`；奇数个结点时前半段会多剩一个。
- 循环结束后必须补 `tail->next = p`，漏了奇数个就丢掉正中间那个结点。
- 逆置时 slow 当哑结点用，它自己不参与逆置，正好成为后半段逆置后的前驱。
- 同型变式「判断回文链表」：找中点 + 逆后半段 + 逐个比较，不合并、不补 p，遇到不等就立刻返回假。
- 复杂度写「链表近似走两遍，常数忽略，仍是 $O(n)$」，别写成 $O(n\log n)$。
**模板/流水线**
```c
/* 2019：L = (a1..an) 重排为 (a1, an, a2, an-1, ...)，空间 O(1) */
typedef struct node {
    int data;
    struct node *next;
} node;
void Reorder(node *L) {                    /* L 是头结点 */
    /* ① 找中点：偶数个停前半段最后一个，奇数个停正中间 */
    node *fast = L, *slow = L;
    while (fast != NULL && fast->next != NULL) {
        fast = fast->next->next;
        slow = slow->next;
    }
    /* ② 后半段头插逆置：slow 当哨兵，自己不参与逆置 */
    node *cur = slow->next;
    slow->next = NULL;
    while (cur != NULL) {
        node *temp = cur->next;
        cur->next = slow->next;
        slow->next = cur;
        cur = temp;
    }
    /* ③ 拆成两条链表：先取后断，顺序不能反 */
    node *q = slow->next;                  /* 先取后半段 */
    node *p = L->next;                     /* 前半段第一个 */
    node *tail = L;                        /* 合并时的尾指针 */
    slow->next = NULL;                     /* 再断开 */
    /* ④ 交替合并：以后半段（短的）为循环条件 */
    while (q != NULL) {
        tail->next = p;  p = p->next;  tail = tail->next;
        tail->next = q;  q = q->next;  tail = tail->next;
    }
    tail->next = p;                        /* 注：奇数个时补最后一个，偶数个接 NULL 无害 */
}
```
> 复杂度：时间 $O(n)$，链表近似走两遍（常数忽略）；空间 $O(1)$，只借用 4 个指针。

! 先断后取，q 恒为 NULL，后半段整条丢失·循环条件写成 `p != NULL`，奇数个时 p 先空、访问 `p->next` 崩溃·循环外漏写 `tail->next = p`，正中间那个结点被丢掉·把 slow 也一起逆置进去，后半段多一个结点错位

## 哨兵结点与 free 纪律
**考频**：2009–2019（通用）｜不直接得分，但决定代码能否一次写对、内存题会不会被扣
**必背结论**
- 哑结点的作用只有一个：让「第一个结点」也有前驱，删除和插入都不用特判表头。
- 题目给的是不带头结点的链表时：函数第一句建哑结点，最后 `return dummy.next`，中间逻辑与带头结点完全一样。
- 哑结点放栈上（`LNode dummy;`）最省事，不用 malloc，也就不存在忘 free 的问题。
- 删掉的结点要 free，但顺序是先让 cur 走、再 free：free 之后再读 `cur->next` 就是野指针。
- 返回 void 的题就地改链；返回 LinkList 的题要返回新表头（哑结点的 next）。
- 头结点与哑结点不是一回事：头结点是题干给的、真实存在的结点；哑结点是你临时加的、用完可以丢的结点。
**模板/流水线**
```c
/* 哨兵法：删除所有值为 x 的结点；链表不带头结点也能统一处理 */
LinkList DeleteX(LinkList L, int x) {
    LNode dummy;                           /* 注：栈上哑结点：不用 malloc，不用 free */
    dummy.next = L;                        /* 哑结点指向原来的第一个结点 */
    LNode *pre = &dummy, *cur = L;
    while (cur != NULL) {
        if (cur->data == x) {
            pre->next = cur->next;         /* 前驱越过 cur */
            LNode *del = cur;
            cur = cur->next;               /* 注：先让 cur 走 */
            free(del);                     /* 注：再 free，顺序反了就野指针 */
        } else {
            pre = cur;                     /* 只有留下时 pre 才跟着走 */
            cur = cur->next;
        }
    }
    return dummy.next;                     /* 新表头：原来第一个可能就是被删的那个 */
}
```
> 复杂度：时间 $O(n)$ 一遍；空间 $O(1)$，哑结点在栈上。

! free 之后又用 `cur->next`，野指针（最容易被扣分的一处）·用 malloc 建哑结点却忘 free，内存泄漏·返回 L 而不是 `dummy.next`，删掉第一个结点后表头就丢了

## 树 · 递归遍历四件套
**考频**：2014/2017/2022/2026｜树的大题 100% 落在递归或遍历上，四件套是唯一入口
**必背结论**
- 四件套：结点定义（照抄题干）→ 递归出口（`if (T == NULL) return;` 永远第一句）→ 单层做什么（访问、累加、判断）→ 递归左右子树的顺序（决定先序、中序、后序）。
- 先序、中序、后序只差「访问根」那一行放在两次递归之前、之间、之后。
- 递归函数三种形态：void 加全局量（最省事，考场首选）、返回 int（求和、计数、高度）、返回结点指针（查找、插入）。
- 全局量就写在函数外面，不用 static，也不用引用参数。
- 先写出口再写函数体：出口写错整题 0 分，而树题出口只有 `T == NULL` 一种形态。
- 前序适合自顶向下传参（传深度、传路径），后序适合自底向上收集（返回高度、返回 WPL）。
**模板/流水线**
```c
/* 二叉链表结点定义：2014 用 weight、2017 用 char data[10]、2022 用顺序存储，都按题干换 */
typedef struct BiTNode {
    int data;
    struct BiTNode *lchild, *rchild;
} BiTNode, *BiTree;

/* 形态一：void + 全局量 —— 遍历、计数、求和的万能壳 */
int cnt = 0;                               /* 全局量写在函数外 */
void PreOrder(BiTree T) {
    if (T == NULL) return;                 /* ① 递归出口永远第一句 */
    cnt++;                                 /* ② 单层：访问根（先序放这里） */
    PreOrder(T->lchild);                   /* ③ 左子树 */
    PreOrder(T->rchild);                   /* ④ 右子树 */
}
/* 中序：把 cnt++ 挪到两句递归之间；后序：挪到最后。三行位置决定一切 */

/* 形态二：返回 int —— 结点数、高度 */
int Count(BiTree T) {
    if (T == NULL) return 0;
    return Count(T->lchild) + Count(T->rchild) + 1;
}
int Height(BiTree T) {
    if (T == NULL) return 0;               /* 空树高 0，单结点高 1 */
    int l = Height(T->lchild), r = Height(T->rchild);
    return (l > r ? l : r) + 1;
}
```
> 复杂度：时间 $O(n)$，每个结点访问一次；空间 $O(h)$，递归栈深度等于树高，最坏 $O(n)$。

! 递归出口写成 `if (T->lchild == NULL)` 当出口，叶子结点会漏·全局量定义在函数内，每层递归都被重置成 0·高度空树返回 0 还是 -1 必须全局统一，混用会让所有高度整体差 1

## 树 · 带权路径长度 WPL
**考频**：2014（13分）｜树题里代码最短、最好背的一道，递归不到十行就满分
**必背结论**
- 定义：WPL 是所有叶结点的「权值 × 深度」之和；根深度取 0 还是 1 都行，但全文必须一致（取 0 时单结点树 WPL 为 0）。
- 叶子判定：`T->left == NULL && T->right == NULL`，两个都要判，只判一个会把单分支结点当叶子。
- 递归参数必须多带一个 depth：往下传 `depth + 1`，回溯时不用减，这就是「递归自带路径」。
- 非叶结点不贡献权值，只贡献深度。
- 用层次遍历按层号算 WPL 能得到同一结果，两个答案互验，用来检查递归写没写错。
- 左右子树的递归顺序不影响结果，先左后右或先右后左都行，不必纠结。
**模板/流水线**
```c
/* 2014：结点 weight 存权值，求 WPL */
typedef struct BiTNode {
    int weight;
    struct BiTNode *left, *right;
} BiTNode, *BiTree;

int wpl(BiTree T, int depth) {
    if (T == NULL) return 0;                            /* 空树不贡献 */
    if (T->left == NULL && T->right == NULL)            /* 注：叶子判定要左右都空 */
        return T->weight * depth;                       /* 权值 × 深度 */
    return wpl(T->left, depth + 1) + wpl(T->right, depth + 1);
}
int WPL(BiTree T) { return wpl(T, 0); }                 /* 根深度取 0 */
```
> 复杂度：时间 $O(n)$，每个结点恰好进一次；空间 $O(h)$ 递归栈。

! 只判 `T->left == NULL` 就当叶子，单分支结点被误算·根深度取 1 却在公式里又减 1，结果差一个常数·把非叶结点的 weight 也累加进去（题干明说只有叶结点存非负权值）

## 树 · 中序遍历转中缀
**考频**：2017（15分）｜遍历加括号的综合题，考的是中序框架不是新算法
**必背结论**
- 中序序列天然就是中缀表达式的顺序：左子树 → 根（运算符）→ 右子树。
- 括号规则：根那一层不加；只要不是根、且子树里还有运算符，整棵子表达式外面套一对括号。
- 叶结点是操作数，直接输出，绝不加括号。
- 递归参数带 depth（层号），靠 depth 判断「是不是根」，比另设标志位干净。
- 结点 data 是 `char[10]`，用 `%s` 输出，不是 `%c`。
- 单目运算符（负号）只有一个孩子，只输出一侧，括号仍要成套；左右孩子都空才是操作数。
- 反向题（中缀转表达式树）是同一套栈操作：操作数建叶结点入栈，运算符弹两棵子树做左右孩子。
**模板/流水线**
```c
/* 2017：表达式树转等价中缀表达式，结点 data 是 char[10] */
typedef struct node {
    char data[10];
    struct node *left, *right;
} BTree;

void InOrder(BTree *T, int depth) {        /* 首次调用传 depth = 0 */
    if (T == NULL) return;
    if (T->left == NULL && T->right == NULL) {   /* 叶子：操作数，直接输出 */
        printf("%s", T->data);
        return;
    }
    if (depth > 0) printf("(");                  /* 注：非根的子表达式整体加括号 */
    InOrder(T->left, depth + 1);                 /* 左子树 */
    printf("%s", T->data);                       /* 根：运算符放中间 */
    InOrder(T->right, depth + 1);                /* 右子树 */
    if (depth > 0) printf(")");                  /* 与左括号配对 */
}
/* 调用：InOrder(T, 0) —— 根这一层不加括号 */
```
> 复杂度：时间 $O(n)$，每个结点输出一次；空间 $O(h)$ 递归栈。

! 给根也加括号，输出最外层多一对·给叶子也加括号，操作数变成 (a)·用 `%c` 输出 char[10]，只打出首字符·括号只加左边忘了右边，左右不配对

## 树 · 二叉搜索树判定
**考频**：2022（13分）｜顺序存储加 BST 判定的组合，坑全在下标和 -1 上
**必背结论**
- 顺序存储下标：根为 0，下标 i 的左孩子 2i+1、右孩子 2i+2；i 大于等于 ElemNum 即越界（空）。
- -1 表示空结点：判值之前必须先判不等于 -1，否则 -1 会当成合法值参与比较。
- 判定等价于「中序遍历序列严格递增」：递归中用全局 pre 记住前驱值，当前值小于等于 pre 就返回 false。
- 权值为正整数，pre 初值取 -1 就够（若权值可能为 0，初值要取更小的负数）。
- 不要用「左孩子小于根、根小于右孩子」的局部判定，那只保证局部有序，不保证整棵是 BST，这是经典错法。
- 另一条等价路线：先中序遍历把非 -1 的值存进数组，再判数组严格递增；时间仍 $O(n)$、空间 $O(n)$，比全局 pre 好写但多花空间。
**模板/流水线**
```c
/* 2022：顺序存储的二叉树，SqBiTNode[] 存值，-1 表示空，判是否 BST
   MAX_SIZE 题干已定义为常量，这里不再重复定义 */
typedef struct {
    int SqBiTNode[MAX_SIZE];
    int ElemNum;                           /* 实际占用的数组元素个数 */
} SqBiTree;

int pre = -1;                              /* 中序前驱的值；权值为正整数，初值 -1 可用 */
int JudgeBST(SqBiTree T, int i) {
    if (i >= T.ElemNum) return 1;                  /* 越界当作空树，是 BST */
    if (!JudgeBST(T, 2 * i + 1)) return 0;         /* 左子树不是就整体不是 */
    if (T.SqBiTNode[i] != -1) {                    /* 注：-1 是空结点，必须跳过 */
        if (T.SqBiTNode[i] <= pre) return 0;       /* 中序必须严格递增 */
        pre = T.SqBiTNode[i];
    }
    return JudgeBST(T, 2 * i + 2);                 /* 右子树 */
}
/* 调用：pre = -1; JudgeBST(T, 0) */
```
> 复杂度：时间 $O(n)$，每个数组元素访问一次；空间 $O(h)$，递归深度不超过树高。

! 忘判不等于 -1，-1 被当值比较导致误判·pre 用局部变量，每次递归重置，判定永远通过·判成大于等于而不是严格大于，重复值被当成合法 BST·下标写成 2i、2i+1（那是 1 起编号的写法）

## 树 · 层次遍历
**考频**：选择常考，大题未考｜2014 的 WPL 题可以用它替代递归，求宽度、判完全二叉树也靠这一层队列
**必背结论**
- 队列用数组实现：front、rear 两个下标，入队 rear 加一，出队 front 加一，容量取 MAX_SIZE 或 100。
- 循环条件是 `front < rear`（队非空）；队空就是 front 等于 rear，入队前先确认数组没满。
- 出队时才判叶子、才累加；入队时判空，空孩子不入队。
- 想按层算 WPL：每轮先记 `cnt = rear - front`（本层结点数），内层循环正好处理一层，depth 在外层加一。
- 数组队列不能循环复用，rear 一路只增不减，容量必须按最多结点数给（满二叉树约 n）。
- 判完全二叉树也用它：一旦出队遇到空孩子，此后出队的结点必须全是叶子，否则不是完全二叉树。
**模板/流水线**
```c
/* 层次遍历 + 按层求 WPL（非递归版） */
typedef struct BiTNode {
    int weight;
    struct BiTNode *lchild, *rchild;
} BiTNode, *BiTree;

int WPL_Level(BiTree T) {
    BiTree q[100];
    int front = 0, rear = 0, depth = 0, sum = 0, i;
    if (T == NULL) return 0;
    q[rear++] = T;                          /* 根入队 */
    while (front < rear) {
        int cnt = rear - front;             /* 注：本层结点数 */
        for (i = 0; i < cnt; i++) {
            BiTree p = q[front++];          /* 出队 */
            if (p->lchild == NULL && p->rchild == NULL)
                sum += p->weight * depth;   /* 叶子：权值 × 当前层号 */
            if (p->lchild) q[rear++] = p->lchild;
            if (p->rchild) q[rear++] = p->rchild;
        }
        depth++;                            /* 本层处理完，层号加一 */
    }
    return sum;
}
```
> 复杂度：时间 $O(n)$；空间 $O(n)$，队列最多存一层结点（满二叉树最宽层约 n/2）。

! 队列容量开小了，满二叉树最后一层就溢出·depth 加一的位置写错（写进内层 for 或干脆忘了），同一层叶子被算成不同深度·出队前不判空、空孩子也入队，rear 一路冲出数组

## 树 · 线索二叉树
**考频**：2026｜最新一年考「遍历与线索二叉树」，2027 极可能延续
**必背结论**
- 线索化的本质：把 n+1 个空指针域改成指向前驱、后继的线索，用 ltag、rtag 区分「孩子」和「线索」，1 表示线索。
- 中序线索化就是中序遍历，在「访问根」的位置补两件事：左空则建前驱线索，前驱右空则建后继线索，然后 pre 后移。
- 必须有一个全局 pre 指向「刚访问过的结点」，初值 NULL。
- 中序后继：rtag 等于 1 直接取 rchild；rtag 等于 0 则是右子树中最左下的结点。
- 线索化收尾要给中序最后一个结点补 `rtag = 1`，否则它的 rtag 仍是 0、rchild 又是空，求后继时解引用空指针。
- 线索化之后中序遍历不用栈、不用递归，顺着 rchild 一路走，空间 $O(1)$。
- 中序前驱对称：ltag 等于 1 直接取 lchild；ltag 等于 0 则是左子树中最右下的结点。
**模板/流水线**
```c
/* 中序线索二叉树：ltag=1 表示 lchild 存前驱，rtag=1 表示 rchild 存后继 */
typedef struct ThreadNode {
    int data;
    struct ThreadNode *lchild, *rchild;
    int ltag, rtag;                        /* 建树时把两者都置 0 */
} ThreadNode, *ThreadTree;

ThreadNode *pre = NULL;                    /* 全局：刚访问过的结点 */

void InThread(ThreadTree p) {
    if (p == NULL) return;
    InThread(p->lchild);                   /* 左子树线索化 */
    if (p->lchild == NULL) {               /* 左空 → 建前驱线索 */
        p->lchild = pre;  p->ltag = 1;
    }
    if (pre != NULL && pre->rchild == NULL) {   /* 前驱右空 → 建后继线索 */
        pre->rchild = p;  pre->rtag = 1;
    }
    pre = p;                               /* 注：访问完就后移 */
    InThread(p->rchild);                   /* 右子树线索化 */
}

/* 线索化收尾：中序最后一个结点没有后继，必须显式把 rtag 置 1，否则遍历到它就崩 */
void CreateInThread(ThreadTree T) {
    pre = NULL;
    if (T != NULL) {
        InThread(T);
        pre->rchild = NULL;
        pre->rtag = 1;
    }
}

/* 中序第一个结点：从根一路向左 */
ThreadNode *FirstNode(ThreadNode *p) {
    while (p != NULL && p->ltag == 0 && p->lchild != NULL) p = p->lchild;
    return p;
}
/* 中序后继：rtag=1 直接取 rchild，否则是右子树的最左下结点 */
ThreadNode *NextNode(ThreadNode *p) {
    if (p->rtag == 1) return p->rchild;
    return FirstNode(p->rchild);
}
/* 线索树上不用栈、不用递归的中序遍历 */
void InOrderThread(ThreadTree T) {
    ThreadNode *p;
    if (T == NULL) return;
    for (p = FirstNode(T); p != NULL; p = NextNode(p))
        printf("%d ", p->data);
}
```
> 复杂度：线索化时间 $O(n)$、空间 $O(h)$ 递归栈；线索化后遍历时间 $O(n)$、空间 $O(1)$。

! 建树时忘把 ltag、rtag 置 0，后续判断全反·pre 没在「访问根」之后后移，后继线索全部指错·求后继时只看 rtag 不看 rchild 是否为空，最后一个结点会跳到 NULL 之后·把线索当孩子去递归，遍历进入死循环