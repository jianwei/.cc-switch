---
name: implement-design
description: 将 Figma 设计稿转换为像素级精确的生产级代码。适用于实现 Figma 设计稿、生成代码、实现组件、提供 Figma URL 或请求构建与 Figma 规范匹配的组件时使用。需要 Figma MCP 服务器连接。
disable-model-invocation: false
---

# 实现设计

## 概述

本技能提供了一套结构化工作流程，用于将 Figma 设计稿转换为生产级代码，实现像素级精确度。它确保与 Figma MCP 服务器的一致集成、正确使用设计令牌，以及与设计稿 1:1 的视觉保真度。

## 技能边界

- 当交付物为用户仓库中的代码时，使用本技能。
- 如果用户要求在 Figma 内部创建/编辑/删除节点，切换到 [figma-use](../figma-use/SKILL.md)。
- 如果用户要求根据代码或描述在 Figma 中构建或更新完整页面，切换到 [figma-generate-design](../figma-generate-design/SKILL.md)。
- 如果用户仅要求 Code Connect 映射，切换到 [figma-code-connect-components](../figma-code-connect-components/SKILL.md)。
- 如果用户要求编写可复用的代理规则（`AGENTS.md`/`AGENTS.md`），切换到 [figma-create-design-system-rules](../figma-create-design-system-rules/SKILL.md)。

## 前置条件

- Figma MCP 服务器已连接且可访问
- 用户需提供格式为 `https://figma.com/design/:fileKey/:fileName?node-id=1-2` 的 Figma URL
  - `:fileKey` 为文件密钥
  - `1-2` 为节点 ID（具体的组件或画板）
- **或者**使用 `figma-desktop` MCP 时：用户可直接在 Figma 桌面应用中选择节点（无需 URL）
- 项目应有已建立的设计系统或组件库（推荐）

## 必需工作流程

**按顺序执行以下步骤，切勿跳过。**

### 步骤 1：获取节点 ID

#### 选项 A：从 Figma URL 解析

当用户提供 Figma URL 时，提取文件密钥和节点 ID 作为 MCP 工具参数传递。

**URL 格式：** `https://figma.com/design/:fileKey/:fileName?node-id=1-2`

**提取内容：**

- **文件密钥：** `:fileKey`（`/design/` 之后的段落）
- **节点 ID：** `1-2`（`node-id` 查询参数的值）

**注意：** 使用本地桌面 MCP（`figma-desktop`）时，`fileKey` 不作为参数传递给工具调用。服务器自动使用当前打开的文件，因此只需传递 `nodeId`。

**示例：**

- URL: `https://figma.com/design/kL9xQn2VwM8pYrTb4ZcHjF/DesignSystem?node-id=42-15`
- 文件密钥: `kL9xQn2VwM8pYrTb4ZcHjF`
- 节点 ID: `42-15`

#### 选项 B：使用 Figma 桌面应用的当前选择（仅限 figma-desktop MCP）

当使用 `figma-desktop` MCP 且用户**未提供** URL 时，工具自动使用 Figma 桌面应用中当前选择的节点。

**注意：** 基于选择的提示仅适用于 `figma-desktop` MCP 服务器。远程服务器需要指向画板或图层的链接来提取上下文。用户必须打开 Figma 桌面应用并选中一个节点。

### 步骤 2：获取设计上下文

使用提取的文件密钥和节点 ID 运行 `get_design_context`。

```
get_design_context(fileKey=":fileKey", nodeId="1-2")
```

这提供包括以下内容的结构化数据：

- 布局属性（Auto Layout、约束、尺寸）
- 排版规格
- 颜色值和设计令牌
- 组件结构和变体
- 间距和内边距值

**如果响应过大或被截断：**

1. 运行 `get_metadata(fileKey=":fileKey", nodeId="1-2")` 获取高层级节点映射
2. 从元数据中识别所需的特定子节点
3. 使用 `get_design_context(fileKey=":fileKey", nodeId=":childNodeId")` 获取各个子节点

### 步骤 3：捕获视觉参考

使用相同的文件密钥和节点 ID 运行 `get_screenshot`。

```
get_screenshot(fileKey=":fileKey", nodeId="1-2")
```

此截图作为视觉验证的真实来源。在整个实现过程中保持可访问。

### 步骤 4：下载所需资源

下载 Figma MCP 服务器返回的所有资源（图片、图标、SVG）。

**重要：** 遵循以下资源规则：

- 如果 Figma MCP 服务器返回图片或 SVG 的 `localhost` 源，直接使用该源
- **不要**导入或添加新的图标包——所有资源应来自 Figma 载荷
- 如果提供了 `localhost` 源，**不要**使用或创建占位符
- 资源通过 Figma MCP 服务器的内置资源端点提供服务

### 步骤 5：转换为项目约定

将 Figma 输出转换为项目的框架、样式和约定。

**核心原则：**

- 将 Figma MCP 输出（通常为 React + Tailwind）视为设计和行为的表示，而非最终代码风格
- 用项目的首选工具或设计系统令牌替换 Tailwind 工具类
- 复用现有组件（按钮、输入框、排版、图标包装器）而非重复功能
- 一致使用项目的颜色系统、排版刻度和间距令牌
- 遵守现有路由、状态管理和数据获取模式

### 步骤 6：实现 1:1 视觉保真度

力求与 Figma 设计稿的像素级视觉一致性。

**指南：**

- 优先保证与设计的完全一致
- 避免硬编码值——尽可能使用 Figma 的设计令牌
- 当设计系统令牌与 Figma 规范冲突时，优先使用设计系统令牌，但最小程度调整间距或尺寸以匹配视觉
- 遵循 WCAG 无障碍要求
- 根据需要添加组件文档

