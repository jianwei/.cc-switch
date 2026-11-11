---
name: vitepress-internationalization
description: Setting up multi-language sites with locale configuration and RTL support
---

# @author Claude Code (claude-sonnet-4-6)

# 国际化

VitePress 通过区域配置支持多语言站点。

## 目录结构

按语言组织内容：

```
docs/
├─ en/
│  ├─ guide.md
│  └─ index.md
├─ zh/
│  ├─ guide.md
│  └─ index.md
└─ fr/
   ├─ guide.md
   └─ index.md
```

或者以根目录作为默认语言：

```
docs/
├─ guide.md        # 英语（根目录）
├─ index.md
├─ zh/
│  ├─ guide.md
│  └─ index.md
└─ fr/
   ├─ guide.md
   └─ index.md
```

## 配置

```ts
// .vitepress/config.ts
import { defineConfig } from 'vitepress'

export default defineConfig({
  locales: {
    root: {
      label: 'English',
      lang: 'en'
    },
    zh: {
      label: '简体中文',
      lang: 'zh-CN',
      link: '/zh/'
    },
    fr: {
      label: 'Français',
      lang: 'fr',
      link: '/fr/'
    }
  }
})
```

## 语言特定配置

为每个语言覆盖站点配置：

```ts
locales: {
  root: {
    label: 'English',
    lang: 'en',
    title: 'My Docs',
    description: 'Documentation site',
    themeConfig: {
      nav: [
        { text: 'Guide', link: '/guide/' }
      ],
      sidebar: {
        '/guide/': [
          { text: 'Introduction', link: '/guide/' }
        ]
      }
    }
  },
  zh: {
    label: '简体中文',
    lang: 'zh-CN',
    link: '/zh/',
    title: '我的文档',
    description: '文档站点',
    themeConfig: {
      nav: [
        { text: '指南', link: '/zh/guide/' }
      ],
      sidebar: {
        '/zh/guide/': [
          { text: '介绍', link: '/zh/guide/' }
        ]
      }
    }
  }
}
```

## 语言特定属性

每个语言可以覆盖以下配置：

```ts
interface LocaleSpecificConfig {
  lang?: string
  dir?: string              // 'ltr' 或 'rtl'
  title?: string
  titleTemplate?: string | boolean
  description?: string
  head?: HeadConfig[]       // 与现有配置合并
  themeConfig?: ThemeConfig // 浅合并
}
```

## 搜索国际化

### 本地搜索

```ts
themeConfig: {
  search: {
    provider: 'local',
    options: {
      locales: {
        zh: {
          translations: {
            button: {
              buttonText: '搜索',
              buttonAriaLabel: '搜索'
            },
            modal: {
              noResultsText: '没有结果',
              resetButtonTitle: '重置搜索',
              footer: {
                selectText: '选择',
                navigateText: '导航',
                closeText: '关闭'
              }
            }
          }
        }
      }
    }
  }
}
```

### Algolia 搜索

```ts
themeConfig: {
  search: {
    provider: 'algolia',
    options: {
      appId: '...',
      apiKey: '...',
      indexName: '...',
      locales: {
        zh: {
          placeholder: '搜索文档',
          translations: {
            button: { buttonText: '搜索文档' }
          }
        }
      }
    }
  }
}
```

## 独立的语言目录

对于完全独立的语言目录，没有根目录回退：

```
docs/
├─ en/
│  └─ index.md
├─ zh/
│  └─ index.md
└─ fr/
   └─ index.md
```

需要服务器重定向来处理 `/` → `/en/`。Netlify 示例：

```
/* /en/:splat 302 Language=en
/* /zh/:splat 302 Language=zh
/* /en/:splat 302
```

## 持久化语言选择

在语言切换时设置 Cookie：

```vue
<!-- .vitepress/theme/Layout.vue -->
<script setup>
import DefaultTheme from 'vitepress/theme'
import { useData, inBrowser } from 'vitepress'
import { watchEffect } from 'vue'

const { lang } = useData()

watchEffect(() => {
  if (inBrowser) {
    document.cookie = `nf_lang=${lang.value}; expires=Mon, 1 Jan 2030 00:00:00 UTC; path=/`
  }
})
</script>

<template>
  <DefaultTheme.Layout />
</template>
```

## RTL 支持（实验性）

对于从右到左的语言：

```ts
locales: {
  ar: {
    label: 'العربية',
    lang: 'ar',
    dir: 'rtl'
  }
}
```

需要 PostCSS 插件如 `postcss-rtlcss`：

```ts
// postcss.config.js
import rtlcss from 'postcss-rtlcss'

export default {
  plugins: [
    rtlcss({
      ltrPrefix: ':where([dir="ltr"])',
      rtlPrefix: ':where([dir="rtl"])'
    })
  ]
}
```

## 组织配置

将配置拆分为多个文件：

```
.vitepress/
├─ config/
│  ├─ index.ts      # 主配置，合并 locales
│  ├─ en.ts         # 英语配置
│  ├─ zh.ts         # 中文配置
│  └─ shared.ts     # 共享配置
```

```ts
// .vitepress/config/index.ts
import { defineConfig } from 'vitepress'
import { shared } from './shared'
import { en } from './en'
import { zh } from './zh'

export default defineConfig({
  ...shared,
  locales: {
    root: { label: 'English', ...en },
    zh: { label: '简体中文', ...zh }
  }
})
```

## 关键要点

- 在配置中使用 `locales` 对象，`root` 表示默认语言
- 每个语言可以覆盖 title、description 和 themeConfig
- `themeConfig` 是浅合并（每个语言需要定义完整的 nav/sidebar）
- 不要在语言级别覆盖 `themeConfig.algolia`
- `dir: 'rtl'` 需要配合 PostCSS 插件启用 RTL
- 语言切换器会在导航栏自动显示

<!--
Source references:
- https://vitepress.dev/guide/i18n
-->
