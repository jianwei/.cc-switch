# Initializer Agent 详细规范

> 触发时机：新任务首次会话（任务与上次不同，或上次已完成，或首次执行）

---

## 执行步骤（按顺序）

### 0. 确定任务编号

```bash
# 确保根目录存在
mkdir -p long-running-agents

# 读取 long-running-agents.md，找出上一次任务编号
# 若无记录 → task-001
# 否则 → 上次编号 +1（如上次是 task-003 则本次为 task-004）

mkdir -p long-running-agents/task-NNN
cd long-running-agents/task-NNN
```

### 1. 创建 `start-server.sh`

```bash
#!/bin/bash
# 启动开发服务器
# 运行基础冒烟测试，确认 App 可用
```

### 2. 创建 `feature_list.json`

根据用户初始 prompt 展开**完整**功能列表，所有功能初始为 `"passes": false`：

```json
[
  {
    "id": 1,
    "category": "functional",
    "description": "用户可以点击新建聊天按钮创建新对话",
    "steps": [
      "导航到主界面",
      "点击「新建聊天」按钮",
      "验证新对话已创建",
      "确认聊天区域显示欢迎状态",
      "验证对话出现在侧边栏"
    ],
    "passes": false,
    "started_at": null,
    "completed_at": null
  }
]
```

**字段说明**：
- `id`：功能序号，从 1 开始，初始化时按顺序写入，**永远不变**
- `passes`：初始为 `false`，测试通过后改为 `true`
- `started_at`：Coding Agent 开始实现该功能时写入当前时间，格式 `"2025-11-26 14:00:00"`
- `completed_at`：测试通过、passes 改为 true 时写入当前时间，格式同上
- 未开始的功能两个时间字段保持 `null`

> **用 JSON 不用 Markdown**：模型更不容易不适当地覆盖 JSON 文件。
> **功能要尽量完整**：后续 Coding Agent 以此为唯一任务清单。
> **严禁修改 id、description、steps 字段**，只允许更新 passes、started_at、completed_at。

### 3. 创建 `claude-progress.txt`

```
[时间] 初始化完成。共 N 个功能待实现。
```

### 4. 初始 git commit

```bash
git init
git add .
git commit -m "Initial setup: project structure and feature list"
```

### 5. 追加写入 `long-running-agents/long-running-agents.md`

文件不存在则先创建，写入标题 `# Long-Running Agents 执行记录`，然后追加：

```markdown
## task-NNN

- **目录**：`long-running-agents/task-NNN/`
- **执行时间**：[当前时间]
- **任务描述**：[用户原始需求一句话概括]
- **状态**：🔄 进行中
- **完成功能数**：0 / N
- **与上次对比（task-NNN-1）**：[首次写"首次初始化，无上次记录"]
- **备注**：初始化完成，等待 Coding Agent 介入
```

---

## long-running-agents.md 格式说明

### 状态字段取值

| 值 | 含义 |
|----|------|
| `🔄 进行中` | 正在执行中 |
| `⚠️ 已中断` | 意外或主动中止，下次同任务将续接 |
| `✅ 已完成` | 所有功能 pass，下次同任务将新建 |

### 完整示例

```markdown
# Long-Running Agents 执行记录

---

## task-001

- **目录**：`long-running-agents/task-001/`
- **执行时间**：2025-11-26 10:00
- **任务描述**：构建 claude.ai 克隆应用
- **状态**：✅ 已完成
- **完成功能数**：42 / 42
- **与上次对比（task-001-1）**：首次初始化，无上次记录
- **备注**：全部功能完成

---

## task-002

- **目录**：`long-running-agents/task-002/`
- **执行时间**：2025-11-26 14:30
- **任务描述**：构建数据看板
- **状态**：⚠️ 已中断
- **完成功能数**：3 / 20
- **与上次对比（task-001）**：
  - 新增：图表组件、数据接口
  - 修复：无
  - 功能进度：0 → 3 / 20
- **备注**：context 耗尽中断，剩余功能：实时刷新、导出 CSV...
```