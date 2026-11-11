---
name: vitepress-dynamic-routes
description: Generate multiple pages from a single markdown template using paths loader files
---

# @author Claude Code (claude-sonnet-4-6)

# 动态路由

从单个 Markdown 文件和动态数据生成多个页面。适用于博客、包文档或任何数据驱动的页面。

## 基本设置

创建带括号参数的模板文件和 paths 加载器：

```
.
└─ packages/
   ├─ [pkg].md           # 路由模板
   └─ [pkg].paths.js     # Paths 加载器
```

paths 加载器导出返回路由参数的 `paths` 方法：

```js
// packages/[pkg].paths.js
export default {
  paths() {
    return [
      { params: { pkg: 'foo' }},
      { params: { pkg: 'bar' }},
      { params: { pkg: 'baz' }}
    ]
  }
}
```

生成的页面：
- `/packages/foo.html`
- `/packages/bar.html`
- `/packages/baz.html`

## 多参数

```
.
└─ packages/
   ├─ [pkg]-[version].md
   └─ [pkg]-[version].paths.js
```

```js
// packages/[pkg]-[version].paths.js
export default {
  paths() {
    return [
      { params: { pkg: 'foo', version: '1.0.0' }},
      { params: { pkg: 'foo', version: '2.0.0' }},
      { params: { pkg: 'bar', version: '1.0.0' }}
    ]
  }
}
```

## 动态路径生成

从本地文件：

```js
// packages/[pkg].paths.js
import fs from 'node:fs'

export default {
  paths() {
    return fs.readdirSync('packages').map(pkg => ({
      params: { pkg }
    }))
  }
}
```

从远程 API：

```js
// packages/[pkg].paths.js
export default {
  async paths() {
    const packages = await fetch('https://api.example.com/packages').then(r => r.json())

    return packages.map(pkg => ({
      params: {
        pkg: pkg.name,
        version: pkg.version
      }
    }))
  }
}
```

## 在页面中访问参数

模板全局变量：

```md
<!-- packages/[pkg].md -->
# Package: {{ $params.pkg }}

Version: {{ $params.version }}
```

在脚本中：

```vue
<script setup>
import { useData } from 'vitepress'
const { params } = useData()
</script>

<template>
  <h1>{{ params.pkg }}</h1>
</template>
```

## 传递内容

对于重型内容（来自 CMS 的原始 markdown/HTML），使用 `content` 而非 params 以避免客户端包臃肿：

```js
// posts/[slug].paths.js
export default {
  async paths() {
    const posts = await fetch('https://cms.example.com/posts').then(r => r.json())

    return posts.map(post => ({
      params: { slug: post.slug },
      content: post.content  // 原始 markdown 或 HTML
    }))
  }
}
```

在模板中渲染内容：

```md
<!-- posts/[slug].md -->
---
title: {{ $params.title }}
---

<!-- @content -->
```

`<!-- @content -->` 占位符会被 paths 加载器中的内容替换。

## Watch 选项

模板或数据文件更改时自动重建：

```js
// posts/[slug].paths.js
export default {
  watch: [
    './templates/**/*.njk',
    '../data/**/*.json'
  ],

  paths(watchedFiles) {
    const dataFiles = watchedFiles.filter(f => f.endsWith('.json'))

    return dataFiles.map(file => {
      const data = JSON.parse(fs.readFileSync(file, 'utf-8'))
      return {
        params: { slug: data.slug },
        content: renderTemplate(data)
      }
    })
  }
}
```

## 完整示例：博客

```js
// posts/[slug].paths.js
import fs from 'node:fs'
import matter from 'gray-matter'

export default {
  watch: ['./posts/*.md'],

  paths(files) {
    return files
      .filter(f => !f.includes('[slug]'))
      .map(file => {
        const content = fs.readFileSync(file, 'utf-8')
        const { data, content: body } = matter(content)
        const slug = file.match(/([^/]+)\.md$/)[1]

        return {
          params: {
            slug,
            title: data.title,
            date: data.date
          },
          content: body
        }
      })
  }
}
```

```md
<!-- posts/[slug].md -->
---
layout: doc
---

# {{ $params.title }}

<time>{{ $params.date }}</time>

<!-- @content -->
```

## 关键要点

- 模板文件在文件名中使用 `[param]` 语法
- Paths 加载器文件必须命名为 `[param].paths.js` 或 `.ts`
- `paths()` 返回 `{ params: {...}, content?: string }` 数组
- 在模板中使用 `$params` 或在脚本中使用 `useData().params`
- 对重型数据使用 `content` 以避免客户端包臃肿
- `watch` 支持模板/数据文件更改时的 HMR

<!--
Source references:
- https://vitepress.dev/guide/routing#dynamic-routes
-->
