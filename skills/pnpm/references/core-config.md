---
name: pnpm-configuration
description: Configuration options via pnpm-workspace.yaml and .npmrc settings
---

# pnpm 配置

pnpm 使用两个主要配置文件：`pnpm-workspace.yaml` 用于工作区和 pnpm 特定设置，`.npmrc` 用于 npm 兼容和 pnpm 特定设置。

## pnpm-workspace.yaml

推荐的 pnpm 特定配置位置。放置在项目根目录。

```yaml
# Define workspace packages
packages:
  - 'packages/*'
  - 'apps/*'
  - '!**/test/**'  # Exclude pattern

# Catalog for shared dependency versions
catalog:
  react: ^18.2.0
  typescript: ~5.3.0

# Named catalogs for different dependency groups
catalogs:
  react17:
    react: ^17.0.2
    react-dom: ^17.0.2
  react18:
    react: ^18.2.0
    react-dom: ^18.2.0

# Override resolutions (preferred location)
overrides:
  lodash: ^4.17.21
  'foo@^1.0.0>bar': ^2.0.0

# pnpm settings (alternative to .npmrc)
settings:
  auto-install-peers: true
  strict-peer-dependencies: false
  link-workspace-packages: true
  prefer-workspace-packages: true
  shared-workspace-lockfile: true
```

## .npmrc 设置

pnpm 从 `.npmrc` 文件读取设置。在项目根目录或用户主目录创建。

### 常用 pnpm 设置

```ini
# Automatically install peer dependencies
auto-install-peers=true

# Fail on peer dependency issues
strict-peer-dependencies=false

# Hoist patterns for dependencies
public-hoist-pattern[]=*types*
public-hoist-pattern[]=*eslint*
shamefully-hoist=false

# Store location
store-dir=~/.pnpm-store

# Virtual store location
virtual-store-dir=node_modules/.pnpm

# Lockfile settings
lockfile=true
prefer-frozen-lockfile=true

# Side effects cache (speeds up rebuilds)
side-effects-cache=true

# Registry settings
registry=https://registry.npmjs.org/
@myorg:registry=https://npm.myorg.com/
```

### 工作区设置

```ini
# Link workspace packages
link-workspace-packages=true

# Prefer workspace packages over registry
prefer-workspace-packages=true

# Single lockfile for all packages
shared-workspace-lockfile=true

# Save prefix for workspace dependencies
save-workspace-protocol=rolling
```

### Node.js 设置

```ini
# Use specific Node.js version
use-node-version=20.10.0

# Node.js version file
node-version-file=.nvmrc

# Manage Node.js versions
manage-package-manager-versions=true
```

### 安全设置

```ini
# Ignore specific scripts
ignore-scripts=false

# Allow specific build scripts
onlyBuiltDependencies[]=esbuild
onlyBuiltDependencies[]=sharp

# Package extensions for missing peer deps
package-extensions[foo@1].peerDependencies.bar=*
```

## 配置层级

设置按顺序读取（后者覆盖前者）：

1. `/etc/npmrc` - 全局配置
2. `~/.npmrc` - 用户配置
3. `<project>/.npmrc` - 项目配置
4. 环境变量：`npm_config_<key>=<value>`
5. `pnpm-workspace.yaml` 设置字段

## 环境变量

```bash
# Set config via env
npm_config_registry=https://registry.npmjs.org/

# pnpm-specific env vars
PNPM_HOME=~/.local/share/pnpm
```

## Package.json 字段

pnpm 从 `package.json` 读取特定字段：

```json
{
  "pnpm": {
    "overrides": {
      "lodash": "^4.17.21"
    },
    "peerDependencyRules": {
      "ignoreMissing": ["@babel/*"],
      "allowedVersions": {
        "react": "17 || 18"
      }
    },
    "neverBuiltDependencies": ["fsevents"],
    "onlyBuiltDependencies": ["esbuild"],
    "allowedDeprecatedVersions": {
      "request": "*"
    },
    "patchedDependencies": {
      "express@4.18.2": "patches/express@4.18.2.patch"
    }
  }
}
```

## 与 npm/yarn 的关键差异

1. **默认严格**：无幽灵依赖
2. **workspace 协议**：本地包使用 `workspace:*`
3. **目录**：集中式版本管理
4. **内容寻址存储**：跨项目共享

<!--
Source references:
- https://pnpm.io/pnpm-workspace_yaml
- https://pnpm.io/npmrc
- https://pnpm.io/package_json
-->
