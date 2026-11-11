---
name: vitepress-cli
description: Command-line interface for development, building, and previewing VitePress sites
---

# @author Claude Code (claude-sonnet-4-6)

# CLI 命令

VitePress 提供四个主要命令：`dev`、`build`、`preview` 和 `init`。

## 开发服务器

启动带有热模块替换的开发服务器：

```bash
# 在当前目录中（dev 命令是可选的）
vitepress

# 或显式指定
vitepress dev

# 子目录中的项目
vitepress dev docs
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--open [path]` | 启动时打开浏览器 |
| `--port <port>` | 指定端口号 |
| `--base <path>` | 覆盖基础 URL |
| `--cors` | 启用 CORS |
| `--strictPort` | 端口被占用时退出 |
| `--force` | 忽略缓存并重新打包 |

```bash
vitepress dev docs --port 3000 --open
```

## 生产构建

构建用于生产的静态文件：

```bash
vitepress build docs
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--base <path>` | 覆盖基础 URL |
| `--target <target>` | 转译目标（默认：`modules`）|
| `--outDir <dir>` | 输出目录（相对于当前工作目录）|
| `--assetsInlineLimit <n>` | 资源内联阈值（字节）|
| `--mpa` | MPA 模式构建（无客户端水合）|

```bash
vitepress build docs --outDir dist
```

## 预览生产构建

本地预览生产构建：

```bash
vitepress preview docs
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--port <port>` | 指定端口号 |
| `--base <path>` | 覆盖基础 URL |

```bash
vitepress preview docs --port 4173
```

## 初始化项目

启动设置向导：

```bash
vitepress init
```

这将创建基本的文件结构：
- `.vitepress/config.js` - 配置文件
- `index.md` - 首页
- 可选的示例页面

## package.json 脚本

典型的脚本配置：

```json
{
  "scripts": {
    "docs:dev": "vitepress dev docs",
    "docs:build": "vitepress build docs",
    "docs:preview": "vitepress preview docs"
  }
}
```

## 关键要点

- 开发服务器默认运行在 `http://localhost:5173`
- 预览服务器默认运行在 `http://localhost:4173`
- 生产输出默认到 `.vitepress/dist`
- `docs` 参数指定项目根目录
- 使用 `--base` 可以覆盖基础路径而无需修改配置

<!--
Source references:
- https://vitepress.dev/reference/cli
-->
