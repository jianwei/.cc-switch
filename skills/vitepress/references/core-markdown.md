---
name: vitepress-markdown
description: Markdown extensions including frontmatter, custom containers, tables, anchors, and file includes
---

# @author Claude Code (claude-sonnet-4-6)

# Markdown 扩展

VitePress 扩展了标准 Markdown，添加了文档专用的额外功能。

## Frontmatter

Markdown 文件顶部的 YAML 元数据：

```md
---
title: Page Title
description: Page description for SEO
layout: doc
outline: [2, 3]
---

# Content starts here
```

在模板中访问 frontmatter：

```md
# {{ $frontmatter.title }}
```

或在脚本中：

```vue
<script setup>
import { useData } from 'vitepress'
const { frontmatter } = useData()
</script>
```

## 自定义容器

样式化的提示块：

```md
::: info
This is an info box.
:::

::: tip
This is a tip.
:::

::: warning
This is a warning.
:::

::: danger
This is a dangerous warning.
:::

::: details Click to expand
Hidden content here.
:::
```

自定义标题：

```md
::: danger STOP
Do not proceed!
:::

::: details Click me {open}
Open by default with {open} attribute.
:::
```

## GitHub 风格 Alerts

使用块引用的替代语法：

```md
> [!NOTE]
> Highlights information users should know.

> [!TIP]
> Optional information for success.

> [!WARNING]
> Critical content requiring attention.

> [!CAUTION]
> Negative potential consequences.
```

## 标题锚点

标题自动获得锚链接。自定义锚点：

```md
# My Heading {#custom-anchor}

[Link to heading](#custom-anchor)
```

## 目录

使用以下方式生成目录：

```md
[[toc]]
```

## GitHub 风格表格

```md
| Feature | Status |
|---------|--------|
| SSR     | ✅     |
| HMR     | ✅     |
```

## Emoji

使用简码：

```md
:tada: :rocket: :100:
```

## 文件包含

包含其他文件的内容：

```md
<!--@include: ./shared/header.md-->
```

带行范围：

```md
<!--@include: ./code.md{3,10}-->  <!-- 第 3-10 行 -->
<!--@include: ./code.md{3,}-->   <!-- 从第 3 行开始 -->
<!--@include: ./code.md{,10}-->  <!-- 到第 10 行 -->
```

带区域：

```md
<!-- In parts/basics.md -->
<!-- #region usage -->
Usage content here
<!-- #endregion usage -->

<!-- Include just that region -->
<!--@include: ./parts/basics.md#usage-->
```

## 代码片段导入

从文件导入代码：

```md
<<< @/snippets/example.js
```

带行高亮：

```md
<<< @/snippets/example.js{2,4-6}
```

带语言覆盖：

```md
<<< @/snippets/example.cs{1,2 c#:line-numbers}
```

导入特定区域：

```md
<<< @/snippets/example.js#regionName{1,2}
```

## 代码组

代码变体的标签页组：

````md
::: code-group

```js [config.js]
export default { /* ... */ }
```

```ts [config.ts]
export default defineConfig({ /* ... */ })
```

:::
````

在代码组中导入文件：

```md
::: code-group

<<< @/snippets/config.js
<<< @/snippets/config.ts

:::
```

## 数学公式

需要设置：

```bash
npm add -D markdown-it-mathjax3@^4
```

```ts
// .vitepress/config.ts
export default {
  markdown: {
    math: true
  }
}
```

然后使用 LaTeX：

```md
Inline: $E = mc^2$

Block:
$$
\frac{-b \pm \sqrt{b^2-4ac}}{2a}
$$
```

## 图片懒加载

```ts
export default {
  markdown: {
    image: {
      lazyLoading: true
    }
  }
}
```

## 原始容器

防止 VitePress 样式冲突：

```md
::: raw
<CustomComponent />
:::
```

## 关键要点

- Frontmatter 支持 YAML 或 JSON 格式
- 自定义容器支持 info、tip、warning、danger、details
- `[[toc]]` 生成目录
- `@` 在导入中表示源根目录（或 `srcDir` 如果配置了）
- 代码组创建带标签的代码块
- 数学支持需要 markdown-it-mathjax3 包

<!--
Source references:
- https://vitepress.dev/guide/markdown
- https://vitepress.dev/guide/frontmatter
-->
