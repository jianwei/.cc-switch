# Playwriter 连接与执行排查

仅在出现实际异常时读取。

## 扩展未连接

出现“extension is not connected”或“no browser tabs have Playwriter enabled”时，请用户在目标标签页点击 Playwriter 扩展图标使其变绿，然后重试。不要在尚未报错时提前询问。

## 连接或页面对象失效

页面关闭、上下文没有页面、断言失败或 MCP 无响应时调用 `reset`。重置后 `state` 为空，重新选择已有标签页：

```javascript
state.page = context.pages().find((candidate) => candidate.url().includes('目标主机')) ?? page
console.log('恢复页面:', state.page.url())
```

如果所有页面长期显示 `about:blank` 且无法执行脚本，再请用户重启 Chrome。

## 操作超时

1. 重新获取 `snapshot()`，确认 locator 仍然有效。
2. 检查是否有对话框、遮罩层、Cookie 提示或导航。
3. 查询 `getLatestLogs({ page: state.page, sinceLastCall: true })`。
4. 根据真实页面状态修正目标或等待条件；不要用 `{ force: true }` 或 DOM 注入点击绕过问题。

## 页面内容未加载

`goto()` 完成不代表 SPA 数据已经渲染。等待明确元素或使用：

```javascript
await waitForPageLoad({ page: state.page, timeout: 5000 })
```

不要把 `networkidle` 当作所有页面的默认完成条件；持续轮询、WebSocket 或分析脚本可能使其永远不满足。

## Relay 日志

Playwriter 内部错误可查看 `~/.playwriter/relay-server.log`。只提取与当前时间和错误相关的行，避免输出整份日志。

上游 MCP 配置与环境变量：https://github.com/remorses/playwriter/blob/main/MCP.md
