---
name: playwriter-connect
description: 使用 Playwriter MCP 连接用户已经打开的 Chrome，在现有标签页中打开、检查、调试或测试网页。用户明确指定 Playwriter Connect，或全局浏览器规则要求使用它时启用。
---

# Playwriter Connect

通过 Playwriter MCP 控制用户现有的 Chrome、登录状态、Cookie 和扩展。

## 默认行为

- 直接调用 Playwriter，不先询问用户是否已经打开浏览器或页面。
- 复用当前已连接标签页。需要访问指定 URL 时，在该标签页执行 `goto()`；不要主动创建新窗口或新标签页。
- 只有收到“extension is not connected”或“no browser tabs have Playwriter enabled”等实际连接错误时，才请用户点击扩展图标。
- 不调用 `browser.close()` 或 `context.close()`，也不关闭用户已有页面。
- 测试文件或测试用例已给出时，直接逐条执行并汇总结果。

## 执行流程

1. 从 `context.pages()` 中选择与目标 URL 最匹配的现有页面；没有明确 URL 时使用 MCP 提供的 `page`。保存为 `state.page`，后续统一使用。
2. 先输出当前 URL，并用 `snapshot({ page: state.page })` 获取结构化页面状态。只有视觉、布局或空间位置重要时才截图。
3. 每次只执行一个关键交互。优先使用快照返回的 locator、`getByRole()` 或稳定 CSS 选择器；使用 Playwright 的 `click()`、`fill()` 等正常交互。
4. 操作后再次检查 URL、页面快照和 `getLatestLogs({ page: state.page, sinceLastCall: true })`，确认结果后继续。
5. 使用条件等待，例如 `waitForSelector()`、`waitForURL()`、`waitForLoadState()` 或 `waitForPageLoad()`；避免无依据的固定等待。

初始化示例：

```javascript
state.page = context.pages().find((candidate) => candidate.url().includes('目标主机')) ?? page
console.log('URL:', state.page.url())
console.log('日志:', await getLatestLogs({ page: state.page, sinceLastCall: true }))
await snapshot({ page: state.page }).then(console.log)
```

## 交互原则

- 不要用 `page.evaluate(() => element.click())`、`dispatchEvent()` 或 `{ force: true }` 绕过真实交互。点击超时时先用新快照查找遮罩、弹窗或错误元素。
- 输入前先点击目标输入框，再调用 `fill()` 或键盘 API，随后读取输入值或页面状态验证。
- 快照中的 locator 可能随页面更新失效；页面变化后重新获取快照。
- `page.evaluate()` 用于读取运行时变量、localStorage 或执行必要的页面内状态操作，不用于替代常规元素定位和交互。
- 网络问题优先检查真实请求与响应；控制台问题使用 `getLatestLogs()`，不要临时挂载重复监听器。

## 连接恢复

只在连接中断、页面已关闭、上下文没有页面或 MCP 无响应时调用 `reset`。重置会清空 `state`；重置后重新选择现有页面并继续，不要创建新页面。

## 按需读取

- 执行边界和页面选择：[references/RULES.md](references/RULES.md)
- 当前常用 API：[references/API.md](references/API.md)
- 超时与上下文优化：[references/OPTIMIZATION.md](references/OPTIMIZATION.md)
- 仅在连接或执行异常时读取：[references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)

上游文档：https://github.com/remorses/playwriter/blob/main/MCP.md
