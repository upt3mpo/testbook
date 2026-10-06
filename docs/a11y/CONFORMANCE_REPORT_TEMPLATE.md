# Accessibility Conformance Report: template

Copy this file to your capstone folder, rename it `ACCESSIBILITY_CONFORMANCE_REPORT.md`, and fill it in **for your capstone
feature** (the Saved Posts view and the bookmark control, or your own feature). Delete this instruction block when you are done.
Testbook's own report, [CONFORMANCE_REPORT.md](CONFORMANCE_REPORT.md), is the worked example. Read a few rows of it first.

## How to fill it in

1. **Scope it.** Say exactly what you evaluated: which pages, which states, which themes and widths. A claim about "the app"
   when you only tested one view is a false claim.
2. **Fill in the header** (product, feature, date, evaluator, methods). **Say who evaluated it** and whether anyone independent
   or any disabled user was involved. If not, say so plainly, as Testbook's report does.
3. **Go through every row.** Choose one status from the table below. Do not leave a row blank.
4. **Write evidence for every status**, in a sentence, with a link to the test, scan, script run or screenshot that backs it.
   "Supports" with no evidence is a guess.
5. **Use "Not evaluated" honestly.** It is far better than an unearned "Supports". It tells the reader what is left to do.
6. **Mark "Not applicable" only when the criterion cannot apply**, and say why (for example, "no live media").
7. **Finish with limitations and next steps**, then fill in the summary counts at the top.

## Statuses

| Status | Meaning |
| --- | --- |
| **Supports** | The criterion is met, on the evidence listed |
| **Partially supports** | Some of the feature meets the criterion and some does not |
| **Does not support** | Most of the relevant content does not meet the criterion |
| **Not applicable** | The criterion does not apply to this feature |
| **Not evaluated** | There is not yet evidence either way. This is **not** a pass |

## Example rows

| Criterion | Name | Level | Status | Evidence and notes |
| --- | --- | --- | --- | --- |
| 4.1.2 | Name, Role, Value | A | Supports | The bookmark button is named "Save post" and exposes its state with `aria-pressed`. Axe scan of the feed with a post bookmarked passes (`saved-posts.spec.js`, "bookmarked state") |
| 2.4.3 | Focus Order | A | Not evaluated | Focus after un-bookmarking from the Saved Posts list has not been tested with a screen reader. The browser test checks focus lands on the list heading |

## Report header

| Field | Value |
| --- | --- |
| Product and feature | |
| Standard | WCAG 2.2, Level A and AA (55 success criteria) |
| Report date | |
| Evaluated by | |
| Independent review or disabled testers involved? | |
| Methods used | |
| Not yet done | |

## Summary

| Status | Criteria |
| --- | --- |
| Supports | |
| Partially supports | |
| Does not support | |
| Not applicable | |
| Not evaluated | |
| **Total** | **55** |

## 1. Perceivable

| Criterion | Name | Level | Status | Evidence and notes |
| --- | --- | --- | --- | --- |
| 1.1.1 | Non-text Content | A | | |
| 1.2.1 | Audio-only and Video-only (Prerecorded) | A | | |
| 1.2.2 | Captions (Prerecorded) | A | | |
| 1.2.3 | Audio Description or Media Alternative (Prerecorded) | A | | |
| 1.2.4 | Captions (Live) | AA | | |
| 1.2.5 | Audio Description (Prerecorded) | AA | | |
| 1.3.1 | Info and Relationships | A | | |
| 1.3.2 | Meaningful Sequence | A | | |
| 1.3.3 | Sensory Characteristics | A | | |
| 1.3.4 | Orientation | AA | | |
| 1.3.5 | Identify Input Purpose | AA | | |
| 1.4.1 | Use of Color | A | | |
| 1.4.2 | Audio Control | A | | |
| 1.4.3 | Contrast (Minimum) | AA | | |
| 1.4.4 | Resize Text | AA | | |
| 1.4.5 | Images of Text | AA | | |
| 1.4.10 | Reflow | AA | | |
| 1.4.11 | Non-text Contrast | AA | | |
| 1.4.12 | Text Spacing | AA | | |
| 1.4.13 | Content on Hover or Focus | AA | | |

## 2. Operable

| Criterion | Name | Level | Status | Evidence and notes |
| --- | --- | --- | --- | --- |
| 2.1.1 | Keyboard | A | | |
| 2.1.2 | No Keyboard Trap | A | | |
| 2.1.4 | Character Key Shortcuts | A | | |
| 2.2.1 | Timing Adjustable | A | | |
| 2.2.2 | Pause, Stop, Hide | A | | |
| 2.3.1 | Three Flashes or Below Threshold | A | | |
| 2.4.1 | Bypass Blocks | A | | |
| 2.4.2 | Page Titled | A | | |
| 2.4.3 | Focus Order | A | | |
| 2.4.4 | Link Purpose (In Context) | A | | |
| 2.4.5 | Multiple Ways | AA | | |
| 2.4.6 | Headings and Labels | AA | | |
| 2.4.7 | Focus Visible | AA | | |
| 2.4.11 | Focus Not Obscured (Minimum) | AA | | |
| 2.5.1 | Pointer Gestures | A | | |
| 2.5.2 | Pointer Cancellation | A | | |
| 2.5.3 | Label in Name | A | | |
| 2.5.4 | Motion Actuation | A | | |
| 2.5.7 | Dragging Movements | AA | | |
| 2.5.8 | Target Size (Minimum) | AA | | |

## 3. Understandable

| Criterion | Name | Level | Status | Evidence and notes |
| --- | --- | --- | --- | --- |
| 3.1.1 | Language of Page | A | | |
| 3.1.2 | Language of Parts | AA | | |
| 3.2.1 | On Focus | A | | |
| 3.2.2 | On Input | A | | |
| 3.2.3 | Consistent Navigation | AA | | |
| 3.2.4 | Consistent Identification | AA | | |
| 3.2.6 | Consistent Help | A | | |
| 3.3.1 | Error Identification | A | | |
| 3.3.2 | Labels or Instructions | A | | |
| 3.3.3 | Error Suggestion | AA | | |
| 3.3.4 | Error Prevention (Legal, Financial, Data) | AA | | |
| 3.3.7 | Redundant Entry | A | | |
| 3.3.8 | Accessible Authentication (Minimum) | AA | | |

## 4. Robust

| Criterion | Name | Level | Status | Evidence and notes |
| --- | --- | --- | --- | --- |
| 4.1.2 | Name, Role, Value | A | | |
| 4.1.3 | Status Messages | AA | | |

## Known limitations and next steps

1.
2.
3.
