---
name: jquery-reverse-docs
description: 从现有 jQuery 项目代码逆向生成完整文档体系。适用于传统 jQuery/Bootstrap 项目的系统梳理、重构前准备、技术评审。当用户有大量 jQuery 代码需要生成文档、梳理系统架构、准备重构、分析遗留系统时务必使用此 Skill。触发关键词：逆向生成文档、从代码生成文档、分析jQuery代码、梳理系统、重构前准备、代码转文档、生成PRD/接口文档/模块文档。
---

# jQuery 逆向生成文档 Skill

## 工作方式

扫描 jQuery 项目源码，直接在 `docs/PRD/` 目录下生成各类文档。每次 Session 专注完成一个文档文件，生成后继续下一个，直到全部完成。

---

## 输出目录结构

```
docs/PRD/
├── architecture.md           ← 架构文档
├── tech-debt.md              ← 技术债务报告
├── api/                      ← AJAX 接口文档（每个 JS 文件一个）
├── pages/                    ← 页面功能文档（每个 HTML 页面一个）
├── modules/                  ← JS 模块/工具库文档
└── events/                   ← 事件系统文档
```

---

## 文档生成顺序

| 优先级 | 类别 | 说明 |
|--------|------|------|
| 1 | architecture | 整体架构，最先生成 |
| 2 | module | 公共 JS 模块/工具库 |
| 3 | api | AJAX 接口，按 JS 文件拆分 |
| 4 | page | 页面功能，按 HTML 文件拆分 |
| 5 | events | 全局事件系统 |
| 6 | tech-debt | 技术债务报告，最后生成 |

---

## 文档模板索引

| 文档类型 | 模板文件 |
|---------|---------|
| 扫描与生成流程 | `references/workflow.md` |
| 架构文档 | `references/tpl-architecture.md` |
| AJAX 接口文档 | `references/tpl-api.md` |
| 页面功能文档 | `references/tpl-page.md` |
| JS 模块文档 | `references/tpl-module.md` |
| 事件系统文档 | `references/tpl-events.md` |
| 技术债务报告 | `references/tpl-tech-debt.md` |
