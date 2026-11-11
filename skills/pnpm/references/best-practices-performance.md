---
name: pnpm-performance-optimization
description: Tips and tricks for faster installs and better performance
---

# pnpm 性能优化

pnpm 默认情况下很快，但这些优化可以使其更快。

## 安装优化

### 使用 Frozen Lockfile

当 lockfile 存在时跳过解析：

```bash
pnpm install --frozen-lockfile
```

这更快，因为 pnpm 完全跳过解析阶段。

### 优先离线模式

尽可能使用缓存的包：

```bash
pnpm install --prefer-offline
```

或全局配置：
```ini
# .npmrc
prefer-offline=true
```

### 跳过可选依赖

如果不需要可选依赖：

```bash
pnpm install --no-optional
```

### 跳过脚本

对于 CI 或不需要脚本的场景：

```bash
pnpm install --ignore-scripts
```

**注意：** 某些包需要 postinstall 脚本才能正常工作。

### 仅构建特定依赖

仅对特定包运行构建脚本：

```ini
# .npmrc
onlyBuiltDependencies[]=esbuild
onlyBuiltDependencies[]=sharp
onlyBuiltDependencies[]=@swc/core
```

或完全跳过不需要构建的依赖：

```json
{
  "pnpm": {
    "neverBuiltDependencies": ["fsevents", "cpu-features"]
  }
}
```

## 存储优化

### 副作用缓存

缓存本地模块的构建结果：

```ini
# .npmrc
side-effects-cache=true
```

这会缓存 postinstall 脚本的结果，加快后续安装。

### 共享存储

为所有项目使用单一存储（默认行为）：

```ini
# .npmrc
store-dir=~/.pnpm-store
```

优势：
- 所有项目下载一次包
- 硬链接节省磁盘空间
- 从缓存安装更快

### 存储维护

定期清理未引用的包：

```bash
# Remove unreferenced packages
pnpm store prune

# Check store integrity
pnpm store status
```

## 工作区优化

### 并行执行

并行运行工作区脚本：

```bash
pnpm -r --parallel run build
```

控制并发数：
```ini
# .npmrc
workspace-concurrency=8
```

### 流式输出

实时查看输出：

```bash
pnpm -r --stream run build
```

### 过滤到已更改的包

仅构建更改的内容：

```bash
# Build packages changed since main branch
pnpm --filter "...[origin/main]" run build
```

### 拓扑顺序

先构建依赖再构建依赖项：

```bash
pnpm -r run build
# Automatically runs in topological order
```

显式顺序构建：
```bash
pnpm -r --workspace-concurrency=1 run build
```

## 网络优化

### 配置 Registry

使用最近/最快的 registry：

```ini
# .npmrc
registry=https://registry.npmmirror.com/
```

### HTTP 设置

调整网络设置：

```ini
# .npmrc
fetch-retries=3
fetch-retry-mintimeout=10000
fetch-retry-maxtimeout=60000
network-concurrency=16
```

### 代理配置

```ini
# .npmrc
proxy=http://proxy.company.com:8080
https-proxy=http://proxy.company.com:8080
```

## Lockfile 优化

### 单一 Lockfile（Monorepo）

为所有包使用共享 lockfile（默认）：

```ini
# .npmrc
shared-workspace-lockfile=true
```

优势：
- 单一真相来源
- 解析更快
- 工作区版本一致

### 仅 Lockfile 模式

仅更新 lockfile 而不安装：

```bash
pnpm install --lockfile-only
```

## 基准测试

### 比较安装时间

```bash
# Clean install
rm -rf node_modules pnpm-lock.yaml
time pnpm install

# Cached install (with lockfile)
rm -rf node_modules
time pnpm install --frozen-lockfile

# With store cache
time pnpm install --frozen-lockfile --prefer-offline
```

### 分析解析

调试慢速安装：

```bash
# Verbose logging
pnpm install --reporter=append-only

# Debug mode
DEBUG=pnpm:* pnpm install
```

## 配置总结

优化的性能 `.npmrc`：

```ini
# Install behavior
prefer-offline=true
auto-install-peers=true

# Build optimization
side-effects-cache=true
# Only build what's necessary
onlyBuiltDependencies[]=esbuild
onlyBuiltDependencies[]=@swc/core

# Network
fetch-retries=3
network-concurrency=16

# Workspace
workspace-concurrency=4
```

## 快速参考

| 场景 | 命令/设置 |
|----------|-----------------|
| CI 安装 | `pnpm install --frozen-lockfile` |
| 离线开发 | `--prefer-offline` |
| 跳过本地构建 | `neverBuiltDependencies` |
| 并行工作区 | `pnpm -r --parallel run build` |
| 仅构建更改 | `pnpm --filter "...[origin/main]" build` |
| 清理存储 | `pnpm store prune` |

<!--
Source references:
- https://pnpm.io/npmrc
- https://pnpm.io/cli/install
- https://pnpm.io/filtering
-->
