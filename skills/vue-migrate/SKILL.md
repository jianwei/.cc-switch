<!-- @author Codex (K2.6) -->
---
name: vue-migrate
description: 迁移 Vue 模块到 Vue 3、Composition API 和 TypeScript。支持完整迁移和 logic-only 逻辑迁移。触发关键词：vue-migrate、迁移 Vue 模块、Vue2 升 Vue3、Options API 转 Composition API、JS 转 TS、logic-only 迁移。
---

# Vue Migration Skill

用于将用户明确指定的 Vue 模块进行现代化迁移，目标是 Vue 3 + `<script setup lang="ts">` + TypeScript，同时保持 UI、功能、接口调用和控制台行为符合迁移模式要求。

## 必读顺序

1. 先读 `references/input-contract.md`
2. 完整迁移读 `references/full-migration-workflow.md`
3. `logic-only` 迁移读 `references/logic-only-workflow.md`
4. 验证和产物规则读 `references/validation-and-output.md`
5. 报告格式读 `references/report-templates.md`

## 支持模式

| 模式 | 说明 |
|------|------|
| `page` | 单页面完整迁移 |
| `module` | 功能模块完整迁移 |
| `deploy` | 全项目按模块拓扑顺序迁移 |
| `logic-only` | 新 UI 已存在，仅迁移旧业务逻辑、数据处理和接口调用 |

## 硬门槛

- `modulePath` 必须明确指定，且必须存在 Vue 文件
- 完整迁移必须提供可访问的 `originalUrl`
- `logic-only` 必须提供 `newUiPath`
- 诊断报告必须经用户确认后才进入基线捕获
- `page` 模式必须先列出页面候选模块清单，让用户选择转换范围；选项必须包含“全部”
- 模块重组方案或逻辑映射方案必须经用户确认后才进入代码迁移
- 不得越界修改用户未指定的模块
- 不得覆盖、回退或格式化与本次迁移无关的用户改动
- 不得自动提交或自动执行破坏性回滚命令
- 验证失败或未验证时，不得宣称迁移成功

## 执行摘要

完整迁移：

1. Phase 0 输入校验
2. Phase 1 诊断分析和模块边界识别
3. Phase 2 视觉、DOM、接口、交互、控制台基线捕获
4. Phase 3 测试基线补齐
5. Phase 4 代码迁移
6. Phase 5 全量验证
7. Phase 6 收尾报告

逻辑迁移：

1. 校验 `modulePath`、`newUiPath`、`targetUrl`
2. 分析旧逻辑和新 UI 接口
3. 输出逻辑映射方案并等待用户确认
4. 仅修改 `<script setup>`，不修改新 UI 的 `<template>` 和 `<style>`
5. 验证逻辑等价性、接口调用、功能完整性、控制台和 TypeScript

## 输出约定

- 源码默认原地迁移
- 测试代码统一放到项目根目录 `__test__/`，并按源码相对路径镜像组织
- 截图统一放到项目根目录 `screenshot/`，并按页面或模块相对路径镜像组织
- 迁移报告和中间记录放到 `.omc/vue-migration/[module-name]/`
