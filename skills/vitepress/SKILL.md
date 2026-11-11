---
name: vitepress
description: VitePress 是一个由 Vite 和 Vue 驱动的静态网站生成器。适用于构建文档站点、配置主题，或编写包含 Vue 组件的 Markdown。
metadata:
  author: Anthony Fu
  version: "2026.1.28"
  source: Generated from https://github.com/vuejs/vitepress, scripts located at https://github.com/antfu/skills
---

// @author Codex (Codex-sonnet-4-6)

VitePress 是一个基于 Vite 和 Vue 3 构建的静态网站生成器（SSG）。它接收 Markdown 内容，应用主题，然后生成静态 HTML，最终成为一个用于快速导航的单页应用（SPA）。非常适合用于文档、博客和营销站点。

**核心特性：**
- 基于文件的路由，使用 `.md` 文件
- Vue 组件可直接在 Markdown 中使用
- 快速的热模块替换（<100ms 即时更新）
- 默认主题针对文档进行了优化
- 内置搜索功能（本地或 Algolia）

**在处理 VitePress 项目之前：**
- 检查 `.vitepress/config.ts` 了解站点配置
- 查看 `.vitepress/theme/` 了解自定义主题扩展
- `public/` 目录包含静态资源，会原样提供服务

> 此技能基于 VitePress 1.x，生成于 2026-01-28。

## 核心内容

| 主题 | 描述 | 参考文档 |
|-------|-------------|-----------|
| 配置 | 配置文件设置、defineConfig、站点元数据 | [core-config](references/core-config.md) |
| CLI | 命令行界面：dev、build、preview、init | [core-cli](references/core-cli.md) |
| 路由 | 基于文件的路由、源目录、重写 | [core-routing](references/core-routing.md) |
| Markdown | Frontmatter、容器、表格、锚点、包含文件 | [core-markdown](references/core-markdown.md) |

## 功能特性

### 代码与内容

| 主题 | 描述 | 参考文档 |
|-------|-------------|-----------|
| 代码块 | 语法高亮、行高亮、彩色差异、聚焦 | [features-code-blocks](references/features-code-blocks.md) |
| Markdown 中的 Vue | 组件、script setup、指令、模板 | [features-vue](references/features-vue.md) |
| 数据加载 | 构建时数据加载器、createContentLoader | [features-data-loading](references/features-data-loading.md) |
| 动态路由 | 从数据生成页面、paths 加载文件 | [features-dynamic-routes](references/features-dynamic-routes.md) |

## 主题

| 主题 | 描述 | 参考文档 |
|-------|-------------|-----------|
| 主题配置 | 导航、侧边栏、搜索、社交链接、页脚 | [theme-config](references/theme-config.md) |
| 定制化 | CSS 变量、插槽、字体、全局组件 | [theme-customization](references/theme-customization.md) |
| 自定义主题 | 从零开始构建主题、主题接口 | [theme-custom](references/theme-custom.md) |

## 高级用法

| 主题 | 描述 | 参考文档 |
|-------|-------------|-----------|
| 国际化 | 多语言站点、区域配置 | [advanced-i18n](references/advanced-i18n.md) |
| SSR 兼容性 | 服务端渲染、ClientOnly、动态导入 | [advanced-ssr](references/advanced-ssr.md) |

## 实战配方

| 主题 | 描述 | 参考文档 |
|-------|-------------|-----------|
| 部署 | GitHub Pages、Netlify、Vercel、Cloudflare、Nginx | [recipes-deploy](references/recipes-deploy.md) |
