---
name: vitepress-custom-themes
description: Building custom themes from scratch with the theme interface, Layout component, and enhanceApp
---

# @author Claude Code (claude-sonnet-4-6)

# 自定义主题

当默认主题不满足需求时，从头构建主题。

## 主题入口

创建 `.vitepress/theme/index.ts`：

```ts
// .vitepress/theme/index.ts
import Layout from './Layout.vue'

export default {
  Layout,
  enhanceApp({ app, router, siteData }) {
    // 注册全局组件、插件等
  }
}
```

## 主题接口

```ts
interface Theme {
  // 必需：根布局组件
  Layout: Component

  // 可选：增强 Vue 应用实例
  enhanceApp?: (ctx: EnhanceAppContext) => Awaitable<void>

  // 可选：扩展另一个主题
  extends?: Theme
}

interface EnhanceAppContext {
  app: App              // Vue 应用实例
  router: Router        // VitePress 路由
  siteData: Ref<SiteData>  // 站点级元数据
}
```

## 基础布局

布局组件必须为 Markdown 渲染 `<Content />`：

```vue
<!-- .vitepress/theme/Layout.vue -->
<script setup>
import { useData } from 'vitepress'
const { page, frontmatter } = useData()
</script>

<template>
  <div class="layout">
    <header>
      <nav>My Site</nav>
    </header>

    <main>
      <div v-if="page.isNotFound">
        <h1>404 - Page Not Found</h1>
      </div>

      <div v-else-if="frontmatter.layout === 'home'">
        <h1>Welcome!</h1>
      </div>

      <article v-else>
        <Content />
      </article>
    </main>

    <footer>
      <p>© 2024 My Site</p>
    </footer>
  </div>
</template>
```

## 运行时 API

在主题中访问 VitePress 数据：

```vue
<script setup>
import { useData, useRoute, useRouter } from 'vitepress'

// 页面和站点数据
const {
  site,        // 站点配置（title、description 等）
  theme,       // 主题配置
  page,        // 当前页面数据
  frontmatter, // 当前页面 frontmatter
  title,       // 页面标题
  description, // 页面描述
  lang,        // 当前语言
  isDark,      // 深色模式状态
  params       // 动态路由参数
} = useData()

// 路由
const route = useRoute()
const router = useRouter()

// 编程式导航
const goToGuide = () => router.go('/guide/')
</script>
```

## 内置组件

```vue
<script setup>
import { Content } from 'vitepress'
</script>

<template>
  <!-- 渲染 Markdown 内容 -->
  <Content />

  <!-- 仅在客户端渲染插槽（SSR 安全）-->
  <ClientOnly>
    <NonSSRComponent />
  </ClientOnly>
</template>
```

## 扩展另一个主题

在默认主题或任何其他主题上构建：

```ts
// .vitepress/theme/index.ts
import DefaultTheme from 'vitepress/theme'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    // 你的自定义
  }
}
```

## 注册插件和组件

```ts
// .vitepress/theme/index.ts
import Layout from './Layout.vue'
import GlobalComponent from './GlobalComponent.vue'

export default {
  Layout,
  enhanceApp({ app }) {
    // 注册全局组件
    app.component('GlobalComponent', GlobalComponent)

    // 注册插件
    app.use(MyPlugin)

    // Provide/inject
    app.provide('key', value)
  }
}
```

## 异步 enhanceApp

对于需要异步初始化的插件：

```ts
export default {
  Layout,
  async enhanceApp({ app }) {
    if (!import.meta.env.SSR) {
      // 仅客户端插件
      const plugin = await import('browser-only-plugin')
      app.use(plugin.default)
    }
  }
}
```

## 主题感知布局

处理不同页面布局：

```vue
<script setup>
import { useData } from 'vitepress'
import Home from './Home.vue'
import Doc from './Doc.vue'
import Page from './Page.vue'
import NotFound from './NotFound.vue'

const { page, frontmatter } = useData()
</script>

<template>
  <NotFound v-if="page.isNotFound" />
  <Home v-else-if="frontmatter.layout === 'home'" />
  <Page v-else-if="frontmatter.layout === 'page'" />
  <Doc v-else />
</template>
```

## 分发主题

作为 npm 包：

```ts
// my-theme/index.ts
import Layout from './Layout.vue'
export default { Layout }

// 导出配置类型
export type { ThemeConfig } from './types'
```

使用者：

```ts
// .vitepress/theme/index.ts
import Theme from 'my-vitepress-theme'

export default Theme

// 或扩展它
export default {
  extends: Theme,
  enhanceApp({ app }) {
    // 额外自定义
  }
}
```

## 主题配置类型

自定义主题配置类型：

```ts
// .vitepress/config.ts
import { defineConfigWithTheme } from 'vitepress'
import type { ThemeConfig } from 'my-theme'

export default defineConfigWithTheme<ThemeConfig>({
  themeConfig: {
    // 类型检查的主题配置
  }
})
```

## 关键要点

- 主题必须导出 `Layout` 组件
- `<Content />` 渲染 Markdown 内容
- 使用 `useData()` 访问页面/站点数据
- `enhanceApp` 在服务器和客户端都运行
- 使用 `import.meta.env.SSR` 判断仅客户端代码
- 使用 `extends` 在现有主题上构建

<!--
Source references:
- https://vitepress.dev/guide/custom-theme
-->
