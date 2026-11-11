---
name: vitepress-theme-configuration
description: Default theme configuration for navigation, sidebar, search, social links, and footer
---

# @author Claude Code (claude-sonnet-4-6)

# 主题配置

通过 VitePress 配置中的 `themeConfig` 配置默认主题。

## 导航

```ts
export default {
  themeConfig: {
    // 导航栏中的站点标题（覆盖 config.title）
    siteTitle: 'My Docs',
    siteTitle: false,  // 隐藏标题

    // Logo
    logo: '/logo.svg',
    logo: { light: '/light-logo.svg', dark: '/dark-logo.svg', alt: 'Logo' },

    // 导航链接
    nav: [
      { text: 'Guide', link: '/guide/' },
      { text: 'API', link: '/api/' },
      { text: 'GitHub', link: 'https://github.com/...' }
    ]
  }
}
```

### 下拉菜单

```ts
nav: [
  {
    text: 'Dropdown',
    items: [
      { text: 'Item A', link: '/item-a' },
      { text: 'Item B', link: '/item-b' }
    ]
  },
  // 带分区
  {
    text: 'Versions',
    items: [
      {
        text: 'v2.x',
        items: [
          { text: 'v2.0', link: '/v2/' },
          { text: 'v2.1', link: '/v2.1/' }
        ]
      }
    ]
  }
]
```

### 激活匹配

控制导航项何时显示为激活状态：

```ts
nav: [
  {
    text: 'Guide',
    link: '/guide/',
    activeMatch: '/guide/'  // 正则表达式模式
  }
]
```

## 侧边栏

### 简单侧边栏

```ts
sidebar: [
  {
    text: 'Guide',
    items: [
      { text: 'Introduction', link: '/guide/' },
      { text: 'Getting Started', link: '/guide/getting-started' }
    ]
  }
]
```

### 多侧边栏

不同部分使用不同侧边栏：

```ts
sidebar: {
  '/guide/': [
    {
      text: 'Guide',
      items: [
        { text: 'Introduction', link: '/guide/' },
        { text: 'Getting Started', link: '/guide/getting-started' }
      ]
    }
  ],
  '/api/': [
    {
      text: 'API Reference',
      items: [
        { text: 'Config', link: '/api/config' },
        { text: 'Methods', link: '/api/methods' }
      ]
    }
  ]
}
```

### 可折叠组

```ts
sidebar: [
  {
    text: 'Section A',
    collapsed: false,  // 默认展开，可以折叠
    items: [...]
  },
  {
    text: 'Section B',
    collapsed: true,   // 默认折叠
    items: [...]
  }
]
```

### 基础路径

使用公共基础简化链接：

```ts
sidebar: {
  '/guide/': {
    base: '/guide/',
    items: [
      { text: 'Intro', link: 'intro' },        // /guide/intro
      { text: 'Setup', link: 'getting-started' } // /guide/getting-started
    ]
  }
}
```

## 搜索

### 本地搜索

```ts
themeConfig: {
  search: {
    provider: 'local'
  }
}
```

带选项：

```ts
search: {
  provider: 'local',
  options: {
    miniSearch: {
      searchOptions: {
        fuzzy: 0.2,
        prefix: true
      }
    }
  }
}
```

### Algolia DocSearch

```ts
search: {
  provider: 'algolia',
  options: {
    appId: 'YOUR_APP_ID',
    apiKey: 'YOUR_API_KEY',
    indexName: 'YOUR_INDEX_NAME'
  }
}
```

## 社交链接

```ts
socialLinks: [
  { icon: 'github', link: 'https://github.com/...' },
  { icon: 'twitter', link: 'https://twitter.com/...' },
  { icon: 'discord', link: 'https://discord.gg/...' },
  // 自定义 SVG
  {
    icon: { svg: '<svg>...</svg>' },
    link: 'https://...',
    ariaLabel: 'Custom Link'
  }
]
```

## 页脚

```ts
footer: {
  message: 'Released under the MIT License.',
  copyright: 'Copyright © 2024 My Project'
}
```

页脚仅在没有侧边栏的页面上显示。

## 编辑链接

```ts
editLink: {
  pattern: 'https://github.com/org/repo/edit/main/docs/:path',
  text: 'Edit this page on GitHub'
}
```

`:path` 会被页面的源文件路径替换。

## 最后更新

在站点配置中启用：

```ts
export default {
  lastUpdated: true  // 从 git 获取时间戳
}
```

自定义显示：

```ts
themeConfig: {
  lastUpdated: {
    text: 'Updated at',
    formatOptions: {
      dateStyle: 'full',
      timeStyle: 'medium'
    }
  }
}
```

## 大纲（目录）

```ts
outline: {
  level: [2, 3],      // 显示哪些标题级别
  label: 'On this page'
}
```

或只设置级别：

```ts
outline: 'deep'  // 同 [2, 6]
outline: 2       // 仅 h2
outline: [2, 4]  // h2 到 h4
```

## 文档页脚导航

```ts
docFooter: {
  prev: 'Previous page',
  next: 'Next page'
}
// 或禁用：
docFooter: {
  prev: false,
  next: false
}
```

## 外部链接图标

```ts
externalLinkIcon: true  // 在外部链接上显示图标
```

## 外观切换标签

```ts
darkModeSwitchLabel: 'Appearance',
lightModeSwitchTitle: 'Switch to light theme',
darkModeSwitchTitle: 'Switch to dark theme',
sidebarMenuLabel: 'Menu',
returnToTopLabel: 'Return to top'
```

## 关键要点

- `nav` 定义顶部导航链接
- `sidebar` 可以是数组（单个）或对象（多个侧边栏）
- 使用 `collapsed` 实现可折叠侧边栏部分
- 本地搜索开箱即用
- `editLink.pattern` 使用 `:path` 占位符
- 在站点配置中启用 `lastUpdated`，在 themeConfig 中自定义

<!--
Source references:
- https://vitepress.dev/reference/default-theme-config
- https://vitepress.dev/reference/default-theme-nav
- https://vitepress.dev/reference/default-theme-sidebar
- https://vitepress.dev/reference/default-theme-search
-->
