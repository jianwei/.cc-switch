# 事件系统文档模板（tpl-events）—— jQuery 版

> 适用于项目中使用 $.trigger / $(document).on 实现的自定义事件体系

```markdown
# 事件系统文档

> 生成时间：2026-03-05 09:16:18

## 概述

本项目通过以下方式实现跨模块/跨页面通信：

| 通信类型 | 实现方式 | 适用场景 |
|---------|---------|---------|
| 同页面模块间 | `$(document).trigger()` 自定义事件 | 表单提交后刷新列表 |
| 跨页面传值 | `localStorage` + 页面 ready 读取 | 从列表页传 ID 到详情页 |
| 父子页面（iframe） | `window.parent.postMessage` | 弹出子窗口回传结果 |
| URL 参数 | `window.location.href = '...?id=xxx'` | 页面跳转携带参数 |

---

## 自定义事件清单

### 全局事件（$(document) 上）

| 事件名 | 触发方 | 监听方 | 触发时机 | 携带数据 |
|--------|--------|--------|---------|---------|
| `userLogout` | common.js 退出登录函数 | 所有页面（header） | 点击退出时 | 无 |
| `tableRefresh` | 增删改操作成功回调 | loadList 监听 | 数据变更后 | `{ page: 1 }` |
| `modalClosed` | 弹窗关闭按钮 | 父页面 | 弹窗关闭时 | `{ action: 'confirm'/'cancel', data: {} }` |

**代码示例：**
\`\`\`javascript
// 触发（在 saveRecord 成功后）
$(document).trigger('tableRefresh', [{ page: 1 }]);

// 监听（在 bindEvents 中）
$(document).on('tableRefresh', function(e, params) {
  loadList(params.page || currentPage);
});
\`\`\`

---

## 事件委托模式（动态元素）

> jQuery 项目最重要的事件模式：对动态渲染的 DOM 元素使用事件委托

\`\`\`javascript
// ✅ 正确：事件委托，对动态渲染的按钮有效
$(document).on('click', '.btn-edit', function() {
  var id = $(this).data('id');
  openEditModal(id);
});

// ❌ 错误：直接绑定，对动态渲染的元素无效
$('.btn-edit').on('click', function() { ... });  // 如果 .btn-edit 是动态生成的，此写法无效
\`\`\`

**项目中使用事件委托的场景：**

| 选择器 | 事件 | 说明 |
|--------|------|------|
| `.btn-edit` | click | 表格行编辑按钮（动态生成） |
| `.btn-delete` | click | 表格行删除按钮（动态生成） |
| `.btn-view` | click | 表格行查看按钮（动态生成） |
| `.row-checkbox` | change | 表格行勾选框（动态生成） |
| `.page-link` | click | 分页按钮（动态生成） |

---

## localStorage 跨页面通信

\`\`\`javascript
// 页面A（列表页）：点击"编辑"跳转前存储数据
$('.btn-edit').on('click', function() {
  var id = $(this).data('id');
  localStorage.setItem('editRecordId', id);
  window.location.href = '/pages/xxx/edit.html';
});

// 页面B（编辑页）：ready 时读取
$(document).ready(function() {
  var editId = localStorage.getItem('editRecordId');
  if (editId) {
    loadDetail(editId);
    localStorage.removeItem('editRecordId'); // 读取后清除，避免脏数据
  }
});
\`\`\`

**项目中 localStorage 存储的数据：**

| Key | 存储内容 | 存储位置 | 读取位置 | 清除时机 |
|-----|---------|---------|---------|---------|
| `access_token` | 登录 token | login.html 登录成功 | common.js 鉴权检查 / 每次请求 | 退出登录时 |
| `current_user` | 用户信息 JSON | login.html 登录成功 | 需要展示用户名的页面 | 退出登录时 |
| `editRecordId` | 待编辑记录ID | list.html 点击编辑 | edit.html ready | 读取后立即清除 |

---

## iframe 父子通信（如有）

\`\`\`javascript
// 子页面（iframe 内）：完成操作后通知父页面
function notifyParent(action, data) {
  window.parent.postMessage({
    action: action,   // 'saved' | 'cancelled'
    data: data
  }, '*');
}

// 父页面：监听子页面消息
window.addEventListener('message', function(e) {
  if (e.data.action === 'saved') {
    // 刷新父页面列表
    loadList(currentPage);
    // 关闭 iframe 弹窗
    layer.closeAll('iframe');
  }
});
\`\`\`

---

## 常见反模式（应避免）

| 反模式 | 问题 | 建议替代方案 |
|--------|------|------------|
| `$(window).on('load', ...)` 滥用 | 等待所有资源加载完才执行，延迟高 | 改用 `$(document).ready()` |
| `$('.dynamic-btn').on('click', ...)` 直接绑定动态元素 | 动态生成的元素无法响应 | 改用事件委托 |
| 全局 `setInterval` 不清除 | 内存泄漏，页面切换后仍在执行 | 在合适时机 `clearInterval` |
| `$(document).on('click', '*', ...)` 过宽委托 | 性能问题，每次点击都冒泡到顶 | 使用更具体的选择器 |
```
