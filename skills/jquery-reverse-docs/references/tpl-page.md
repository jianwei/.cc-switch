# 页面功能文档模板（tpl-page）—— jQuery 版

> 生成原则：必须追踪每一个渲染区域的数据来源，做到"数据从哪来、经过什么处理、渲染到哪个 DOM 节点"全链路清晰。

```markdown
# [页面中文名称] 页面文档

> **HTML 文件：** `pages/xxx/list.html`
> **JS 文件：** `js/pages/xxx-list.js`
> **需要登录：** 是 / 否

---

## 一、页面概述

**页面定位：** 一句话说清楚这个页面负责什么业务。

**进入方式：** 侧边栏菜单 / 从 xxx 页跳转（携带参数：?id=xxx）/ 直接访问 URL

**离开去向：**

| 触发操作 | 目标页面 | 携带参数 |
|---------|---------|---------|
| 点击列表行"查看" | `pages/xxx/detail.html` | `?id=xxx` |

---

## 二、页面渲染分析

> 这是本文档的核心章节。逐一列出页面中每个动态区域，说明数据从哪来、怎么渲染。

### 渲染区域总览

| 区域 | DOM 节点 | 数据来源类型 | 渲染方式 | 渲染时机 |
|------|---------|------------|---------|---------|
| 主列表表格 | `#tableBody` | AJAX 接口 | 字符串拼接 `.html()` | 页面 ready / 查询 / 翻页 |
| 状态下拉选项 | `#status` | AJAX 接口（字典） | `$.each` append `<option>` | 页面 ready，仅一次 |
| 分页组件 | `#pagination` | AJAX 接口（total 字段） | 字符串拼接 `.html()` | 每次列表加载后 |
| 编辑弹窗表单 | `#addName` `#addStatus` | AJAX 接口（详情） | `$().val()` 回填 | 点击编辑按钮时 |
| 页面标题用户名 | `#username` | localStorage | `.text()` | 页面 ready |

---

### 渲染区域详情

#### 区域①：主列表表格 `#tableBody`

**数据来源：** AJAX 接口 `GET /api/xxx/list`

**数据流向：**
```
用户操作（查询/翻页）
  → loadList(page) 被调用
  → 收集搜索条件：$('#keyword').val() / $('#status').val()
  → $.ajax GET /api/xxx/list?page=1&keyword=xxx
  → success 回调拿到 res.data.list
  → renderTable(res.data.list) 生成 HTML
  → $('#tableBody').html(html) 写入 DOM
```

**渲染方式：字符串拼接**
```javascript
function renderTable(list) {
  var html = '';
  $.each(list, function(i, item) {
    html += '<tr>' +
      '<td>' + item.id + '</td>' +
      '<td>' + item.name + '</td>' +          // ⚠️ 未转义，存在 XSS 风险
      '<td>' + renderStatus(item.status) + '</td>' +
      '<td>' + item.createTime + '</td>' +
    '</tr>';
  });
  $('#tableBody').html(html);
}
```

**用到的接口字段：**

| 字段 | 用途 | 渲染位置 |
|------|------|---------|
| `item.id` | 行唯一标识，存入 `data-id` | `<tr data-id>` / 编辑删除按钮 |
| `item.name` | 显示名称 | 第2列 td |
| `item.status` | 状态枚举，映射为 Badge 文字 | 第3列 td |
| `item.createTime` | 创建时间字符串 | 第4列 td |

**空数据处理：**
```javascript
if (!list || list.length === 0) {
  $('#tableBody').html('<tr><td colspan="5" class="text-center">暂无数据</td></tr>');
}
```

---

#### 区域②：状态下拉 `#status`

**数据来源：** AJAX 接口 `GET /api/dict/status` / 前端硬编码常量

**数据流向：**
```
页面 ready
  → loadStatusDict() 被调用
  → $.get /api/dict/status
  → success 回调拿到 res.data（数组）
  → $.each 遍历，append <option> 到 #status
```

