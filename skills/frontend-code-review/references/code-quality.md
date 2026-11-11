# 规则目录 — 代码质量

## 条件类名使用工具函数

IsUrgent: True
Category: Code Quality

### Description

确保条件 CSS 通过共用的 `classNames` 处理，而不是自定义三元运算、字符串拼接或模板字符串。集中化类逻辑可以使组件保持一致且更易于维护。

### Suggested Fix

```ts
import { cn } from '@/utils/classnames'
const classNames = cn(isActive ? 'text-primary-600' : 'text-gray-500')
```

## Tailwind 优先的样式方案

IsUrgent: True
Category: Code Quality

### Description

优先使用 Tailwind CSS 工具类，而不是添加新的 `.module.css` 文件，除非 Tailwind 组合无法实现所需的样式。将样式保持在 Tailwind 中可以提高一致性并减少维护负担。

添加、编辑或删除"代码质量"规则时更新此文件，以保持目录的准确性。

## 类名排序以便覆盖

### Description

编写组件时，始终将传入的 `className` 属性放在组件自身类值之后，以便下游使用者可以覆盖或扩展样式。这样可以保持组件的默认值，同时仍让外部调用者更改或删除特定样式。

Example:

```tsx
import { cn } from '@/utils/classnames'

const Button = ({ className }) => {
  return <div className={cn('bg-primary-600', className)}></div>
}
```
