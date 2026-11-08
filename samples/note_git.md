# Git 常用命令速查

## 日常三连

1. `git add .` 把改动放进暂存区
2. `git commit -m "说明"` 提交到本地仓库
3. `git push` 推送到远端

## 查看状态

`git status` 看哪些文件被改过，`git log --oneline` 看提交历史。

## 回退

`git restore <文件>` 撤销工作区改动，`git reset --soft HEAD~1` 撤销上一次提交但保留改动。
