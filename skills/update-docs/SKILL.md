---
name: update-docs
description: 当用户请求"根据我的变更更新文档"、"检查此 PR 的文档"、"需要更新哪些文档"、"将文档与代码同步"、"为此功能搭建文档"、"记录此功能"、"审查文档完整性"、"为此变更添加文档"、"哪些文档受影响"、"文档影响"，或提到 "docs/"、"docs/01-app"、"docs/02-pages"、"MDX"、"文档更新"、"API 文档"、".mdx 文件"时使用此技能。提供基于代码变更更新 Next.js 文档的引导式工作流程。
---

# Next.js 文档更新工具

// @author Codex (Codex-sonnet-4-6)

指导您根据代码变更更新 Next.js 文档。专为维护者审查 PR 文档完整性而设计。

## 快速开始

1. **分析变更**：运行 `git diff canary...HEAD --stat` 查看变更的文件
2. **识别受影响的文档**：将变更的源文件映射到文档路径
3. **审查每个文档**：在用户确认后逐步更新
4. **验证**：运行 `pnpm lint` 检查格式
5. **提交**：暂存文档变更

## 工作流程：分析代码变更

### 步骤 1：获取差异

```bash
# 查看此分支上所有变更的文件
git diff canary...HEAD --stat

# 查看特定区域的变更
git diff canary...HEAD -- packages/next/src/
```

### 步骤 2：识别与文档相关的变更

查找以下区域的变更：

| 源文件路径                              | 可能影响的文档类型       |
| -------------------------------------- | ------------------------ |
| `packages/next/src/client/components/` | 组件 API 参考            |
| `packages/next/src/server/`            | 函数 API 参考            |
| `packages/next/src/shared/lib/`        | 因导出内容而异           |
| `packages/next/src/build/`             | 配置或构建文档           |
| `packages/next/src/lib/`               | 各种功能                  |

### 步骤 3：映射到文档文件

使用 `references/CODE-TO-DOCS-MAPPING.md` 中的代码到文档映射来查找对应的文档文件。

映射示例：

- `src/client/components/image.tsx` → `docs/01-app/03-api-reference/02-components/image.mdx`
- `src/server/config-shared.ts` → `docs/01-app/03-api-reference/05-config/`

## 工作流程：更新现有文档

### 步骤 1：阅读当前文档

在做出更改之前，请阅读现有文档以了解：

- 当前结构和章节
- 正在使用的 frontmatter 字段
- 是否使用 `<AppOnly>` / `<PagesOnly>` 来处理路由特定内容

### 步骤 2：确定需要更新的内容

常见更新包括：

- **新 props/选项**：添加到 props 表格并创建说明用法的章节
- **行为变更**：更新描述和示例
- **弃用功能**：添加弃用通知和迁移指南
- **新示例**：按照约定添加代码块

### 步骤 3：在确认后应用更新

对于每个变更：

1. 向用户展示您计划更改的内容
2. 在编辑前等待确认
3. 应用编辑
4. 进入下一个变更

### 步骤 4：检查共享内容

如果文档使用 `source` 字段模式（Pages Router 文档常见），源文件是需要编辑的文件。示例：

```yaml
# docs/02-pages/... 包含共享内容的文件
---
source: app/building-your-application/optimizing/images
---
```

请编辑 App Router 源文件，而不是 Pages Router 文件。

### 步骤 5：验证更改

```bash
pnpm lint          # 检查格式
pnpm prettier-fix  # 自动修复格式问题
```

## 工作流程：搭建新功能文档

当为全新功能添加文档时使用此流程。

### 步骤 1：确定文档类型

| 功能类型          | 文档位置                                          | 模板             |
| ---------------- | ------------------------------------------------ | ---------------- |
| 新组件           | `docs/01-app/03-api-reference/02-components/`   | API 参考         |
| 新函数           | `docs/01-app/03-api-reference/04-functions/`    | API 参考         |
| 新配置选项       | `docs/01-app/03-api-reference/05-config/`       | 配置参考         |
| 新概念/指南       | `docs/01-app/02-guides/`                         | 指南             |
| 新文件约定       | `docs/01-app/03-api-reference/03-file-conventions/` | 文件约定     |

### 步骤 2：使用正确的命名创建文件

- 使用 kebab-case：`my-new-feature.mdx`
- 如果排序重要则添加数字前缀：`05-my-new-feature.mdx`
- 根据功能类型放置在正确的目录中

### 步骤 3：使用适当的模板

**API 参考模板：**

```mdx
---
title: Feature Name
description: Brief description of what this feature does.
---

{/* 此文档的内容在 app 和 pages router 之间共享。您可以使用 `<PagesOnly>Content</PagesOnly>` 组件来添加特定于 Pages Router 的内容。任何共享内容都不应包装在组件中。 */}

Brief introduction to the feature.

## Reference

### Props

<div style={{ overflowX: 'auto', width: '100%' }}>

| Prop                    | Example            | Type   | Status   |
| ----------------------- | ------------------ | ------ | -------- |
| [`propName`](#propname) | `propName="value"` | String | Required |

</div>

#### `propName`

Description of the prop.

\`\`\`tsx filename="app/example.tsx" switcher
// TypeScript example
\`\`\`

\`\`\`jsx filename="app/example.js" switcher
// JavaScript example
\`\`\`
```

**指南模板：**

```mdx
---
title: How to do X in Next.js
nav_title: X
description: Learn how to implement X in your Next.js application.
---

介绍此指南的用途。

## Prerequisites

读者开始之前需要了解的内容。

## Step 1: First Step

解释和代码示例。

\`\`\`tsx filename="app/example.tsx" switcher
// Code example
\`\`\`

## Step 2: Second Step

继续更多步骤...

## Next Steps

探索相关主题。
```

### 步骤 4：添加相关链接

使用相关文档更新 frontmatter：

```yaml
related:
  title: Next Steps
  description: Learn more about related features.
  links:
    - app/api-reference/functions/related-function
    - app/guides/related-guide
```

## 文档约定

有关完整的格式规则，请参阅 `references/DOC-CONVENTIONS.md`。

### 快速参考

**Frontmatter（必需）：**

```yaml
---
title: Page Title (2-3 words)
description: One or two sentences describing the page.
---
```

**代码块：**

```
\`\`\`tsx filename="app/page.tsx" switcher
// TypeScript first
\`\`\`

\`\`\`jsx filename="app/page.js" switcher
// JavaScript second
\`\`\`
```

**路由特定内容：**

```mdx
<AppOnly>仅适用于 App Router 文档的内容。</AppOnly>

<PagesOnly>仅适用于 Pages Router 文档的内容。</PagesOnly>
```

**备注：**

```mdx
> **Good to know**: Single line note.

> **Good to know**:
>
> - Multi-line note point 1
> - Multi-line note point 2
```

## 验证检查清单

在提交文档变更之前：

- [ ] Frontmatter 包含 `title` 和 `description`
- [ ] 代码块具有 `filename` 属性
- [ ] TypeScript 示例使用 `switcher` 配合 JS 变体
- [ ] Props 表格格式正确
- [ ] 相关链接指向有效路径
- [ ] `pnpm lint` 通过
- [ ] 更改渲染正确（如果预览可用）

## 参考资料

- `references/DOC-CONVENTIONS.md` - 完整的 frontmatter 和格式规则
- `references/CODE-TO-DOCS-MAPPING.md` - 源代码到文档的映射
