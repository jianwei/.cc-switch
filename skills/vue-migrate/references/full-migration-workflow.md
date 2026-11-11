<!-- @author Codex (K2.6) -->
# Full Vue Migration Workflow

## Phase 0: Input Validation

运行这些检查后才能改代码：

```bash
test -d "$modulePath"
find "$modulePath" -name "*.vue" -print -quit
git status --short
```

使用 Playwright 或当前环境可用的浏览器自动化工具验证 `originalUrl` 和 `targetUrl`。

遇到以下情况必须停止：

- `modulePath` 不存在
- `modulePath` 下没有 `.vue` 文件
- `originalUrl` 不可访问
- `targetUrl` 不可访问且没有本地 dev server 方案

若 `targetUrl` 不可访问：

- 项目可启动本地 dev server 时，先按项目已有脚本启动并重试
- 端口冲突时换用可用端口，并记录更新后的 `targetUrl`
- 无法启动或无法访问时，可以继续生成代码，但运行时、视觉、DOM、接口和交互验证必须标记为 `未验证`
- `targetUrl` 未验证时，最终状态不得为 `通过`

## Phase 1: Diagnosis

只扫描已确认模块边界：

- `.vue`、`.js`、`.ts`
- `package.json`
- Vue 版本
- Options API 使用情况
- TypeScript 使用情况
- 生命周期钩子
- filters
- directives
- Vue 全局 API
- `.sync`
- Vuex 或 Pinia
- router 版本
- UI 框架
- 接口调用方式
- 样式系统

输出迁移诊断报告，然后等待用户确认。

`page` 模式额外硬门槛：

- 先输出《页面候选模块清单》
- 清单必须列出页面入口、页面私有组件、页面私有 composables、页面私有 API、页面私有 utils、页面私有 store/module、共享依赖和全局基础设施
- 选择项必须包含“全部”
- “全部”默认只包含页面私有候选模块，不包含全局基础设施
- 用户选择前不得进入 Phase 2
- 若用户要求纳入全局基础设施，必须重新确认扩大范围、风险和验证边界

## Phase 2: Baseline Capture

捕获以下基线：

- 视觉截图：`screenshot/[source-relative-path]/visual-baseline/`
- DOM 快照：`.omc/vue-migration/[module-name]/records/snapshot-baseline/`
- API 调用：`.omc/vue-migration/[module-name]/records/api-baseline/`
- 交互脚本：`.omc/vue-migration/[module-name]/records/interaction-baseline/`
- 控制台日志：`.omc/vue-migration/[module-name]/records/console-baseline/`

截图视口固定：

```text
width: 1440
height: 900
```

截图状态：

- default
- loading
- data loaded
- empty
- hover
- focus
- modal or drawer
- validation error
- system error
- key action result

## Phase 3: Test Baseline

测试文件统一放在：

```text
__test__/[source-relative-path]/
```

测试覆盖：

- Props 渲染
- Emits 行为
- v-model 行为
- 异步 loading 到 data 状态
- computed 输出
- method 副作用
- 表单验证
- API payload

优先运行项目已有测试命令，不发明新测试命令。

## Phase 4: Code Migration

Step 4.0 模块重组：

- 识别超过 300 行的大组件
- 识别可提取为 composable 的 data 分组
- 识别纯工具函数
- 识别重复逻辑
- 输出模块重组方案
- 等待用户确认

Step 4.1 Vue 2 到 Vue 3 运行时：

- `beforeDestroy` 转 `beforeUnmount`
- `destroyed` 转 `unmounted`
- `Vue.set` 转赋值
- `Vue.delete` 转 `delete`
- `Vue.extend` 转 `defineComponent`
- `.sync` 转 `v-model:prop`
- 移除 `.native`
- 旧指令钩子转 Vue 3 钩子
- `>>>`、`/deep/`、`::v-deep` 转 `:deep()`

Step 4.2 Options API 到 Composition API：

- 使用 `<script setup lang="ts">`
- props 转 `defineProps`
- emits 转 `defineEmits`
- data 转 `ref` 或 `reactive`
- computed 转 `computed`
- watch 转 `watch`
- lifecycle 转导入的生命周期 hooks
- `$refs` 转 template refs
- `$nextTick` 转 `nextTick`

Step 4.3 JavaScript 到 TypeScript：

- 添加 `lang="ts"`
- 为 props、emits、refs、reactive 对象、API 响应和函数签名补类型
- 类型只在复用时抽到共享文件

Step 4.4 样式适配：

- 用户指定样式系统时按用户指定
- 项目已有 Tailwind 时才优先使用 Tailwind
- 否则遵循项目已有样式约定
- Tailwind 无法精确保留视觉时保留自定义样式

## Phase 5: Validation

运行：

- 单元测试
- Playwright 功能测试
- DOM 快照对比
- 视觉回归
- API 调用对比
- 交互回放
- 控制台 warning/error 收集
- TypeScript 检查

必需验证未通过时不得宣称完成。

Phase 4 单文件转换失败时：

- 只允许继续收集其他失败
- 失败文件必须记录到 `migration-unresolved.md`
- 最终状态不得为 `通过`
- 核心功能受影响时最终状态必须为 `未通过`
- 只有用户明确接受非阻断失败时，最多标记为 `有条件通过`

## Phase 6: Closure

写入：

- `.omc/vue-migration/[module-name]/migration-report.md`
- `.omc/vue-migration/[module-name]/migration-unresolved.md`
- `.omc/vue-migration/[module-name]/suggested-commits.md`

最终状态只能是 `通过`、`有条件通过`、`未通过` 或 `未验证`。
