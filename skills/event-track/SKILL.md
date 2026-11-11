---
name: event-track
description: 为 Vue/HTML 前端项目添加埋点（数据打点）代码。当用户提供页面 URL、文件路径或打点文档，并说明需要打哪些点时，必须使用此 skill。触发关键词：打点、埋点、数据统计、事件追踪、eventTrack、添加统计、m="..."、window.eventTrack。即使用户只说"帮我加一下打点"也要触发此 skill。
---

# Event Track Skill — 前端埋点规范

## 概述

本 skill 用于在 Vue/HTML 前端项目中，按照统一规范添加埋点代码。

### 参数收集（逐步引导）

每次触发此 skill 时，**必须**使用 `AskQuestion` 工具逐步收集信息。每一步等用户回答后再进入下一步。如果用户在初始指令中已明确提供某项信息，则跳过对应步骤。

**第 1 步**：使用 `AskQuestion` 询问平台类型
```json
{
  "questions": [{
    "id": "platform",
    "prompt": "选择平台类型",
    "options": [
      { "id": "pc", "label": "PC" },
      { "id": "m", "label": "M（M站）- 默认" }
    ]
  }]
}
```

**第 2 步**：使用 `AskQuestion` 询问目标文件
```json
{
  "questions": [{
    "id": "target",
    "prompt": "请提供需要打点的文件路径或文件夹路径（支持单个文件或整个文件夹）",
    "options": [
      { "id": "file", "label": "单个文件" },
      { "id": "folder", "label": "文件夹" }
    ]
  }]
}
```
用户选择后，再让用户提供具体路径。

**第 3 步**：使用 `AskQuestion` 询问打点类型
```json
{
  "questions": [{
    "id": "track_type",
    "prompt": "选择打点类型（可多选）",
    "allow_multiple": true,
    "options": [
      { "id": "page", "label": "页面点（页面曝光/展示）" },
      { "id": "event", "label": "事件点（用户交互/操作）" }
    ]
  }]
}
```

根据第 3 步的选择，进入不同分支：
- 选择了**页面点** → 进入第 4 步
- 选择了**事件点** → 跳过第 4 步，直接进入第 5 步
- 同时选择了**页面点 + 事件点** → 先第 4 步，再第 5 步

**第 4 步**（仅页面点）：询问 pageName
> 请提供 pageName，或提供前缀（如 `无线:度假:南京`）由我自动拼接 `{前缀}:{页面title}:{平台标识}`

**第 5 步**（仅事件点）：使用 `AskQuestion` 询问事件点范围
```json
{
  "questions": [{
    "id": "event_scope",
    "prompt": "选择事件点的打点范围",
    "options": [
      { "id": "manual", "label": "提供打点清单（手动指定点位）" },
      { "id": "all_actions", "label": "给页面所有操作都加上打点" }
    ]
  }]
}
```

- 选择**提供打点清单** → 让用户提供具体点位名称和触发时机，然后进入确认摘要
- 选择**给页面所有操作都加上打点** → 自动分析页面中所有可交互元素（按钮、链接、表单提交等），为每个元素生成打点，然后进入第 5.1 步

**第 5.1 步**（仅当第 5 步选择 `all_actions` 时）：使用 `AskQuestion` 询问是否包含接口请求
```json
{
  "questions": [{
    "id": "include_api",
    "prompt": "是否也对接口请求事件打点？",
    "options": [
      { "id": "yes", "label": "是，接口请求也打点" },
      { "id": "no", "label": "否，仅打用户操作" }
    ]
  }]
}
```

- 选择**是** → 额外扫描页面中的接口调用，在请求成功/失败回调中添加打点
- 选择**否** → 仅对用户操作打点，不处理接口请求

**收集完成后**，输出确认摘要，然后**必须**使用 `AskQuestion` 等待用户确认，确认前**禁止**执行任何打点操作：
```
确认打点信息：
- 文件：xxx
- 平台：M
- 类型：页面点 + 事件点
- pageName：无线:度假:南京:首页:m
- 事件点位：3 个
```

```json
{
  "questions": [{
    "id": "confirm",
    "prompt": "以上信息是否正确？确认后开始执行",
    "options": [
      { "id": "yes", "label": "确认，开始执行" },
      { "id": "no", "label": "有误，重新填写" }
    ]
  }]
}
```

- 用户选择**确认**后才开始执行打点操作
- 用户选择**有误**则重新从第 1 步开始收集

---

## 页面点

当打点类型为**页面点**时，需要在页面 HTML 中插入一段 `<script>` 标签来声明 pageName。PC 和 M站的变量名大小写不同：

### PC 端页面点

pageName 有两种格式，分别作为 `window.FTA` 的第 2 和第 4 个参数：
- **pageName1**：用 `:` 分隔，如 `无线:度假:南京:首页:m`
- **pageName2**：用 `/` 分隔并以 `/` 开头，如 `/无线/度假/南京/首页/m`

两者内容相同，仅分隔符不同。根据用户提供的 pageName 或自动生成的结果，同时生成这两种格式。

### PC 端页面点

```html
<script type="text/javascript">
    window.FTA && window.FTA("", "pageName1", "", "pageName2");
</script>
```

### M站页面点

```html
<script type="text/javascript">
    window.FTA && window.FTA("", "pageName1", "", "pageName2");
</script>
```

**pageName2 或者 pageName1 生成规则**：
- 如果用户提供了具体的 pageName，直接使用
- 如果用户未提供，自动生成：`{用户提供的前缀}:{页面title}:{平台标识}`，平台标识 PC 为 `pc`，M站为 `m`
- 格式参考：`无线:度假:南京:首页:m`，各层级用 `:` 分隔
- 用户必须提供前缀（如 `无线:度假:南京`），否则需要向用户询问
---

