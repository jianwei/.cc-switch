---
name: vue-legacy-spa-upgrade
description: Use when upgrading a single page in an older Vue SPA, especially Vue 2 or mixed legacy Vue projects, without migrating the whole app; triggers include page refactor, Vue 2 to Vue 3 compatibility, Options API cleanup, Tailwind CSS conversion, CSS/SCSS/SASS/LESS removal, base64 image extraction, route-level modernization, old component replacement, and preserving existing behavior in legacy admin or business systems.
---

# Vue Legacy SPA Upgrade

## Goal

Upgrade one page at a time while preserving routing, API contracts, permission checks, tracking, visual density, and operational habits that old business systems depend on.

## First Pass

1. Identify the page boundary: route, entry component, child components, store modules, API files, CSS/LESS/SCSS scope, feature flags, and external globals.
2. Capture current behavior before editing: URL params, query params, loading/empty/error states, form validation, pagination, table selection, modals, permission branches, and submit side effects.
3. Decide the upgrade shape:
   - **Internal cleanup**: keep Vue 2 and Options API, reduce risk.
   - **Composition bridge**: use Composition API plugin or local composables when the repo already supports it.
   - **Vue 3-ready page**: remove Vue 2-only APIs and isolate compatibility work, but do not force a whole-app migration.
4. Make the smallest vertical slice first: one page shell, one data path, one visible state.

## Upgrade Rules

- Preserve public contracts first: route names, query keys, emitted events, Vuex action names, API payload shapes, and analytics names.
- Prefer local adapters over broad rewrites when old APIs leak into the page.
- Keep Options API if the surrounding page is deeply Options-based and there is no project pattern for Composition API.
- Use `<script setup>` and TypeScript only when the project already supports Vue 3 or has an accepted migration path.
- Do not replace global UI libraries, table components, form systems, or request clients as part of a single-page upgrade unless the user explicitly asks.
- Convert all page-owned handwritten styling to Tailwind utilities, regardless of whether it lives in native CSS, Vue `<style>`, SCSS, SASS, LESS, or separate stylesheet files.
- Keep old CSS selectors only as compatibility hooks when referenced by tests, QA scripts, browser extensions, operations docs, or third-party component overrides; do not keep them for visual styling.
- Convert base64-embedded images into image files and reference those files from markup or Tailwind-compatible styles.
- Avoid "while here" refactors outside the page boundary.

## Tailwind Conversion

1. Confirm Tailwind is available in the project before editing. If it is missing, add a minimal project-compatible Tailwind setup only when the user asks for setup work; otherwise report the blocker.
2. Inventory every handwritten style owned by the page:
   - Vue `<style>`, `<style scoped>`, and inline `style=""`
   - imported `.css`, `.scss`, `.sass`, and `.less` files
   - page-local class maps, BEM classes, CSS modules, and style constants
3. Replace those styles with Tailwind utilities in the template or component props. Delete the old stylesheet rules after their visual behavior is represented by Tailwind.
4. For separate CSS/SCSS/SASS/LESS files, migrate the used selectors into Tailwind classes at call sites, then remove the imports and delete now-unused files when they are page-local.
5. Preserve semantic or integration classes only when they are external contracts; keep them alongside Tailwind classes instead of using them for visual styling.
6. Use existing Tailwind config tokens for spacing, colors, typography, z-index, breakpoints, and shadows. Do not invent one-off arbitrary values unless matching a legacy pixel-perfect requirement.
7. Prefer readable class grouping: layout, spacing, sizing, typography, color, border, state, responsive.
8. Extract repeated utility sets into local components or existing shared components only after duplication appears at least twice in the upgraded page.
9. Leave third-party UI component internals alone. Style them through supported props, wrapper utilities, or the narrowest existing override.

## Base64 Image Extraction

1. Search page-owned styles and templates for `data:image/...;base64,`.
2. Decode each base64 image into an appropriate real image file under the project's existing static asset convention, such as `src/assets`, `public`, or the page's local assets folder.
3. Choose the extension from the media type: `image/png` -> `.png`, `image/jpeg` -> `.jpg`, `image/svg+xml` -> `.svg`, `image/webp` -> `.webp`, `image/gif` -> `.gif`.
4. Replace the base64 string with a normal image reference:
   - use `<img>` or component image props when the image is content
   - use Tailwind `bg-[url(...)]` or an existing asset import when the image is decorative background
5. Keep filenames stable and descriptive enough for future maintenance.
6. Verify the decoded image renders before deleting the embedded base64 source.

## Working Sequence

1. Read local conventions first: nearby pages, router setup, store modules, API helpers, lint/test commands, and existing migration examples.
2. Create or update characterization tests when practical. If no test harness exists, document manual checks and add low-risk assertions around pure helpers or API adapters.
3. Extract risky legacy behavior behind page-local helpers:
   - query parsing and defaulting
   - request parameter building
   - response normalization
   - permission and button visibility rules
   - table/form state transitions
4. Upgrade the page shell after behavior is isolated.
5. Verify every page state that existed before the change.

## Common Legacy Hazards

| Hazard | Safer move |
| --- | --- |
| `this`-heavy methods mixed with watchers | Extract pure helpers first, then move state management |
| Deep `$refs` access | Keep a narrow wrapper function and replace call sites gradually |
| Implicit route query defaults | Centralize query parsing before changing component code |
| Global event bus | Wrap subscribe/unsubscribe and verify cleanup on destroy/unmount |
| Shared mutable table/form config | Clone or factory-create per page instance |
| CSS from global LESS/SCSS | Move page-owned rules to Tailwind; keep only required compatibility selectors |
| Base64 images in CSS or templates | Decode into image assets and reference files normally |
| Old UI component quirks | Keep prop/event names stable and adapt at the edge |

## Verification Checklist

- Run the closest unit/type/lint command available in the repo.
- Start the dev server when the page needs browser verification.
- Check at least desktop width and the smallest supported operations viewport.
- Check that migrated Tailwind classes preserve spacing, alignment, overflow, sticky/fixed areas, and disabled/hover/focus states.
- Check that removed CSS/SCSS/SASS/LESS imports were page-local and no longer used.
- Check that extracted image files render correctly and the base64 strings are gone from upgraded page-owned code.
- Exercise: initial load, reload with query, empty data, API failure, validation failure, successful submit, navigation away/back, and permission-denied state.
- Compare network payloads before and after when changing request-building code.
- Note any behavior intentionally changed, with reason.

## Output Style

When reporting back, include:

- Page boundary touched.
- Upgrade shape chosen and why.
- Behavior preserved or intentionally changed.
- Verification commands and manual states checked.
- Remaining migration debt inside the page, not broad project wish lists.
