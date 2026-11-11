---
name: pnpm-overrides
description: Force specific versions of dependencies including transitive dependencies
---

# pnpm 覆盖

覆盖允许你强制指定包的版本，包括传递依赖。用于修复安全漏洞或兼容性问题。

## 基本语法

在 `pnpm-workspace.yaml`（推荐）或 `package.json` 中定义覆盖：

### 在 pnpm-workspace.yaml 中（推荐）

```yaml
packages:
  - 'packages/*'

overrides:
  # Override all versions of a package
  lodash: ^4.17.21

  # Override specific version range
  "foo@^1.0.0": ^1.2.3

  # Override nested dependency
  "express>cookie": ^0.6.0

  # Override to different package
  "underscore": "npm:lodash@^4.17.21"
```

### 在 package.json 中

```json
{
  "pnpm": {
    "overrides": {
      "lodash": "^4.17.21",
      "foo@^1.0.0": "^1.2.3",
      "bar@^2.0.0>qux": "^1.0.0"
    }
  }
}
```

## 覆盖模式

### 覆盖所有实例
```yaml
overrides:
  lodash: ^4.17.21
```
强制所有 lodash 安装使用 ^4.17.21。

### 覆盖特定父版本
```yaml
overrides:
  "foo@^1.0.0": ^1.2.3
```
仅当请求版本匹配 ^1.0.0 时覆盖 foo。

### 覆盖嵌套依赖
```yaml
overrides:
  "express>cookie": ^0.6.0
  "foo@1.x>bar@^2.0.0>qux": ^1.0.0
```
仅当 cookie 是 express 的依赖时覆盖 cookie。

### 替换为不同的包
```yaml
overrides:
  # Replace underscore with lodash
  "underscore": "npm:lodash@^4.17.21"

  # Use local file
  "some-pkg": "file:./local-pkg"

  # Use git
  "some-pkg": "github:user/repo#commit"
```

### 删除依赖
```yaml
overrides:
  "unwanted-pkg": "-"
```
`-` 完全删除该包。

## 常见使用场景

### 安全修复

强制使用有补丁的易受攻击包版本：

```yaml
overrides:
  # Fix CVE in transitive dependency
  "minimist": "^1.2.6"
  "json5": "^2.2.3"
```

### 去重依赖

当安装多个版本时强制使用单一版本：

```yaml
overrides:
  "react": "^18.2.0"
  "react-dom": "^18.2.0"
```

### 修复同伴依赖问题

```yaml
overrides:
  "@types/react": "^18.2.0"
```

### 替换已弃用包

```yaml
overrides:
  "request": "npm:@cypress/request@^3.0.0"
```

## 钩子替代方案

对于更复杂的场景，使用 `.pnpmfile.cjs`：

```js
// .pnpmfile.cjs
function readPackage(pkg, context) {
  // Override dependency version
  if (pkg.dependencies?.lodash) {
    pkg.dependencies.lodash = '^4.17.21'
  }

  // Add missing peer dependency
  if (pkg.name === 'some-package') {
    pkg.peerDependencies = {
      ...pkg.peerDependencies,
      react: '*'
    }
  }

  return pkg
}

module.exports = {
  hooks: {
    readPackage
  }
}
```

## 覆盖与目录

| 功能 | 覆盖 | 目录 |
|---------|-----------|----------|
| 影响 | 所有依赖（包括传递） | 仅直接依赖 |
| 用法 | 自动 | 显式 `catalog:` 引用 |
| 用途 | 强制版本、修复问题 | 版本管理 |
| 粒度 | 可以针对特定父项 | 仅包范围 |

## 调试

检查解析的版本：

```bash
# See resolved versions
pnpm why lodash

# List all versions
pnpm list lodash --depth=Infinity
```

<!--
Source references:
- https://pnpm.io/package_json#pnpmoverrides
- https://pnpm.io/pnpmfile
-->
