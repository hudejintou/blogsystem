#!/bin/bash
cd "$(dirname "$0")"

if [[ -z $(git status --porcelain) ]]; then
    echo "没有变更，无需存档。"
    exit 0
fi

echo "=== 变更文件 ==="
git status --short

read -p "输入提交信息 (回车使用默认): " msg
if [[ -z "$msg" ]]; then
    msg="存档 $(date '+%Y-%m-%d %H:%M')"
fi

git add -A
git commit -m "$msg"
git push
echo "=== 存档完成 ==="
