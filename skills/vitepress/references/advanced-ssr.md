---
name: vitepress-ssr-compatibility
description: Server-side rendering compatibility, ClientOnly component, and handling browser-only code
---

# @author Claude Code (claude-sonnet-4-6)

# SSR 兼容性

VitePress 在构建期间会在服务器上预渲染页面。所有 Vue 代码必须与 SSR 兼容。

## 规则

只能在下述 Vue 生命周期钩子中访问浏览器/DOM API：
- `onMounted()`
- `onBeforeMount()`

```vue
<script setup>
import { onMounted, ref } from 'vue'

const windowWidth = ref(0)

onMounted(() => {
  // 安全 - 仅在浏览器中运行
  windowWidth.value = window.innerWidth
})
</script>
```

**不要**在顶层访问：

```vue
<script setup>
// 错误 - 在 SSR 期间运行，此时 window 不存在
const width = window.innerWidth
</script>
```

## ClientOnly 组件

包装不兼容 SSR 的组件：

```vue
<template>
  <ClientOnly>
    <BrowserOnlyComponent />
  </ClientOnly>
</template>
```

## 导入时访问浏览器的库

某些库在导入时会访问 `window` 或 `document`：

### 在 onMounted 中动态导入

```vue
<script setup>
import { onMounted } from 'vue'

onMounted(async () => {
  const lib = await import('browser-only-library')
  lib.doSomething()
})
</script>
```

### 条件导入

```ts
if (!import.meta.env.SSR) {
  const lib = await import('browser-only-library')
  lib.doSomething()
}
```

### 在 enhanceApp 中

```ts
// .vitepress/theme/index.ts
export default {
  async enhanceApp({ app }) {
    if (!import.meta.env.SSR) {
      const plugin = await import('browser-plugin')
      app.use(plugin.default)
    }
  }
}
```

## defineClientComponent

用于处理导入时访问浏览器的组件的辅助函数：

```vue
<script setup>
import { defineClientComponent } from 'vitepress'

const BrowserComponent = defineClientComponent(() => {
  return import('browser-only-component')
})
</script>

<template>
  <BrowserComponent />
</template>
```

带 props 和插槽：

```vue
<script setup>
import { ref, h } from 'vue'
import { defineClientComponent } from 'vitepress'

const componentRef = ref(null)

const BrowserComponent = defineClientComponent(
  () => import('browser-only-component'),
  // 传递给 h() 的 props
  [
    { ref: componentRef, someProp: 'value' },
    {
      default: () => 'Default slot content',
      header: () => h('div', 'Header slot')
    }
  ],
  // 组件加载后的回调
  () => {
    console.log('Component loaded', componentRef.value)
  }
)
</script>
```

## Teleport

仅在使用 SSG 时才能 Teleport 到 body：

```vue
<ClientOnly>
  <Teleport to="body">
    <div class="modal">Modal content</div>
  </Teleport>
</ClientOnly>
```

对于其他目标，使用 `postRender` 钩子：

```ts
// .vitepress/config.ts
export default {
  async postRender(context) {
    // 将 teleport 内容注入最终 HTML
  }
}
```

## 常见 SSR 错误

### "window is not defined"

代码在模块级别访问了 `window`：

```ts
// 错误
const width = window.innerWidth

// 正确
let width: number
onMounted(() => {
  width = window.innerWidth
})
```

### "document is not defined"

同样问题，`document` 的访问：

```ts
// 错误
const el = document.querySelector('#app')

// 正确
onMounted(() => {
  const el = document.querySelector('#app')
})
```

### 水合不匹配

服务器和客户端渲染了不同的内容：

```vue
<!-- 错误 - 服务器和客户端结果不同 -->
<div>{{ typeof window !== 'undefined' ? 'client' : 'server' }}</div>

<!-- 正确 - 保持一致 -->
<ClientOnly>
  <div>Client only content</div>
</ClientOnly>
```

## 检查环境

```ts
// 在 Vue 组件中
import.meta.env.SSR  // 服务器端为 true，客户端为 false

// 在 VitePress 中
import { inBrowser } from 'vitepress'
if (inBrowser) {
  // 仅客户端代码
}
```

## 关键要点

- 仅在 `onMounted` 或 `onBeforeMount` 中访问浏览器 API
- 使用 `<ClientOnly>` 包装非 SSR 组件
- 使用 `defineClientComponent` 处理导入时访问浏览器的库
- 使用 `import.meta.env.SSR` 进行环境特定代码判断
- 仅能 Teleport 到 body，或使用 `postRender` 钩子
- 保持渲染一致性以防止水合不匹配

<!--
Source references:
- https://vitepress.dev/guide/ssr-compat
-->