### 步骤 7：对照 Figma 验证

在完成之前，根据 Figma 截图验证最终 UI。

**验证清单：**

- [ ] 布局匹配（间距、对齐、尺寸）
- [ ] 排版匹配（字体、大小、粗细、行高）
- [ ] 颜色精确匹配
- [ ] 交互状态按设计工作（悬停、激活、禁用）
- [ ] 响应式行为遵循 Figma 约束
- [ ] 资源正确渲染
- [ ] 符合无障碍标准

## 实现规范

### 组件组织

- 将 UI 组件放置在项目指定的设计系统目录中
- 遵循项目的组件命名约定
- 除非真正需要动态值，否则避免内联样式

### 设计系统集成

- **始终**尽可能使用项目设计系统中的组件
- 将 Figma 设计令牌映射到项目设计令牌
- 当匹配的组件存在时，扩展它而非创建新组件
- 记录添加到设计系统的任何新组件

### 代码质量

- 避免硬编码值——提取为常量或设计令牌
- 保持组件可组合和可复用
- 为组件 props 添加 TypeScript 类型
- 为导出的组件包含 JSDoc 注释

## 示例

### 示例 1：实现按钮组件

用户说："实现这个 Figma 按钮组件: https://figma.com/design/kL9xQn2VwM8pYrTb4ZcHjF/DesignSystem?node-id=42-15"

**操作：**

1. 解析 URL 提取 fileKey=`kL9xQn2VwM8pYrTb4ZcHjF` 和 nodeId=`42-15`
2. 运行 `get_design_context(fileKey="kL9xQn2VwM8pYrTb4ZcHjF", nodeId="42-15")`
3. 运行 `get_screenshot(fileKey="kL9xQn2VwM8pYrTb4ZcHjF", nodeId="42-15")` 获取视觉参考
4. 从资源端点下载任何按钮图标
5. 检查项目是否有现有按钮组件
6. 如果有，用新变体扩展它；如果没有，使用项目约定创建新组件
7. 将 Figma 颜色映射到项目设计令牌（例如 `primary-500`、`primary-hover`）
8. 对照截图验证内边距、边框半径、排版

**结果：** 与 Figma 设计匹配的按钮组件，集成到项目设计系统中。

### 示例 2：构建仪表盘布局

用户说："构建这个仪表盘: https://figma.com/design/pR8mNv5KqXzGwY2JtCfL4D/Dashboard?node-id=10-5"

**操作：**

1. 解析 URL 提取 fileKey=`pR8mNv5KqXzGwY2JtCfL4D` 和 nodeId=`10-5`
2. 运行 `get_metadata(fileKey="pR8mNv5KqXzGwY2JtCfL4D", nodeId="10-5")` 了解页面结构
3. 从元数据识别主要部分（头部、侧边栏、内容区域、卡片）及其子节点 ID
4. 为每个主要部分运行 `get_design_context(fileKey="pR8mNv5KqXzGwY2JtCfL4D", nodeId=":childNodeId")`
5. 运行 `get_screenshot(fileKey="pR8mNv5KqXzGwY2JtCfL4D", nodeId="10-5")` 获取完整页面
6. 下载所有资源（Logo、图标、图表）
7. 使用项目的布局原语构建布局
8. 尽可能使用现有组件实现每个部分
9. 根据 Figma 约束验证响应式行为

**结果：** 与 Figma 设计匹配的完整仪表盘，具有响应式布局。

## 最佳实践

### 始终从上下文开始

永远不要基于假设实现。始终首先获取 `get_design_context` 和 `get_screenshot`。

### 增量验证

在实现过程中频繁验证，而非仅在最后验证。这样可以及早发现问题。

### 记录偏差

如果必须偏离 Figma 设计（例如，由于无障碍或技术约束），在代码注释中记录原因。

### 复用优于重建

在创建新组件之前，始终检查现有组件。代码库的一致性比精确复制 Figma 更重要。

### 设计系统优先

当存在疑问时，优先使用项目的设计系统模式而非逐字翻译 Figma。

## 常见问题与解决方案

### 问题：Figma 输出被截断

**原因：** 设计过于复杂或嵌套层级过多，无法在单次响应中返回。

**解决方案：** 使用 `get_metadata` 获取节点结构，然后使用 `get_design_context` 单独获取特定节点。

### 问题：实现后设计与预期不符

**原因：** 实现的代码与原始 Figma 设计之间存在视觉差异。

**解决方案：** 与步骤 3 的截图进行逐行对比。检查间距、颜色和排版值。

### 问题：资源不加载

**原因：** Figma MCP 服务器的资源端点不可访问或 URL 被修改。

**解决方案：** 验证 Figma MCP 服务器的资源端点可访问。服务器通过 `localhost` URL 提供资源服务。使用这些 URL 且不要修改。

### 问题：设计令牌值与 Figma 不同

**原因：** 项目的设计系统令牌具有与 Figma 设计中指定的不同值。

**解决方案：** 当项目令牌与 Figma 值不同时，为保持一致性优先使用项目令牌，但调整间距/尺寸以保持视觉保真度。

## 理解设计实现

Figma 实现工作流程建立了将设计转换为代码的可靠流程：

**对于设计师：** 相信实现将与他们的设计像素级精确匹配。

**对于开发者：** 消除猜测并减少来回返工的结构化方法。

**对于团队：** 保持设计系统完整性的高质量实现。

通过遵循此工作流程，确保每个 Figma 设计都以同样的关怀和细节关注来实现。

## 其他资源

- [Figma MCP 服务器文档](https://developers.figma.com/docs/figma-mcp-server/)
- [Figma MCP 服务器工具和提示](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/)
- [Figma 变量和设计令牌](https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma)
