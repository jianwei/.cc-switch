# 扫描与文档生成流程

## Step 1：扫描项目结构

```bash
# 扫描 HTML 页面
find . -name "*.html" -not -path "*/node_modules/*" | sort

# 扫描业务 JS 文件
find . -name "*.js" -not -path "*/node_modules/*" -not -path "*/vendor/*" -not -path "*/lib/*" | sort

# 查看项目配置
cat package.json 2>/dev/null || echo "无 package.json"

# 扫描所有 AJAX 调用（数据来源线索）
grep -rn "\.ajax\|\.get\|\.post\|fetch(" --include="*.js" . | grep -v "node_modules\|vendor\|lib" | head -80

# 扫描所有 DOM 写入点（渲染落点线索）
grep -rn "\.html(\|\.append(\|\.prepend(\|\.text(\|\.val(\|innerHTML" --include="*.js" . | grep -v "node_modules\|vendor\|lib" | head -80

# 扫描服务端模板标记（Thymeleaf / JSP / PHP）
grep -rn "th:\|<%=\|<?php\|\${" --include="*.html" . 2>/dev/null | head -30

# 查看引入的第三方库（判断是否用了模板引擎/表格插件）
grep -rn "<script" --include="*.html" . | grep "src=" | head -30
```

根据扫描结果，规划需要生成的文档清单（不写入任何文件，仅列出给用户确认）：

| 文档 | 输出路径 | 来源文件 |
|------|---------|---------|
| 架构文档 | `docs/PRD/architecture.md` | package.json, index.html, js/config.js |
| common 模块 | `docs/PRD/modules/common.md` | js/common.js |
| 用户接口 | `docs/PRD/api/user.md` | js/pages/user-list.js |
| 用户列表页 | `docs/PRD/pages/user-list.md` | pages/user/list.html + js |
| 事件系统 | `docs/PRD/events/global-events.md` | js/common.js + 各页面 js |
| 技术债务 | `docs/PRD/tech-debt.md` | 全量扫描 |

---

## Step 2：建立输出目录

```bash
mkdir -p docs/PRD/api docs/PRD/pages docs/PRD/modules docs/PRD/events
```

---

## Step 3：按顺序生成文档

生成顺序：
1. `docs/PRD/architecture.md` — 整体架构
2. `docs/PRD/modules/*.md` — 公共模块（每个文件一篇）
3. `docs/PRD/api/*.md` — AJAX 接口（每个 JS 文件一篇）
4. `docs/PRD/pages/*.md` — 页面功能（每个 HTML 一篇）**← 重点分析数据来源与渲染**
5. `docs/PRD/events/*.md` — 事件系统
6. `docs/PRD/tech-debt.md` — 技术债务报告

每个文档生成时：
- 读取对应源文件
- 按对应模板（`tpl-*.md`）填写内容
- 不允许出现"TODO"或"待补充"占位
- 生成完毕输出：`✅ 已生成：[文件路径]`

### 页面文档的数据来源分析重点

生成 `pages/*.md` 时，必须对每个渲染区域追踪完整的数据链路：

**第一步：识别渲染落点**
找出页面中所有被 JS 动态写入的 DOM 节点：
```bash
# 找 JS 中所有写入 DOM 的位置
grep -n "\.html(\|\.append(\|\.text(\|innerHTML\|DataTable\|layui\.table" js/pages/xxx.js
```

**第二步：追溯每个落点的数据来源**

对每一个渲染落点，向上追踪数据从哪里来，必须明确到以下类型之一：

| 来源类型 | 典型代码特征 | 说明 |
|---------|------------|------|
| AJAX 接口 | `$.ajax success` 回调中取 `res.data.xxx` | 最常见，异步获取 |
| URL 参数 | `location.search` / `getUrlParam('id')` | 页面跳转携带的参数 |
| localStorage | `localStorage.getItem('key')` | 跨页面传值 |
| 表单输入 | `$('#input').val()` | 用户直接输入，回显用 |
| 服务端直出 | `th:text` / `<%=value%>` / `<?php echo` | HTML 加载时已渲染完毕，JS 读取的是已渲染结果 |
| 全局变量 | `window.xxx` / 顶层 `var` | 由其他模块/接口预先写入 |
| 上级页面传入 | `window.opener.xxx` / `postMessage` | iframe 或弹出窗口场景 |

**第三步：识别渲染方式**

| 渲染方式 | 典型代码特征 | 注意点 |
|---------|------------|-------|
| 字符串拼接 | `html += '<tr>' + item.name + '</tr>'` | 注意 XSS 风险，item.name 是否转义 |
| jQuery DOM 操作 | `$('#el').text(val)` / `.attr()` / `.val()` | `.text()` 安全，`.html()` 有 XSS 风险 |
| **art-template** | `template('tpl-id', data)` + `$('#el').html(html)` | 见下方专项说明 |
| 第三方表格插件 | `$('#table').DataTable({data: list})` | 数据由插件接管渲染 |
| layui 表格 | `layui.table.render({data: list})` | layui 自有渲染机制 |
| 服务端模板直出 | `th:each` / `c:forEach` / `@foreach` | 页面加载时已完成，JS 只做增量操作 |

**art-template 识别与分析要点：**

识别特征——在 HTML 或 JS 中出现以下任意一种：
```bash
# 扫描 art-template 使用痕迹
grep -rn "template(" --include="*.js" . | grep -v "node_modules"
grep -rn 'type="text/html"' --include="*.html" .
grep -rn "template-web\|art-template" --include="*.html" .
```

art-template 的完整数据链路：
```
①  HTML 中用 <script type="text/html" id="tpl-xxx"> 定义模板
       内含 {{each list}} / {{if}} / {{value}} 等模板语法

②  JS 中 AJAX 拿到数据后调用：
       var html = template('tpl-xxx', { list: res.data.list })

③  将渲染结果写入 DOM：
       $('#container').html(html)
```

分析时必须同时读取：
- **模板定义**（`<script type="text/html">` 里的结构）→ 说明渲染出的 HTML 结构
- **传入数据对象**（`template('id', data)` 的第二个参数）→ 说明数据字段映射
- **写入目标**（`.html(html)` 的选择器）→ 说明渲染落点

---

## Step 4：生成完毕

```
🎉 文档生成完毕

docs/PRD/
├── architecture.md
├── tech-debt.md
├── api/
├── pages/
├── modules/
└── events/
```

---

## 异常处理

**源文件不存在：** 标注 `⚠️ 源文件不存在：[路径]`，继续生成其余内容。

**上下文即将耗尽：** 末尾标注 `[待续]`，告知用户从哪个文件继续。

**HTML 内嵌大量 JS：** 纳入分析，标注"逻辑内嵌于 xxx.html"。

**服务端模板（JSP/PHP/Thymeleaf）：** 区分"服务端直出区域"和"JS 动态渲染区域"分别描述。