**渲染方式：`$.each` + `append`**
```javascript
function loadStatusDict() {
  $.get(BASE_URL + '/api/dict/status', function(res) {
    if (res.code === 200) {
      $.each(res.data, function(i, item) {
        $('#status').append('<option value="' + item.value + '">' + item.label + '</option>');
      });
    }
  });
}
```

**若为硬编码（无接口）：**
```javascript
// 直接写死，无接口依赖
var statusMap = { 1: '正常', 2: '禁用' };
```
> 说明：此处无接口调用，状态映射由前端维护，后端新增状态值需同步修改前端代码。

---

#### 区域③：编辑弹窗表单回填

**数据来源：** AJAX 接口 `GET /api/xxx/:id`（点击编辑时按需加载）

**数据流向：**
```
点击 .btn-edit 按钮（事件委托）
  → 取 $(this).data('id')
  → $.get /api/xxx/:id
  → success 回调拿到 res.data
  → $('input').val() / $('select').val() 逐字段回填
  → $('#addModal').modal('show') 打开弹窗
```

**渲染方式：`$.val()` 逐字段回填**
```javascript
function openEditModal(id) {
  $.get(BASE_URL + '/api/xxx/' + id, function(res) {
    var d = res.data;
    $('#addName').val(d.name);
    $('#addStatus').val(d.status);
    $('#addRemark').val(d.remark || '');
  });
}
```

**字段映射：**

| 接口字段 | 表单控件 | 控件类型 |
|---------|---------|---------|
| `name` | `#addName` | input text |
| `status` | `#addStatus` | select |
| `remark` | `#addRemark` | textarea |

---

#### 区域④：页面顶部用户名 `#username`

**数据来源：** localStorage（登录时写入，非接口）

**数据流向：**
```
页面 ready
  → localStorage.getItem('current_user')
  → JSON.parse 得到用户对象
  → $('#username').text(user.name)
```

**渲染方式：`.text()` 直接写入（安全）**
```javascript
var user = JSON.parse(localStorage.getItem('current_user') || '{}');
$('#username').text(user.name || '未登录');
```

---

#### 区域⑤：服务端直出区域（如有）

**数据来源：** 服务端模板（Thymeleaf / JSP / PHP）在 HTML 加载时已渲染

**识别方式：** HTML 中包含 `th:text` / `${xxx}` / `<%=xxx%>` / `<?php echo` 等标记

```html
<!-- Thymeleaf 示例：页面标题由服务端直出，JS 无法修改初始值 -->
<h2 th:text="${pageTitle}">默认标题</h2>
```

> ⚠️ 此类区域数据由后端 Controller 注入，前端 JS 拿不到原始数据对象。若 JS 需要读取该值，通常后端会额外输出一个全局 JS 变量：
> ```javascript
> var PAGE_DATA = { userId: 123, userName: '张三' };
> ```

---

#### 区域⑥：art-template 模板渲染（如有）

**识别特征：**
- HTML 中存在 `<script type="text/html" id="tpl-xxx">` 的模板块
- JS 中调用 `template('tpl-xxx', data)` 并将结果写入 DOM

**数据流向：**
```
AJAX 拿到数据
  → 构造数据对象：{ list: res.data.list, total: res.data.total }
  → var html = template('tpl-list', { list: res.data.list })
  → $('#tableBody').html(html)
```

**模板定义（在 HTML 中）：**
```html
<script type="text/html" id="tpl-list">
  {{each list item}}
  <tr>
    <td>{{item.id}}</td>
    <td>{{item.name}}</td>
    <td>{{item.status === 1 ? '正常' : '禁用'}}</td>
    <td>{{item.createTime}}</td>
    <td>
      <a class="btn-edit" data-id="{{item.id}}">编辑</a>
      <a class="btn-delete" data-id="{{item.id}}">删除</a>
    </td>
  </tr>
  {{/each}}
  {{if list.length === 0}}
  <tr><td colspan="5" class="text-center">暂无数据</td></tr>
  {{/if}}
</script>
```

**JS 调用：**
```javascript
$.ajax({
  url: BASE_URL + '/api/xxx/list',
  success: function(res) {
    var html = template('tpl-list', {
      list: res.data.list        // 传入数组，模板内用 {{each list item}} 遍历
    });
    $('#tableBody').html(html);  // 写入渲染落点
  }
});
```

