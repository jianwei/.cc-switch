---
# @author Codex (K2.6)
name: vue-feature-reverse-prd
description: Use when converting existing Vue page source code into feature-oriented PRD, page layout maps, feature position maps, behavior contracts, data-source maps, enum dictionaries, or rewrite-ready documentation before refactoring or rebuilding legacy frontend pages.
---

# Vue Feature Reverse PRD

## Goal

Turn existing Vue page source into rewrite-ready product and behavior documentation. Organize by business feature and user flow, not by file tree.

## Use When

- The user wants to generate requirements from Vue source code.
- The user wants to refactor or rewrite a legacy Vue page after understanding current behavior.
- The user wants to first draw the page layout, page structure, wireframe, feature positions, or module locations before discussing APIs or source code.
- The user provides a route path or URL and asks what functions a page has, where page data comes from, or which enums/rules affect the UI.
- The code is messy and file-level documentation would only mirror the mess.

## Required Input

The user must provide either:

- a route path, such as `/order/list`
- a full URL, such as `https://example.com/order/list?status=1`

Do not start source analysis without a route path or URL. If the user provides only a vague page name, ask for the route or URL first.

## Output Principle

Documents must answer business questions first:

1. What can the user do on this page?
2. What does the page roughly look like, and where is each feature located?
3. Where does each piece of page data come from?
4. Which enums, permissions, states, and side effects control behavior?
5. Which source files prove or implement each behavior?
6. How should the page be split when rewritten?
7. How will the rewrite be accepted, tested, migrated, and rolled back?

Use source files as evidence, not as the documentation structure.

Save final requirement documents and all enum dictionaries under `docs/requirements/` in the target repository. Save API contract documents under `docs/apis/`. Create these directories when they do not exist.

For each analyzed page, create a page requirement directory: `docs/requirements/<page-or-route-name>/`. The first document to produce for human reading is `docs/requirements/<page-or-route-name>/page-layout-map.md`. The page index document goes in `docs/requirements/<page-or-route-name>/index.md`. Every feature discovered on the page must be written as its own separate requirement file under the same directory.

All output documents must use the fixed templates in this skill. Do not invent new section structures. If information is missing or uncertain, keep the section and write `unknown`, `none`, or `inferred` as appropriate.

## Workflow

### 1. Identify Page Boundary

Start from the provided route path or URL. Normalize full URLs into path, query, and hash. Then find the matching router record, entry component, child components, store modules, API modules, constants, utils, styles, permission checks, and tracking code involved in the page.

Record the boundary like this:

```md
## Page Boundary

| Type | Source | Purpose |
| --- | --- | --- |
| Input | /order/list?status=1 | User-provided route or URL |
| Route | src/router/index.js | Page entry and query contract |
| View | src/views/order/List.vue | Main page shell |
| API | src/api/order.js | Query, export, detail requests |
| State | src/store/modules/order.js | Shared list/filter state |
| Constants | src/constants/order.js | Status and type enums |
```

### 2. Draw Page Layout First

Before deep technical documentation, produce a low-fidelity page layout map for non-technical readers. This is the first required output document. The map must show the page's major visual blocks from top to bottom and mark which feature IDs live in each block.

Write this document to `docs/requirements/<page-or-route-name>/page-layout-map.md` using `templates/page-layout-map.md`.

If the feature list is not fully stable yet, create provisional feature IDs while drawing the layout, then reconcile those IDs when writing the feature list and individual feature documents. Do not postpone the layout map until after API or source-level documentation.

The layout map should be source-informed but business-readable:

- Use plain language for page regions, such as header/status area, search/filter area, list/table area, detail area, action bar, dialog area, bottom fixed action area.
- Mark feature IDs in each region, such as `F-001`, `F-002`.
- Include a feature location table: feature ID, feature name, page position, user trigger, and main result.
- Include a user-question table, such as "Where does the user pay?", "Where does the user see refund progress?", mapped to page region and feature IDs.
- Include one-line acceptance notes for product, QA, operations, or customer-service readers.
- If a rendered page or screenshot is available, use it to validate the layout map. If only source code is available, infer the layout from the template/render structure and mark confidence as inferred.

Do not use component names, file names, or CSS class names as the primary layout labels. Technical evidence can appear in later documents.

### 3. Build Feature List First

List user-visible capabilities before describing files.

```md
## Feature List

| Feature | User Action | UI Result | Involved State | Notes |
| --- | --- | --- | --- | --- |
| Query orders | Submit filter form | Refresh table | loading / success / empty / error | Preserve route query |
| Reset filters | Click reset | Restore defaults and reload | success | Check default date rule |
| View detail | Click detail/order number | Navigate or open dialog | - | Preserve route params |
| Export | Click export | Download or toast | loading / success / fail | Permission controlled |
```

