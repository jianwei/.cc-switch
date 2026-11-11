---
name: git-rollback
description: 将 Git 仓库强制回滚到指定版本号（commit hash），永久删除该版本之后的所有提交，并强制推送到远程仓库。当用户说"回滚到某个版本"、"回到指定 commit"、"删除某次提交之后的所有记录"、"版本回退并推送远程"、"git reset 到某个 hash"、"hard reset 到指定版本"时，必须使用此 Skill。触发关键词：回滚版本、回退到某个 commit、删除提交历史、强制回滚、git reset hard、回到指定版本号、版本号回滚、撤销所有提交。注意：此操作不可逆，会永久丢失指定版本之后的所有提交，务必在执行前向用户确认。
---

# Git 回滚 Skill

将当前分支强制重置到指定的 commit 版本，**永久删除**该版本之后的所有提交记录，并强制推送到远程仓库。

> ⚠️ **此操作不可逆**：目标版本之后的所有 commit 将从历史记录中彻底移除。执行前必须获得用户明确确认。

---

## 工作流程概览

```
1. 验证 Git 环境
      ↓
2. 输出当前分支信息，等待用户确认分支
      ↓
3. 确认目标版本号（必填）
      ↓
4. 展示回滚影响范围（将被删除的提交列表）
      ↓
5. 用户最终确认
      ↓
6. 执行 git reset --hard <commit>
      ↓
7. 强制推送到远程
      ↓
8. 验证结果
```

---

## 第一步：验证 Git 环境

```bash
# 确认是否在 git 仓库中
git rev-parse --is-inside-work-tree

# 查看当前分支
git branch --show-current

# 查看远程仓库配置
git remote -v
```

如果不在 Git 仓库中，停止并提示用户先进入正确的目录。

---

## 第二步：输出当前分支，等待用户确认

收集好环境信息后，**必须先向用户展示当前分支信息并等待确认**，然后才能继续后续步骤。

```bash
# 获取当前分支名
git branch --show-current

# 获取远程仓库地址
git remote get-url origin

# 展示最近几条提交，让用户确认上下文
git log --oneline -5
```

向用户展示以下确认信息，**等待用户回复后才继续**：

```
📌 当前操作分支信息：

  本地分支：main
  远程仓库：origin → https://github.com/xxx/repo.git
  当前 HEAD：a1b2c3d  feat: 最新提交信息

  最近提交记录：
    a1b2c3d  feat: 最新功能
    b2c3d4e  fix: 修复某个 bug
    c3d4e5f  docs: 更新文档

请确认：是否在正确的分支上操作？（请回复"是"或"确认"继续）
```

如果用户说分支不对，引导他们先切换分支：
```bash
git checkout <目标分支>
# 或
git switch <目标分支>
```
切换后重新从第一步开始。

---

## 第三步：验证目标版本号

版本号（commit hash）是**必填参数**，如果用户没有提供，必须立即询问：

```
请提供要回滚到的 commit hash（版本号）。
可以使用以下命令查看提交历史：
  git log --oneline -20
```

验证版本号是否存在：
```bash
git cat-file -t <commit-hash>
# 应输出 "commit"，否则说明版本号无效
```

支持的格式：
- 完整 hash：`a1b2c3d4e5f6...`（40位）
- 短 hash：`a1b2c3d`（7位以上）
- 标签名：`v1.0.0`

---

## 第四步：展示将被删除的提交

在执行回滚前，**必须**向用户展示将被永久删除的提交列表：

```bash
# 展示目标版本到当前 HEAD 之间的所有提交（将被删除的部分）
git log --oneline <commit-hash>..HEAD
```

向用户展示类似以下信息：
```
⚠️  以下提交将被永久删除：

  abc1234  feat: 添加用户登录功能
  def5678  fix: 修复数据库连接问题
  ghi9012  docs: 更新 README

回滚目标版本：
  <commit-hash>  <commit 信息>

当前分支：main
远程仓库：origin
```

---

## 第五步：最终确认

综合展示所有关键信息后，等待用户最终确认。向用户展示：

```
操作分支：main（origin）
回滚目标：<commit-hash>  <commit 信息>
将被删除：共 N 条提交（见上方列表）
执行命令：git reset --hard + git push --force-with-lease

确认继续吗？（请回复"确认"或"是"）
```

如果用户没有明确确认，**不得执行**回滚操作。

---

## 第六步：执行回滚

用户确认后，依次执行：

```bash
# 1. 重置到目标版本（硬重置，删除所有后续提交）
git reset --hard <commit-hash>

# 2. 确认当前 HEAD 已经是目标版本
git log --oneline -3
```

---

## 第七步：强制推送到远程

```bash
# 优先使用 --force-with-lease（更安全，防止覆盖他人推送）
git push --force-with-lease origin <分支名>

# 如果 --force-with-lease 失败（远程有本地不知道的更新），
# 需再次向用户确认后才能使用 --force：
git push --force origin <分支名>
```

**`--force-with-lease` vs `--force` 的区别：**
| 选项 | 说明 |
|------|------|
| `--force-with-lease` | 如果远程有本地未知的新提交，拒绝推送（更安全） |
| `--force` | 无论如何强制覆盖远程（危险，可能覆盖他人工作） |

默认使用 `--force-with-lease`，只有在用户明确要求或再次确认时才使用 `--force`。

---

## 第八步：验证回滚结果

```bash
# 查看当前最新提交，确认是目标版本
git log --oneline -5

# 确认本地与远程分支一致
git status

# 查看远程分支最新状态（可选）
git fetch origin
git log --oneline origin/<分支名> -3
```

向用户展示验证结果，确认回滚成功。

---

## 常见问题处理

### 问题一：版本号不存在
```bash
# 查看完整提交历史，帮助用户找到正确的 hash
git log --oneline --all -30
```

### 问题二：`--force-with-lease` 被拒绝
说明远程有本地未拉取的新提交，需要告知用户：
```
远程分支存在您本地没有的提交，强制推送可能会覆盖他人的工作。
请确认：
  1. 这些提交是否可以丢弃？
  2. 或者您需要先 git fetch 查看远程的提交？
```

### 问题三：工作区有未提交的修改
```bash
# 查看当前工作区状态
git status
```
提醒用户：`git reset --hard` 会**丢弃所有未提交的本地修改**，询问是否需要先 stash：
```bash
git stash push -m "回滚前的临时保存"
```

### 问题四：回滚后反悔（补救方案）
如果用户在推送前反悔，可以用 `ORIG_HEAD` 恢复：
```bash
# git reset --hard 执行后，ORIG_HEAD 指向回滚前的位置
git reset --hard ORIG_HEAD
```
> ⚠️ 一旦强制推送到远程，远程历史已被改写，恢复将更加复杂，需要从其他克隆或备份中重新推送。

---

## 执行原则

1. **分支必须先确认**：展示当前分支信息后，必须等用户确认分支正确才能继续
2. **版本号必填**：没有版本号绝不执行，必须向用户索取
3. **最终确认**：展示将被删除的 commit 列表后，必须获得用户明确确认
4. **优先安全推送**：默认使用 `--force-with-lease`，不随意使用 `--force`
5. **展示每步结果**：每条命令执行后展示输出，让用户了解当前状态
6. **提供补救提示**：告知用户在推送前可以通过 `ORIG_HEAD` 撤销
