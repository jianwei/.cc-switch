# Next.js 文档约定

frontmatter 模式、代码块格式和 MDX 组件用法的完整参考。

## Frontmatter 模式

所有 MDX 文件必须以 `---` 分隔符包裹的 YAML frontmatter 开头。

### 必需字段

| 字段          | 描述                                    | 示例                                       |
| ------------ | -------------------------------------- | ------------------------------------------ |
| `title`       | 用于 SEO 和标题的页面标题（2-3 个词）   | `title: Image Component`                         |
| `description` | 简短描述（1-2 句话）                   | `description: Optimize images using next/image.` |

### 可选字段

| 字段         | 描述                                          | 示例                                      |
| ----------- | -------------------------------------------- | ---------------------------------------- |
| `nav_title` | 导航侧边栏的简短标题                           | `nav_title: Image`                           |
| `source`    | 从另一个页面拉取内容（避免重复）               | `source: app/api-reference/components/image` |
| `related`   | 带相关链接的下一步骤章节                      | 参见下文                                    |
| `version`   | 开发阶段指示器                                | `version: experimental`                      |

### 相关链接格式

```yaml
---
title: My Feature
description: Description here.
related:
  title: Next Steps
  description: Learn more about related features.
  links:
    - app/api-reference/components/image
    - app/guides/optimizing/images
---
```

### Version 字段值

- `experimental` - 实验性功能，可能会变更
- `legacy` - 遗留功能，考虑使用替代方案
- `unstable` - 不稳定的 API，不推荐用于生产环境
- `RC` - 发布候选版

## 代码块约定

### 基本语法

````
```language filename="path/to/file.ext"
code here
```
````

### 必需属性

| 属性        | 使用时机                        | 示例                    |
| ----------- | ------------------------------ | ---------------------- |
| `filename`  | 代码示例始终使用                  | `filename="app/page.tsx"` |
| `switcher`  | 提供 TS 和 JS 变体时              | `switcher`                |
| `highlight` | 高亮特定行时                     | `highlight={1,3-5}`       |

### TypeScript/JavaScript 切换器模式

始终先提供 TypeScript，然后是 JavaScript：

````mdx
```tsx filename="app/page.tsx" switcher
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'My Page',
}
```

```jsx filename="app/page.js" switcher
export const metadata = {
  title: 'My Page',
}
```
````

### 终端命令

使用 `bash` 语言，不带文件名：

````mdx
```bash
npm install next
```
````

### 行高亮

```
highlight={1}        # 单行
highlight={1,3}      # 多行
highlight={1-5}      # 范围
highlight={1,3-5,8}  # 组合
```

## MDX 组件

### AppOnly / PagesOnly

用于共享文档中的路由特定内容：

```mdx
<AppOnly>

此内容仅显示在 App Router 文档中。

</AppOnly>

<PagesOnly>

此内容仅显示在 Pages Router 文档中。

</PagesOnly>
```

**重要提示：** 在组件内部包含空行以确保正确的 markdown 解析。

### Image 组件

用于具有浅色/深色变体的主题图像：

```mdx
<Image
  alt="Description of the image"
  srcLight="/docs/light/image-name.png"
  srcDark="/docs/dark/image-name.png"
  width={1600}
  height={800}
/>
```

### 备注和提示

**单行：**

```mdx
> **Good to know**: Important information here.
```

**多行：**

```mdx
> **Good to know**:
>
> - First point
> - Second point
> - Third point
```

## Props 表格

在移动端使用 HTML 表格包装器实现水平滚动：

```mdx
<div style={{ overflowX: 'auto', width: '100%' }}>

| Prop              | Example             | Type    | Status   |
| ----------------- | ------------------- | ------- | -------- |
| [`src`](#src)     | `src="/image.png"`  | String  | Required |
| [`alt`](#alt)     | `alt="Description"` | String  | Required |
| [`width`](#width) | `width={500}`       | Integer | -        |

</div>
```

### Status 值

- `Required` - 必须提供
- `-` - 可选
- `Deprecated` - 将被移除，请使用替代方案

## 共享内容模式

用于与 App Router 共享内容的 Pages Router 文档：

**App Router（源）：** `docs/01-app/03-api-reference/02-components/image.mdx`

- 包含完整文档
- 使用 `<AppOnly>` 和 `<PagesOnly>` 处理路由特定章节

**Pages Router（使用者）：** `docs/02-pages/03-api-reference/01-components/image.mdx`

```yaml
---
title: Image Component
description: Optimize images using next/image.
source: app/api-reference/components/image
---
```

`source` 字段从 App Router 文档拉取内容。

## 写作风格

### 语气

- **指南：** 教学式，使用"您"来称呼用户
- **API 参考：** 技术性，使用祈使动词（"创建"、"传递"、"返回"）

### 清晰度

- 使用简单词汇而非复杂替代词
- 要具体："the `src` prop"而非"this prop"
- 除非正在解释，否则避免使用术语

### 结构

典型页面结构：

1. 简要介绍（是什么以及为什么）
2. 最小可用示例
3. 详细参考/选项
4. 不同用例的示例
5. 相关链接（通过 frontmatter）

## 文件命名

- 使用 kebab-case：`generate-metadata.mdx`
- 添加数字前缀用于排序：`01-installation.mdx`
- 索引页面：`index.mdx`

## 验证命令

```bash
pnpm lint              # 完整 lint 检查
pnpm prettier-fix      # 修复格式
pnpm types             # TypeScript 检查
```
