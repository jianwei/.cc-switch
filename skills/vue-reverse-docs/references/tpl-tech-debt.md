# 技术债务报告模板（tpl-tech-debt — Vue 版）

> 👤 负责角色：**tech-debt-agent**（技术审计员）
> 📋 职责：在完成所有其他文档后，对比代码与文档，识别不一致、潜在风险、Vue 2 特有问题和重构建议

```markdown
# 技术债务报告

> 扫描时间：2026-03-05 09:16:18 | 框架：Vue 2 + Webpack

## 总体评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 代码质量 | x/10 | |
| 可维护性 | x/10 | |
| 性能风险 | x/10 | |
| 升级紧迫度（Vue 3 迁移） | 高/中/低 | Vue 2 于 2023-12 停止维护 |
| 重构紧迫度 | 高/中/低 | |

## 🔴 高优先级问题

> **问题：** [描述]
> **位置：** [文件/函数/组件]
> **影响：** [危害说明]
> **建议：** [解决方案]

## 🟡 中优先级问题

（同上格式）

## 🟢 低优先级 / 优化建议

（同上格式）

---

## Vue 2 特有检查清单

### 组件写法问题
- [ ] 存在大量 Mixins（代码来源不透明，建议迁移为 Composable）
- [ ] 组件使用 `this.$parent` 或 `this.$children`（强耦合，难维护）
- [ ] 存在 `this.$refs` 滥用（大量跨组件调用，应改为 props/emit）
- [ ] 全局 Event Bus（`Vue.prototype.$bus`）导致事件追踪困难
- [ ] 使用 `Vue.set` / `this.$set` 处理响应式（说明存在响应式边界问题）
- [ ] 组件 `data` 不是函数（多实例共享数据的严重错误）

### 生命周期问题
- [ ] `mounted` 中直接操作 DOM（应改用 `nextTick` 或 `ref`）
- [ ] `created`/`mounted` 中未清理的定时器（`setInterval` 未在 `beforeDestroy` 清除）
- [ ] `watch` 缺少 `immediate: false` 导致重复请求
- [ ] `watch` 使用 `deep: true` 监听大对象（性能问题）

### 模板语法问题
- [ ] `v-for` 使用 index 作为 key（列表更新性能问题）
- [ ] `v-if` 和 `v-for` 同时作用于同一元素（Vue 2 中 v-for 优先级更高，逻辑混乱）
- [ ] 模板内有复杂表达式（应提取为 computed）
- [ ] 使用已废弃的 `.sync` 修饰符或 `$listeners`（Vue 3 已移除）
- [ ] 过滤器（`filters`）使用（Vue 3 已移除，建议改为 computed 或方法）

### Vuex 问题
- [ ] 直接修改 `state`（未通过 `commit` mutation）
- [ ] 在 `mutation` 中执行异步操作（应在 action 中）
- [ ] Vuex 模块未开启命名空间（`namespaced: true`），存在命名冲突风险
- [ ] Store 中存储了非序列化数据（如 DOM 节点、函数）

### 性能问题
- [ ] 未使用路由懒加载（`() => import('./views/xxx.vue')`）
- [ ] 组件未合理使用 `keep-alive`（频繁创建销毁的重型页面）
- [ ] 长列表未使用虚拟滚动（超过 200 条数据直接渲染）
- [ ] 图片未懒加载（首屏大量图片请求）
- [ ] 未拆分 vendor chunk，导致首包过大

### 安全问题
- [ ] `v-html` 直接渲染用户输入（XSS 风险）
- [ ] 路由未配置权限守卫
- [ ] token 存储在 localStorage（建议 httpOnly Cookie）
- [ ] API 请求未校验响应数据结构（直接访问可能为 undefined 的字段）

### Vue 2 停止维护风险
- [ ] Vue 2 已于 2023-12-31 停止官方维护（EOL）
- [ ] 依赖的 Element UI 2.x 不兼容 Vue 3
- [ ] 项目使用 `@vue/composition-api` 插件（说明在 Vue 2 上使用 Composition API，迁移 Vue 3 后可移除）

---

## 通用检查清单

- [ ] 硬编码魔法字符串 / 数字（应提取为常量）
- [ ] 接口 baseURL 硬编码（未使用环境变量）
- [ ] 过时的 npm 依赖（有已知安全漏洞）
- [ ] 缺少 eslint / prettier 配置
- [ ] 存在大量 `console.log` 未清理
- [ ] 组件文件超过 500 行（应拆分）

---

## 重构优先级路线图

```
第一阶段（本月）：高优先级 - 修复影响功能/安全的问题
  - 任务1：清理所有 v-html 中的用户输入风险
  - 任务2：补全路由权限守卫

第二阶段（本季度）：中优先级 - 提升代码质量
  - 任务1：将 Mixins 逐步迁移为 Composable（可与 Vue 3 迁移一起做）
  - 任务2：为 Vuex 所有模块开启命名空间

第三阶段（下半年）：Vue 3 迁移准备
  - 评估 Element UI → Element Plus 迁移成本
  - 梳理所有 Vue 2 废弃 API 使用情况
  - 制定分模块渐进式迁移方案
```
```