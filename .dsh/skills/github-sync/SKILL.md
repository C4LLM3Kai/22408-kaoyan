---
name: github-sync
description: 把 /Users/shaoyikai/Desktop/考研 工作区里新增或修改的文件同步上传到 GitHub 仓库 C4LLM3Kai/22408-kaoyan。当你在该目录下新建、生成、修改或删除了任何文件（笔记 PDF、错题、讲义、脚本、资料等），并且这些改动需要留存到 GitHub 时使用。也用于用户说"上传到 GitHub""同步一下""push 上去""备份到仓库"等。仅作用于本文件夹。
whenToUse: 上传, 同步, push, GitHub, 备份, 提交, 仓库, 上传到github, 同步到github, 保存到仓库
---

# 考研资料 GitHub 同步

把本工作区（`/Users/shaoyikai/Desktop/考研`）的内容同步到
**https://github.com/C4LLM3Kai/22408-kaoyan**（public）。

**作用范围**：只作用于这个文件夹。不要用这个 skill 去同步其他目录。

## 一、什么时候用

在**本工作区**里做完下面任何一件事之后，主动运行同步（不用等用户开口）：

- 新建了笔记 / PDF / 讲义 / 错题 / 资料文件
- 修改或删除了已有文件
- 生成了新的脚本、配置

用户明确说"上传""同步""push""备份到仓库"时，也走这个流程。

**不用**同步的情况：纯问答、没有落盘文件、或改动的是 `.gitignore` 已排除的内容
（`.work/`、`.dsh/`、`.venv/`、`node_modules/` 等）。

## 二、怎么用

一条命令，全自动：

```bash
python3 .dsh/skills/github-sync/scripts/sync.py
```

自定义提交说明：

```bash
python3 .dsh/skills/github-sync/scripts/sync.py -m "新增 408 操作系统第三章笔记"
```

只想看会发生什么、不改动任何东西：

```bash
python3 .dsh/skills/github-sync/scripts/sync.py --dry-run
```

脚本会依次完成：

1. **网络**：探测本机代理（7897/7890/…），SSH 自动走代理。直连 GitHub 会超时，
   必须走代理。
2. **变更**：列出将要上传的文件。
3. **大文件**：超过 100 MiB 的文件自动分卷为 `.part-NNN`（每卷 90 MiB），
   并把原始文件写入 `.gitignore`。
4. **分批推送**：按 900 MiB 装箱，逐批推送，规避 GitHub 单次 pack 2 GiB 上限。
   带指数退避重试，网络抖动不会前功尽弃。
5. **校验**：比对本地与远端 commit SHA，一致才算成功。

## 三、三个必须知道的坑

这些是实测踩出来的，遇到时不要慌：

| 现象 | 原因 | 处理 |
|---|---|---|
| `Could not resolve host` / 超时 | 直连 GitHub 不通 | 脚本已自动走代理；若仍失败，确认代理软件在运行 |
| `exceeds GitHub's file size limit of 100.00 MB` | 单文件超限 | 脚本会自动分卷；若手动 git push 撞上，改用脚本 |
| `pack exceeds maximum allowed size (2.00 GiB)` | 单次推送总量超限 | 脚本已自动分批；一次性 push 大仓库必然失败 |

**重要**：脚本失败时，提交已经保存在本地了。网络恢复后**重新运行同一个命令**
即可自动补推，不会丢失，也不会重复提交。

## 四、大文件还原（给克隆仓库的人）

超过 100 MiB 的文件以 `.part-NNN` 分卷形式存放。克隆后运行：

```bash
./restore-large-files.sh
```

会按序合并并用 SHA-256 校验。只校验不合并：加 `--verify-only`。

## 五、排查

```bash
# 看当前状态
cd /Users/shaoyikai/Desktop/考研
git status --short
git log --oneline -5
git ls-remote origin refs/heads/main   # 远端当前 commit

# 代理是否在跑
nc -z 127.0.0.1 7897 && echo "代理正常"

# 干跑一次看计划
python3 .dsh/skills/github-sync/scripts/sync.py --dry-run
```

如果远端 SHA 与本地 HEAD 不一致，直接重新运行 `sync.py` 补推即可。

## 六、约束

- **不要**手动 `git push` 整个大仓库——必然撞 2 GiB 上限，用脚本分批。
- **不要**把 `.work/`、`.dsh/`、`.venv/` 加进版本控制（`.gitignore` 已排除）。
- **不要**删除 `.gitignore` 里那些大文件原始路径条目——它们是防止超限文件被
  误提交的关键。
- 分卷文件每个 90 MB，GitHub 会提示 "larger than recommended 50 MB"，
  这只是**建议性警告**，不影响使用。
