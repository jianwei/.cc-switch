# Playwriter 执行优化

## 减少上下文和超时

- 文本和结构优先使用 `snapshot()`；只有视觉问题才截图。
- 使用 `search` 缩小快照和日志结果，避免输出整页 HTML、全部日志或大型对象。
- 复杂流程拆成多个 `execute` 调用，每次完成一个可验证动作；不要把整套用例塞进一次调用。
- 使用条件等待代替固定等待。动画等没有可靠条件的短暂变化才使用 1–2 秒的短等待。
- 页面更新后重新获取快照；不要反复尝试旧 locator。

## 推荐反馈循环

```javascript
console.log('URL:', state.page.url())
await snapshot({ page: state.page }).then(console.log)
```

执行一个动作：

```javascript
await state.page.getByRole('button', { name: '提交' }).click()
```

验证动作结果：

```javascript
console.log('URL:', state.page.url())
console.log('日志:', await getLatestLogs({ page: state.page, sinceLastCall: true }))
await snapshot({ page: state.page, search: /成功|失败|错误/ }).then(console.log)
```

## 页面与网络调试

- 页面行为异常时先查新增日志、URL 和可见状态。
- 接口问题使用 `page.on('request')`、`page.on('response')` 或 CDP Network，只保留与目标接口相关的数据。
- 保留注册函数引用，并在完成后只移除本任务的监听器。
- 下载、截图、PDF 等产物使用绝对路径。
