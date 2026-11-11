---
name: pnpm-catalogs
description: Centralized dependency version management for workspaces
---

# pnpm 目录

目录提供了一种在个工作区中集中管理依赖版本的方 式。定义一次版本，在所有地方使用。

## 基本用法

在 `pnpm-workspace.yaml` 中定义目录：

```yaml
packages:
  - 'packages/*'

catalog:
  react: ^18.2.0
  react-dom: ^18.2.0
  typescript: ~5.3.0
  vite: ^5.0.0
```

使用 `catalog:` 在 `package.json` 中引用：

```json
{
  "dependencies": {
    "react": "catalog:",
    "react-dom": "catalog:"
  },
  "devDependencies": {
    "typescript": "catalog:",
    "vite": "catalog:"
  }
}
```

## 命名目录

为不同场景创建多个目录：

```yaml
packages:
  - 'packages/*'

# Default catalog
catalog:
  lodash: ^4.17.21

# Named catalogs
catalogs:
  react17:
    react: ^17.0.2
    react-dom: ^17.0.2

  react18:
    react: ^18.2.0
    react-dom: ^18.2.0

  testing:
    vitest: ^1.0.0
    "@testing-library/react": ^14.0.0
```

引用命名目录：

```json
{
  "dependencies": {
    "react": "catalog:react18",
    "react-dom": "catalog:react18"
  },
  "devDependencies": {
    "vitest": "catalog:testing"
  }
}
```

## 优势

1. **单一真相来源**：在一处更新版本
2. **一致性**：所有包使用相同版本
3. **轻松升级**：更改一次，影响整个工作区
4. **类型安全**：pnpm-workspace.yaml 中的 TypeScript 支持

## 目录与覆盖

| 功能 | 目录 | 覆盖 |
|---------|----------|-----------|
| 用途 | 为直接依赖定义版本 | 强制任何依赖的版本 |
| 范围 | 仅直接依赖 | 所有依赖（包括传递） |
| 用法 | `"pkg": "catalog:"` | 自动应用 |
| 主动选择 | 每个 package.json 显式 | 全局到工作区 |

## 使用目录发布

发布时，`catalog:` 引用被替换为实际版本：

```json
// Before publish (source)
{
  "dependencies": {
    "react": "catalog:"
  }
}

// After publish (published package)
{
  "dependencies": {
    "react": "^18.2.0"
  }
}
```

## 从覆盖迁移

如果使用覆盖来保持版本一致性：

```yaml
# Before (using overrides)
overrides:
  react: ^18.2.0
  react-dom: ^18.2.0
```

迁移到目录以获得更清晰的依赖管理：

```yaml
# After (using catalogs)
catalog:
  react: ^18.2.0
  react-dom: ^18.2.0
```

然后更新 package.json 文件使用 `catalog:`。

## 最佳实践

1. **使用默认目录** 用于常见共享依赖
2. **使用命名目录** 用于版本变体（例如不同的 React 版本）
3. **保持目录最小化** - 只包含共享依赖
4. **与 workspace 协议结合** 用于内部包

```yaml
catalog:
  # External shared dependencies
  lodash: ^4.17.21
  zod: ^3.22.0

# Internal packages use workspace: protocol instead
# "dependencies": { "@myorg/utils": "workspace:^" }
```

<!--
Source references:
- https://pnpm.io/catalogs
-->
