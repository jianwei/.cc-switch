<!-- @author Codex (K2.6) -->
# UI Verification: <Page Name>

## 1. UI Scope

| Item | Value |
| --- | --- |
| Input Route/URL | unknown |
| Page Name | unknown |
| Related Requirement Doc | docs/requirements/unknown/index.md |
| Related Test Cases Doc | docs/requirements/unknown/test-cases.md |
| Source Confidence | unknown |

## 2. Viewport Matrix

| Viewport | Device Type | Must Verify |
| --- | --- | --- |
| 375x667 | small mobile | layout, overflow, fixed bottom |
| 375x812 | mobile | primary flow |
| 414x896 | large mobile | spacing, line wrap |
| 768x1024 | tablet/webview | responsive behavior |

## 3. Screenshot Baselines

| Scene | Viewport | Legacy Screenshot | New Screenshot | Match Rule |
| --- | --- | --- | --- | --- |
| initial screen | 375x812 | unknown | unknown | core modules match |
| full page | 375x812 | unknown | unknown | module order and visibility match |
| key module | 375x812 | unknown | unknown | content and spacing match |
| dialog/overlay | 375x812 | unknown | unknown | layer, mask, and close behavior match |

## 4. UI State Matrix

| Feature ID | State | Trigger | Expected UI | Evidence |
| --- | --- | --- | --- | --- |
| F-001 | loading | unknown | unknown | unknown |
| F-001 | success | unknown | unknown | unknown |
| F-001 | empty | unknown | unknown | unknown |
| F-001 | error | unknown | unknown | unknown |
| F-001 | disabled | unknown | unknown | unknown |
| F-001 | permission denied | unknown | unknown | unknown |

## 5. Interaction Checks

| Feature ID | Element | Action | Expected Result | Evidence |
| --- | --- | --- | --- | --- |
| F-001 | unknown | click | unknown | unknown |

## 6. Text And Format Checks

| Field | Expected Format | Empty/Fallback | Evidence |
| --- | --- | --- | --- |
| amount | unknown | unknown | unknown |
| date/time | unknown | unknown | unknown |
| status text | unknown | unknown | unknown |
| button text | unknown | unknown | unknown |
| long text | unknown | unknown | unknown |

## 7. Layout And Overflow Checks

| Area | Viewport | Expected Behavior | Evidence |
| --- | --- | --- | --- |
| header | 375x667 | unknown | unknown |
| content module | 375x812 | unknown | unknown |
| fixed bottom area | 375x812 | unknown | unknown |
| dialog/overlay | 414x896 | unknown | unknown |

## 8. Playwright Verification Plan

| Check | Tooling | Assertion | Artifact |
| --- | --- | --- | --- |
| screenshot baseline | Playwright screenshot | core modules match | unknown |
| DOM text | Playwright locator | key text visible | unknown |
| interaction | Playwright click | expected state/change | unknown |
| console errors | Playwright console logs | no unexpected errors | unknown |
| network payload | Playwright network capture | payload matches contract | unknown |

## 9. Visual Regression Notes

| Issue | Severity | Location | Expected Fix |
| --- | --- | --- | --- |
| unknown | unknown | unknown | unknown |

## 10. Open Questions

| ID | Question | Why It Matters | Suggested Owner |
| --- | --- | --- | --- |
| Q-001 | unknown | unknown | unknown |
