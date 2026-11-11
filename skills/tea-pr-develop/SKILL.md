---
name: tea-pr-develop
description: 将当前 Git 分支通过 tea CLI 提交 PR 到 Gitea 仓库的 develop 分支。当用户说"提交 PR"、"创建 PR"、"发 PR"、"提个 PR"、"帮我 PR 到 develop"、"用 tea 创建 PR"或类似请求时必须使用本 Skill；即使用户没有点名 tea，只要是在 Gitea 仓库（如 tuniu 项目）中要求创建 PR 到 develop 分支，也要使用本 Skill。Skill 会自动完成分支检查、推送、检查已有 PR 避免重复创建、调用 create-pr-msg 生成完整 PR 描述、用 tea pr create 创建 PR。
---

# Tea PR Develop：当前分支提交 PR 到 develop

在 Gitea（tea CLI 0.16.x）上把当前分支提交 PR 到 `develop` 分支的完整工作流。

## 为什么这样做

- 公司仓库是私有 Gitea 实例，PR 用 `tea` 而非 `gh`；两者命令不通用
- 直接 `tea pr create` 容易因分支未推送、PR 已存在而失败或产生重复 PR，所以先做前置检查
- 简单一句话描述的 PR 评审体验差，所以必须先调用 `create-pr-msg` Skill 基于真实代码 diff 生成完整描述

## 前置约定

- tea 登录名默认 `tuniu`，仓库 slug 从 git 远端解析（如 `origin` 为
  `https://gitea.infra.tuniu.org/mob/mtuniu.git` → `-r mob/mtuniu`）
- 目标分支固定为 `develop`
- 全程中文输出

## 工作流

### 1. 分支与仓库检查

```bash
git branch --show-current        # 当前分支
git status --short               # 工作区状态
git remote get-url origin        # 解析仓库 slug
```

- 如果当前分支是 `develop` 或 `main`，**停止**并告知用户：不允许从这些分支发 PR，请先切到功能分支
- 如果当前是 detached HEAD，同样停止并提示
- 有未提交的改动时，先询问用户是否需要先提交（不要擅自 commit）

### 2. 推送分支（如未推送）

```bash
git ls-remote --heads origin <当前分支>
```

远端不存在该分支时执行 `git push -u origin HEAD`；已存在则对比本地是否落后/领先，本地有未推送提交时先推送。

### 3. 检查是否已有 PR，避免重复创建

```bash
tea pr list -r <repo> -o json
```

从结果中找 `head` 为当前分支的 PR：

- 已存在 open 的 PR：告知用户已存在（附链接），询问是更新描述（走第 5 步后用 `tea pr edit <idx>`）还是直接结束
- 已存在 closed 的 PR：告知用户，询问是否 `tea pr reopen <idx>` 重新打开
- 不存在：继续创建

### 4. 生成 PR 描述（必须）

**调用 `create-pr-msg` Skill**，参数为「当前分支提交到 develop 的 PR，基于 origin/develop...HEAD 的代码变更生成完整 PR 描述」。

它会读取 `git diff origin/develop...HEAD --stat` 和关键 diff，输出包含背景、目的、实现方案、测试/影响范围的完整 Markdown。把这份内容原样写入临时文件（如 `/tmp/pr-body-<branch>.md`），不要自己另写一份简化描述。

如果 `origin/develop` 不存在（如全新仓库），退化为基于提交记录生成，并在描述中注明。

### 5. 创建 PR

```bash
tea pr create -r <repo> -l tuniu \
  -t "<PR 标题>" \
  --description-file /tmp/pr-body-<branch>.md \
  --base develop --head <当前分支>
```

- 标题用 create-pr-msg 生成的动宾结构标题
- 完成后删除临时文件
- 如果创建失败提示已存在 PR，回到第 3 步处理

### 6. 结果汇报

用表格汇报：PR 编号与链接、标题、分支方向、状态、是否有冲突。

## 注意事项

- 不要自动加 reviewer / label / milestone，除非用户明确要求
- 不要把 token、临时描述文件提交进仓库
- tea 0.16 的 `pr create` 没有 `--yes`，只要传齐 `-t` 和 `--description-file` 就不会进入交互
