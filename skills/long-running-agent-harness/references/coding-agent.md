# Coding Agent 详细规范

> 运行环境：Claude Code
> 触发时机：Initializer 完成后，或每次 /clear 后自动开启的新 session

---

## 自动循环机制

每个 session 结束后 Agent 自己执行 `/clear`，Claude Code 自动开启下一个干净 session。
循环持续直到 `feature_list.json` 中所有功能 `passes: true` 为止。

```
[Session 开始] → 读文件判断状态 → 执行一个功能 → 更新日志
      ↓
  还有未完成功能？
  ├── 是 → /clear → [自动开启下一 Session]
  └── 否 → 写入 ✅ 已完成 → /clear → 停止
```

---

## Session 开始：定向阶段

```
1. 读取 long-running-agents/long-running-agents.md
   → 找到最后一条记录，确认工作目录（task-NNN）
   → 记录上一条记录（task-NNN-1）作为对比基准

2. 进入任务目录
   cd long-running-agents/task-NNN

3. 若为中断恢复（状态为 ⚠️ 已中断）
   → 读取 claude-progress.txt，找到最后一条 ⚠️ 记录确认中断点
   → claude-progress.txt 追加：「[时间] 🔄 恢复执行，从「[功能名称]」继续」
   → long-running-agents.md 追加：「[时间] 中断后恢复，从[中断功能]继续」

4. 读取 claude-progress.txt 和 git log 了解任务历史

5. 读取 feature_list.json，选出优先级最高的未完成功能（只选一个）

6. 运行 start-server.sh，启动开发服务器

7. 执行基础端到端测试，确认 App 可用
   → 发现 bug：先修复，再开始新功能
```

---

## 执行阶段：每次只做一件事

### 开始前：输出进度

选定功能后，**立即输出进度信息**（已完成数 = passes: true 的数量）：

```
================================================
📋 进度：第 3 个 / 共 42 个（已完成 2 个）
📊 完成率：4.8%  ████░░░░░░░░░░░░░░░░
🔧 本次实现：用户可以点击新建聊天按钮创建新对话
⏱️  开始时间：2025-11-26 14:00:00
================================================
```

同时将该功能的 `started_at` 写入当前时间：

```json
{ "started_at": "2025-11-26 14:00:00" }
```

### 实现与测试

- **只选一个功能**实现
- 实现完成后用 Puppeteer MCP 做完整端到端测试
- **测试通过后**才更新 `feature_list.json`：

```json
{
  "passes": true,
  "completed_at": "2025-11-26 14:23:15"
}
```

完成后输出耗时：

```
✅ 完成：用户可以点击新建聊天按钮创建新对话
⏱️  耗时：23 分 15 秒（14:00:00 → 14:23:15）
================================================
```

> **严格禁止**：删除或修改 `feature_list.json` 中的 id、description、steps 字段。
> 只允许更新 passes、started_at、completed_at 三个字段。

### 端到端测试要求

```
1. 打开应用页面
2. 执行 feature_list.json 中该功能的 steps
3. 逐步验证每个步骤的预期结果
4. 全部通过 → passes: true，写入 completed_at
```

> 已知限制：浏览器原生 alert 弹窗无法通过 Puppeteer MCP 截图，这类功能需额外关注。

---

## Session 结束：清理阶段

### 1. 提交进度

```bash
git add .
git commit -m "feat: 实现[功能名称] - [简短说明]"
```

### 2. 更新 `claude-progress.txt`

```bash
echo "[时间] ✅ 完成：[功能名称]" >> claude-progress.txt

# 若全部完成
echo "[时间] ✅ 全部 N 个功能完成，任务结束" >> claude-progress.txt

# 若中断
echo "[时间] ⚠️ 中断，剩余：[功能1、功能2...]" >> claude-progress.txt
```

### 3. 更新 `long-running-agents.md`

```markdown
- **状态**：🔄 进行中  ← 或 ✅ 已完成 / ⚠️ 已中断
- **完成功能数**：[当前数] / N
- **与上次对比（task-NNN-1）**：
  - 新增：[本次新增功能/模块]
  - 修复：[本次修复的 bug]
  - 功能进度：[上次数] → [当前数] / N
- **备注**：[下一步建议 或 中断原因]
```

> 只与上一次（task-NNN-1）对比，更早历史忽略不计。

### 4. 执行 `/clear` 开启下一 Session

```
还有未完成功能 → 状态写「🔄 进行中」→ /clear → 自动开启下一 session 继续
全部功能完成   → 状态写「✅ 已完成」 → /clear → 循环结束，停止
```

**`/clear` 是最后一步，所有文件必须在此之前写入完毕。**

---

## 干净状态标准

- 无重大 bug
- 代码有序且文档完善
- 任何开发者可直接开始下一个功能，无需先清理遗留问题

---

## 失败模式速查

| 问题 | 解法 |
|------|------|
| 提前宣告完成 | 读 feature_list.json，逐一推进未完成功能 |
| 留下 bug 或未记录进度 | 结束时必须 git commit + 更新两个日志文件 |
| 未测试就标记完成 | 端到端测试通过后才改 passes: true |
| 每次摸索如何启动 | 运行 start-server.sh |
| 历史上下文干扰 | 结束时执行 /clear，下一 session 从文件重建状态 |