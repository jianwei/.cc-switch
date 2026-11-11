<!-- @author Codex (K2.6) -->
# Vue Migration Validation And Output Rules

## Output Locations

所有测试代码：

```text
__test__/[source-relative-path]/
```

所有截图：

```text
screenshot/[source-relative-path]/
```

所有迁移记录和报告：

```text
.omc/vue-migration/[module-name]/
```

## Path Examples

| Source | Unit Test | E2E Test |
|--------|-----------|----------|
| `src/pages/User/List.vue` | `__test__/src/pages/User/List.spec.ts` | `__test__/src/pages/User/List.e2e.spec.ts` |
| `src/pages/User/components/UserTable.vue` | `__test__/src/pages/User/components/UserTable.spec.ts` | `__test__/src/pages/User/components/UserTable.e2e.spec.ts` |
| `src/pages/User/composables/useUserList.ts` | `__test__/src/pages/User/composables/useUserList.spec.ts` | Not required unless behavior is only verifiable end-to-end |

| Page Or Module | Screenshot |
|----------------|------------|
| `src/pages/User/List.vue` | `screenshot/src/pages/User/List/visual-baseline/01-default.png` |
| `src/pages/User/List.vue` | `screenshot/src/pages/User/List/visual-diff/01-default.diff.png` |

## Required Complete Migration Checks

- unit tests pass
- Playwright functional tests pass
- DOM snapshot diff is zero after dynamic content normalization
- visual regression diff is below threshold
- API calls match URL, Method, key Headers, Payload, count, and order
- interaction replay passes
- no new console warning or error
- TypeScript check passes
- scope boundary respected

## Required Logic-Only Checks

- unit tests prove logic equivalence
- Playwright functional tests pass
- API calls match URL, Method, key Headers, Payload, count, and order
- same input produces same state/output
- old functionality is fully mapped or listed as unresolved
- no new console warning or error
- TypeScript check passes
- template and style are unchanged

## Validation Authenticity

这些不能作为成功验证：

- tests that only mount a component
- Playwright tests that only open a page
- tests that mock all migrated business logic
- snapshots without state coverage
- API comparison that only checks request count
- console checks that ignore warnings
- skipped checks reported as passing

## Status Grades

| 状态 | 含义 | 允许发布 |
|------|------|----------|
| 通过 | 所有必需验证项通过，且无新增错误/警告 | 是 |
| 有条件通过 | 核心功能、接口、TS、单测通过，但存在已记录且用户接受的非阻断差异 | 需用户确认 |
| 未通过 | 任一核心验证项失败，或存在功能、接口、TS 编译错误 | 否 |
| 未验证 | 验证环境、原始 URL、测试数据或工具不可用，无法完成必需验证 | 否 |

只有 `通过` 可以称为迁移成功。

## Screenshot Naming

使用稳定数字前缀：

```text
01-default.png
02-loading.png
03-data-loaded.png
04-empty.png
05-hover-[element].png
06-focus-[element].png
07-modal-[name].png
08-validation-error.png
09-system-error.png
10-action-result.png
```
