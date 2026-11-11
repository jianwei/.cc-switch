---
name: vitepress-configuration
description: Config file setup, defineConfig helper, site metadata, and build options
---

# @author Claude Code (claude-sonnet-4-6)

# 配置

VitePress 配置定义在 `.vitepress/config.[js|ts|mjs|mts]` 文件中。使用 `defineConfig` 以获得 TypeScript 智能提示。

## 基础配置

```ts
// .vitepress/config.ts
import { defineConfig } from 'vitepress'

export default defineConfig({
  // 站点元数据
  title: 'My Docs',
  description: 'Documentation site',
  lang: 'en-US',

  // URL 基础路径（用于 GitHub Pages：'/repo-name/'）
  base: '/',

  // 主题配置
  themeConfig: {
    // 参见 theme-config.md
  }
})
```

## 站点元数据

```ts
export default defineConfig({
  title: 'VitePress',           // 显示在导航栏，用于页面标题
  titleTemplate: ':title - Docs', // 页面标题格式（:title = h1）
  description: 'Site description', // meta 描述
  lang: 'en-US',                 // HTML lang 属性

  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }],
    ['meta', { name: 'theme-color', content: '#5f67ee' }],
    ['script', { async: '', src: 'https://analytics.example.com/script.js' }]
  ]
})
```

## 构建选项

```ts
export default defineConfig({
  // 源文件目录（相对于项目根目录）
  srcDir: './src',

  // 源文件排除模式
  srcExclude: ['**/README.md', '**/TODO.md'],

  // 输出目录
  outDir: './.vitepress/dist',

  // 缓存目录
  cacheDir: './.vitepress/cache',

  // 干净的 URL，不带 .html 扩展名（需要服务器支持）
  cleanUrls: true,

  // 构建时忽略死链
  ignoreDeadLinks: true,
  // 或使用特定模式：
  ignoreDeadLinks: ['/playground', /^https?:\/\/localhost/],

  // 从 git 获取最后更新时间戳
  lastUpdated: true
})
```

## 路由重写

将源路径映射到不同的输出路径：

```ts
export default defineConfig({
  rewrites: {
    // 静态映射
    'packages/pkg-a/src/index.md': 'pkg-a/index.md',

    // 动态参数
    'packages/:pkg/src/:slug*': ':pkg/:slug*'
  }
})
```

## 外观（深色模式）

```ts
export default defineConfig({
  appearance: true,           // 启用切换（默认）
  appearance: 'dark',         // 默认深色
  appearance: 'force-dark',   // 始终深色，无切换
  appearance: 'force-auto',   // 始终跟随系统偏好
  appearance: false           // 禁用深色模式
})
```

## Vite 和 Vue 配置

```ts
export default defineConfig({
  // 传递给 Vite 的选项
  vite: {
    plugins: [],
    resolve: { alias: {} },
    css: { preprocessorOptions: {} }
  },

  // 传递给 @vitejs/plugin-vue 的选项
  vue: {
    template: { compilerOptions: {} }
  },

  // 配置 markdown-it
  markdown: {
    lineNumbers: true,
    toc: { level: [1, 2, 3] },
    math: true, // 需要 markdown-it-mathjax3
    container: {
      tipLabel: 'TIP',
      warningLabel: 'WARNING',
      dangerLabel: 'DANGER'
    }
  }
})
```

## 构建钩子

```ts
export default defineConfig({
  // 转换页面数据
  transformPageData(pageData, { siteConfig }) {
    pageData.frontmatter.head ??= []
    pageData.frontmatter.head.push([
      'meta', { name: 'og:title', content: pageData.title }
    ])
  },

  // 生成每个页面之前转换 head
  async transformHead(context) {
    return [['meta', { name: 'custom', content: context.page }]]
  },

  // 构建完成后
  async buildEnd(siteConfig) {
    // 生成 sitemap、RSS 等
  }
})
```

## 动态配置

用于异步配置：

```ts
export default async () => {
  const data = await fetch('https://api.example.com/data').then(r => r.json())

  return defineConfig({
    title: data.title,
    themeConfig: {
      sidebar: data.sidebar
    }
  })
}
```

## 关键要点

- 配置文件支持 `.js`、`.ts`、`.mjs`、`.mts` 扩展名
- 使用 `defineConfig` 以获得 TypeScript 支持
- `base` 必须以 `/` 开头和结尾，用于子路径部署
- `srcDir` 将源文件与项目根目录分离
- 构建钩子支持自定义转换和后处理

<!--
Source references:
- https://vitepress.dev/reference/site-config
- https://vitepress.dev/guide/getting-started
-->
