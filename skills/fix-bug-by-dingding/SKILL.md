---
name: fix-bug-by-dingding
description: Triage and fix specified DingDing bug rows. Ensure local and reason columns exist, fix frontend bugs with before/after screenshots and one commit per bug, and record detailed evidence in reason for API or other non-frontend issues without changing code.
---

# Fix Bug By DingDing

## Overview

Use this skill to triage DingDing-tracked bugs before editing code. Ensure the tracking columns exist, discover the reproduction entry, and determine whether the cause belongs to the frontend. Fix confirmed frontend bugs with screenshots, verification, one commit per bug, and `local=done`. For API or other non-frontend issues, leave code unchanged and write the diagnosis and evidence to `reason`.

## Mandatory Checklist

For every requested bug:

- Ensure the `local` and `reason` columns exist and record their actual positions.
- Before starting the bug, output its row number and complete current content, including `local` and `reason`.
- Reproduce or inspect the issue and classify the cause before editing code.
- For a confirmed non-frontend issue, follow the non-frontend branch in step 4: record detailed `reason`, read it back, leave code and `local` unchanged, and report that no fix was made.

For a confirmed frontend bug, also complete all items below before moving to the next bug:

- Capture a before screenshot.
- Capture an after screenshot.
- Compare the before/after screenshots yourself and keep iterating until the bug is fixed.
- Start the local app yourself and locate the page/reproduction entry yourself.
- Run the relevant build and/or test command for the changed surface.
- Create exactly one commit for that bug.
- Include the DingDing row number and problem description in the commit message.
- Update the DingDing `local` column to `done`.
- Read the DingDing row back and confirm `local` is `done`.
- After finishing each bug, output that the bug has been fixed. If it cannot be fixed or no code change is needed, output the reason instead.

After all requested bugs are processed, output a final summary. Before/after screenshots, build/tests, a commit, and `local=done` are required only for frontend fixes. If required evidence or verification is technically impossible, record the blocker in `reason` when writable and report it; do not claim a fix.

## Workflow

1. Load the DingDing workflow first.
   - Use the `dws` skill/tooling to read the DingDing document or sheet.
   - Identify the requested bug numbers exactly. Treat user numbering as the source of truth.
   - The number provided by the user is the current sheet row number and must be used directly; do not add or subtract any offset. For example, bug number `55` means sheet row `55`.
   - Read the actual headers and occupied columns. Reuse existing `local` and `reason` columns; append only missing columns after the occupied columns without shifting rows or overwriting existing headers/data. Create missing AI-table fields using the product's supported tooling instead of spreadsheet coordinates.
   - The canonical column names are `local` and `reason` (not `reson`). If only a legacy `reson` column exists, preserve its data and append `reason`; use `reason` for this workflow.
   - Read the headers back after adding columns and resolve their actual cells/field IDs. If column creation is unavailable or fails, report the blocker before editing code.
   - Record the bug number, actual sheet row/range, page, issue description, assignee/status, and the `local` and `reason` cells/fields and values for every requested bug. Output this content before starting the bug.

2. Inspect the repository before editing.
   - Read `AGENTS.md` and any referenced local rules.
   - Read `package.json` files and workspace scripts to determine the correct install, dev, build, and test commands.
   - Check `git status -sb` and preserve unrelated user changes.
   - Use `rg`/targeted file reads to find the real implementation path.

3. Discover and start the reproduction entry yourself.
   - Treat the DingDing first column as the primary page clue, such as `航班列表页`, `首页`, `详情页`, or `预订页`.
   - Map that page clue to the project route by reading router files, page directories, app entry files, and existing links.
   - Start the relevant local dev server using the scripts discovered from `package.json`. If the default port is occupied, use the next available port and record the final URL.
   - Use Playwright/Playwriter to open the local page, interact with it, inspect console/network state, and capture screenshots.
   - If data is needed to reproduce the issue, prefer existing mocks, local API routes, intercepted network responses, or minimal browser-only fixtures. Do not commit throwaway reproduction fixtures unless they are real tests or required project mocks.
   - Mocks and intercepted failures verify frontend behavior only; they do not establish that a real API is faulty. For API diagnosis, remove interception and inspect the real request/response using the existing authenticated session.
   - Ask the user only when reproduction requires external credentials, captcha/manual verification, unavailable private data, or a decision that cannot be inferred safely.

