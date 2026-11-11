---
name: pnpm-patches
description: Patch third-party packages directly with customized fixes
---

# pnpm 补丁

pnpm 的补丁功能允许你直接修改第三方包。用于在上游发布修复之前应用修复或自定义包行为。

## 创建补丁

### 步骤 1：初始化补丁

```bash
pnpm patch <pkg>@<version>

# Example
pnpm patch express@4.18.2
```

这会创建一个包含包源代码的临时目录并输出路径：

```
You can now edit the following folder: /tmp/abc123...
```

### 步骤 2：编辑文件

导航到临时目录并进行更改：

```bash
cd /tmp/abc123...
# Edit files as needed
```

### 步骤 3：提交补丁

```bash
pnpm patch-commit <path-from-step-1>

# Example
pnpm patch-commit /tmp/abc123...
```

这会在 `patches/` 中创建一个 `.patch` 文件并更新 `package.json`：

```
patches/
└── express@4.18.2.patch
```

```json
{
  "pnpm": {
    "patchedDependencies": {
      "express@4.18.2": "patches/express@4.18.2.patch"
    }
  }
}
```

## 补丁文件格式

补丁使用标准 unified diff 格式：

```diff
diff --git a/lib/router/index.js b/lib/router/index.js
index abc123..def456 100644
--- a/lib/router/index.js
+++ b/lib/router/index.js
@@ -100,6 +100,7 @@ function createRouter() {
   // Original code
-  const timeout = 30000;
+  const timeout = 60000; // Extended timeout
   return router;
 }
```

## 管理补丁

### 列出已补丁的包

```bash
pnpm list --depth=0
# Shows (patched) marker for patched packages
```

### 更新补丁

```bash
# Edit existing patch
pnpm patch express@4.18.2

# After editing
pnpm patch-commit <path>
```

### 删除补丁

```bash
pnpm patch-remove <pkg>@<version>

# Example
pnpm patch-remove express@4.18.2
```

或手动：
1. 从 `patches/` 删除补丁文件
2. 从 `package.json` 的 `patchedDependencies` 中删除条目
3. 运行 `pnpm install`

## 补丁配置

### 自定义补丁目录

```json
{
  "pnpm": {
    "patchedDependencies": {
      "express@4.18.2": "custom-patches/my-express-fix.patch"
    }
  }
}
```

### 多个包

```json
{
  "pnpm": {
    "patchedDependencies": {
      "express@4.18.2": "patches/express@4.18.2.patch",
      "lodash@4.17.21": "patches/lodash@4.17.21.patch",
      "@types/node@20.10.0": "patches/@types__node@20.10.0.patch"
    }
  }
}
```

## 工作区

补丁在工作区之间共享。在根 `package.json` 中定义：

```json
// Root package.json
{
  "pnpm": {
    "patchedDependencies": {
      "express@4.18.2": "patches/express@4.18.2.patch"
    }
  }
}
```

所有使用 `express@4.18.2` 的工作区包都会应用补丁。

## 最佳实践

1. **版本特异性**：补丁与精确版本绑定。升级依赖时更新补丁。

2. **记录补丁**：添加注释解释为什么存在补丁：
   ```bash
   # In patches/README.md
   ## express@4.18.2.patch
   Fixes timeout issue. PR pending: https://github.com/expressjs/express/pull/1234
   ```

3. **最小化补丁**：保持补丁小而专注。大型补丁难以维护。

4. **跟踪上游**：记录上游问题/PR 以便修复时可以删除补丁。

5. **测试补丁**：确保补丁代码在你的用例中正常工作。

## 故障排除

### 补丁应用失败

```
ERR_PNPM_PATCH_FAILED  Cannot apply patch
```

包版本已更改。重新创建补丁：
```bash
pnpm patch-remove express@4.18.2
pnpm patch express@4.18.2
# Reapply changes
pnpm patch-commit <path>
```

### 补丁未应用

确保：
1. `patchedDependencies` 中的版本与安装的版本完全匹配
2. 添加补丁配置后运行 `pnpm install`

<!--
Source references:
- https://pnpm.io/cli/patch
- https://pnpm.io/cli/patch-commit
- https://pnpm.io/package_json#pnpmpatcheddependencies
-->
