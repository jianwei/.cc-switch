---
name: pnpm-aliases
description: Install packages under custom names for versioning, forks, or alternatives
---

# pnpm 别名

pnpm 支持使用 `npm:` 协议的包别名。这允许你以不同名称安装包、使用同一包的多个版本或替换包。

## 基本语法

```bash
pnpm add <alias>@npm:<package>@<version>
```

在 `package.json` 中：
```json
{
  "dependencies": {
    "<alias>": "npm:<package>@<version>"
  }
}
```

## 使用场景

### 同一包的多个版本

并排安装不同版本：

```json
{
  "dependencies": {
    "lodash3": "npm:lodash@3",
    "lodash4": "npm:lodash@4"
  }
}
```

用法：
```js
import lodash3 from 'lodash3'
import lodash4 from 'lodash4'
```

### 用 Fork 替换包

用 fork 或替代品替换包：

```json
{
  "dependencies": {
    "original-pkg": "npm:my-fork@^1.0.0"
  }
}
```

所有对 `original-pkg` 的导入都将解析到 `my-fork`。

### 替换已弃用包

```json
{
  "dependencies": {
    "request": "npm:@cypress/request@^3.0.0"
  }
}
```

### 作用域到非作用域（或反之）

```json
{
  "dependencies": {
    "vue": "npm:@anthropic/vue@^3.0.0",
    "@myorg/utils": "npm:lodash@^4.17.21"
  }
}
```

## CLI 用法

### 添加别名

```bash
# Add lodash under alias
pnpm add lodash4@npm:lodash@4

# Add fork as original name
pnpm add request@npm:@cypress/request
```

### 添加多个版本

```bash
pnpm add react17@npm:react@17 react18@npm:react@18
```

## 与 TypeScript 一起使用

对于别名的类型解析，可能需要配置 TypeScript：

```json
// tsconfig.json
{
  "compilerOptions": {
    "paths": {
      "lodash3": ["node_modules/lodash3"],
      "lodash4": ["node_modules/lodash4"]
    }
  }
}
```

或使用带别名的 `@types` 包：

```json
{
  "devDependencies": {
    "@types/lodash3": "npm:@types/lodash@3",
    "@types/lodash4": "npm:@types/lodash@4"
  }
}
```

## 与覆盖结合

强制所有传递依赖使用别名：

```yaml
# pnpm-workspace.yaml
overrides:
  "underscore": "npm:lodash@^4.17.21"
```

这会将所有 `underscore` 导入（包括在依赖中）替换为 lodash。

## Git 和本地别名

别名适用于任何有效的 pnpm specifier：

```json
{
  "dependencies": {
    "my-fork": "npm:user/repo#commit",
    "local-pkg": "file:../local-package"
  }
}
```

## 最佳实践

1. **清晰的命名**：使用描述性别名名称表明用途
   ```json
   "lodash-legacy": "npm:lodash@3"
   "lodash-modern": "npm:lodash@4"
   ```

2. **记录别名**：添加注释或文档解释为什么存在别名

3. **全局替换优先使用覆盖**：如果想替换所有地方的包，使用覆盖而不是别名

4. **全面测试**：别名包可能有细微的行为差异

<!--
Source references:
- https://pnpm.io/aliases
-->
