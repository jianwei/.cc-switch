---
name: pnpm-store
description: Content-addressable storage system that makes pnpm fast and disk-efficient
---

# pnpm 存储

pnpm 使用内容寻址存储来节省磁盘空间并加快安装速度。所有包都存储一次全局存储，并通过硬链接到项目的 `node_modules`。

## 工作原理

1. **全局存储**：包下载一次到中央存储
2. **硬链接**：项目链接到存储而不是复制文件
3. **内容寻址**：文件按内容哈希存储，相同文件去重

### 存储布局

```
~/.pnpm-store/              # Global store (default location)
└── v3/
    └── files/
        └── <hash>/         # Files stored by content hash

project/
└── node_modules/
    ├── .pnpm/              # Virtual store (hard links to global store)
    │   ├── lodash@4.17.21/
    │   │   └── node_modules/
    │   │       └── lodash/
    │   └── express@4.18.2/
    │       └── node_modules/
    │           ├── express/
    │           └── <deps>/  # Flat structure for dependencies
    ├── lodash -> .pnpm/lodash@4.17.21/node_modules/lodash
    └── express -> .pnpm/express@4.18.2/node_modules/express
```

## 存储命令

```bash
# Show store location
pnpm store path

# Remove unreferenced packages
pnpm store prune

# Check store integrity
pnpm store status

# Add package to store without installing
pnpm store add <pkg>
```

## 配置

### 存储位置

```ini
# .npmrc
store-dir=~/.pnpm-store

# Or use environment variable
PNPM_HOME=~/.local/share/pnpm
```

### 虚拟存储

虚拟存储（`.pnpm` 在 `node_modules` 中）包含指向全局存储的符号链接：

```ini
# Customize virtual store location
virtual-store-dir=node_modules/.pnpm

# Alternative flat layout
node-linker=hoisted
```

## 磁盘空间优势

pnpm 节省大量磁盘空间：

- **去重**：相同包版本在所有项目中只存储一次
- **内容去重**：不同包中的相同文件只存储一次
- **硬链接**：不复制，只链接

### 检查磁盘使用

```bash
# Compare actual vs apparent size
du -sh node_modules        # Apparent size
du -sh --apparent-size node_modules  # With hard links counted
```

## 节点链接器模式

配置 `node_modules` 的结构方式：

```ini
# Default: Symlinked structure (recommended)
node-linker=isolated

# Flat node_modules (npm-like, for compatibility)
node-linker=hoisted

# PnP mode (experimental, like Yarn PnP)
node-linker=pnp
```

### 隔离模式（默认）

- 严格的依赖解析
- 无幽灵依赖
- 包只能访问声明的依赖

### 提升模式

- 像 npm 一样的扁平 `node_modules`
- 用于兼容不支持符号链接的工具
- 失去严格性优势

## 副作用缓存

缓存本地模块的构建输出：

```ini
# Enable side effects caching
side-effects-cache=true

# Store side effects in project (instead of global store)
side-effects-cache-readonly=true
```

## 跨机器共享存储

对于 CI/CD，可以共享存储：

```yaml
# GitHub Actions example
- uses: pnpm/action-setup@v4
  with:
    run_install: false

- name: Get pnpm store directory
  shell: bash
  run: echo "STORE_PATH=$(pnpm store path --silent)" >> $GITHUB_ENV

- uses: actions/cache@v4
  with:
    path: ${{ env.STORE_PATH }}
    key: ${{ runner.os }}-pnpm-store-${{ hashFiles('**/pnpm-lock.yaml') }}
```

## 故障排除

### 存储损坏
```bash
# Verify and fix store
pnpm store status
pnpm store prune
```

### 硬链接问题（网络驱动器、Docker）
```ini
# Use copying instead of hard links
package-import-method=copy
```

### 权限问题
```bash
# Fix store permissions
chmod -R u+w ~/.pnpm-store
```

<!--
Source references:
- https://pnpm.io/symlinked-node-modules-structure
- https://pnpm.io/cli/store
- https://pnpm.io/npmrc#store-dir
-->
