<!-- @author Codex (K2.6) -->
# Logic-Only Vue Migration Workflow

当新 UI 已经存在，只需要把旧业务逻辑、数据处理和接口调用迁入新 UI 时使用此流程。

## Hard Rules

- Do not modify `<template>`
- Do not modify `<style>`
- Preserve existing Props, Emits, Slots, and Expose definitions
- Only edit `<script>` or `<script setup>`
- Do not verify visual or DOM equality against the old UI

## Step 4.0: Logic Mapping Analysis

从旧代码提取：

- data state
- computed values
- methods
- watchers
- lifecycle hooks
- API calls
- route usage
- store usage
- side effects

从新 UI 提取：

- props
- emits
- slots
- exposed methods
- template refs
- existing local state
- event handlers used by the template

生成 `logic-mapping.md`，必须包含：

- state mapping
- method mapping
- API call mapping
- lifecycle mapping
- watcher mapping
- unresolved features

等待用户确认后才能改代码。

## Step 4.1: Extract Old Logic

提取旧逻辑时保持旧行为：

- API URL、Method、Headers、Payload、调用顺序不变
- loading 行为不变
- error handling 行为不变
- pagination 和 filter 转换不变
- route parameter 使用不变
- store mutation/action 语义不变

## Step 4.2: Inject Into New UI

只编辑 script 内容。Vue 3 目标代码优先使用：

```vue
<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'

interface ListResponse<T> {
  list: T[]
  total: number
}

const loading = ref(false)
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
})

async function fetchData() {
  loading.value = true
  try {
    // 这里保留旧代码的接口调用形状。
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})

defineExpose({
  reload: fetchData,
})
</script>
```

如果旧逻辑必须改模板才能映射，记录到 `migration-unresolved.md`，不要改模板。

## Step 4.3: TypeScript Completion

补齐类型：

- state
- computed values
- method parameters
- API responses
- emitted events
- refs
- route params
- store values

## Step 4.4: Interface Verification

对比新旧接口调用：

- URL path and query
- Method
- Content-Type
- Authorization or custom headers
- Payload shape
- call count
- call order

## Validation

必需项：

- unit tests under `__test__/[source-relative-path]/unit/`
- e2e tests under `__test__/[source-relative-path]/e2e/`
- API baseline records under `.omc/vue-migration/[module-name]/records/api-baseline/`
- console records under `.omc/vue-migration/[module-name]/records/console-baseline/`
- TypeScript check

禁止项：

- screenshot comparison
- DOM structure comparison
- old UI visual comparison
- interaction position comparison
