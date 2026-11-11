---
name: vue-reverse-docs
description: 从现有 Vue 项目代码逆向生成完整文档体系，支持跨多个上下文窗口的长任务执行。采用 Initializer Agent + Coding Agent 双代理模式，适用于大型项目的系统梳理、重构前准备、技术评审。支持 Vue 2 + Webpack、Vuex 3/4、Composition API 自管理状态。当用户有大量 Vue 代码需要生成文档、梳理系统架构、准备重构、分析遗留系统时务必使用此 Skill。触发关键词：逆向生成文档、从代码生成文档、分析Vue代码、梳理系统、重构前准备、代码转文档、生成PRD/接口文档/组件文档。
---


# Vue 逆向生成文档 Skill（Team 模式）

采用 **Initializer Agent + Coordinator + 多 Writer Agent** 的 Team 架构，利用 OMC Task 系统实现 Phase 化并行生成。

---

## 前置检查：OMC 依赖

在使用本 Skill 前，确保 oh-my-claudecode 已安装：

```bash
omc --version 2>/dev/null || echo "⚠️ OMC 未安装，请先运行: omc setup"
```

若未安装，引导用户执行 `omc setup`。

---

## 入口：/vue-reverse-docs

### Step 0：时间检查

```bash
if [ ! -f "vue-docs-config.json" ]; then
  echo "未找到 vue-docs-config.json，全新开始"
else
  python3 -c "
import json, datetime
d = json.load(open('vue-docs-config.json'))
created = d.get('created_at', '')
print(f'FOUND|{d[\'docs_dir\']}|{d[\'total\']}|{created}')
"
fi
```

**根据检查结果询问用户（唯一一次交互）：**

情况 A：`vue-docs-config.json` 已存在：
```
检测到已有配置（创建于 [created_at]，共 [N] 个任务，目录：[docs_dir]）。

请选择：
  1. 全新开始（清除旧记录，重新扫描项目）
  2. 使用已有配置（直接启动 Team）
```

情况 B：`vue-docs-config.json` 不存在：
```
未检测到进行中的任务，将全新开始。

请确认：
1. 项目根目录路径是什么？
2. 有什么特别要注意的吗？（没有直接回答"没有"）
```

> 用户回答后，立即执行，**不再询问任何问题**。

---

### Step 1：Initializer Agent 扫描项目

Initializer 执行以下操作（全自动，无需交互）：

1. **识别模型名**：从环境变量或配置文件获取，生成 `project-docs-{model}` 目录
2. **识别 Vue 项目类型**：读取 `package.json`，判断 Vue 版本、构建工具、状态管理方案
3. **扫描项目结构**：路由、store、composables、api、views、components
4. **生成 `vue-docs-config.json`**：包含所有任务定义（category、template、source_files、priority），**不含状态跟踪字段**
5. **建立目录结构**：`$DOCS_DIR/` 及各子目录
6. **git commit**：提交初始化结果

详细执行步骤见 `references/initializer.md`。

---

### Step 2：Coordinator 启动 Team

Initializer 完成后，Coordinator 接管：

1. **创建团队**：`TeamCreate(team_name="vue-docs-team", description="Vue 项目文档生成团队")`
2. **启动各角色 Agent**：按角色启动 6 个 Writer Agent
   - `architecture-agent`
   - `state-agent`
   - `api-agent`
   - `view-agent`
   - `component-agent`
   - `tech-debt-agent`
3. **创建 OMC Task**：读取 `vue-docs-config.json`，为每个任务创建 OMC Task，按 Phase 设置 `blockedBy`

详细调度逻辑见 `references/coordinator.md`。

---

### Step 3：Team 执行文档生成

Coordinator 进入主循环，按 Phase 推进：

```
Phase 1: architecture（1 个任务，无依赖）
    → architecture-agent
         │
         ▼
Phase 2: state + api（并行，依赖 Phase 1）
    → state-agent + api-agent
         │
         ▼
Phase 3: view + component（并行，最多 3 个并发，依赖 Phase 2）
    → view-agent (×3) + component-agent (×3)
         │
         ▼
Phase 4: tech-debt（依赖所有前面任务）
    → tech-debt-agent
```

