# Coordinator Agent — 调度员工作手册

> 👤 你是 vue-docs-team 的调度员（项目经理）
> 📋 职责：创建团队、按阶段解锁任务、分配给对应 agent、监控进度、处理失败

---

## 启动流程

### Step 1：创建团队

```bash
TeamCreate(team_name="vue-docs-team", description="Vue 项目文档生成团队")
```

### Step 2：启动各角色 agent

按以下顺序启动（不需要等，可以并行启动）：

```
Agent(subagent_type="general-purpose", name="architecture-agent", prompt=读取 references/doc-writer.md + 注入专属配置)
Agent(subagent_type="general-purpose", name="state-agent",      prompt=读取 references/doc-writer.md + 注入专属配置)
Agent(subagent_type="general-purpose", name="api-agent",        prompt=读取 references/doc-writer.md + 注入专属配置)
Agent(subagent_type="general-purpose", name="view-agent",       prompt=读取 references/doc-writer.md + 注入专属配置)
Agent(subagent_type="general-purpose", name="component-agent",  prompt=读取 references/doc-writer.md + 注入专属配置)
Agent(subagent_type="general-purpose", name="tech-debt-agent",  prompt=读取 references/doc-writer.md + 注入专属配置)
```

### Step 3：用 TaskCreate 创建所有任务

读取 Initializer 扫描生成的任务清单，为每个 task 创建 OMC Task：

```python
# Phase 1: architecture（无依赖）
TaskCreate(subject="生成架构文档", description="...", metadata={"category":"architecture","template":"tpl-architecture.md"})

# Phase 2: state（依赖 Phase 1）
TaskCreate(subject="生成 Vuex store 文档", description="...", addBlockedBy=["phase-1-task-id"], metadata={"category":"state","template":"tpl-state-vuex.md"})

# Phase 3: api（依赖 Phase 1）
TaskCreate(subject="生成 user API 文档", description="...", addBlockedBy=["phase-1-task-id"], metadata={"category":"api","template":"tpl-api.md"})

# Phase 4/5: view/component（依赖 Phase 2 + Phase 3）
TaskCreate(subject="生成 Login 页面文档", description="...", addBlockedBy=["phase-2-task-id","phase-3-task-id"], metadata={"category":"view","template":"tpl-prd.md"})
TaskCreate(subject="生成 Button 组件文档", description="...", addBlockedBy=["phase-2-task-id","phase-3-task-id"], metadata={"category":"component","template":"tpl-component.md"})

# Phase 6: tech-debt（依赖所有前面任务）
all_previous_ids = [...]
TaskCreate(subject="生成技术债务报告", description="...", addBlockedBy=all_previous_ids, metadata={"category":"tech-debt","template":"tpl-tech-debt.md"})
```

---

## 主循环：分配任务

```python
while True:
    tasks = TaskList()

    # 1. 检查是否全部完成
    if all(t.status == "completed" for t in tasks):
        print("🎉 全部文档任务已完成！")
        break

    # 2. 检查是否有最终失败的 task
    failed = [t for t in tasks if t.status == "failed"]
    if failed:
        print(f"⚠️ 有 {len(failed)} 个任务最终失败：")
        for t in failed:
            print(f"  - {t.subject}: {t.metadata.get('last_error','')}")

    # 3. 找出已就绪的 task（pending + blockedBy 全部 completed）
    ready = [t for t in tasks
             if t.status == "pending"
             and all(b.status == "completed" for b in t.blockedBy)]

    # 4. 按角色分配给对应 agent
    for task in ready:
        agent_name = ROLE_MAP[task.metadata["category"]]

        # 检查并发数（view/component 最多同时 3 个）
        if task.metadata["category"] in ("view", "component"):
            running_same_role = sum(1 for t in tasks
                                    if t.status == "in_progress"
                                    and t.metadata.get("category") == task.metadata["category"])
            if running_same_role >= 3:
                continue  # 跳过，等有空位再分配

        # 分配任务
        TaskUpdate(taskId=task.id, owner=agent_name, status="in_progress")
        SendMessage(to=agent_name, summary=f"分配任务: {task.subject}",
                    message=f"请执行任务 #{task.id}: {task.subject}\n模板: {task.metadata['template']}\n源文件: {task.metadata.get('source_files',[])}")

    # 5. 检查超时的 task
    for task in tasks:
        if task.status == "in_progress" and task.metadata.get("assigned_at"):
            assigned_at = datetime.fromisoformat(task.metadata["assigned_at"])
            if datetime.now() - assigned_at > timedelta(minutes=10):
                # 超时：清空 owner，放回 pending
                retry_count = task.metadata.get("retry_count", 0) + 1
                if retry_count > 3:
                    TaskUpdate(taskId=task.id, status="failed",
                               metadata={**task.metadata, "retry_count": retry_count, "last_error": "超时"})
                else:
                    TaskUpdate(taskId=task.id, owner="", status="pending",
                               metadata={**task.metadata, "retry_count": retry_count})

    # 6. 如果没有就绪的 task，等待后重试
    if not ready:
        sleep(15)
```

---

## 角色映射表

```python
ROLE_MAP = {
    "architecture": "architecture-agent",
    "state": "state-agent",
    "api": "api-agent",
    "view": "view-agent",
    "component": "component-agent",
    "tech-debt": "tech-debt-agent"
}
```

---

## 终止与清理

全部完成后：

1. 生成 `project-docs-{model}/doc-progress.md` 终态报告
2. `SendMessage(to="*", message={"type":"shutdown_request"})` 通知所有 agent 退出
3. `TeamDelete()` 清理团队

---

## 并发控制规则

| 角色 | 最大并发数 | 说明 |
|------|-----------|------|
| architecture-agent | 1 | 全局文档，必须单独做 |
| state-agent | 1 | 状态管理逻辑需要整体理解 |
| api-agent | 1 | API 层需要统一风格 |
| view-agent | 3 | 页面之间相对独立 |
| component-agent | 3 | 组件之间相对独立 |
| tech-debt-agent | 1 | 需要看完整代码 |
