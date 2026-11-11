# 规则目录 — 性能

## React Flow 数据使用

IsUrgent: True
Category: Performance

### Description

渲染 React Flow 时，优先使用 `useNodes`/`useEdges` 进行 UI 消费，并在修改或读取节点/边状态的回调中依赖 `useStoreApi`。避免在这些钩子之外手动获取 Flow 数据。

## 复杂 prop 记忆化

IsUrgent: True
Category: Performance

### Description

在将复杂 prop 值（对象、数组、映射）传递到子组件之前，用 `useMemo` 包装它们以保证稳定的引用并防止不必要的渲染。

添加、编辑或删除"性能"规则时更新此文件，以保持目录的准确性。

Wrong:

```tsx
<HeavyComp
    config={{
        provider: ...,
        detail: ...
    }}
/>
```

Right:

```tsx
const config = useMemo(() => ({
    provider: ...,
    detail: ...
}), [provider, detail]);

<HeavyComp
    config={config}
/>
```
