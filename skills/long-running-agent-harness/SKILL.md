---
name: long-running-agents
description: 构建能够跨多个上下文窗口持续运行的 AI Agent 的最佳实践 Skill。当用户需要构建长时间运行的 Agent、跨 context window 的自动化任务、多会话持续进展的编程 Agent、或问到"如何让 Agent 记住上次做了什么"时，必须使用此 Skill。触发关键词：长时间 Agent、多 context window、Agent 跨会话、自动化编程 Agent、Agent 持续运行、initializer agent、coding agent、agent harness、Codex-progress、feature list、跨上下文任务。
---

# Long-Running Agents Skill

基于 Anthropic 工程实践，提供跨多个 context window 持续运行 Agent 的完整方案。
运行环境：**Codex**（Agent 自动循环，无需人工介入）。

> 详细规范见 `references/` 目录，按需读取对应文件。

---

## 核心设计原则

**每个 task = 一个独立 session**

```
你只需启动一次
       ↓
Session 1 → task-001 → git commit → 更新日志 → /clear（自动）
Session 2 → task-002 → git commit → 更新日志 → /clear（自动）
Session N → task-NNN → ...
       ↓
所有 feature passes: true → 自动停止
```

- `/clear` 由 Agent 自己执行，开启下一个干净 session
- 每次 session 只从文件系统读取状态，不依赖历史上下文
- 中途中断后重启，自动续接未完成的 task

---

## 目录结构

```
项目根目录/
└── long-running-agents/
    ├── long-running-agents.md   ← 总索引日志（必须维护）
    ├── task-001/                ← 每个 task 独立目录
    │   ├── start-server.sh
    │   ├── feature_list.json
    │   ├── Codex-progress.txt
    │   └── ...
    ├── task-002/
    └── task-NNN/                ← 当前 task
```

**为什么每个 task 独立目录**：保留每次执行的完整产出，可随时回溯任意历史 task。

---

## 常见失败模式

| 失败模式 | 表现 |
|---------|------|
| 一次性完成 | 试图单次 session 完成所有功能，context 耗尽只做了一半 |
| 提前宣告完成 | 看到进展就认为任务已完成 |
| 未测试就标记完成 | 实现了代码但未端到端验证 |
| 环境状态混乱 | session 结束时留下 bug 或未记录的半成品 |

---

## ⚙️ 启动前确认（最优先执行）

在做任何事之前，**必须先询问用户**：

> 「本次任务完成后是否需要自动 git commit？(是/否)」

- 用户回答**否** → 整个流程中跳过所有 `git commit` 步骤
- 用户回答**是** → 按正常流程在每个功能完成后执行 `git commit`

将用户答案记录到当前 task 的 `Codex-progress.txt` 顶部，格式：
```
AUTO_COMMIT: true | false
```

后续所有步骤依据此标志决定是否执行提交。

---

## 🔀 每次 Session 启动判断（最先执行）

```
读取 long-running-agents/long-running-agents.md
       ↓
  无文件或无记录
  ├── 是 → 🆕 新任务流程
  └── 否 → 读取最后一条记录的「任务描述」和「状态」
               ↓
         与当前任务相同？
         ├── 否 → 🆕 新任务流程（新建 task-NNN+1）
         └── 是 → 检查状态
                   ├── 🔄 进行中 → 🔄 续接流程（同一目录继续）
                   ├── ⚠️ 已中断 → 🔄 续接流程（同一目录继续）
                   └── ✅ 已完成 → 🆕 新任务流程（新建 task-NNN+1）
```

**状态字段**：`🔄 进行中` / `⚠️ 已中断` / `✅ 已完成`
**相同任务判断**：目标实质相同即可，措辞不同没关系

---

## 双 Agent 架构

### 🆕 新任务 → Initializer Agent
> 详细步骤见 `references/initializer-agent.md`

1. 确定编号，创建 `long-running-agents/task-NNN/`
2. 创建 `start-server.sh`、`feature_list.json`、`Codex-progress.txt`（顶部写入 `AUTO_COMMIT: true/false`）
3. 若 `AUTO_COMMIT: true` → 执行初始 git commit；否则跳过
4. 写入 `long-running-agents.md`（状态：🔄 进行中）
5. 执行 `/clear` → 自动进入第一个 Coding Agent session

### 🔄 续接任务 → Coding Agent
> 详细步骤见 `references/coding-agent.md`

- **开始**：读文件 → 定位当前进度 → 启动服务器 → 健康检查
- **执行**：只做一个功能 → 端到端测试通过才标 `passes: true`
- **结束**：读取 `AUTO_COMMIT` 标志 → 若为 `true` 则 git commit，否则跳过 → 更新日志 → 写状态
  - 还有未完成功能 → 状态写 `🔄 进行中` → `/clear` → 自动开启下一 session
  - 全部完成 → 状态写 `✅ 已完成` → `/clear` → 停止

---

## Prompt 模板
> 见 `references/prompts.md`

---

## 参考资源
- 官方博客：https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- 代码示例：https://github.com/anthropics/Codex-quickstarts/tree/main/autonomous-coding