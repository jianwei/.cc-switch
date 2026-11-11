---
name: pnpm-workspaces
description: Monorepo support with workspaces for managing multiple packages
---

# pnpm 工作区

pnpm 通过工作区内置支持 monorepo（多包仓库）。

## 设置工作区

在仓库根目录创建 `pnpm-workspace.yaml`：

```yaml
packages:
  # Include all packages in packages/ directory
  - 'packages/*'
  # Include all apps
  - 'apps/*'
  # Include nested packages
  - 'tools/*/packages/*'
  # Exclude test directories
  - '!**/test/**'
```

## Workspace 协议

使用 `workspace:` 协议引用本地包：

```json
{
  "dependencies": {
    "@myorg/utils": "workspace:*",
    "@myorg/core": "workspace:^",
    "@myorg/types": "workspace:~"
  }
}
```

### 协议变体

| 协议 | 行为 | 发布为 |
|----------|----------|--------------|
| `workspace:*` | 任意版本 | 实际版本（如 `1.2.3`） |
| `workspace:^` | 兼容版本 | `^1.2.3` |
| `workspace:~` | 补丁版本 | `~1.2.3` |
| `workspace:^1.0.0` | Semver 范围 | `^1.0.0` |

## 过滤包

使用 `--filter` 对特定包运行命令：

```bash
# By package name
pnpm --filter @myorg/app build
pnpm -F @myorg/app build

# By directory path
pnpm --filter "./packages/core" test

# Glob patterns
pnpm --filter "@myorg/*" lint
pnpm --filter "!@myorg/internal-*" publish

# All packages
pnpm -r build
pnpm --recursive build
```

### 基于依赖的过滤

```bash
# Package and all its dependencies
pnpm --filter "...@myorg/app" build

# Package and all its dependents
pnpm --filter "@myorg/core..." test

# Both directions
pnpm --filter "...@myorg/shared..." build

# Changed since git ref
pnpm --filter "...[origin/main]" test
pnpm --filter "[HEAD~5]" lint
```

## 工作区命令

### 安装依赖
```bash
# Install all workspace packages
pnpm install

# Add dependency to specific package
pnpm --filter @myorg/app add lodash

# Add workspace dependency
pnpm --filter @myorg/app add @myorg/utils
```

### 运行脚本
```bash
# Run in all packages with that script
pnpm -r run build

# Run in topological order (dependencies first)
pnpm -r --workspace-concurrency=1 run build

# Run in parallel
pnpm -r --parallel run test

# Stream output
pnpm -r --stream run dev
```

### 执行命令
```bash
# Run command in all packages
pnpm -r exec pwd

# Run in specific packages
pnpm --filter "./packages/**" exec rm -rf dist
```

## 工作区设置

在 `.npmrc` 或 `pnpm-workspace.yaml` 中配置：

```ini
# Link workspace packages automatically
link-workspace-packages=true

# Prefer workspace packages over registry
prefer-workspace-packages=true

# Single lockfile (recommended)
shared-workspace-lockfile=true

# Workspace protocol handling
save-workspace-protocol=rolling

# Concurrent workspace scripts
workspace-concurrency=4
```

## 发布工作区

发布时，`workspace:` 协议会被转换：

```json
// Before publish
{
  "dependencies": {
    "@myorg/utils": "workspace:^"
  }
}

// After publish
{
  "dependencies": {
    "@myorg/utils": "^1.2.3"
  }
}
```

使用 `--no-git-checks` 从 CI 发布：
```bash
pnpm publish -r --no-git-checks
```

## 最佳实践

1. **对内部依赖使用 workspace 协议**
2. **启用 `link-workspace-packages`** 以自动链接
3. **使用共享 lockfile** 以保持一致性
4. **构建时按依赖过滤** 以确保正确顺序
5. **使用目录** 管理共享外部依赖版本

## 示例项目结构

```
my-monorepo/
├── pnpm-workspace.yaml
├── package.json
├── pnpm-lock.yaml
├── packages/
│   ├── core/
│   │   └── package.json
│   ├── utils/
│   │   └── package.json
│   └── types/
│       └── package.json
└── apps/
    ├── web/
    │   └── package.json
    └── api/
        └── package.json
```

<!--
Source references:
- https://pnpm.io/workspaces
- https://pnpm.io/filtering
- https://pnpm.io/npmrc#workspace-settings
-->
