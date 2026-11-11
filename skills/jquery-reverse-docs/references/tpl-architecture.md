# 架构文档模板（tpl-architecture）—— jQuery 版

## 输出格式

```markdown
# [项目名] 系统架构文档

> 生成时间：2026-03-05 09:16:18 | 来源：AI 逆向分析 | 技术栈：jQuery

## 1. 技术栈

| 层次 | 技术 | 版本 | 引入方式 | 说明 |
|------|------|------|---------|------|
| 核心库 | jQuery | 3.x / 1.x | CDN / 本地 | |
| UI 框架 | Bootstrap / layui / easyui | x.x | CDN / 本地 | |
| 图表 | ECharts / Highcharts | x.x | CDN | |
| 表格插件 | DataTables / bootstrap-table | x.x | CDN | |
| 表单验证 | jQuery Validate | x.x | CDN | |
| 弹窗 | layer / bootbox | x.x | CDN | |
| 日期 | laydate / datepicker | x.x | CDN | |
| HTTP 请求 | $.ajax / $.get / $.post | — | jQuery 内置 | |
| 构建工具 | Gulp / Grunt / Webpack / 无 | x.x | — | |

## 2. 目录结构职责

\`\`\`
项目根目录/
├── index.html              # 入口页面 / 首页
├── pages/                  # 各功能页面 HTML
│   ├── user/               # 用户管理相关页面
│   ├── order/              # 订单管理相关页面
│   └── ...
├── js/                     # JavaScript 文件
│   ├── common.js           # 公共工具函数、全局初始化
│   ├── config.js           # 全局配置（接口 baseURL、常量等）
│   ├── pages/              # 各页面对应的业务 JS
│   │   ├── user-list.js
│   │   └── ...
│   └── lib/                # 第三方插件（本地引用）
├── css/                    # 样式文件
│   ├── common.css          # 公共样式
│   └── pages/              # 各页面样式
├── images/                 # 图片资源
└── vendor/                 # 第三方库（CDN 降级备份）
\`\`\`

## 3. 页面-脚本对应关系

| HTML 页面 | 对应 JS 文件 | 功能说明 |
|----------|------------|---------|
| pages/user/list.html | js/pages/user-list.js | 用户列表 |
| pages/order/list.html | js/pages/order-list.js | 订单列表 |
| ... | ... | ... |

**公共脚本（所有页面均引入）：**
- `js/common.js`：工具函数、全局初始化、请求拦截封装
- `js/config.js`：接口 baseURL、全局常量配置

## 4. 系统分层架构

\`\`\`mermaid
graph TB
  subgraph 视图层
    H[HTML 页面]
    T[HTML 模板字符串]
  end
  subgraph 业务层
    P[页面 JS 文件]
    C[common.js 公共逻辑]
  end
  subgraph 数据层
    A[$.ajax 请求封装]
    I[请求/响应拦截]
  end
  subgraph 工具层
    U[工具函数]
    CO[config.js 配置]
  end
  subgraph 后端
    API[后端 API]
  end
  H --> P
  P --> C
  P --> A
  C --> A
  A --> I
  I --> API
  API --> I
  I --> P
  P --> T
  T --> H
  P --> U
  A --> CO
\`\`\`

## 5. 页面路由结构

> ⚠️ jQuery 项目通常没有前端路由，页面跳转通过 `window.location.href` 或 `<a>` 标签实现。

| 页面路径 | HTML 文件 | 需要登录 | 说明 |
|---------|---------|---------|------|
| /index.html | index.html | 否 | 首页/仪表盘 |
| /pages/login.html | pages/login.html | 否 | 登录页 |
| /pages/user/list.html | pages/user/list.html | 是 | 用户管理 |

**登录鉴权方式：**
- [ ] Cookie（服务端 Session）
- [ ] localStorage 存储 token，页面加载时检查
- [ ] 后端直接拦截（前端无鉴权逻辑）
- [ ] 其他：___

## 6. 全局变量 / 命名空间

> jQuery 项目常用全局变量污染，记录所有关键全局对象：

| 变量名 | 类型 | 定义位置 | 用途 |
|--------|------|---------|------|
| `window.BASE_URL` | string | config.js | API 接口根地址 |
| `window.MyApp` | object | common.js | 全局命名空间对象 |
| `window.currentUser` | object | common.js | 当前登录用户信息 |
| `window.TOKEN_KEY` | string | config.js | localStorage 中 token 的 key 名 |

## 7. AJAX 请求封装

> 说明项目如何封装 $.ajax（是否有统一的请求函数，如何处理 token、错误）：

\`\`\`javascript
// 典型封装示例（从代码中提取实际实现）
function request(options) {
  return $.ajax({
    url: BASE_URL + options.url,
    type: options.type || 'GET',
    data: options.data || {},
    dataType: 'json',
    beforeSend: function(xhr) {
      // 附加 token
      var token = localStorage.getItem('TOKEN');
      if (token) {
        xhr.setRequestHeader('Authorization', 'Bearer ' + token);
      }
    },
    success: function(res) {
      if (res.code === 401) {
        // 未登录，跳转登录页
        window.location.href = '/pages/login.html';
        return;
      }
      if (res.code !== 200) {
        layer.msg(res.message || '操作失败', { icon: 2 });
        return;
      }
      options.success && options.success(res);
    },
    error: function(xhr, status, error) {
      layer.msg('网络请求失败，请重试', { icon: 2 });
      options.error && options.error(xhr, status, error);
    }
  });
}
\`\`\`

**请求拦截逻辑：**
- Token 附加方式：Header / Cookie / Query Param
- 401 处理：___
- 500/网络错误处理：___

## 8. 事件通信机制

> jQuery 项目的"组件通信"通常通过以下方式实现：

| 通信方式 | 使用场景 | 示例 |
|---------|---------|------|
| 自定义事件 `$.trigger` | 跨模块通知 | `$(document).trigger('userLogout')` |
| 全局变量共享 | 页面内模块间 | `window.selectedRows = []` |
| localStorage | 跨页面传值 | `localStorage.setItem('editId', id)` |
| URL 参数 | 页面跳转传参 | `?id=xxx&type=edit` |
| iframe postMessage | 嵌套页面通信 | — |

## 9. 关键设计决策

- 为什么选择 jQuery 而非现代框架（历史原因 / 团队技术栈 / ...）
- 是否存在服务端渲染（JSP / Thymeleaf / PHP / 纯静态）
- 是否有微前端拆分（iframe 嵌套 / 独立子系统）
- 权限控制方案（前端菜单隐藏 / 后端接口鉴权 / 按钮级别控制）
- 是否有模块化方案（RequireJS / AMD / 无模块化）

## 10. 外部依赖

| 依赖 | 版本 | 引入方式 | 用途 | 文档链接 |
|------|------|---------|------|---------|
| jQuery | 3.6.0 | CDN | DOM 操作、AJAX | https://jquery.com |
| Bootstrap | 4.6.0 | CDN | UI 组件、栅格 | https://getbootstrap.com |
| layer | 3.5.1 | 本地 | 弹窗、消息提示 | https://layui.dev |
| DataTables | 1.13.x | CDN | 表格增强 | https://datatables.net |
```
