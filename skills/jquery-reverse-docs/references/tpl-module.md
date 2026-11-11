# JS 模块文档模板（tpl-module）—— jQuery 版

> 适用于全局工具文件、命名空间对象、公共函数库的文档生成

```markdown
# [模块名称] 模块文档

> 源文件：`js/common.js` / `js/utils.js` / `js/xxx.js`
> 模块类型：全局工具库 / 命名空间对象 / 页面公共逻辑
> 生成时间：2026-03-05 09:16:18

---

## 模块概述

说明本 JS 文件的职责范围，被哪些页面引入，提供哪些能力。

**引入方式：**
\`\`\`html
<!-- 通常在所有页面的 </body> 前引入 -->
<script src="/js/config.js"></script>
<script src="/js/common.js"></script>
<script src="/js/utils.js"></script>
```

---

## 全局配置（config.js 类型）

\`\`\`javascript
// 全局变量/常量说明
var BASE_URL = 'https://api.example.com';   // 接口根地址
var TOKEN_KEY = 'access_token';              // localStorage 中 token 的键名
var PAGE_SIZE = 20;                          // 默认分页大小
var UPLOAD_MAX_SIZE = 5 * 1024 * 1024;      // 文件上传最大限制（5MB）

// 枚举常量
var STATUS = {
  NORMAL: 1,    // 正常
  DISABLED: 2   // 禁用
};

var USER_ROLE = {
  ADMIN: 'admin',
  OPERATOR: 'operator',
  VIEWER: 'viewer'
};
\`\`\`

| 变量名 | 类型 | 值 | 说明 |
|--------|------|-----|------|
| BASE_URL | string | `https://api.example.com` | 接口根地址，生产/开发环境不同 |
| TOKEN_KEY | string | `access_token` | localStorage 存储 token 的 key |
| PAGE_SIZE | number | 20 | 全局默认分页大小 |

---

## 命名空间对象（MyApp 类型）

\`\`\`javascript
// 全局命名空间，避免变量污染
window.MyApp = window.MyApp || {};

// 子模块
MyApp.utils = {};
MyApp.api = {};
MyApp.config = {
  baseUrl: BASE_URL,
  timeout: 10000
};
\`\`\`

---

## 公共函数清单

### 请求封装 `MyApp.request(options)`

\`\`\`javascript
/**
 * 统一 AJAX 请求封装
 * @param {Object} options
 * @param {string} options.url - 接口路径（不含 baseURL）
 * @param {string} [options.type='GET'] - 请求方法
 * @param {Object} [options.data={}] - 请求参数
 * @param {Function} [options.success] - 成功回调 function(res)
 * @param {Function} [options.error] - 失败回调 function(xhr, status, error)
 * @param {boolean} [options.json=false] - 是否以 JSON 格式发送 body
 */
MyApp.request = function(options) { ... };
\`\`\`

**调用示例：**
\`\`\`javascript
MyApp.request({
  url: '/api/user/list',
  type: 'GET',
  data: { page: 1, pageSize: 20 },
  success: function(res) {
    console.log(res.data);
  }
});
\`\`\`

---

### 工具函数清单

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `getUrlParam(name)` | name: string | string/null | 从当前 URL 读取指定参数 |
| `formatDate(date, fmt)` | date: Date/string, fmt: string | string | 格式化日期，fmt 如 `YYYY-MM-DD` |
| `escapeHtml(str)` | str: string | string | HTML 特殊字符转义，防 XSS |
| `isLogin()` | — | boolean | 检查 localStorage 中是否有 token |
| `getToken()` | — | string/null | 读取 token |
| `setToken(token)` | token: string | void | 存储 token 到 localStorage |
| `clearToken()` | — | void | 清除 token，用于退出登录 |
| `getCurrentUser()` | — | Object/null | 读取当前用户信息（从 localStorage） |
| `showLoading(msg)` | msg: string | void | 显示全局 loading（基于 layer） |
| `hideLoading()` | — | void | 关闭全局 loading |

---

### 具体函数实现

#### `getUrlParam(name)`

\`\`\`javascript
/**
 * 从当前页面 URL 获取 query 参数
 * 示例：URL 为 /page.html?id=123&type=edit
 * getUrlParam('id') → '123'
 * getUrlParam('type') → 'edit'
 * getUrlParam('xxx') → null
 */
MyApp.utils.getUrlParam = function(name) {
  var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)');
  var r = window.location.search.substr(1).match(reg);
  if (r != null) return decodeURIComponent(r[2]);
  return null;
};
\`\`\`

---

#### `escapeHtml(str)`

\`\`\`javascript
/**
 * 转义 HTML 特殊字符，防止 XSS
 * 在 renderTable 中使用：escapeHtml(item.name)
 */
MyApp.utils.escapeHtml = function(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
};
\`\`\`

---

## 全局初始化逻辑

\`\`\`javascript
// common.js 中的全局初始化（不在 ready 中，立即执行）

// 登录鉴权检查（每个需要登录的页面引入 common.js 即自动鉴权）
(function checkAuth() {
  var noAuthPages = ['/pages/login.html', '/pages/register.html'];
  var currentPath = window.location.pathname;
  var isNoAuthPage = noAuthPages.some(function(p) { return currentPath.endsWith(p); });

  if (!isNoAuthPage && !MyApp.utils.isLogin()) {
    window.location.href = '/pages/login.html?redirect=' + encodeURIComponent(location.href);
  }
})();

// 全局 AJAX 错误处理
$(document).ajaxError(function(event, xhr, settings, error) {
  if (xhr.status === 401) {
    MyApp.utils.clearToken();
    window.location.href = '/pages/login.html';
  }
});
\`\`\`

---

## 第三方插件封装

### layer 封装

\`\`\`javascript
// 对 layer.js 的封装，统一消息提示风格
MyApp.msg = {
  success: function(msg) { layer.msg(msg, { icon: 1, time: 2000 }); },
  error: function(msg) { layer.msg(msg, { icon: 2, time: 3000 }); },
  warn: function(msg) { layer.msg(msg, { icon: 3, time: 2000 }); },
  confirm: function(msg, callback) {
    layer.confirm(msg, { btn: ['确认', '取消'] }, function(index) {
      layer.close(index);
      callback && callback();
    });
  }
};
\`\`\`

---

## 注意事项

- 本文件必须在 jQuery 加载后引入
- 如使用 layer，必须在 layer.js 之后引入
- 函数挂载在 `window.MyApp` 命名空间，避免全局变量污染
- `checkAuth` 会立即执行，无需等待 DOM ready
```
