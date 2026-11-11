<!-- @author Codex (K2.6) -->
# Vue Migration Input Contract

## Required Inputs

| 输入项 | 是否必填 | 说明 |
|--------|----------|------|
| `modulePath` | 必填 | 需要迁移的模块目录路径 |
| `mode` | 必填 | `page`、`module`、`deploy`、`logic-only` |
| `newUiPath` | `logic-only` 必填 | 新 HTML/UI 代码路径，支持 `.vue` 文件或目录 |
| `originalUrl` | 完整迁移必填，`logic-only` 建议 | 原始页面 URL，用于基线和接口参考 |
| `targetUrl` | 必填 | 迁移后验证 URL |
| `testDataSetup` | 建议 | 准备相同数据环境的说明 |

## Mode Rules

完整迁移模式：

- `originalUrl` 必须可访问
- 必须捕获视觉、DOM、接口、交互和控制台基线
- 验证失败或缺失时，不能标记为成功

`logic-only` 模式：

- `newUiPath` 必须存在
- 不修改新 UI 的 `<template>`
- 不修改新 UI 的 `<style>`
- 仅操作 `<script>` 或 `<script setup>`
- 不做视觉、DOM、交互位置一致性验证

## Scope Rules

- `page` 和 `module` 只处理用户指定的 `modulePath` 及其直接依赖
- `page` 模式必须先调研页面包含的所有候选业务模块，输出候选模块清单，让用户选择后再进入迁移
- 页面候选模块选择项必须包含“全部”，但“全部”默认只包含页面私有模块，不自动包含全局基础设施
- 外部组件只更新必要引用语法，不重组、不重写
- `deploy` 按项目模块拓扑顺序逐个处理
- 任何新增处理范围都必须先获得用户确认

## Page Mode Module Selection

当 `mode=page` 或用户表达“转换整个页面”时，先完成调研，不直接转换：

1. 以页面入口组件为根节点扫描依赖图
2. 按业务语义和目录归属聚合候选模块
3. 标记每个候选模块的文件清单、模块类型、是否页面私有、是否共享依赖、转换建议和风险
4. 输出《页面候选模块清单》
5. 等待用户选择要转换的模块；选项必须包含“全部”
6. 仅将用户选择的模块纳入后续迁移流程

候选模块分类：

| 类型 | 默认建议 | 处理方式 |
|------|----------|----------|
| 页面入口 | 转换 | 用户指定页面根节点 |
| 页面私有组件 | 可选转换 | 让用户选择 |
| 页面私有 composable | 可选转换 | 让用户选择 |
| 页面私有 API | 可选转换 | 让用户选择 |
| 页面私有 utils | 可选转换 | 让用户选择 |
| 页面私有 store/module | 可选转换 | 让用户选择 |
| 全局基础设施 | 不转换 | 只保持引用或做页面侧适配 |
| 共享组件/工具 | 不转换 | 除非用户显式选择纳入范围 |

页面候选模块清单必须提供类似选项：

```text
0. 全部（转换页面私有候选模块，不转换全局基础设施）
1. 仅转换页面入口与容器逻辑
2. 转换页面入口 + 模块 A
3. 转换页面入口 + 模块 B
4. 自定义编号组合
```

## Global Infrastructure Handling

页面使用的全局基础设施默认不纳入页面迁移范围：

| 类型 | 默认处理 |
|------|----------|
| 请求封装 | 保持引用，必要时只改页面侧调用 |
| 路由实例 | 保持配置，页面内改为 `useRouter` / `useRoute` |
| 全局 Store | 保持实现，页面内按现有 store API 适配 |
| 全局插件 | 不修改，记录兼容风险 |
| 共享组件 | 不重构，只调整页面侧 props/emits 用法 |

处理原则：

- 默认保持原 import 路径和基础设施实现
- 只在页面模块内做调用方式适配
- 如需桥接 Vue 2 风格 API，可在页面模块内新增局部 adapter/composable
- 若必须修改全局基础设施，必须暂停并请求用户确认扩大迁移范围
- 用户确认扩大范围后，需要重新输出受影响文件、风险和验证范围
- 用户未确认时，将该问题写入 `migration-unresolved.md`

## Workspace Protection

执行前运行：

```bash
git status --short
```

报告中必须记录迁移前已有变更。执行中不得：

- 覆盖已有用户改动
- 回退用户改动
- 格式化无关文件
- 删除迁移前已经存在的未追踪文件
- 自动执行 `git reset --hard`
- 自动执行 `git checkout --`

## `originalUrl` Failure Policy

若完整迁移模式下 `originalUrl` 不可访问：

1. 停止完整迁移
2. 告知用户无法验证 UI、DOM、视觉和交互一致性
3. 让用户选择修复原始环境、切换为 `logic-only`，或仅生成静态迁移草案
4. 静态迁移草案必须标记为 `未验证`

## Author Comment Rules

新建文件和新建函数必须遵循项目作者注释规范。模型名读取顺序：

```bash
printf '%s\n' "${CLAUDE_MODEL:-${ANTHROPIC_MODEL:-Codex-unknown}}"
```
