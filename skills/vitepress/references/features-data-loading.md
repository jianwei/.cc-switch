---
name: vitepress-data-loading
description: Build-time data loaders for fetching remote data or processing local files
---

# @author Claude Code (claude-sonnet-4-6)

# 数据加载

VitePress 数据加载器在构建时运行，加载任意数据并序列化为 JSON 注入客户端包。

## 基本用法

创建以 `.data.js` 或 `.data.ts` 结尾的文件：

```ts
// example.data.ts
export default {
  load() {
    return {
      hello: 'world',
      timestamp: Date.now()
    }
  }
}
```

导入 `data` 命名导出：

```vue
<script setup>
import { data } from './example.data.ts'
</script>

<template>
  <pre>{{ data }}</pre>
</template>
```

## 异步数据

获取远程数据：

```ts
// api.data.ts
export default {
  async load() {
    const response = await fetch('https://api.example.com/data')
    return response.json()
  }
}
```

## 带监视的本地文件

处理本地文件并支持热重载：

```ts
// posts.data.ts
import fs from 'node:fs'
import { parse } from 'csv-parse/sync'

export default {
  watch: ['./data/*.csv'],
  load(watchedFiles) {
    // watchedFiles = 绝对路径数组
    return watchedFiles.map(file => {
      return parse(fs.readFileSync(file, 'utf-8'), {
        columns: true,
        skip_empty_lines: true
      })
    })
  }
}
```

## createContentLoader

用于加载 Markdown 内容的辅助函数（博客/归档常用）：

```ts
// posts.data.ts
import { createContentLoader } from 'vitepress'

export default createContentLoader('posts/*.md')
```

返回 `ContentData` 数组：

```ts
interface ContentData {
  url: string                    // 例如 /posts/hello.html
  frontmatter: Record<string, any>
  src?: string                   // 原始 markdown（可选）
  html?: string                  // 渲染后的 HTML（可选）
  excerpt?: string               // 摘要 HTML（可选）
}
```

带选项：

```ts
// posts.data.ts
import { createContentLoader } from 'vitepress'

export default createContentLoader('posts/*.md', {
  includeSrc: true,     // 包含原始 markdown
  render: true,         // 包含渲染后的 HTML
  excerpt: true,        // 包含摘要（第一个 --- 之前的内容）

  transform(rawData) {
    // 按日期排序，最新的在前
    return rawData
      .sort((a, b) => +new Date(b.frontmatter.date) - +new Date(a.frontmatter.date))
      .map(page => ({
        title: page.frontmatter.title,
        url: page.url,
        date: page.frontmatter.date,
        excerpt: page.excerpt
      }))
  }
})
```

## 使用示例：博客索引

```ts
// posts.data.ts
import { createContentLoader } from 'vitepress'

export default createContentLoader('posts/*.md', {
  excerpt: true,
  transform(data) {
    return data
      .filter(post => !post.frontmatter.draft)
      .sort((a, b) => +new Date(b.frontmatter.date) - +new Date(a.frontmatter.date))
  }
})
```

```vue
<!-- posts/index.md -->
<script setup>
import { data as posts } from './posts.data.ts'
</script>

<template>
  <ul>
    <li v-for="post in posts" :key="post.url">
      <a :href="post.url">{{ post.frontmatter.title }}</a>
      <span>{{ post.frontmatter.date }}</span>
    </li>
  </ul>
</template>
```

## 类型化数据加载器

```ts
// example.data.ts
import { defineLoader } from 'vitepress'

export interface Data {
  posts: Array<{ title: string; url: string }>
}

declare const data: Data
export { data }

export default defineLoader({
  watch: ['./posts/*.md'],
  async load(): Promise<Data> {
    // ...
    return { posts: [] }
  }
})
```

## 在构建钩子中使用

在配置中用于生成额外文件：

```ts
// .vitepress/config.ts
import { createContentLoader } from 'vitepress'

export default {
  async buildEnd() {
    const posts = await createContentLoader('posts/*.md').load()
    // 生成 RSS feed、sitemap 等
  }
}
```

## 访问配置

```ts
// example.data.ts
import type { SiteConfig } from 'vitepress'

export default {
  load() {
    const config: SiteConfig = (globalThis as any).VITEPRESS_CONFIG
    return { base: config.site.base }
  }
}
```

## 关键要点

- 数据加载器仅在 Node.js 构建时运行
- 文件必须以 `.data.js` 或 `.data.ts` 结尾
- 导入 `data` 命名导出（非默认导出）
- 使用 `watch` 实现本地文件热重载
- `createContentLoader` 简化了加载 Markdown 集合
- 保持数据量小 - 它会被内联到客户端包中
- 大数据应使用 `transform` 减少载荷

<!--
Source references:
- https://vitepress.dev/guide/data-loading
-->