4. Classify the cause, then process one bug at a time.
   - Trace the request construction and response handling against the actual contract or working legacy implementation. An HTTP error, `success:false`, or a failed request alone does not establish ownership: wrong frontend URL/parameters, parsing, or rendering still belongs to the frontend. HTTP 200 may contain a business failure.
   - **Confirmed non-frontend cause** (for example, an API returning a business failure for a contract-correct request, backend data errors, or an external service fault): do not modify frontend/backend code, hide the error, or add a workaround. Revert only uncommitted code/tests introduced for this bug if diagnosis began after editing; preserve unrelated user changes. Do not create a fix commit or set `local=done`; preserve existing `local` and other status values.
   - Write a detailed diagnosis into that row's `reason`, preserving unrelated existing notes. Include the observed issue, reproduction entry and conditions, evidence that the frontend request/handling follows the contract, the non-frontend cause and impact, and the next action needed. For API issues include the actual complete request URL, HTTP method, relevant non-secret parameters, HTTP status, business error code/message, and a minimal response excerpt. Redact credentials and sensitive values. Distinguish verified facts from inferences; a bare URL is insufficient.
   - Read `reason` back and confirm the diagnosis was saved and `local` was not changed. Report `未修复：非前端问题` with the cause, then continue to the next bug. Preserve available reproduction screenshots/network evidence; this branch does not require an after screenshot, build/tests, or a commit.
   - **Insufficient evidence**: record what is known, the missing evidence, and the blocker in `reason`, read it back, and report the issue as unresolved. Do not guess that the API is faulty or change code solely to suppress the symptom.
   - **Confirmed frontend cause**: continue with the frontend fix steps below and steps 5-6.
   - Before changing code, reproduce or inspect the issue in the real local page.
   - Capture a before screenshot and save it with a stable path such as `/tmp/<repo>-bug<N>-before.png`.
   - Make a surgical code change that directly addresses the bug. Do not bundle unrelated cleanup.
   - Capture an after screenshot, compare it yourself against the before screenshot, and iterate until the visual or behavioral problem is fixed.
   - After the bug is processed, output `已修改好` and include the verification result. If the bug cannot be fixed or no change is needed, output the specific reason instead and do not claim it was fixed.

5. Verify each bug before committing.
   - Run the smallest meaningful build and/or test check for the changed surface. For this Vue/Vite project, prefer `rtk pnpm build:domestic` or the relevant app build.
   - If a standard check fails for pre-existing environment reasons, capture the exact reason and continue only when the bug-specific verification is still sound.
   - Re-check `git diff` so the commit contains only this bug’s intended changes.

6. Update DingDing and commit immediately after each fixed bug.
   - This step applies only to verified frontend fixes. Add the resolution and verification result to `reason`; clearly mark any earlier unresolved diagnosis as superseded rather than leaving contradictory notes.
   - Set the bug row’s `local` cell to `done`.
   - Read the row back and confirm both `local=done` and the saved `reason`.
   - Stage only the files for this bug.
   - Commit once. The commit message must include the current sheet row number and the DingDing issue description, using the format `第<行号>行 <问题描述>`.
   - Verify `git log -1 --oneline` and `git status -sb` before moving to the next bug.

7. Finish cleanly.
   - Repeat steps 3-6 for each requested bug.
   - Stop any local dev server you started.
   - Final response in Chinese must provide a summary of every bug, including the bug number and content, frontend/non-frontend/unresolved classification, fixed/not-fixed/no-change result and reason, saved `reason` and readback result, actual `local` value, and current git status. For frontend fixes also provide commit hash/message, verification command result, screenshot paths, and DingDing `done` confirmation; mark those items as not applicable for non-frontend issues.

## Requirements

- One fixed bug equals one commit. Never combine multiple requested bugs in one commit unless the user explicitly changes this requirement.
- Commit message must include the current sheet row number and the problem description from DingDing, not a generated summary. Use the format `第<行号>行 <问题描述>`.
- Before and after screenshots are mandatory for frontend fixes. If a frontend bug is not visually representable, capture the closest observable before/after state and explain it.
- Self-comparison of screenshots is mandatory. Do not ask the user to compare for you.
- Page/reproduction discovery is the agent's responsibility. Do not require the user to provide a URL when the page can be inferred from the DingDing first column and repository routes.
- Relevant build/test verification is mandatory before each commit.
- Do not mark DingDing `local` as `done` until the fix is implemented, visually/behaviorally checked, and the after screenshot is captured.
- Confirm ownership before editing: non-frontend issues receive a detailed `reason` and readback, with no code fix, fix commit, or change to `local`.
- Do not push unless the user explicitly asks.