Each feature should map to observable behavior, not implementation details.

After the feature list is stable, assign each feature a stable feature ID such as `F-001`, `F-002`, and create one feature requirement document per feature. Do not merge multiple features into one requirement file.

### 4. Trace Data Sources

For every visible field, option, button state, list, summary, and dialog value, identify its source.

```md
## Data Sources

| Data | Source | Timing | Used By | Notes |
| --- | --- | --- | --- | --- |
| Table rows | API: /order/list | init, query, pagination | Main table | Depends on form + query |
| Status options | API or local constant | init | Filter select, status tag | Confirm source of truth |
| User permissions | store/user or API | init | Button visibility | Affects export/edit/cancel |
| Default filters | route.query + local defaults | init | Search form | Check date defaults |
```

For each API call, document:

```md
### API: Query List

- Trigger: page init, search, pagination, sorting
- Input sources: form fields, route query, pagination state, user context
- Output targets: table rows, total count, summary, empty state
- Error behavior: toast, inline error, silent fallback, retry, or unknown
- Full parameter details: document every request and response field in `docs/apis/`
```

### 5. Extract Enum Dictionary

Enums must include display text and behavior impact.

Write all enum dictionaries to requirement documents under `docs/requirements/`. API documents may reference enum names and requirement document links, but must not become the source of truth for enum definitions.

```md
## Enum Dictionary

### OrderStatus

| Value | Label | Used In | Source | Behavior Impact |
| --- | --- | --- | --- | --- |
| 0 | Pending payment | filter, table tag | local/API | Show pay button |
| 1 | Paid | filter, table tag | local/API | Hide pay button |
| 2 | Cancelled | filter, table tag | local/API | Hide cancel button |
```

Also record derived rules:

```md
## Enum Rules

| Condition | Effect |
| --- | --- |
| orderStatus = 0 | Show pay action |
| orderStatus = 2 | Hide cancel action |
| refundStatus = 1 | Show refund progress |
```

### 6. Map Features To Interfaces And Source

Create two maps: business-to-interface and business-to-source.

Write detailed API contracts to `docs/apis/<api-domain-or-feature-name>.md`. Each API contract must include complete request and response parameters found in source code, API wrappers, adapters, mock data, or usage sites. In requirement documents, keep the feature/API map and link to the matching API contract document instead of duplicating full API details.

```md
## Feature/API Map

| Feature | Trigger | API | Input Source | Response Affects |
| --- | --- | --- | --- | --- |
| Query orders | init/search/page change | /order/list | form + query + page | table, pagination, empty state |
| Export orders | click export | /order/export | form + current user | download/toast |
```

```md
## Feature/Source Map

| Feature | Source Files | Key Evidence |
| --- | --- | --- |
| Query orders | List.vue, order.js, orderStatus.js | mounted fetch, search handler, status formatter |
| Export orders | List.vue, export.js | export button handler, permission branch |
```

### 7. Produce Rewrite Guidance

Recommend a feature-based target structure.

```text
src/features/order-query/
├── pages/OrderQueryPage.vue
├── components/OrderSearchForm.vue
├── components/OrderTable.vue
├── composables/useOrderQuery.ts
├── services/orderQueryApi.ts
├── adapters/orderQueryAdapter.ts
├── constants.ts
└── types.ts
```

Guidance must distinguish:

- Must preserve: routes, query keys, API payloads, permissions, tracking events, visible behavior.
- Can improve: component boundaries, naming, local state shape, adapter layer, tests, styling.
- Needs confirmation: dead branches, unclear permissions, unused enums, unreachable states.

### 8. Produce Rewrite Execution Documents

After page and feature requirement documents are filled, generate these rewrite documents from the bundled templates:

- `page-layout-map.md`: low-fidelity page layout map, feature positions, user-question map, and non-technical acceptance notes.
- `component-plan.md`: target component tree, props/emits, state ownership.
- `view-model.md`: raw API fields to UI view model fields and adapter rules.
- `test-cases.md`: functional, state, permission, tracking, API, and regression test cases.
- `ui-verification.md`: screenshot baselines, viewport matrix, UI states, interactions, text format, layout, and Playwright verification plan.
- `analytics-contract.md`: tracking events, trigger timing, parameters, exposure/click tracking, and rewrite verification.
- `navigation-contract.md`: route entry, outbound navigation, query/params/hash, history, guards, and back/refresh behavior.
- `mock-scenarios.md`: scenario matrix and API mock data needed for UI, component, and Playwright verification.
- `performance-budget.md`: load, network, rendering, and console-error budgets for the rewritten page.
- `migration-plan.md`: gray release, entry switching, parity checks, monitoring, rollback.
- `external-dependencies.md`: framework globals, app bridge, storage, third-party UI, and rewrite strategy.
- `deprecation-plan.md`: legacy files, APIs, styles, routes, compatibility items, and safe deletion sequence.

