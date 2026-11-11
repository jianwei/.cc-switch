# 技术债务报告模板（tpl-tech-debt）—— jQuery 版

```markdown
# 技术债务报告

> 扫描时间：2026-03-05 09:16:18 | 项目：[项目名]

## 总体评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 代码质量 | x/10 | |
| 可维护性 | x/10 | |
| 安全风险 | x/10 | |
| 性能风险 | x/10 | |
| 重构紧迫度 | 高/中/低 | |

---

## 🔴 高优先级问题（影响安全/功能）

### 问题1：XSS 安全漏洞 — HTML 字符串拼接未转义

> **位置：** `js/pages/user-list.js` → `renderTable()` 函数
> **影响：** 恶意用户可通过 `name` 字段注入 `<script>` 代码
> **示例：**
> ```javascript
> // 危险写法
> html += '<td>' + item.name + '</td>';
>
> // 安全写法
> html += '<td>' + escapeHtml(item.name) + '</td>';
> ```
> **建议：** 在 `common.js` 添加 `escapeHtml` 函数，所有 `item.xxx` 拼接前调用

---

### 问题2：全局变量污染 — 大量 var 声明在全局作用域

> **位置：** 多个页面 JS 文件
> **影响：** 变量命名冲突风险，多页面共享 iframe 时易出错
> **示例：**
> ```javascript
> // 危险：var currentPage 在全局作用域
> var currentPage = 1;
>
> // 建议：包裹在 IIFE 中
> (function($) {
>   var currentPage = 1;
>   // ...
> })(jQuery);
> ```
> **建议：** 用 IIFE 包裹所有页面 JS，或迁移到模块化方案（RequireJS）

---

### 问题3：防重复提交机制不完整

> **位置：** `js/pages/order-list.js` → 提交按钮缺少 isLoading 判断
> **影响：** 快速点击可能导致重复提交
> **建议：** 统一封装 `MyApp.submitButton(btn, fn)` 工具函数

---

## 🟡 中优先级问题（影响可维护性）

### 问题4：jQuery 版本过旧（1.x）

> **位置：** 全局
> **影响：** 1.x 已停止维护，存在已知安全漏洞；`$.parseJSON` 等 API 已废弃
> **建议：** 升级到 jQuery 3.x（注意兼容性：`$.fn.size()` 移除，IE 8 不支持等）

---

### 问题5：$.ajax 错误处理不统一

> **位置：** 多个 JS 文件中有各自的 error 回调，部分接口无错误处理
> **影响：** 网络错误时用户无任何提示
> **建议：** 使用 `$(document).ajaxError()` 全局处理，或封装 `request()` 统一处理

---

### 问题6：innerHTML 字符串拼接方式效率低

> **位置：** 所有 `renderTable()` 函数
> **影响：** 数据量大时（>500行）页面渲染卡顿
> **建议：**
> - 短期：用数组 `push` + `join('')` 替代字符串 `+=` 拼接
> - 长期：考虑引入 DataTables 或 bootstrap-table 等表格插件

---

### 问题7：分页组件重复实现

> **位置：** 10+ 个页面各自实现分页
> **影响：** 改动分页逻辑需修改多处，维护成本高
> **建议：** 提取公共分页组件到 `js/common.js`，统一调用 `renderPagination(total, currentPage, callback)`

---

### 问题8：登录鉴权逻辑分散

> **位置：** 部分页面引入了 `checkAuth()`，部分未引入
> **影响：** 漏引入的页面无鉴权保护
> **建议：** 在 `common.js` 中自动执行鉴权检查，所有需要登录的页面只需引入 `common.js`

---

## 🟢 低优先级（优化建议）

### 问题9：缺少前端路由，页面刷新丢失状态

> **位置：** 所有列表页
> **影响：** 用户在第3页筛选后刷新，回到第1页空条件
> **建议：** 搜索条件同步写入 URL Query：`history.pushState({}, '', '?page=3&keyword=xxx')`

---

### 问题10：静态资源无版本号，缓存难以控制

> **位置：** HTML 文件中的 script/link 引用
> **影响：** 更新 JS/CSS 后用户可能使用旧缓存
> **建议：** 引入构建工具（Gulp/Webpack）在文件名中添加 hash

---

### 问题11：console.log 未清理

> **位置：** 多处调试代码未删除
> **影响：** 暴露内部数据结构，影响性能
> **建议：** 生产构建时去除，或封装 `MyApp.log()` 在生产环境静默

---

## jQuery 特有检查清单

- [ ] 存在 `$.fn.size()`（jQuery 3.x 中已移除，改用 `.length`）
- [ ] 存在 `$.parseJSON()`（jQuery 3.x 中废弃，改用 `JSON.parse()`）
- [ ] 存在 `$.type()`（改用 `typeof` / `instanceof`）
- [ ] 存在 `$(selector).live()`（jQuery 1.9 移除，改用 `.on()` 委托）
- [ ] 存在 `$(selector).die()`（同上）
- [ ] 动态 DOM 未使用事件委托（`.on('click', selector, fn)` 形式）
- [ ] 存在内联 `onclick="xxx"` 属性（应改为 jQuery 事件绑定）
- [ ] AJAX 请求未设置超时 `timeout` 参数
- [ ] 存在同步 AJAX（`async: false`，会阻塞页面）
- [ ] HTML 字符串拼接未转义（XSS 风险）
- [ ] `$.each` 中大量 DOM 操作（应批量生成 HTML 后一次性插入）
- [ ] 重复的 `$(selector)` 调用（应缓存 `var $el = $(selector)`）
- [ ] 全局变量未用 IIFE 包裹

---

## 重构路线图

\`\`\`
第一阶段（本周，紧急安全修复）：
  - 修复 XSS 漏洞：所有 HTML 拼接添加 escapeHtml
  - 完善错误处理：添加全局 ajaxError 处理

第二阶段（本月，代码质量提升）：
  - 统一请求封装：封装 MyApp.request()
  - 提取公共分页组件
  - 用 IIFE 包裹页面 JS，消除全局变量污染

第三阶段（季度，架构改进）：
  - 升级 jQuery 版本 1.x → 3.x
  - 引入 Gulp/Webpack 构建流程
  - URL 参数同步（搜索条件持久化）
  - 评估是否逐步迁移到 Vue/React（建议从新模块开始）
\`\`\`
```
