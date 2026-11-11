---
name: pnpm-hooks
description: Customize package resolution and dependency behavior with pnpmfile hooks
---

# pnpm 钩子

pnpm 通过 `.pnpmfile.cjs` 提供钩子来自定义包的解析方式和元数据处理。

## 设置

在工作区根目录创建 `.pnpmfile.cjs`：

```js
// .pnpmfile.cjs
function readPackage(pkg, context) {
  // Modify package metadata
  return pkg
}

function afterAllResolved(lockfile, context) {
  // Modify lockfile
  return lockfile
}

module.exports = {
  hooks: {
    readPackage,
    afterAllResolved
  }
}
```

## readPackage 钩子

在解析前为每个包调用。用于修改依赖、添加缺失的同伴依赖或修复损坏的包。

### 添加缺失的同伴依赖

```js
function readPackage(pkg, context) {
  if (pkg.name === 'some-broken-package') {
    pkg.peerDependencies = {
      ...pkg.peerDependencies,
      react: '*'
    }
    context.log(`Added react peer dep to ${pkg.name}`)
  }
  return pkg
}
```

### 覆盖依赖版本

```js
function readPackage(pkg, context) {
  // Fix all lodash versions
  if (pkg.dependencies?.lodash) {
    pkg.dependencies.lodash = '^4.17.21'
  }
  if (pkg.devDependencies?.lodash) {
    pkg.devDependencies.lodash = '^4.17.21'
  }
  return pkg
}
```

### 删除不需要的依赖

```js
function readPackage(pkg, context) {
  // Remove optional dependency that causes issues
  if (pkg.optionalDependencies?.fsevents) {
    delete pkg.optionalDependencies.fsevents
  }
  return pkg
}
```

### 替换包

```js
function readPackage(pkg, context) {
  // Replace deprecated package
  if (pkg.dependencies?.['old-package']) {
    pkg.dependencies['new-package'] = pkg.dependencies['old-package']
    delete pkg.dependencies['old-package']
  }
  return pkg
}
```

### 修复损坏的包

```js
function readPackage(pkg, context) {
  // Fix incorrect exports field
  if (pkg.name === 'broken-esm-package') {
    pkg.exports = {
      '.': {
        import: './dist/index.mjs',
        require: './dist/index.cjs'
      }
    }
  }
  return pkg
}
```

## afterAllResolved 钩子

在 lockfile 生成后调用。用于解析后的修改。

```js
function afterAllResolved(lockfile, context) {
  // Log all resolved packages
  context.log(`Resolved ${Object.keys(lockfile.packages || {}).length} packages`)

  // Modify lockfile if needed
  return lockfile
}
```

## Context 对象

`context` 对象提供工具：

```js
function readPackage(pkg, context) {
  // Log messages
  context.log('Processing package...')

  return pkg
}
```

## 与 TypeScript 一起使用

使用 JSDoc 获取类型提示：

```js
// .pnpmfile.cjs

/**
 * @param {import('type-fest').PackageJson} pkg
 * @param {{ log: (msg: string) => void }} context
 * @returns {import('type-fest').PackageJson}
 */
function readPackage(pkg, context) {
  return pkg
}

module.exports = {
  hooks: {
    readPackage
  }
}
```

## 常用模式

### 按包名条件处理

```js
function readPackage(pkg, context) {
  switch (pkg.name) {
    case 'package-a':
      pkg.dependencies.foo = '^2.0.0'
      break
    case 'package-b':
      delete pkg.optionalDependencies.bar
      break
  }
  return pkg
}
```

### 应用于所有包

```js
function readPackage(pkg, context) {
  // Remove all optional fsevents
  if (pkg.optionalDependencies) {
    delete pkg.optionalDependencies.fsevents
  }
  return pkg
}
```

### 调试解析

```js
function readPackage(pkg, context) {
  if (process.env.DEBUG_PNPM) {
    context.log(`${pkg.name}@${pkg.version}`)
    context.log(`  deps: ${Object.keys(pkg.dependencies || {}).join(', ')}`)
  }
  return pkg
}
```

## 钩子与覆盖

| 功能 | 钩子 (.pnpmfile.cjs) | 覆盖 |
|---------|----------------------|-----------|
| 复杂性 | 可以使用 JavaScript 逻辑 | 仅声明式 |
| 范围 | 任何包元数据 | 仅版本 |
| 用途 | 复杂修复、条件逻辑 | 简单版本固定 |

**简单版本修复优先使用覆盖。** 当需要以下内容时使用钩子：
- 条件逻辑
- 非版本修改（exports、同伴依赖）
- 日志/调试

## 故障排除

### 钩子未运行

1. 确保文件名为 `.pnpmfile.cjs`（不是 `.js`）
2. 检查文件在工作区根目录
3. 运行 `pnpm install` 触发钩子

### 调试钩子

```bash
# See hook logs
pnpm install --reporter=append-only
```

<!--
Source references:
- https://pnpm.io/pnpmfile
-->
