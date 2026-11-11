# 组件文档模板（tpl-component — Vue SFC 版）

> 👤 负责角色：**component-agent**（组件分析师）
> 📋 职责：分析复用组件的 Props、Emits、Slots、内部状态、生命周期和使用示例

```markdown
# [ComponentName] 组件文档

> 源文件：src/components/xxx.vue | 生成时间：2026-03-05 09:16:18

## 功能描述
一句话说明组件作用。

## Props

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| value | String | 是 | — | 绑定值 |
| disabled | Boolean | 否 | false | 是否禁用 |

## Emits（对外事件）

| 事件名 | 参数 | 触发时机 | 说明 |
|--------|------|---------|------|
| change | (value: any) | 值变化时 | 用于实现 v-model |
| close | — | 点击关闭按钮 | — |

## v-model 支持

| model.prop | model.event | 说明 |
|-----------|-------------|------|
| value | input | 实现 v-model 双向绑定 |

> Vue 2 中需在组件内声明 `model: { prop: 'value', event: 'input' }`

## Slots（插槽）

| 插槽名 | 说明 | 作用域变量 |
|--------|------|-----------|
| default | 默认内容 | — |
| header | 自定义头部 | { title } |
| footer | 自定义底部 | — |

## Data（内部状态）

| 字段名 | 类型 | 初始值 | 说明 |
|--------|------|--------|------|
| visible | Boolean | false | 控制弹窗显示 |
| loading | Boolean | false | 加载状态 |

## Computed（计算属性）

| 属性名 | 依赖 | 说明 |
|--------|------|------|
| filteredList | list, keyword | 过滤后的列表 |

## Watch（监听）

| 监听目标 | immediate | deep | 作用 |
|---------|-----------|------|------|
| value | true | false | props 变化时同步内部状态 |
| formData | false | true | 表单变化时触发校验 |

## 生命周期

| 钩子 | 作用 |
|------|------|
| created | 初始化默认值 |
| mounted | 绑定 DOM 事件 / 请求初始数据 |
| beforeDestroy | 清除定时器 / 解绑事件 |

## Methods（对外可调用方法）

> 通过 `ref` 调用：`this.$refs.myComp.reset()`

| 方法名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| reset() | — | void | 重置表单 |
| validate() | — | Promise\<boolean\> | 触发校验 |

## 使用示例

```vue
<!-- 基础用法 -->
<MyComponent :value="formValue" @change="handleChange" />

<!-- v-model 写法 -->
<MyComponent v-model="formValue" :disabled="isDisabled" />

<!-- 使用插槽 -->
<MyComponent v-model="formValue">
  <template #header>自定义头部</template>
</MyComponent>

<!-- 通过 ref 调用方法 -->
<MyComponent ref="myComp" />
<!-- 在父组件中：this.$refs.myComp.reset() -->
```

## 注意事项
- Vue 2 中若需支持 v-model，必须声明 `model` 选项
- 组件内部修改 props 会产生警告，应通过 `$emit` 通知父组件更新
- 若组件内有定时器或事件监听，务必在 `beforeDestroy` 中清理
```