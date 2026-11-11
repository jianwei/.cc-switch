---
name: pnpm
description: Node.js 包管理器，支持严格依赖解析。当运行 pnpm 特定命令、配置工作区或使用 catalogs、patches、overrides 管理依赖时使用。
metadata:
  author: Anthony Fu
  version: "2026.1.28"
  source: Generated from https://github.com/pnpm/pnpm, scripts located at https://github.com/antfu/skills
---

pnpm 是一个快速、节省磁盘空间的包管理器。它使用内容寻址存储在所有项目间去重包，节省大量磁盘空间。pnpm 默认启用严格的依赖解析，防止幽灵依赖。配置优先放置在 `pnpm-workspace.yaml` 中用于 pnpm 特定设置。

**重要提示：** 使用 pnpm 项目时，代理应检查 `pnpm-workspace.yaml` 和 `.npmrc` 文件以了解工作区结构和配置。在 CI 环境中始终使用 `--frozen-lockfile`。

> 该技能基于 pnpm 10.x，生成于 2026-01-28。

## 核心功能

| 主题 | 描述 | 参考文档 |
|-------|-------------|-----------|
| CLI 命令 | 安装、添加、删除、更新、运行、执行、dlx 和工作区命令 | [core-cli](references/core-cli.md) |
| 配置 | pnpm-workspace.yaml、.npmrc 设置和 package.json 字段 | [core-config](references/core-config.md) |
| 工作区 | 支持过滤、workspace 协议和共享 lockfile 的 Monorepo | [core-workspaces](references/core-workspaces.md) |
| 存储 | 内容寻址存储、硬链接和磁盘效率 | [core-store](references/core-store.md) |

## 功能特性

| 主题 | 描述 | 参考文档 |
|-------|-------------|-----------|
| 目录 | 工作区集中式依赖版本管理 | [features-catalogs](references/features-catalogs.md) |
| 覆盖 | 强制指定依赖版本，包括传递依赖 | [features-overrides](references/features-overrides.md) |
| 补丁 | 使用自定义修复修改第三方包 | [features-patches](references/features-patches.md) |
| 别名 | 使用 npm: 协议以自定义名称安装包 | [features-aliases](references/features-aliases.md) |
| 钩子 | 使用 .pnpmfile.cjs 钩子自定义解析 | [features-hooks](references/features-hooks.md) |
| 同伴依赖 | 自动安装、严格模式和依赖规则 | [features-peer-deps](references/features-peer-deps.md) |

## 最佳实践

| 主题 | 描述 | 参考文档 |
|-------|-------------|-----------|
| CI/CD 配置 | GitHub Actions、GitLab CI、Docker 和缓存策略 | [best-practices-ci](references/best-practices-ci.md) |
| 迁移 | 从 npm/Yarn 迁移，处理幽灵依赖，monorepo 迁移 | [best-practices-migration](references/best-practices-migration.md) |
| 性能 | 安装优化、存储缓存、工作区并行化 | [best-practices-performance](references/best-practices-performance.md) |
