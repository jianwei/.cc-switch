---
name: page-track
description: 在 React 前端项目中按照统一规范添加页面埋点（页面点）与性能打点（首屏可用耗时）。当用户需要为页面添加页面埋点、trackPageView、页面点、性能打点、business_ready_ms、performTrack、startPageView 时使用此 skill。触发关键词：页面埋点、页面点、trackPageView、添加页面统计、性能打点、首屏耗时、performTrack。
---

## 概述

页面埋点（页面点）用于追踪用户访问页面的行为，与事件埋点（事件点）不同，页面点只在页面加载/展示时触发一次。

**pageName 格式规则**：
- pageName1（冒号分隔）：`无线:打包定:{页面标题}:m`
- pageName2（斜杠分隔）：`/无线/打包定/{页面标题}/m`

---

## 核心方法

页面埋点通过 `bridge.trackPageView()` 方法实现，该方法位于 `assets/src/common/bridge.js`：

```javascript
trackPageView: (title) => {
    try {
        console.log('trackPageView:', title);
        if (title) {
            const pageName1 = `无线:打包定:${title}:m`;
            const pageName2 = `/无线/打包定/${title}/m`;
            window.FTA && window.FTA('', pageName1, '', pageName2);
        }
    } catch (error) {
        console.error('trackPageView error:', error);
    }
},
```

---

## 使用模式

### 模式一：静态标题（固定页面标题）

适用于页面标题固定不变的场景：

```javascript
import { bridge } from '@/common/bridge';

const PAGE_TITLE = '信息填写';

const MyPage = () => {
  useEffect(() => {
    document.title = PAGE_TITLE;
    bridge.trackPageView(PAGE_TITLE);
  }, []);

  // ... 组件其余代码
};
```

### 模式二：动态标题（依赖路由参数或状态）

适用于页面标题根据路由参数或接口返回数据动态变化的场景：

```javascript
import { bridge } from '@/common/bridge';

const MyPage = () => {
  const location = useLocation();

  const pageParams = useMemo(() => location.state || {}, [location.state]);

  useEffect(() => {
    const title = pageParams.title || '默认标题';
    document.title = title;
    bridge.trackPageView(title);
  }, [pageParams.title]);

  // ... 组件其余代码
};
```

### 模式三：带条件判断的动态标题

适用于需要根据状态判断设置不同标题的场景：

```javascript
import { bridge } from '@/common/bridge';

const ScenicDetail = () => {
  const scenicDetailInfo = useSelector(state => state.scenicDetailInfo);

  useEffect(() => {
    if (scenicDetailInfo?.scenicName) {
      document.title = `${scenicDetailInfo.scenicName} - 门票详情`;
      bridge.trackPageView(`${scenicDetailInfo.scenicName} - 门票详情`);
    } else {
      document.title = '门票详情';
      bridge.trackPageView('门票详情');
    }
  }, [scenicDetailInfo?.scenicName]);

  // ... 组件其余代码
};
```

---

## 关键规则

1. **必须在 React 页面组件中实现**：禁止在 EJS 模板中添加页面埋点逻辑
2. **同步调用**：`document.title` 和 `bridge.trackPageView()` 必须在同一个 `useEffect` 中调用
3. **依赖数组**：动态标题需将依赖项（如 `pageParams.title`）加入 `useEffect` 依赖数组
4. **必须导入 bridge**：所有页面必须导入 `import { bridge } from '@/common/bridge'`

## 执行参数

使用本 skill 时必须提供具体目标：
- **单个页面文件**：如 `assets/src/pages/PlaneHotelBook/index.jsx`
- **整个文件夹**：如 `assets/src/pages/`（将为文件夹下所有页面添加埋点）

---

## 快速参考

```javascript
import { bridge } from '@/common/bridge';

// 静态标题
const PAGE_TITLE = '页面标题';
useEffect(() => {
  document.title = PAGE_TITLE;
  bridge.trackPageView(PAGE_TITLE);
}, []);

// 动态标题
useEffect(() => {
  const title = pageParams.title || '默认标题';
  document.title = title;
  bridge.trackPageView(title);
}, [pageParams.title]);
```

---

## 性能打点方案

### 性能打点说明

