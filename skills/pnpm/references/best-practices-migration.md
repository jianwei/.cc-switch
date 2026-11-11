---
name: migration-to-pnpm
description: Migrating from npm or Yarn to pnpm with minimal friction
---

# 迁移到 pnpm

将现有项目从 npm 或 Yarn 迁移到 pnpm 的指南。

## 快速迁移

### 从 npm 迁移

```bash
# Remove npm lockfile and node_modules
rm -rf node_modules package-lock.json

# Install with pnpm
pnpm install
```

### 从 Yarn 迁移

```bash
# Remove yarn lockfile and node_modules
rm -rf node_modules yarn.lock

# Install with pnpm
pnpm install
```

### 导入现有 Lockfile

pnpm 可以导入现有的 lockfile：

```bash
# Import from npm or yarn lockfile
pnpm import

# This creates pnpm-lock.yaml from:
# - package-lock.json (npm)
# - yarn.lock (yarn)
# - npm-shrinkwrap.json (npm)
```

## 处理常见问题

### 幽灵依赖

pnpm 对依赖管理非常严格。如果代码导入了 `package.json` 中不存在的包，将会失败。

**问题：**
```js
// Works with npm (hoisted), fails with pnpm
import lodash from 'lodash' // Not in dependencies, installed by another package
```

**解决方案：** 显式添加缺失的依赖：
```bash
pnpm add lodash
```

### 缺失的同伴依赖

pnpm 默认会报告同伴依赖问题。

**选项 1：** 让 pnpm 自动安装：
```ini
# .npmrc (default in pnpm v8+)
auto-install-peers=true
```

**选项 2：** 手动安装：
```bash
pnpm add react react-dom
```

**选项 3：** 如果可以接受则抑制警告：
```json
{
  "pnpm": {
    "peerDependencyRules": {
      "ignoreMissing": ["react"]
    }
  }
}
```

### 符号链接问题

某些工具不能与符号链接配合工作。使用提升模式：

```ini
# .npmrc
node-linker=hoisted
```

或提升特定包：

```ini
public-hoist-pattern[]=*eslint*
public-hoist-pattern[]=*babel*
```

### 本地模块重建

如果本地模块失败，尝试：

```bash
# Rebuild all native modules
pnpm rebuild

# Or reinstall
rm -rf node_modules
pnpm install
```

## Monorepo 迁移

### 从 npm Workspaces 迁移

1. 创建 `pnpm-workspace.yaml`：
   ```yaml
   packages:
     - 'packages/*'
   ```

2. 更新内部依赖以使用 workspace 协议：
   ```json
   {
     "dependencies": {
       "@myorg/utils": "workspace:^"
     }
   }
   ```

3. 安装：
   ```bash
   rm -rf node_modules packages/*/node_modules package-lock.json
   pnpm install
   ```

### 从 Yarn Workspaces 迁移

1. 删除 Yarn 特定文件：
   ```bash
   rm yarn.lock .yarnrc.yml
   rm -rf .yarn
   ```

2. 创建与 package.json 中 `workspaces` 匹配的 `pnpm-workspace.yaml`：
   ```yaml
   packages:
     - 'packages/*'
   ```

3. 更新 `package.json` - 删除不需要的 Yarn workspace 配置：
   ```json
   {
     // Remove "workspaces" field (optional, pnpm uses pnpm-workspace.yaml)
   }
   ```

4. 转换 workspace 引用：
   ```json
   // From Yarn
   "@myorg/utils": "*"

   // To pnpm
   "@myorg/utils": "workspace:*"
   ```

### 从 Lerna 迁移

pnpm 可以替代 Lerna 用于大多数场景：

```bash
# Lerna: run script in all packages
lerna run build

# pnpm equivalent
pnpm -r run build

# Lerna: run in specific package
lerna run build --scope=@myorg/app

# pnpm equivalent
pnpm --filter @myorg/app run build

# Lerna: publish
lerna publish

# pnpm: use changesets instead
pnpm add -Dw @changesets/cli
pnpm changeset
pnpm changeset version
pnpm publish -r
```

## 配置迁移

### .npmrc 设置

大多数 npm/Yarn 设置在 pnpm 的 `.npmrc` 中同样适用：

```ini
# Registry settings (same as npm)
registry=https://registry.npmjs.org/
@myorg:registry=https://npm.myorg.com/

# Auth tokens (same as npm)
//registry.npmjs.org/:_authToken=${NPM_TOKEN}

# pnpm-specific additions
auto-install-peers=true
strict-peer-dependencies=false
```

### 脚本迁移

大多数脚本保持不变。更新 pnpm 特定模式：

```json
{
  "scripts": {
    // npm: recursive scripts
    "build:all": "npm run build --workspaces",
    // pnpm: use -r flag
    "build:all": "pnpm -r run build",

    // npm: run in specific workspace
    "dev:app": "npm run dev -w packages/app",
    // pnpm: use --filter
    "dev:app": "pnpm --filter @myorg/app run dev"
  }
}
```

## CI/CD 迁移

更新 CI 配置：

```yaml
# Before (npm)
- run: npm ci

# After (pnpm)
- uses: pnpm/action-setup@v4
- run: pnpm install --frozen-lockfile
```

添加到 `package.json` 以使用 Corepack：
```json
{
  "packageManager": "pnpm@9.0.0"
}
```

## 渐进式迁移

对于大型项目，渐进式迁移：

1. **从 CI 开始**：在 CI 中使用 pnpm，本地保留 npm/yarn
2. **添加 pnpm-lock.yaml**：运行 `pnpm import` 创建 lockfile
3. **全面测试**：确保使用 pnpm 构建正常工作
4. **更新文档**：更新 README、CONTRIBUTING
5. **删除旧文件**：团队采用后删除旧 lockfile

## 回滚计划

如果迁移导致问题：

```bash
# Remove pnpm files
rm -rf node_modules pnpm-lock.yaml pnpm-workspace.yaml

# Restore npm
npm install

# Or restore Yarn
yarn install
```

在 git 历史中保留旧的 lockfile 以便轻松回滚。

<!--
Source references:
- https://pnpm.io/installation
- https://pnpm.io/cli/import
- https://pnpm.io/limitations
-->
