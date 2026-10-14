#!/bin/bash
# ============================================================
#  restore-large-files.sh
#  还原被分卷的超大文件（GitHub 单文件上限 100 MiB）
#
#  用法：
#     ./restore-large-files.sh               # 还原全部并校验
#     ./restore-large-files.sh --verify-only # 只校验，不合并
#
#  说明：遍历仓库内所有 *.part-NNN 分卷，按序合并回原始文件名，
#        并用 LARGE-FILES.md 记录的 SHA-256 校验完整性。
#        兼容 macOS 自带的 bash 3.2。
# ============================================================
set -u
cd "$(dirname "$0")"

VERIFY_ONLY=0
[ "${1:-}" = "--verify-only" ] && VERIFY_ONLY=1

command -v shasum >/dev/null 2>&1 || { echo "错误：未找到 shasum。" >&2; exit 1; }

echo "============================================"
echo " 还原分卷大文件"
echo "============================================"
echo

# 用临时文件收集待还原文件的基名（去重），避免依赖 bash 4 的 mapfile
LIST=$(mktemp) || exit 1
trap 'rm -f "$LIST"' EXIT

find . -type f -name '*.part-[0-9][0-9][0-9]' -print \
  | sed -E 's/\.part-[0-9]{3}$//' \
  | sort -u > "$LIST"

TOTAL=$(grep -c . "$LIST" 2>/dev/null || echo 0)
if [ "$TOTAL" -eq 0 ]; then
  echo "未发现任何分卷文件（*.part-NNN）。"
  exit 0
fi

echo "发现 $TOTAL 个待还原文件。"
echo

FAIL=0
OK=0
SKIP=0

# 逐行读取基名（IFS= 保留前后空格，-r 不解释反斜杠）
while IFS= read -r base; do
  [ -z "$base" ] && continue

  dir=$(dirname "$base")
  name=$(basename "$base")

  # 收集本文件的分卷，按名称排序
  PARTS=$(mktemp) || exit 1
  find "$dir" -maxdepth 1 -type f -name "$name.part-*" -print | sort > "$PARTS"
  count=$(grep -c . "$PARTS" 2>/dev/null || echo 0)

  # 从 LARGE-FILES.md 取期望 SHA-256（若存在）
  expect=""
  if [ -f LARGE-FILES.md ]; then
    expect=$(grep -F "\`${base#./}\`" LARGE-FILES.md 2>/dev/null \
             | grep -oE '[0-9a-f]{64}' | head -1 || true)
  fi

  # ---- 只校验模式 ----
  if [ "$VERIFY_ONLY" -eq 1 ]; then
    if [ -n "$expect" ]; then
      actual=$(cat $(tr '\n' ' ' < "$PARTS") | shasum -a 256 | cut -d' ' -f1)
      if [ "$actual" = "$expect" ]; then
        echo "  [通过] ${base#./}  ($count 卷)"
        OK=$((OK+1))
      else
        echo "  [失败] ${base#./}"
        echo "         期望 $expect"
        echo "         实际 $actual"
        FAIL=$((FAIL+1))
      fi
    else
      echo "  [跳过] ${base#./}（清单中无 SHA 记录）"
      SKIP=$((SKIP+1))
    fi
    rm -f "$PARTS"
    continue
  fi

  # ---- 已存在且校验通过则不再合并 ----
  if [ -f "$base" ] && [ -n "$expect" ]; then
    if [ "$(shasum -a 256 "$base" | cut -d' ' -f1)" = "$expect" ]; then
      echo "  [已存在] ${base#./}"
      SKIP=$((SKIP+1))
      rm -f "$PARTS"
      continue
    fi
  fi

  # ---- 合并 ----
  echo "  合并 ${base#./}  ($count 卷) ..."
  : > "$base"
  while IFS= read -r p; do
    [ -z "$p" ] && continue
    cat "$p" >> "$base"
  done < "$PARTS"

  if [ -n "$expect" ]; then
    actual=$(shasum -a 256 "$base" | cut -d' ' -f1)
    if [ "$actual" = "$expect" ]; then
      echo "    ✓ SHA-256 校验通过"
      OK=$((OK+1))
    else
      echo "    ✗ SHA-256 校验失败！文件可能损坏。"
      echo "      期望 $expect"
      echo "      实际 $actual"
      FAIL=$((FAIL+1))
    fi
  else
    echo "    （清单中无 SHA 记录，跳过校验）"
    OK=$((OK+1))
  fi

  rm -f "$PARTS"
done < "$LIST"

echo
echo "============================================"
if [ "$VERIFY_ONLY" -eq 1 ]; then
  echo " 校验结果：通过 $OK / 跳过 $SKIP / 失败 $FAIL"
else
  echo " 还原结果：成功 $OK / 跳过 $SKIP / 失败 $FAIL"
fi
echo "============================================"

if [ "$FAIL" -gt 0 ]; then
  echo
  echo "存在失败项。请确认克隆是否完整，或重新下载。"
  exit 1
fi

echo
if [ "$VERIFY_ONLY" -eq 0 ]; then
  echo "全部完成。原始大文件已还原到各自目录。"
  echo "注意：还原后的文件与 .gitignore 规则同名，git 不会追踪它们。"
fi
