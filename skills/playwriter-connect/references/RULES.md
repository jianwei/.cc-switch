# Playwriter Connect 执行规则

## 页面边界

- 默认用户已经打开 Chrome 和目标页面，直接调用 MCP。
- 从 `context.pages()` 复用现有标签页；需要访问 URL 时在选定页面执行 `goto()`。
- 不主动调用 `context.newPage()`、`browser.newContext()`、`window.open()` 或浏览器启动 API。
- 页面自身触发 OAuth、支付或业务弹窗时，可以接管新出现的页面，但不要把这种情况当作主动创建标签页的许可。
- 不调用 `browser.close()`、`context.close()`，不关闭用户已有标签页。

## 状态一致性

- 任务开始时把选定页面保存为 `state.page`，后续统一使用。
- `reset` 会清空 `state`；重置后重新从已有页面初始化 `state.page`。
- 页面导航或显著更新后重新获取快照，不复用旧快照中的临时定位信息。

## 交互与验证

- 使用 Playwright locator、`getByRole()`、`click()`、`fill()` 等真实交互 API。
- 不用 DOM `element.click()`、`dispatchEvent()` 或 `{ force: true }` 绕过遮罩与可交互性检查。
- 每个关键动作遵循“观察 → 操作 → 再观察”：检查 URL、快照及新增页面日志。
- 调用日志 helper 时始终传入页面：`getLatestLogs({ page: state.page, sinceLastCall: true })`。
- 只清理本任务注册的监听器；不要调用无范围的 `removeAllListeners()`。

## 用户授权

- 浏览、读取和调试按用户请求直接执行。
- 提交表单、发布、付款、删除、发送消息等有外部副作用的操作，沿用当前会话已有授权；没有授权时在最终动作前确认。
