---
name: vue
description: Vue 3 Composition API、script setup 宏、响应式系统和内置组件。用于编写 Vue SFC、defineProps/defineEmits/defineModel、watcher，或使用 Transition/Teleport/Suspense/KeepAlive。
metadata:
  author: Anthony Fu
  version: "2026.1.31"
  source: Generated from https://github.com/vuejs/docs, scripts at https://github.com/antfu/skills
---

# Vue

> 基于 Vue 3.5。始终使用 Composition API 和 `<script setup lang="ts">`。

## 偏好设置

- 优先使用 TypeScript 而非 JavaScript
- 优先使用 `<script setup lang="ts">` 而非 `<script>`
- 对于性能，如果不需要深层响应式，优先使用 `shallowRef`
- 始终使用 Composition API 而非 Options API
- 不推荐使用响应式 Props 解构

## 核心内容

| 主题 | 描述 | 参考 |
|-------|-------------|-----------|
| Script Setup 与宏 | `<script setup>`、defineProps、defineEmits、defineModel、defineExpose、defineOptions、defineSlots、泛型 | [script-setup-macros](references/script-setup-macros.md) |
| 响应式与生命周期 | ref、shallowRef、computed、watch、watchEffect、effectScope、生命周期钩子、composables | [core-new-apis](references/core-new-apis.md) |

## 功能特性

| 主题 | 描述 | 参考 |
|-------|-------------|-----------|
| 内置组件与指令 | Transition、Teleport、Suspense、KeepAlive、v-memo、自定义指令 | [advanced-patterns](references/advanced-patterns.md) |

## 快速参考

### 组件模板

```vue
<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'

const props = defineProps<{
  title: string
  count?: number
}>()

const emit = defineEmits<{
  update: [value: string]
}>()

const model = defineModel<string>()

const doubled = computed(() => (props.count ?? 0) * 2)

watch(() => props.title, (newVal) => {
  console.log('Title changed:', newVal)
})

onMounted(() => {
  console.log('Component mounted')
})
</script>

<template>
  <div>{{ title }} - {{ doubled }}</div>
</template>
```

### 关键导入

```ts
// 响应式
import { ref, shallowRef, computed, reactive, readonly, toRef, toRefs, toValue } from 'vue'

// 监听器
import { watch, watchEffect, watchPostEffect, onWatcherCleanup } from 'vue'

// 生命周期
import { onMounted, onUpdated, onUnmounted, onBeforeMount, onBeforeUpdate, onBeforeUnmount } from 'vue'

// 工具函数
import { nextTick, defineComponent, defineAsyncComponent } from 'vue'
```