## 事件点（核心规则：HTML vs JS 打点）

### 规则判断逻辑

```
该打点是否包含逻辑判断/动态数据/条件分支？
├── 否 → 使用 HTML 属性打点（m="..."）
└── 是 → 使用 JS 代码打点（window.eventTrack）
```

### ✅ URL 链接打点（a 标签）

所有带有 `href` 属性的 `<a>` 标签，统一使用 HTML `m` 属性打点，无需 JS 代码。

```html
<a href="https://example.com/detail" m="点击_中部____查看详情">查看详情</a>
<a :href="item.url" m="点击_列表____{{item.name}}">{{ item.name }}</a>
```

> 即使 `href` 是动态绑定（`:href`），只要不需要根据条件上报不同点位，仍使用 `m` 属性。

### ✅ HTML 属性打点（无逻辑，静态打点）

适用于：点击某按钮、展示某区域等**无需额外逻辑**的纯静态事件。

**写法**：在对应的 HTML 元素上添加 `m` 属性。

```html
<!-- 格式：m="动作_位置____描述" -->
<button class="pay-btn" @click="handlePay" m="点击_底部____立即支付">立即支付</button>

<span class="cancel-btn"
  @click="showMaskContent = true"
  v-if="renderData.nowOrderStatus == 3"
  m="点击_尾部____取消订单">取消订单</span>
```

**命名规范**：
- 格式：`动作_区域____描述`（区域和描述之间用四个下划线 `____`）
- 动作：`点击` / `展示` / `曝光` / `滑动` 等
- 区域：`顶部` / `中部` / `底部` / `尾部` / `弹窗` 等
- 描述：简短说明该元素的业务含义

### ✅ JS 代码打点（有逻辑，动态打点）

适用于：需要根据**条件判断**、**异步回调**、**动态参数**决定是否触发或传递动态数据的事件。

**写法**：在对应的 JS 方法中调用 `window.eventTrack`。

```javascript
// 格式
window.eventTrack && eventTrack.push({
  text: `xx-xx-xx`,  // 点位名称，支持模板字符串插入动态值
  x: 0,
  y: 0,
});
```

**示例场景**：

```javascript
// 场景1：根据状态决定上报不同点位
handleOrderAction() {
  if (this.orderStatus === 'paid') {
    window.eventTrack && eventTrack.push({
      text: `点击_订单详情____已支付-查看物流`,
      x: 0,
      y: 0,
    });
  } else {
    window.eventTrack && eventTrack.push({
      text: `点击_订单详情____未支付-去支付`,
      x: 0,
      y: 0,
    });
  }
},

// 场景2：异步请求成功后打点
async submitOrder() {
  const res = await api.submitOrder(this.form);
  if (res.code === 0) {
    window.eventTrack && eventTrack.push({
      text: `提交_下单页____下单成功`,
      x: 0,
      y: 0,
    });
  }
},

// 场景3：动态点位名称（带业务数据）
trackProductView(productType) {
  window.eventTrack && eventTrack.push({
    text: `展示_商品页____${productType}-商品详情`,
    x: 0,
    y: 0,
  });
},
```

---

## 执行流程

### Step 1：读取目标文件

- 如果用户提供了**文件路径**，直接读取文件内容
- 如果用户提供了**URL**，说明需要用户提供对应的源码文件
- 理解页面结构：模板区域划分、现有方法逻辑

### Step 2：理解打点清单

仔细阅读用户提供的打点需求，对每一条打点：
- 确认触发时机（点击/展示/提交/回调等）
- 判断是否涉及逻辑（条件/异步/动态数据）
- 确定点位命名

### Step 3：逐一判断打点类型

对每个打点点位，按照核心规则判断：

| 场景 | 类型 | 实现方式 |
|------|------|----------|
| 点击固定按钮，无条件 | 静态 | HTML `m` 属性 |
| 展示某区域，无条件 | 静态 | HTML `m` 属性 |
| 点击后根据状态上报不同点 | 动态 | JS `eventTrack.push` |
| 接口成功/失败回调中打点 | 动态 | JS `eventTrack.push` |
| 需要带动态业务参数 | 动态 | JS `eventTrack.push`（模板字符串） |

### Step 4：修改代码

- **HTML 打点**：在对应标签上追加 `m="..."` 属性，不改动其他属性
- **JS 打点**：在对应方法的正确位置插入 `eventTrack.push(...)` 代码块
- 保持原有代码格式和缩进风格不变

### Step 5：输出结果

输出完整修改后的文件内容，并在末尾列出打点清单说明：

```
## 打点汇总

| 点位名称 | 类型 | 位置 |
|---------|------|------|
| 点击_底部____立即支付 | HTML m属性 | .pay-btn 按钮 |
| 点击_订单详情____已支付-查看物流 | JS eventTrack | handleOrderAction 方法 |
```

---

## 注意事项

1. **不要过度打点**：用户给哪些就打哪些，不要自行添加额外点位
2. **不改动业务逻辑**：只添加打点代码，不修改任何现有功能代码
3. **m 属性位置**：放在元素的最后一个属性位置，保持模板整洁
4. **JS 打点位置**：
   - 点击事件 → 方法开头（除非需要根据结果判断）
   - 接口回调 → 在 `if (res.code === 0)` 判断内
   - 条件分支 → 在对应 `if/else` 分支内
5. **点位命名**：与用户提供的打点文档/需求保持一致，不要自行修改点位名称

---

## 快速参考

```
静态场景（直接写 m 属性）：
  <div m="点击_区域____描述">

动态场景（写到 JS 中）：
  window.eventTrack && eventTrack.push({
    text: `点击_区域____描述`,
    x: 0,
    y: 0,
  });
```