记录页面开始加载到关键内容可见、核心操作可用的耗时，字段为 `business_ready_ms`，按毫秒四舍五入为整数上报（有效正耗时最小为 1ms）。整页首屏从浏览器导航开始计时（含 SSR 等待）；SPA 路由切换从 `startPageView()` 调用时计时。

### 调用方法

在首屏关键数据、必要图片和核心事件绑定就绪后调用；SSR 页面需等待核心操作依赖的 hydration 完成。

```javascript
window.eventTrack.performTrack('PAGE_CODE'); // 推荐
window.eventTrack.performTrack('PAGE_CODE', undefined, recordedReadyEpochMs); // 已有完成时间时使用
window.eventTrack.performTrack('PAGE_CODE', 'fail'); // 页面不可用
```

**参数说明**：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| page_code | 是 | 非空字符串，页面业务编码，编码规则及现有枚举值参考 WIKI |
| status | 否 | 当前业务状态：`success` 表示可用，`fail` 表示不可用；默认 `success`，其他值会被忽略 |
| recordedReadyEpochMs | 否 | 第三个参数。客户端完成时刻的 epoch 毫秒时间戳（如在完成时记录的 `Date.now()`），兼容数字字符串；省略或传 `undefined` 时，由 SDK 等待两帧后记录 |
| pageViewId | SPA 必填 | 第四个参数。`startPageView()` 返回的本次访问 ID；普通整页接入无需传入 |

### SPA 路由切换（history/hash 均适用）

在路由开始时创建访问，在该页面真正可用时结束计时：

```javascript
// 路由开始：将 ID 保存到本次导航/加载任务的上下文。
var pageViewId = window.eventTrack.startPageView();

// 本次页面就绪：异步回调须捕获上述 ID，不能读取全局最新 ID。
window.eventTrack.performTrack('PAGE_CODE', undefined, undefined, pageViewId);

// 页面加载完成但业务不可用。
window.eventTrack.performTrack('PAGE_CODE', 'fail', undefined, pageViewId);

// 导航取消、失败时调用；已完成的记录不会被撤回。
window.eventTrack.cancelPageView(pageViewId);
```

- `startPageView()` 返回新的访问 ID；缺少可信时钟时返回 `null`。每次访问独立计时、去重，同一 URL 可再次统计。
- 首次路由初始化使用 `startPageView({ initial: true })`，保留浏览器导航起点；后续切换不传该选项。开始路由测量后，`performTrack` 必须携带 ID，缺失或过期 ID 会被忽略。
- 新导航开始即终止旧的未完成测量；取消导航不恢复旧测量。重定向重新开始一次导航，已完成且等待 SDK 的记录仍会补报。SDK 不自动监听 URL 变化，也不会触发 PV 上报。
- Vue Router 4 的守卫、取消处理和就绪回调示例见 `vue-router4-perform-example.js`。在 `app.use(router)` 和业务守卫之前安装；页面数据/渲染任务开始时调用示例返回的 `captureReady('PAGE_CODE')`，保留其返回的回调，待关键内容及交互就绪后再执行。复用组件时，每次路由访问都要重新捕获回调，不能只在首次 mounted 时处理。`afterEach` 仅确认路由成功，不代表页面可用（见 Vue Router 导航守卫说明）。

### 注意事项

- 调用前设置好页面名称：M 使用 `window.pageName`，PC 使用 `window.PageName`。仅请求结束或组件挂载不一定代表首屏可用；两帧等待只是绘制时机近似。
- 第三个参数不能传服务器时间、秒级时间戳、耗时或 `performance.now()`；非法值会被忽略。SDK 晚加载和重试不会改变原始完成时间。
- 每次访问只记录首次有效调用。BFCache 恢复不自动打点；预渲染、访问开始时隐藏或就绪前切后台的测量会被忽略，之后在前台开始的新路由可正常统计。
- 缺少可信时钟不报成功；无 rAF 时需显式传入完成时间。前置入口执行前的调用无法补记，SDK 始终加载失败或页面提前关闭时不保证送达。
- SDK 加载前最多缓存最近 100 条已完成记录，超出时丢弃最早记录；单条补报异常不会阻断后续记录或 SDK 初始化。
- 单次请求超时 10 秒，传输失败最多重试 2 次（间隔 1/2 秒）。同步异常仅 NetworkError、TimeoutError 可重试；编程、配置或记录组装异常不重试，并在控制台记录错误。
