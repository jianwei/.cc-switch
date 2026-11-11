---
name: pnpm-cli-commands
description: Essential pnpm commands for package management, running scripts, and workspace operations
---

# pnpm CLI 命令

pnpm 提供全面的 CLI 用于包管理，命令与 npm/yarn 类似，但具有独特功能。

## 安装命令

### 安装所有依赖
```bash
pnpm install
# or
pnpm i
```

### 添加依赖
```bash
# Production dependency
pnpm add <pkg>

# Dev dependency
pnpm add -D <pkg>
pnpm add --save-dev <pkg>

# Optional dependency
pnpm add -O <pkg>

# Global package
pnpm add -g <pkg>

# Specific version
pnpm add <pkg>@<version>
pnpm add <pkg>@next
pnpm add <pkg>@^1.0.0
```

### 删除依赖
```bash
pnpm remove <pkg>
pnpm rm <pkg>
pnpm uninstall <pkg>
pnpm un <pkg>
```

### 更新依赖
```bash
# Update all
pnpm update
pnpm up

# Update specific package
pnpm update <pkg>

# Update to latest (ignore semver)
pnpm update --latest
pnpm up -L

# Interactive update
pnpm update --interactive
pnpm up -i
```

## 脚本命令

### 运行脚本
```bash
pnpm run <script>
# or shorthand
pnpm <script>

# Pass arguments to script
pnpm run build -- --watch

# Run script if exists (no error if missing)
pnpm run --if-present build
```

### 执行二进制文件
```bash
# Run local binary
pnpm exec <command>

# Example
pnpm exec eslint .
```

### dlx - 无需安装运行
```bash
# Like npx but for pnpm
pnpm dlx <pkg>

# Examples
pnpm dlx create-vite my-app
pnpm dlx degit user/repo my-project
```

## 工作区命令

### 在所有包中运行
```bash
# Run script in all workspace packages
pnpm -r run <script>
pnpm --recursive run <script>

# Run in specific packages
pnpm --filter <pattern> run <script>

# Examples
pnpm --filter "./packages/**" run build
pnpm --filter "!./packages/internal/**" run test
pnpm --filter "@myorg/*" run lint
```

### 过滤模式
```bash
# By package name
pnpm --filter <pkg-name> <command>
pnpm --filter "@scope/pkg" build

# By directory
pnpm --filter "./packages/core" test

# Dependencies of a package
pnpm --filter "...@scope/app" build

# Dependents of a package
pnpm --filter "@scope/core..." test

# Changed packages since commit/branch
pnpm --filter "...[origin/main]" build
```

## 其他常用命令

### 链接包
```bash
# Link global package
pnpm link --global
pnpm link -g

# Use linked package
pnpm link --global <pkg>
```

### 补丁包
```bash
# Create patch for a package
pnpm patch <pkg>@<version>

# After editing, commit the patch
pnpm patch-commit <path>

# Remove a patch
pnpm patch-remove <pkg>
```

### 存储管理
```bash
# Show store path
pnpm store path

# Remove unreferenced packages
pnpm store prune

# Check store integrity
pnpm store status
```

### 其他命令
```bash
# Clean install (like npm ci)
pnpm install --frozen-lockfile

# List installed packages
pnpm list
pnpm ls

# Why is package installed?
pnpm why <pkg>

# Outdated packages
pnpm outdated

# Audit for vulnerabilities
pnpm audit

# Rebuild native modules
pnpm rebuild

# Import from npm/yarn lockfile
pnpm import

# Create tarball
pnpm pack

# Publish package
pnpm publish
```

## 常用参数

```bash
# Ignore scripts
pnpm install --ignore-scripts

# Prefer offline (use cache)
pnpm install --prefer-offline

# Strict peer dependencies
pnpm install --strict-peer-dependencies

# Production only
pnpm install --prod
pnpm install -P

# No optional dependencies
pnpm install --no-optional
```

<!--
Source references:
- https://pnpm.io/cli/install
- https://pnpm.io/cli/add
- https://pnpm.io/cli/run
- https://pnpm.io/filtering
-->
