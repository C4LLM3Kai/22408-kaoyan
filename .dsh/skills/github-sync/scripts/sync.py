#!/usr/bin/env python3
"""github-sync: 把本仓库的新增/修改文件同步到 GitHub。

自动处理三件事，全部是踩过坑的：
  1. 网络：直连 GitHub 不通时，自动改走本机代理（SSH-over-proxy）。
  2. 单文件 100 MiB 上限：超限文件自动分卷为 .part-NNN。
  3. 单次 pack 2 GiB 上限：自动分批推送。

用法:
    sync.py                 # 提交并推送全部变更
    sync.py --dry-run       # 只报告将要做什么，不改动任何东西
    sync.py -m "提交说明"    # 自定义提交信息
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

# scripts/ 位于 .dsh/skills/github-sync/scripts/，仓库根在其上四级
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", ".."))

FILE_LIMIT = 100 * 1024 * 1024      # GitHub 单文件硬上限
CHUNK = 90 * 1024 * 1024            # 分卷大小，留余量
PACK_CAP_MIB = 900                  # 每批上限，规避 2 GiB pack 限制

PROXY_CANDIDATES = [7897, 7890, 1087, 1080, 8889, 6152, 7891]


def run(args, cwd=REPO, env=None, check=True, capture=True):
    """执行命令。返回 (returncode, stdout+stderr)。"""
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.run(args, cwd=cwd, env=e,
                       stdout=subprocess.PIPE if capture else None,
                       stderr=subprocess.STDOUT if capture else None)
    out = (p.stdout or b"").decode("utf-8", "replace") if capture else ""
    if check and p.returncode != 0:
        print(out)
        raise SystemExit("命令失败 (%d): %s" % (p.returncode, " ".join(args)))
    return p.returncode, out


def detect_proxy():
    """探测可用的本机 HTTP 代理端口。"""
    import socket
    for port in PROXY_CANDIDATES:
        s = socket.socket()
        s.settimeout(0.3)
        try:
            s.connect(("127.0.0.1", port))
            s.close()
            return port
        except OSError:
            pass
        finally:
            try:
                s.close()
            except OSError:
                pass
    return None


def ssh_env(proxy_port):
    """构造 git 用的 SSH 环境；有代理则走代理。"""
    if proxy_port:
        cmd = ("ssh -o StrictHostKeyChecking=no -o ConnectTimeout=15 "
               "-o ServerAliveInterval=30 -o ServerAliveCountMax=6 "
               "-o ProxyCommand='nc -X connect -x 127.0.0.1:%d %%h %%p'" % proxy_port)
    else:
        cmd = "ssh -o StrictHostKeyChecking=no -o ConnectTimeout=15"
    return {"GIT_SSH_COMMAND": cmd}


def test_remote(proxy_port):
    """测试远端可达性，返回 (ok, 描述)。"""
    env = ssh_env(proxy_port)
    rc, out = run(["git", "ls-remote", "--heads", "origin"], env=env, check=False)
    if rc == 0:
        return True, "直连/代理可用"
    return False, out.strip().splitlines()[-1] if out.strip() else "未知错误"


def push_with_retry(args, env, attempts=5, label=""):
    """带指数退避的推送。网络抖动（尤其走代理时）很常见，必须重试。

    返回 (ok, 最后一次输出)。
    """
    import time
    delay = 5
    out = ""
    for k in range(1, attempts + 1):
        rc, out = run(args, env=env, check=False)
        if rc == 0:
            if k > 1:
                print("    第 %d 次尝试成功" % k)
            return True, out
        low = out.lower()
        # 认证/权限/体积超限属确定性失败，重试无意义
        fatal = ("exceeds github" in low or "pre-receive hook declined" in low
                 or "permission denied" in low or "repository not found" in low
                 or "authentication failed" in low)
        if fatal:
            return False, out
        if k < attempts:
            print("    第 %d 次失败，%d 秒后重试..." % (k, delay))
            time.sleep(delay)
            delay = min(delay * 2, 60)
    return False, out


def unpushed_commits(env, branch):
    """返回本地领先远端的提交数（>0 表示有已提交但未推送的内容）。"""
    rc, out = run(["git", "rev-list", "--count", "origin/%s..HEAD" % branch],
                  env=env, check=False)
    if rc != 0:
        return 0
    try:
        return int(out.strip())
    except ValueError:
        return 0


def find_oversized():
    """找出工作区中超过单文件上限、且未被 .gitignore 排除的文件。"""
    # 用 git 判定哪些文件会被追踪（尊重 .gitignore）
    rc, out = run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
                  check=False)
    if rc != 0:
        return []
    names = [n for n in out.split("\0") if n]
    big = []
    for n in names:
        try:
            if os.path.getsize(n) > FILE_LIMIT:
                big.append(n)
        except OSError:
            pass
    return big


def split_file(path):
    """把超限文件分卷为 path.part-NNN（90 MiB 一卷）。返回卷数。"""
    if any(f.startswith(os.path.basename(path) + ".part-") for f in os.listdir(os.path.dirname(path) or ".")):
        return len([f for f in os.listdir(os.path.dirname(path) or ".")
                    if f.startswith(os.path.basename(path) + ".part-")])
    n = 0
    with open(path, "rb") as src:
        while True:
            block = src.read(CHUNK)
            if not block:
                break
            with open("%s.part-%03d" % (path, n), "wb") as dst:
                dst.write(block)
            n += 1
    return n


def ensure_gitignore_entries(paths):
    """把超限原始文件路径写入 .gitignore（若尚未存在）。"""
    gi = os.path.join(REPO, ".gitignore")
    try:
        content = open(gi, encoding="utf-8").read()
    except OSError:
        content = ""
    added = []
    lines = content.splitlines()
    for p in paths:
        entry = "/" + p.replace(os.sep, "/")
        if entry not in lines:
            added.append(entry)
    if added:
        if content and not content.endswith("\n"):
            content += "\n"
        content += "\n# 超过 GitHub 100MB 单文件上限的原始文件（已分卷）\n"
        content += "\n".join(added) + "\n"
        open(gi, "w", encoding="utf-8").write(content)
    return added


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="只报告，不改动")
    ap.add_argument("-m", "--message", default=None, help="提交信息")
    args = ap.parse_args()

    os.chdir(REPO)
    print("仓库: %s" % REPO)
    print()

    # ---------- 1. 代理探测 ----------
    proxy = detect_proxy()
    print("[1/5] 网络")
    if proxy:
        print("  发现本机代理 127.0.0.1:%d，SSH 走代理" % proxy)
    else:
        print("  未发现代理，尝试直连")

    ok, desc = test_remote(proxy)
    if not ok and proxy:
        print("  代理失败，回退直连...")
        proxy = None
        ok, desc = test_remote(proxy)
    if not ok:
        print("  ✗ 远端不可达: %s" % desc)
        return 1
    print("  ✓ 远端可达 (%s)" % desc)
    print()

    # ---------- 2. 变更概览 ----------
    # 分支名：未出生分支用 symbolic-ref
    rc, branch = run(["git", "symbolic-ref", "--short", "HEAD"], check=False)
    branch = branch.strip() or "main"

    rc, status = run(["git", "status", "--porcelain"], check=False)
    pending = unpushed_commits(ssh_env(proxy), branch)

    if not status.strip() and pending == 0:
        print("[2/5] 无变更，无需上传。")
        return 0

    if not status.strip() and pending > 0:
        # 工作区干净，但有提交没推上去（比如上次推送网络中断）
        print("[2/5] 工作区干净，但有 %d 个提交尚未推送，直接补推。" % pending)
        if args.dry_run:
            print("  (dry-run，不推送)")
            return 0
        print()
        print("[4/5] 补推未上传的提交")
        ok, out = push_with_retry(["git", "push", "-u", "origin", branch],
                                  ssh_env(proxy), label="补推")
        if not ok:
            print(out)
            print("  ✗ 补推失败")
            return 1
        print("  ✓ 成功")
        rc, local = run(["git", "rev-parse", "HEAD"], check=False)
        rc, remote = run(["git", "ls-remote", "origin", "refs/heads/%s" % branch],
                         env=ssh_env(proxy), check=False)
        if local.strip() == (remote.split()[0] if remote.strip() else ""):
            print("  ✓ 本地与远端一致: %s" % local.strip()[:12])
            return 0
        print("  ✗ 校验不一致")
        return 1

    changed = [l for l in status.splitlines() if l.strip()]
    print("[2/5] 检测到 %d 项变更" % len(changed))
    for l in changed[:10]:
        print("  " + l)
    if len(changed) > 10:
        print("  ... 另有 %d 项" % (len(changed) - 10))
    print()

    # ---------- 3. 大文件处理 ----------
    print("[3/5] 大文件检查 (上限 100 MiB)")
    big = find_oversized()
    if big:
        for p in big:
            sz = os.path.getsize(p) / 2 ** 20
            print("  %s  %.1f MiB -> 分卷" % (p, sz))
        if args.dry_run:
            print("  (dry-run，跳过实际分卷)")
        else:
            for p in big:
                n = split_file(p)
                print("    生成 %d 卷" % n)
            added = ensure_gitignore_entries(big)
            if added:
                print("  已写入 .gitignore: %d 条" % len(added))
    else:
        print("  无超限文件")
    print()

    if args.dry_run:
        print("dry-run 结束，未做任何改动。")
        return 0

    # ---------- 4. 分批提交并推送 ----------
    print("[4/5] 分批提交并推送")
    env = ssh_env(proxy)

    # 关键：不能依赖 `git status --porcelain` 的路径来做逐文件匹配——未跟踪的新目录
    # 会被折叠成一行 `?? dir/`，里面的文件会漏掉。
    # 做法：先 `git add -A` 让 git 自己判定哪些文件该纳入（尊重 .gitignore），
    # 读出精确清单后立刻 `git reset` 清空索引，再按批次重新分批暂存。
    run(["git", "add", "-A", "--", "."], check=False)

    rc, out = run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"],
                  check=False)
    files = [n for n in out.split("\0") if n]

    rc, delout = run(["git", "diff", "--cached", "--name-only", "--diff-filter=D", "-z"],
                     check=False)
    deleted = [n for n in delout.split("\0") if n]

    # 清空索引，避免所有文件挤在第一批
    run(["git", "reset", "-q"], check=False)

    if not files and not deleted:
        print("  无可提交文件")
        return 0

    if deleted:
        print("  待删除 %d 个文件" % len(deleted))

    tmpdir = tempfile.mkdtemp(prefix="ghsync-")
    listfile = os.path.join(tmpdir, "all.nul")
    with open(listfile, "wb") as f:
        for n in files:
            f.write(n.encode("utf-8", "surrogateescape") + b"\0")

    # 分支名：未出生分支用 symbolic-ref
    rc, branch = run(["git", "symbolic-ref", "--short", "HEAD"], check=False)
    branch = branch.strip() or "main"

    if not files:
        # 只有删除，无需装箱，直接提交推送
        batches = []
        print("  仅删除变更，单批处理")
    else:
        # 用 plan_batches.py 装箱
        script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plan_batches.py")
        rc, out = run([sys.executable, script, listfile, tmpdir, str(PACK_CAP_MIB)], check=False)
        print(out.rstrip())
        if rc != 0:
            shutil.rmtree(tmpdir, ignore_errors=True)
            return 1
        batches = sorted(f for f in os.listdir(tmpdir) if re.match(r"^b\d+\.nul$", f))

    total_bytes = sum(os.path.getsize(os.path.join(REPO, n))
                      for n in files if os.path.exists(os.path.join(REPO, n)))
    print("  待上传 %.2f GiB，分 %d 批" % (total_bytes / 2 ** 30, max(len(batches), 1)))
    print()

    # 只有删除变更时构造一个空批次，走同一套提交推送流程
    if not batches:
        batches = [None]

    first_push = True
    for i, bf in enumerate(batches, 1):
        print("  ---- 批次 %d/%d ----" % (i, len(batches)))
        if bf is None:
            # 仅删除变更：把删除重新登记到索引
            names = []
            for d in deleted:
                run(["git", "add", "-A", "--", d], check=False)
        else:
            raw = open(os.path.join(tmpdir, bf), "rb").read()
            names = [n.decode("utf-8", "surrogateescape") for n in raw.split(b"\0") if n]
            for n in names:
                run(["git", "add", "--", n], check=False)
            # 删除变更挂在最后一批，确保不会被 reset 丢掉
            if i == len(batches) and deleted:
                for d in deleted:
                    run(["git", "add", "-A", "--", d], check=False)

        rc, _ = run(["git", "diff", "--cached", "--quiet"], check=False)
        if rc == 0:
            print("    无新增变更，跳过提交")
        else:
            msg = args.message or "同步 %d 个文件" % max(len(names), len(deleted))
            run(["git", "commit", "-q", "-m", "%s (批次 %d/%d)" % (msg, i, len(batches))])
            rc, out = run(["git", "log", "--oneline", "-1"], check=False)
            print("    提交: %s" % out.strip())

        print("    推送中...")
        push = ["git", "push"]
        if first_push:
            push.append("--force-with-lease")
        push += ["-u", "origin", branch]
        ok, out = push_with_retry(push, env, label="批次 %d" % i)
        if not ok and first_push and ("rejected" in out or "fetch first" in out):
            # 远端为空或历史不一致时，首次改用 --force
            print("    首次推送被拒，改用 --force 覆盖远端")
            ok, out = push_with_retry(["git", "push", "--force", "-u", "origin", branch],
                                      env, label="批次 %d(force)" % i)
        if not ok:
            print(out)
            print("    ✗ 批次 %d 推送失败（已重试）" % i)
            print("    提示：提交已在本地保存，网络恢复后重新运行本脚本会自动补推。")
            shutil.rmtree(tmpdir, ignore_errors=True)
            return 1
        first_push = False
        print("    ✓ 成功")

    shutil.rmtree(tmpdir, ignore_errors=True)

    # ---------- 5. 校验 ----------
    print()
    print("[5/5] 校验")
    rc, local = run(["git", "rev-parse", "HEAD"], check=False)
    rc, remote = run(["git", "ls-remote", "origin", "refs/heads/%s" % branch], env=env, check=False)
    local = local.strip()
    remote_sha = remote.split()[0] if remote.strip() else ""
    if local and local == remote_sha:
        print("  ✓ 本地与远端一致: %s" % local[:12])
    else:
        print("  ✗ 不一致  本地=%s  远端=%s" % (local[:12], remote_sha[:12]))
        return 1

    print()
    print("完成。仓库: https://github.com/C4LLM3Kai/22408-kaoyan")
    return 0


if __name__ == "__main__":
    sys.exit(main())
