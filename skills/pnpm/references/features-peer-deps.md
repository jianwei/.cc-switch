---
name: pnpm-peer-dependencies
description: Handling peer dependencies with auto-install and resolution rules
---

# pnpm 同伴依赖

pnpm 默认具有严格的同伴依赖处理。它提供配置选项来控制同伴依赖的解析和报告方式。

## 自动安装同伴依赖

默认情况下，pnpm 自动安装同伴依赖：

```ini
# .npmrc (default is true since pnpm v8)
auto-install-peers=true
```

启用后，pnpm 根据最佳匹配版本自动添加缺失的同伴依赖。

## 严格同伴依赖

控制同伴依赖问题是否导致错误：

```ini
# Fail on peer dependency issues (default: false)
strict-peer-dependencies=true
```

严格模式下，如果满足以下条件，pnpm 将失败：
- 同伴依赖缺失
- 安装的版本不符合要求范围

## 同伴依赖规则

在 `package.json` 中配置同伴依赖行为：

```json
{
  "pnpm": {
    "peerDependencyRules": {
      "ignoreMissing": ["@babel/*", "eslint"],
      "allowedVersions": {
        "react": "17 || 18"
      },
      "allowAny": ["@types/*"]
    }
  }
}
```

### ignoreMissing

抑制缺失同伴依赖的警告：

```json
{
  "pnpm": {
    "peerDependencyRules": {
      "ignoreMissing": [
        "@babel/*",
        "eslint",
        "webpack"
      ]
    }
  }
}
```

使用模式：
- `"react"` - 精确包名
- `"@babel/*"` - 作用域中的所有包
- `"*"` - 所有包（不推荐）

### allowedVersions

允许否则会导致警告的特定版本：

```json
{
  "pnpm": {
    "peerDependencyRules": {
      "allowedVersions": {
        "react": "17 || 18",
        "webpack": "4 || 5",
        "@types/react": "*"
      }
    }
  }
}
```

### allowAny

允许指定同伴依赖的任何版本：

```json
{
  "pnpm": {
    "peerDependencyRules": {
      "allowAny": ["@types/*", "eslint"]
    }
  }
}
```

## 通过钩子添加同伴依赖

使用 `.pnpmfile.cjs` 添加缺失的同伴依赖：

```js
// .pnpmfile.cjs
function readPackage(pkg, context) {
  // Add missing peer dependency
  if (pkg.name === 'problematic-package') {
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

## 工作区中的同伴依赖

工作区包可以满足同伴依赖：

```json
// packages/app/package.json
{
  "dependencies": {
    "react": "^18.2.0",
    "@myorg/components": "workspace:^"
  }
}

// packages/components/package.json
{
  "peerDependencies": {
    "react": "^17.0.0 || ^18.0.0"
  }
}
```

工作区 `app` 提供的 `react` 满足了 `components` 的同伴依赖。

## 常见场景

### 具有共享 React 的 Monorepo

```yaml
# pnpm-workspace.yaml
catalog:
  react: ^18.2.0
  react-dom: ^18.2.0
```

```json
// packages/ui/package.json
{
  "peerDependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  }
}

// apps/web/package.json
{
  "dependencies": {
    "react": "catalog:",
    "react-dom": "catalog:",
    "@myorg/ui": "workspace:^"
  }
}
```

### 抑制 ESLint 插件警告

```json
{
  "pnpm": {
    "peerDependencyRules": {
      "ignoreMissing": [
        "eslint",
        "@typescript-eslint/parser"
      ]
    }
  }
}
```

### 允许多个大版本

```json
{
  "pnpm": {
    "peerDependencyRules": {
      "allowedVersions": {
        "webpack": "4 || 5",
        "postcss": "7 || 8"
      }
    }
  }
}
```

## 调试同伴依赖

```bash
# See why a package is installed
pnpm why <package>

# List all peer dependency warnings
pnpm install --reporter=append-only 2>&1 | grep -i peer

# Check dependency tree
pnpm list --depth=Infinity
```

## 最佳实践

1. **启用 auto-install-peers** 以获得便利性（pnpm v8+ 默认）

2. **使用 peerDependencyRules** 而不是忽略所有警告

3. **记录抑制的警告** 解释为什么它们是安全的

4. **在库中保持同伴依赖范围广泛**：
   ```json
   {
     "peerDependencies": {
       "react": "^17.0.0 || ^18.0.0"
     }
   }
   ```

5. **如果支持多个主要版本，用不同同伴版本测试**

<!--
Source references:
- https://pnpm.io/package_json#pnpmpeerdependencyrules
- https://pnpm.io/npmrc#auto-install-peers
-->
