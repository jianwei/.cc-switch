---
name: vitepress-routing
description: File-based routing, source directory structure, clean URLs, and route rewrites
---

# @author Claude Code (claude-sonnet-4-6)

# 路由

VitePress 使用基于文件的路由，Markdown 文件直接映射到 HTML 页面。

## 文件到 URL 的映射

```
.
├─ index.md           →  /index.html (/)
├─ about.md           →  /about.html
├─ guide/
│  ├─ index.md        →  /guide/index.html (/guide/)
│  └─ getting-started.md → /guide/getting-started.html
```

## 项目结构

```
.
├─ docs                    # 项目根目录
│  ├─ .vitepress          # VitePress 目录
│  │  ├─ config.ts        # 配置文件
│  │  ├─ theme/           # 自定义主题
│  │  ├─ cache/           # 开发服务器缓存（gitignore）
│  │  └─ dist/            # 构建输出（gitignore）
│  ├─ public/             # 静态资源（原样复制）
│  ├─ index.md            # 首页
│  └─ guide/
│     └─ intro.md
```

## 源目录

将源文件与项目根目录分离：

```ts
// .vitepress/config.ts
export default {
  srcDir: './src'  // Markdown 文件位于 ./src/
}
```

使用 `srcDir: 'src'` 时：

```
.
├─ .vitepress/           # 配置保持在项目根目录
└─ src/                  # 源目录
   ├─ index.md          →  /
   └─ guide/intro.md    →  /guide/intro.html
```

## 页面间链接

使用相对或绝对路径。省略文件扩展名：

```md
<!-- 推荐 -->
[Getting Started](./getting-started)
[Guide](/guide/)

<!-- 可以工作但不推荐 -->
[Getting Started](./getting-started.md)
[Getting Started](./getting-started.html)
```

## 干净的 URL

从 URL 中移除 `.html` 扩展名（需要服务器支持）：

```ts
export default {
  cleanUrls: true
}
```

**服务器要求：**
- Netlify、GitHub Pages：默认支持
- Vercel：在 `vercel.json` 中启用 `cleanUrls`
- Nginx：配置 `try_files $uri $uri.html $uri/ =404`

## 路由重写

自定义源路径和输出路径之间的映射：

```ts
export default {
  rewrites: {
    // 静态映射
    'packages/pkg-a/src/index.md': 'pkg-a/index.md',
    'packages/pkg-a/src/foo.md': 'pkg-a/foo.md',

    // 动态参数
    'packages/:pkg/src/:slug*': ':pkg/:slug*'
  }
}
```

这将 `packages/pkg-a/src/intro.md` 映射到 `/pkg-a/intro.html`。

**重要：** 重写文件中的相对链接应基于重写后的路径，而非源路径。

重写也可以是函数：

```ts
export default {
  rewrites(id) {
    return id.replace(/^packages\/([^/]+)\/src\//, '$1/')
  }
}
```

## public 目录

`public/` 中的文件会原样复制到输出根目录：

```
docs/public/
  ├─ favicon.ico     →  /favicon.ico
  ├─ robots.txt      →  /robots.txt
  └─ images/logo.png →  /images/logo.png
```

使用绝对路径引用：

```md
![Logo](/images/logo.png)
```

## 基础 URL

用于子路径部署（如 GitHub Pages）：

```ts
export default {
  base: '/repo-name/'
}
```

所有绝对路径都会自动添加 base 前缀。对于组件中的动态路径，使用 `withBase`：

```vue
<script setup>
import { withBase } from 'vitepress'
</script>

<template>
  <img :src="withBase('/logo.png')" />
</template>
```

## 关键要点

- `index.md` 文件映射到目录根（`/guide/` 而非 `/guide/index`）
- 在链接中使用不带扩展名的路径以保持灵活性
- `srcDir` 将源文件与配置分离
- `cleanUrls` 移除 `.html` 但需要服务器支持
- `rewrites` 支持复杂源结构与干净的输出 URL

<!--
Source references:
- https://vitepress.dev/guide/routing
- https://vitepress.dev/guide/asset-handling
-->