**模板语法说明：**

| 语法 | 含义 | 示例 |
|------|------|------|
| `{{value}}` | 输出变量（HTML 编码，防 XSS） | `{{item.name}}` |
| `{{@ value}}` | 原始输出（不编码，慎用） | `{{@ item.htmlContent}}` |
| `{{each list item}}` | 遍历数组 | `{{each list item}} ... {{/each}}` |
| `{{if}} / {{else}}` | 条件判断 | `{{if item.status === 1}}正常{{/if}}` |
| `<%= value %>` | 原始语法输出（等价 `{{value}}`） | `<%= item.name %>` |
| `<% code %>` | 原始语法执行 JS | `<% for(var i=0;i<list.length;i++){ %>` |

**传入数据对象的字段映射：**

| 传入字段 | 类型 | 模板中用法 | 说明 |
|---------|------|---------|------|
| `list` | array | `{{each list item}}` | 列表数据 |
| `list[].id` | number | `{{item.id}}` | 记录 ID，用于按钮 data-id |
| `list[].name` | string | `{{item.name}}` | 名称，`{{}}` 自动 HTML 编码 |
| `list[].status` | number | `{{item.status === 1 ? '正常' : '禁用'}}` | 状态枚举 |
| `list[].createTime` | string | `{{item.createTime}}` | 创建时间 |

> ✅ art-template 的 `{{value}}` 默认对输出做 HTML 编码，比字符串拼接更安全。
> ⚠️ 使用 `{{@ value}}` 原始输出时不编码，需确认数据可信。

---

## 三、$(document).ready 初始化顺序

| 步骤 | 操作 | 数据来源 | 渲染目标 |
|------|------|---------|---------|
| 1 | 读取 URL 参数恢复搜索条件 | `location.search` | 搜索表单各字段 |
| 2 | 读取 localStorage 显示用户名 | localStorage | `#username` |
| 3 | 加载状态字典 | `GET /api/dict/status` | `#status` 下拉选项 |
| 4 | 加载列表数据（首屏） | `GET /api/xxx/list` | `#tableBody` + 分页 |
| 5 | 绑定事件 | — | — |

> 步骤 3 和 4 并行发起，互不阻塞。

---

## 四、全局变量（页面状态）

| 变量名 | 类型 | 初始值 | 作用 | 修改时机 |
|--------|------|--------|------|---------|
| `currentPage` | number | 1 | 当前页码 | 翻页、查询时重置为 1 |
| `pageSize` | number | 20 | 每页条数 | 分页组件改变时 |
| `totalCount` | number | 0 | 总条数 | 接口返回后 |
| `selectedIds` | array | [] | 已勾选 ID | 勾选/取消时 |
| `isLoading` | boolean | false | 防重复提交 | 请求前/后 |
| `editingId` | null/number | null | 当前编辑的记录 ID | 点击编辑时赋值，弹窗关闭后清空 |

---

## 五、接口汇总

| 用途 | 方法 | 路径 | 触发时机 |
|------|------|------|---------|
| 获取列表 | GET | `/api/xxx/list` | ready / 查询 / 翻页 / 增删改后 |
| 获取状态字典 | GET | `/api/dict/status` | ready，仅一次 |
| 获取详情 | GET | `/api/xxx/:id` | 点击"编辑" |
| 新增 | POST | `/api/xxx/add` | 弹窗提交（editingId 为 null） |
| 编辑 | POST | `/api/xxx/update` | 弹窗提交（editingId 有值） |
| 删除 | POST | `/api/xxx/delete` | 删除确认后 |

---

## 六、注意事项

- **XSS 风险：** `item.name` 等字段通过字符串拼接写入 `.html()`，未调用 `escapeHtml`，存在注入风险
- **事件委托：** 表格行按钮由 `$(document).on()` 绑定，因为 `#tableBody` 是动态生成的
- **服务端直出区域** 与 **JS 动态渲染区域** 需明确区分，前者 JS 改不了初始值
```
