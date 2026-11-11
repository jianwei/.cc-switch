# Playwriter MCP 常用 API

以下内容对应当前 Playwriter MCP。完整能力以 MCP 工具描述和上游文档为准。

## MCP 工具

- `execute({ code, timeout? })`：在持久化沙盒中执行 Playwright JavaScript。
- `reset({})`：连接损坏、页面关闭或上下文异常时重建连接，并清空 `state`。

## 沙盒对象

- `page`：MCP 提供的默认页面。
- `context`：当前浏览器上下文，可通过 `context.pages()` 获取已有页面。
- `browser`：已连接浏览器。不要调用 `close()`。
- `state`：同一 MCP 会话内跨调用保存的状态。

## 观察与调试 helper

```javascript
await snapshot({ page: state.page, search: /关键词/ })
await screenshotWithAccessibilityLabels({ page: state.page })
await getLatestLogs({ page: state.page, sinceLastCall: true })
await waitForPageLoad({ page: state.page, timeout: 5000 })
await inspect({ locator: state.page.locator('.target') })
const cdp = await getCDPSession({ page: state.page })
```

- `snapshot()`：首选的结构化页面观察方式，适合读取文本、角色和 locator。
- `screenshotWithAccessibilityLabels()`：仅在布局、图片、坐标或空间关系重要时使用。
- `getLatestLogs()`：读取已缓存的控制台日志和页面错误；必须传 `page`。
- `inspect()`：查看边界、滚动和计算样式。
- `getCDPSession()`：需要 Network、Debugger 等原始 CDP 能力时使用。

## 常用交互

```javascript
await state.page.getByRole('button', { name: '提交' }).click()
await state.page.locator('input[name="email"]').click()
await state.page.locator('input[name="email"]').fill('user@example.com')
await state.page.waitForURL('**/success**')
```

优先使用快照返回的 locator、语义角色或稳定属性。点击失败时重新观察页面，查找弹窗、遮罩和错误目标；不要改用 DOM 注入点击。

## 高级能力

调用样式、断点或实时编辑能力前，读取其最新上游说明：

- 样式：https://playwriter.dev/resources/styles-api.md
- 调试器：https://playwriter.dev/resources/debugger-api.md
- 编辑器：https://playwriter.dev/resources/editor-api.md