每个 Writer Agent：
1. 接收 Coordinator 分配的任务
2. 读取模板 + 源文件
3. 生成文档并写入 `$DOCS_DIR/`
4. 验证文件非空
5. `TaskUpdate(status="completed")` 报告 Coordinator

详细执行步骤见 `references/doc-writer.md`。

---

### Step 4：终止与清理

全部 Task 完成后：

1. Coordinator 生成 `$DOCS_DIR/doc-progress.md` 终态报告
2. `SendMessage(to="*", message={"type":"shutdown_request"})` 通知所有 Agent 退出
3. `TeamDelete()` 清理团队

---

## 核心设计：Initializer → Coordinator → Writer Agents

```
/vue-reverse-docs（首次，只需一次确认）
         │
         ▼
  ┌─────────────────────┐
  │  Initializer Agent  │
  │  扫描项目 → 生成    │
  │  vue-docs-config    │
  │  建立目录 → git commit│
  └─────────────────────┘
         │
         ▼
  ┌─────────────────────┐
  │   Coordinator       │
  │  TeamCreate → 启动  │
  │  6 个 Writer Agent  │
  │  TaskCreate → 按    │
  │  Phase 分配任务     │
  └─────────────────────┘
         │
    ┌────┴────┬────────┬────────┬────────┬────────┐
    ▼         ▼        ▼        ▼        ▼        ▼
 arch-agent state   api     view    comp    tech-debt
            agent   agent   agent   agent   agent
    │         │        │        │        │        │
    └─────────┴────────┴────────┴────────┴────────┘
         │
         ▼
  🎉 全部完成，终态报告
```

**用户总共只需要一次输入：**
1. 回答启动确认（项目路径 + 注意事项 / 或选择继续已有配置）

**之后全程自动执行，无需人工干预。**

---

## 执行规则（Team 模式）

- ✅ Coordinator 通过 OMC Task 系统管理所有任务状态
- ✅ 每类 Writer Agent 最多并发数：`architecture/state/api/tech-debt` = 1，`view/component` = 3
- ✅ 任务按 Phase 顺序解锁，同 Phase 内并行执行
- ✅ 每个 Agent 完成 1 个 Task 后立即报告，等待下一个分配
- ✅ Agent 必须使用 bash `cat >` 写入文件（禁止使用 Write 工具）
- ✅ 每次生成文档后必须验证文件非空（`ls -lh` + `wc -l`）
- ✅ Coordinator 在每 Phase 完成后更新 `doc-progress.md`
- ❌ 不允许跳过 Phase 依赖直接执行后续任务
- ❌ 不允许在文件验证失败前标记 Task 完成

---

## Vue 项目特有扫描规则

### 支持的项目类型

| 类型 | 特征文件 | 说明 |
|------|---------|------|
| Vue 2 + Webpack | `vue.config.js` + `package.json` 中 `"vue": "^2"` | 主流遗留项目 |
| Vue 2 + Vue CLI | `@vue/cli-service` 在 devDependencies | Vue CLI 脚手架 |
| Vue 3 + Vite | `"vue": "^3"` + `vite` 在 devDependencies | 现代项目 |

### 状态管理识别

| 方案 | 识别特征 | 文档模板 |
|------|---------|---------|
| Vuex 3（Vue 2） | `vuex@^3` in package.json | `references/tpl-state-vuex.md` |
| Vuex 4（Vue 3） | `vuex@^4` in package.json | `references/tpl-state-vuex.md` |
| Composition API 自管理 | `src/composables/` 或 `useXxx.js` 命名规范 | `references/tpl-state-composable.md` |
| 混合模式 | Vuex + composables 同时存在 | 两套模板均使用 |

### 文件路径映射（Vue vs React）

| React | Vue 2/3 | 说明 |
|-------|---------|------|
| `src/pages/` | `src/views/` | 页面组件 |
| `src/components/` | `src/components/` | 公共组件（同名） |
| `src/store/` | `src/store/` | 状态管理（同名） |
| `src/router/index.js` | `src/router/index.js` | 路由配置（同名） |
| `*.jsx` / `*.tsx` | `*.vue` | 组件文件扩展名 |
| `useEffect(,[])` | `mounted()` / `onMounted()` | 生命周期 |
| `useState` | `data()` / `ref()` / `reactive()` | 响应式状态 |
| `useSelector` | `this.$store.state` / `mapState` | 读取 Store |
| `dispatch` | `this.$store.dispatch` / `store.dispatch` | 触发 Action |

