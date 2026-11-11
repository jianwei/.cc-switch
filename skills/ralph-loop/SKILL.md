---
name: ralph-loop
description: 自动化代理驱动开发的完整配置。将功能定义为用户故事（User Stories）并附带可测试的验收标准，然后运行 AI 代理循环直至所有故事通过。
---

# Ralph Loop

自动化代理驱动开发的完整配置。将功能定义为用户故事（User Stories）并附带可测试的验收标准，然后运行 AI 代理循环直至所有故事通过。

## 前置条件

按顺序完成以下配方（Recipe）：

### AI 编码代理配置

为 AI 编码代理（如 Cursor、GitHub Copilot 或 Claude Code）配置项目特定的模式、编码指南和 MCP 服务器，以实现一致的 AI 辅助开发。

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/agent-setup
```

##  cookbook - 按顺序完成以下配方

### 用户故事配置

创建用于将功能需求文档化为用户故事的结构化格式。使用包含可测试验收标准的 JSON 文件，供 AI 代理验证和跟踪。

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/user-stories-setup
```

### 使用用户故事

使用用户故事记录和跟踪功能实现。包括编写故事、构建功能以及标记验收标准为通过的工作流。

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/using-user-stories
```

### Ralph 代理循环

使用 Ralph 设置自动化代理驱动开发。在循环中运行 AI 代理以实现用户故事中的功能、验证验收标准并记录进度供下一个代理使用。

```bash
curl -H "Accept: text/markdown" https://fullstackrecipes.com/api/recipes/ralph-setup
```
