# AJAX 接口文档模板（tpl-api）—— jQuery 版

> ⚠️ 生成原则：
> 1. 从前端 $.ajax 调用代码**反向推理**接口的完整数据结构
> 2. 分析 success 回调中对 res 字段的使用，推断响应结构
> 3. 分析 data 参数，推断请求参数结构
> 4. 每个接口必须提供可直接运行的 **Mock 数据**
> 5. 注意 jQuery 特有的 JSONP、文件上传等特殊接口类型

```markdown
# [模块名称] 接口文档

> 源文件：`js/pages/xxx.js`（及相关 HTML 内嵌脚本）
> 生成时间：2026-03-05 09:16:18
> 接口调用方式：$.ajax / $.get / $.post（jQuery AJAX）

---

## 模块概述

说明本 JS 文件负责哪块业务，包含几个 AJAX 接口，对应哪些 HTML 页面。

| 接口 | 方法 | 路径 | 所在函数/位置 |
|------|------|------|-------------|
| 列表查询 | GET | `/api/xxx/list` | `loadList()` 函数 |
| 新增记录 | POST | `/api/xxx/add` | 表单 submit 回调 |
| 删除记录 | POST | `/api/xxx/delete` | 删除按钮点击事件 |

---

## 接口详情

---

### 接口一：列表查询

**基本信息**

| 项目 | 内容 |
|------|------|
| 调用方式 | `$.ajax` / `$.get` |
| 请求方式 | GET |
| 接口路径 | `/api/xxx/list` |
| 调用位置 | `js/pages/xxx.js` → `loadList()` 函数，页面 ready 时调用 |

**原始调用代码（用于推理）**

\`\`\`javascript
// 前端原始调用
function loadList() {
  var params = {
    page: currentPage,
    pageSize: 20,
    keyword: $('#keyword').val(),
    status: $('#status').val()
  };
  $.ajax({
    url: BASE_URL + '/api/xxx/list',
    type: 'GET',
    data: params,
    success: function(res) {
      if (res.code === 200) {
        renderTable(res.data.list);
        updatePagination(res.data.total);
      }
    }
  });
}

function renderTable(list) {
  var html = '';
  $.each(list, function(i, item) {
    html += '<tr>' +
      '<td>' + item.id + '</td>' +
      '<td>' + item.name + '</td>' +
      '<td>' + (item.status === 1 ? '正常' : '禁用') + '</td>' +
      '<td>' + item.createTime + '</td>' +
      '</tr>';
  });
  $('#tableBody').html(html);
}
\`\`\`

**请求参数（从 data 参数推理）**

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|-------|------|
| page | number | ✅ | 1 | 页码 |
| pageSize | number | ✅ | 20 | 每页条数 |
| keyword | string | ❌ | — | 名称关键词，`$('#keyword').val()` |
| status | string/number | ❌ | — | 状态，`$('#status').val()` |

**响应字段推理（从 success 回调分析）**

| 字段路径 | 类型 | 推理来源 | 说明 |
|---------|------|---------|------|
| code | number | `res.code === 200` | 业务状态码 |
| data.list | array | `renderTable(res.data.list)` | 列表数据 |
| data.list[].id | string/number | `item.id` | 记录ID |
| data.list[].name | string | `item.name` | 名称 |
| data.list[].status | number | `item.status === 1 ? '正常' : '禁用'` | 1=正常 2=禁用 |
| data.list[].createTime | string | `item.createTime` | 创建时间 |
| data.total | number | `updatePagination(res.data.total)` | 总条数 |

**Mock 数据**

\`\`\`json
{
  "code": 200,
  "message": "success",
  "data": {
    "list": [
      {
        "id": 1,
        "name": "测试记录一",
        "status": 1,
        "createTime": "2026-03-05 09:16:18"
      },
      {
        "id": 2,
        "name": "测试记录二",
        "status": 2,
        "createTime": "2026-03-04 14:30:00"
      }
    ],
    "total": 58
  }
}
\`\`\`

**Mock 空数据**
\`\`\`json
{
  "code": 200,
  "data": { "list": [], "total": 0 }
}
\`\`\`

**错误响应**
\`\`\`json
{ "code": 401, "message": "请先登录" }
{ "code": 500, "message": "服务器内部错误" }
\`\`\`

---

### 接口二：新增记录

**基本信息**

| 项目 | 内容 |
|------|------|
| 调用方式 | `$.ajax` |
| 请求方式 | POST |
| 接口路径 | `/api/xxx/add` |
| Content-Type | `application/x-www-form-urlencoded`（jQuery 默认）/ `application/json` |
| 调用位置 | `js/pages/xxx.js` → 表单 submit 事件回调 |

**原始调用代码**

\`\`\`javascript
$('#addForm').on('submit', function(e) {
  e.preventDefault();
  var formData = {
    name: $('#addName').val(),
    status: $('#addStatus').val(),
    remark: $('#addRemark').val()
  };
  $.ajax({
    url: BASE_URL + '/api/xxx/add',
    type: 'POST',
    data: JSON.stringify(formData),
    contentType: 'application/json',
    success: function(res) {
      if (res.code === 200) {
        layer.msg('新增成功', { icon: 1 });
        $('#addModal').modal('hide');
        loadList();
      } else {
        layer.msg(res.message, { icon: 2 });
      }
    }
  });
});
\`\`\`

**请求参数**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | ✅ | 名称，`$('#addName').val()` |
| status | string | ✅ | 状态，`$('#addStatus').val()` |
| remark | string | ❌ | 备注，`$('#addRemark').val()` |

**响应字段推理**

| 字段路径 | 类型 | 推理来源 | 说明 |
|---------|------|---------|------|
| code | number | `res.code === 200` | 业务状态码 |
| message | string | `layer.msg(res.message)` | 提示信息（失败时展示） |

**Mock 数据**
\`\`\`json
{ "code": 200, "message": "新增成功", "data": null }
\`\`\`

**错误响应**
\`\`\`json
{ "code": 400, "message": "名称不能为空" }
{ "code": 409, "message": "名称已存在" }
\`\`\`

---

### 接口三：删除记录

**基本信息**

| 项目 | 内容 |
|------|------|
| 请求方式 | POST（jQuery 项目常用 POST 替代 DELETE） |
| 接口路径 | `/api/xxx/delete` |
| 调用位置 | 删除按钮 click 事件 |

**原始调用代码**

\`\`\`javascript
$(document).on('click', '.btn-delete', function() {
  var id = $(this).data('id');
  layer.confirm('确认删除该记录吗？', function(index) {
    $.post(BASE_URL + '/api/xxx/delete', { id: id }, function(res) {
      layer.close(index);
      if (res.code === 200) {
        layer.msg('删除成功', { icon: 1 });
        loadList();
      } else {
        layer.msg(res.message, { icon: 2 });
      }
    });
  });
});
\`\`\`

**请求参数**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | number/string | ✅ | 记录ID，来自 `$(this).data('id')` |

**Mock 数据**
\`\`\`json
{ "code": 200, "message": "删除成功", "data": null }
\`\`\`

---

## 统一响应结构规范

> 根据代码中对 `res.code` 的判断，推理出的统一响应格式：

\`\`\`json
{
  "code": 200,       // number，200=成功
  "message": "xxx",  // string，提示信息
  "data": {}         // any，业务数据，失败时为 null
}
\`\`\`

**错误码汇总（从代码中推理）**

| code | 前端处理逻辑 | 推理来源 |
|------|------------|---------|
| 200 | 正常处理 | `if(res.code===200)` |
| 401 | 跳转登录页 | `window.location.href='/login.html'` |
| 400 | toast 显示 message | `layer.msg(res.message)` |
| 500 | toast 提示错误 | error 回调处理 |

---

## 文件上传接口（如有）

\`\`\`javascript
// jQuery 文件上传特殊写法
var formData = new FormData();
formData.append('file', $('#uploadFile')[0].files[0]);
formData.append('type', 'avatar');

$.ajax({
  url: BASE_URL + '/api/upload',
  type: 'POST',
  data: formData,
  processData: false,   // ⚠️ 必须 false
  contentType: false,   // ⚠️ 必须 false
  success: function(res) {
    if (res.code === 200) {
      $('#avatar').attr('src', res.data.url);
    }
  }
});
\`\`\`

| 字段 | 类型 | 说明 |
|------|------|------|
| file | File | 上传文件，`FormData` 方式 |
| type | string | 文件类型标识 |

响应：`{ "code": 200, "data": { "url": "https://xxx/avatar.jpg" } }`

---

## Mock 方案说明

### 方案一：本地 json-server（推荐）

\`\`\`bash
npm install -g json-server
json-server --watch mock/db.json --port 3001
\`\`\`

\`\`\`json
// mock/db.json
{
  "xxx": [
    { "id": 1, "name": "测试记录一", "status": 1, "createTime": "2026-03-05 09:16:18" }
  ]
}
\`\`\`

### 方案二：Mock.js 拦截（开发阶段）

\`\`\`javascript
// 在 js/mock.js 中配置，仅开发环境引入
Mock.mock(/\/api\/xxx\/list/, 'get', function(options) {
  return {
    code: 200,
    data: {
      list: Mock.mock({ 'array|10': [{ 'id|+1': 1, 'name': '@cname', 'status|1-2': 1 }] }).array,
      total: 58
    }
  };
});
\`\`\`

### 方案三：修改 BASE_URL 指向 Mock 服务

\`\`\`javascript
// js/config.js
var BASE_URL = location.hostname === 'localhost'
  ? 'http://localhost:3001'   // 开发环境：指向 json-server
  : 'https://api.example.com'; // 生产环境
\`\`\`
```