### 路由文件识别

```bash
ls src/router/index.js 2>/dev/null \
  || ls src/router/index.ts 2>/dev/null \
  || ls src/router.js 2>/dev/null \
  || ls src/routes/index.js 2>/dev/null
```

### API 文件识别

```bash
ls src/api/ 2>/dev/null \
  || ls src/services/ 2>/dev/null \
  || ls src/request/ 2>/dev/null
```

---

## 目录命名规则

- 格式：`project-docs-{模型名}`（转小写，空格替换为 `-`）
- 例：`project-docs-claude-sonnet-4-6`
- 目录已存在时**直接覆盖**，不追加日期

**产出结构：**
```
project-docs-{model}/
├── doc-progress.md
├── architecture.md
├── tech-debt.md
├── api/
├── views/           ← Vue 用 views（对应 React 的 pages）
├── components/
└── state/

vue-docs-config.json     ← 放项目根目录（任务定义，不含状态）
```

---

## 文档模板索引

| 文档类型 | 参考文件 | 负责角色 |
|---------|---------|---------|
| Initializer Agent 完整提示 | `references/initializer.md` | Initializer |
| 调度员工作手册 | `references/coordinator.md` | **coordinator**（调度员） |
| 通用写手工作手册 | `references/doc-writer.md` | 所有 Writer Agent 共享 |
| 架构文档模板 | `references/tpl-architecture.md` | **architecture-agent**（架构师） |
| PRD 页面文档模板 | `references/tpl-prd.md` | **view-agent**（页面分析师） |
| API 接口文档模板 | `references/tpl-api.md` | **api-agent**（接口管理员） |
| 组件文档模板（Vue SFC） | `references/tpl-component.md` | **component-agent**（组件分析师） |
| 状态管理文档模板（Vuex） | `references/tpl-state-vuex.md` | **state-agent**（状态管理员） |
| 状态管理文档模板（Composable） | `references/tpl-state-composable.md` | **state-agent**（状态管理员） |
| 技术债务报告模板 | `references/tpl-tech-debt.md` | **tech-debt-agent**（技术审计员） |

---

## vue-docs-config.json 结构

```json
{
  "project": "my-vue-app",
  "framework": "vue2",
  "model": "claude-sonnet-4-6",
  "docs_dir": "project-docs-claude-sonnet-4-6",
  "created_at": "2026-03-07 14:48:48",
  "total": 37,
  "tasks": [
    {
      "id": "arch-001",
      "category": "architecture",
      "description": "生成整体架构文档",
      "target_file": "project-docs-claude-sonnet-4-6/architecture.md",
      "source_files": ["package.json", "src/App.vue", "src/router/index.js"],
      "template": "references/tpl-architecture.md",
      "priority": 1,
      "phase": 1
    },
    {
      "id": "state-001",
      "category": "state",
      "description": "生成 Vuex store 文档",
      "target_file": "project-docs-claude-sonnet-4-6/state/store.md",
      "source_files": ["src/store/index.js", "src/store/modules/user.js"],
      "template": "references/tpl-state-vuex.md",
      "priority": 2,
      "phase": 2
    }
  ]
}
```

**与旧版 doc-tasks.json 的差异：**
- 新增 `framework` 字段：`"vue2"` | `"vue3"`
- 新增 `phase` 字段：标识任务所属执行阶段
- `source_files` 中使用 `.vue` 扩展名
- 页面任务的 `target_file` 路径用 `views/` 而非 `pages/`
- **移除了状态跟踪字段**：`seq`、`passes`、`completed_at`、`session_started_at`
- 运行时状态由 OMC Task 系统管理，不再由 JSON 文件跟踪

**任务分类与优先级：**

| 类别 | priority | phase | 说明 |
|------|---------|-------|------|
| architecture | 1 | 1 | 整体架构，最先做 |
| state | 2 | 2 | 状态管理（Vuex store / composables） |
| api | 3 | 2 | 接口文档，每个文件一个任务 |
| view | 4 | 3 | 页面 PRD（对应 src/views/），每个路由一个任务 |
| component | 5 | 3 | 重要复用组件 |
| tech-debt | 6 | 4 | 技术债务，最后做 |