## Final Document Shape

Use the template files bundled with this skill:

| Document | Template File | Output Path |
| --- | --- | --- |
| Page layout and feature position map | `templates/page-layout-map.md` | `docs/requirements/<page-or-route-name>/page-layout-map.md` |
| Page index requirement document | `templates/requirement.md` | `docs/requirements/<page-or-route-name>/index.md` |
| Single feature requirement document | `templates/feature-requirement.md` | `docs/requirements/<page-or-route-name>/<feature-id>-<feature-name>.md` |
| API contract document | `templates/api-contract.md` | `docs/apis/<api-domain-or-feature-name>.md` |
| Component split plan | `templates/component-plan.md` | `docs/requirements/<page-or-route-name>/component-plan.md` |
| View model and adapter contract | `templates/view-model.md` | `docs/requirements/<page-or-route-name>/view-model.md` |
| Test cases | `templates/test-cases.md` | `docs/requirements/<page-or-route-name>/test-cases.md` |
| UI verification plan | `templates/ui-verification.md` | `docs/requirements/<page-or-route-name>/ui-verification.md` |
| Analytics contract | `templates/analytics-contract.md` | `docs/requirements/<page-or-route-name>/analytics-contract.md` |
| Navigation contract | `templates/navigation-contract.md` | `docs/requirements/<page-or-route-name>/navigation-contract.md` |
| Mock scenarios | `templates/mock-scenarios.md` | `docs/requirements/<page-or-route-name>/mock-scenarios.md` |
| Performance budget | `templates/performance-budget.md` | `docs/requirements/<page-or-route-name>/performance-budget.md` |
| Migration and rollback plan | `templates/migration-plan.md` | `docs/requirements/<page-or-route-name>/migration-plan.md` |
| External dependencies | `templates/external-dependencies.md` | `docs/requirements/<page-or-route-name>/external-dependencies.md` |
| Deprecation plan | `templates/deprecation-plan.md` | `docs/requirements/<page-or-route-name>/deprecation-plan.md` |

Before writing each output document, read the matching template file and preserve its section order and table columns exactly. Fill all sections. If a section has no proven data, keep the section and write `unknown`, `none`, or `inferred`.

The page index document lists page boundary, feature list, shared data sources, shared enums, cross-feature maps, and legacy parity checklist. It must link to `page-layout-map.md` near the top so non-technical readers can first understand page shape and feature positions. Each feature requirement document contains only one feature's user goal, flow, data, API usage, enum/rule dependencies, state transitions, acceptance criteria, source evidence, and rewrite guidance.

API contract documents must include complete input and output parameter tables using the columns in `templates/api-contract.md`.

If a parameter is inferred but not proven by source code, mark it as `unknown` or `inferred` instead of presenting it as certain.

For `Enum Dependencies`, reference the enum dictionary in `docs/requirements/` and only list the fields that depend on each enum. Do not duplicate full enum value tables in `docs/apis/`.

## Quality Bar

- Do not organize primary docs by `components`, `api`, `store`, or `utils`.
- Do not skip the page layout map; every analyzed page must include `page-layout-map.md`, and it must be created before feature details, API contracts, and rewrite execution documents.
- The layout map must be readable by product, QA, operations, and customer-service readers without source-code knowledge.
- Do not merge multiple page features into one feature requirement file; one feature equals one file.
- Do not claim a page is rewrite-ready without acceptance criteria, legacy parity checklist, component plan, view model contract, test cases, UI verification plan, analytics contract, navigation contract, mock scenarios, performance budget, migration plan, external dependency inventory, and deprecation plan.
- Keep all enum value tables in `docs/requirements/`; API docs only reference them.
- Do not invent product intent that source code does not prove; mark it as an open question.
- Do not copy large code blocks into docs; cite files, functions, and behavior evidence.
- Preserve legacy behavior as the default unless the user asks to redesign it.
- Call out unknowns explicitly: unclear source, dead code, unused enum, ambiguous permission, inconsistent API field.
- The output should be useful for rebuilding the page without reading the old implementation line by line.
