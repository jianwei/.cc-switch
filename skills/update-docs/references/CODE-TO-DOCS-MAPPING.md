# 代码到文档映射

将 Next.js 源代码目录映射到对应的文档文件。

## 核心映射

### 组件

| 源文件路径                                      | 文档路径                                              |
| ---------------------------------------------- | ---------------------------------------------------- |
| `packages/next/src/client/components/image.tsx`  | `docs/01-app/03-api-reference/02-components/image.mdx`  |
| `packages/next/src/client/components/link.tsx`   | `docs/01-app/03-api-reference/02-components/link.mdx`   |
| `packages/next/src/client/components/script.tsx` | `docs/01-app/03-api-reference/02-components/script.mdx` |
| `packages/next/src/client/components/form.tsx`   | `docs/01-app/03-api-reference/02-components/form.mdx`   |

### 函数

| 源文件路径                                          | 文档路径                                                    |
| -------------------------------------------------- | ---------------------------------------------------------- |
| `packages/next/src/server/request/`                  | `docs/01-app/03-api-reference/04-functions/`                      |
| `packages/next/src/server/lib/metadata/`             | `docs/01-app/03-api-reference/04-functions/generate-metadata.mdx` |
| `packages/next/src/client/components/navigation.tsx` | `docs/01-app/03-api-reference/04-functions/use-router.mdx`        |
| `packages/next/src/client/components/navigation.tsx` | `docs/01-app/03-api-reference/04-functions/use-pathname.mdx`      |
| `packages/next/src/client/components/navigation.tsx` | `docs/01-app/03-api-reference/04-functions/use-search-params.mdx` |

### 文件约定

| 源文件路径                                | 文档路径                                                  |
| ---------------------------------------- | -------------------------------------------------------- |
| `packages/next/src/build/webpack/loaders/` | `docs/01-app/03-api-reference/03-file-conventions/`           |
| `packages/next/src/server/app-render/`     | `docs/01-app/03-api-reference/03-file-conventions/layout.mdx` |
| `packages/next/src/server/app-render/`     | `docs/01-app/03-api-reference/03-file-conventions/page.mdx`   |

### 配置

| 源文件路径                                 | 文档路径                                                |
| ----------------------------------------- | ------------------------------------------------------ |
| `packages/next/src/server/config-shared.ts` | `docs/01-app/03-api-reference/05-config/01-next-config-js/` |
| `packages/next/src/server/config.ts`        | `docs/01-app/03-api-reference/05-config/01-next-config-js/` |
| `packages/next/src/build/webpack-config.ts` | `docs/01-app/03-api-reference/05-config/01-next-config-js/` |

### 指令

| 源文件路径                              | 文档路径                                                |
| -------------------------------------- | ------------------------------------------------------ |
| `packages/next/src/server/use-cache/`    | `docs/01-app/03-api-reference/01-directives/use-cache.mdx`  |
| `packages/next/src/client/use-client.ts` | `docs/01-app/03-api-reference/01-directives/use-client.mdx` |
| `packages/next/src/server/use-server.ts` | `docs/01-app/03-api-reference/01-directives/use-server.mdx` |

### 元数据文件约定

| 源文件路径                       | 文档路径                                                                  |
| -------------------------------- | ------------------------------------------------------------------------ |
| `packages/next/src/lib/metadata/` | `docs/01-app/03-api-reference/03-file-conventions/01-metadata/`                    |
| Metadata icons 处理               | `docs/01-app/03-api-reference/03-file-conventions/01-metadata/app-icons.mdx`       |
| Open Graph 图片                 | `docs/01-app/03-api-reference/03-file-conventions/01-metadata/opengraph-image.mdx` |
| Sitemap 生成                    | `docs/01-app/03-api-reference/03-file-conventions/01-metadata/sitemap.mdx`         |

## 目录模式映射

### 按功能区域

| 源目录                           | 文档区域                                      | 说明                    |
| -------------------------------- | -------------------------------------------- | ---------------------- |
| `packages/next/src/client/`            | `docs/01-app/03-api-reference/02-components/` | 客户端组件             |
| `packages/next/src/server/`            | `docs/01-app/03-api-reference/04-functions/`  | 服务器函数             |
| `packages/next/src/build/`             | `docs/01-app/03-api-reference/05-config/`     | 构建配置              |
| `packages/next/src/shared/lib/router/` | `docs/01-app/02-guides/`                      | 路由指南               |
| `packages/next/src/lib/metadata/`      | `docs/01-app/02-guides/metadata/`             | 元数据指南             |

### CLI 命令

| 源文件路径                           | 文档路径                                                    |
| ----------------------------------- | ---------------------------------------------------------- |
| `packages/next/src/cli/next-dev.ts`   | `docs/01-app/03-api-reference/06-cli/next-dev.mdx`   |
| `packages/next/src/cli/next-build.ts` | `docs/01-app/03-api-reference/06-cli/next-build.mdx` |
| `packages/next/src/cli/next-start.ts` | `docs/01-app/03-api-reference/06-cli/next-start.mdx` |

## 查找相关文档

### 步骤 1：识别变更的导出

查看变更文件导出的内容：

- 公共 API 导出 → API 参考文档
- 内部工具函数 → 通常不需要文档
- 配置类型 → 配置文档

### 步骤 2：搜索现有文档

使用 Claude 的内置工具进行搜索：

- **查找提及某个术语的文档**：使用 Grep 工具，搜索模式和 `docs/` 作为路径
- **列出目录中的文档**：使用 Glob 工具，模式如 `docs/01-app/03-api-reference/04-functions/*.mdx`

### 步骤 3：检查共享内容

如果编辑 App Router 文档，检查 Pages Router 是否有对应的带 `source` 字段的文件：

- **查找 source 引用**：在 `docs/02-pages/` 中使用模式 `source: app/api-reference` 进行 Grep 搜索

## 常见模式

### 新 API 函数

1. 添加导出到 `packages/next/src/server/`
2. 在 `docs/01-app/03-api-reference/04-functions/function-name.mdx` 创建文档
3. 如适用，更新索引/列表页面

### 新组件 Prop

1. 在 `packages/next/src/client/components/` 中的组件添加 prop
2. 更新对应文档中的 props 表格
3. 添加说明新 prop 的章节及示例

### 新配置选项

1. 在 `packages/next/src/server/config-shared.ts` 中添加选项
2. 在 `docs/01-app/03-api-reference/05-config/01-next-config-js/` 中找到相关配置文档
3. 添加选项及其描述和示例

### 行为变更

1. 在任何源文件中更改逻辑
2. 找到描述此行为的所有文档
3. 更新描述和示例以匹配新行为
4. 如有破坏性变更，添加迁移说明

## 快速搜索命令

使用 Claude 的内置工具进行高效搜索：

- **查找提及某个术语的所有文档**：使用 Grep 工具和搜索模式，以 `docs/` 为路径，过滤 `*.mdx` 文件
- **列出所有 API 参考文档**：使用 Glob 工具，模式为 `docs/01-app/03-api-reference/**/*.mdx`
- **按文件名模式查找文档**：使用 Glob 工具，模式如 `docs/**/*image*.mdx`
- **读取文档的 frontmatter**：使用 Read 工具并限制行数，以检查 `source` 字段
