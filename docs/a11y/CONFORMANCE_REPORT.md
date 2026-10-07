# Accessibility Conformance Report: Testbook

**Standard:** WCAG 2.2, Level A and Level AA (55 success criteria)
**Product:** Testbook, the social app in this repository
**Report date:** 2026-10-06
**Evaluated by:** the project's maintainers and their AI assistant, using the methods below

> **Read this first: this is a self-assessment, not an independent audit.** It was written by the people who
> built and fixed the product, it relies on automated and scripted checks, and **no screen reader has been
> operated by a person yet and no disabled users have tested the product.** Statements marked "Supports" mean
> the criterion is met *as far as these checks can tell*. Treat the report as an honest map of what has and
> has not been verified, not as a certificate. For a real procurement or legal need, commission an independent
> evaluation that includes disabled testers.

It follows the shape of a Voluntary Product Accessibility Template (VPAT) report, which is what procurement
teams ask vendors for, in a lighter form. Stage 5 asks you to produce one for your own capstone feature using the
[template](CONFORMANCE_REPORT_TEMPLATE.md).

## How it was evaluated

| Method | What it covers | Where |
| --- | --- | --- |
| Automated scans (axe-core 4.13, WCAG 2.2 AA plus best practice) | Every route, interaction states, dark theme, 320 px width | [accessibility-axe.spec.js](../../tests/e2e/accessibility-axe.spec.js), [test_accessibility.py](../../tests/e2e-python/test_accessibility.py) |
| Scripted browser tests | Focus, tab order, announcements, reflow, target size, sticky-header coverage | [accessibility-behavior.spec.js](../../tests/e2e/accessibility-behavior.spec.js) |
| Component and unit tests | Names, roles, states, focus management, design-token contrast | [a11y-regressions.test.jsx](../../frontend/src/tests/accessibility/a11y-regressions.test.jsx), [tokens.test.js](../../frontend/src/tests/accessibility/tokens.test.js) |
| Lighthouse | Accessibility score on six pages, including signed-in pages | [accessibility.yml](../../.github/workflows/accessibility.yml) |
| Code and CSS review | The audit that found 20 defects, all since fixed | [AUDIT_LOG.md](AUDIT_LOG.md) |
| A machine-executed preview of the manual scripts | Text spacing, pointer cancellation, target sizes, focus-ring contrast | [2026-10-04-machine-preview.md](manual/runs/2026-10-04-machine-preview.md) |

**Not yet done:** a human run of the [manual test scripts](manual/README.md), in particular VoiceOver and NVDA; testing
with disabled users; zoom to 200% by hand; voice control.

## Terms

| Status | Meaning |
| --- | --- |
| **Supports** | The criterion is met, on the evidence listed |
| **Partially supports** | Some of the product meets the criterion and some does not |
| **Does not support** | Most of the relevant content does not meet the criterion |
| **Not applicable** | The criterion does not apply to this product |
| **Not evaluated** | There is not yet evidence either way. This is **not** a pass |

## Summary

| Status | Criteria |
| --- | --- |
| Supports | 33 |
| Partially supports | 3 |
| Does not support | 4 |
| Not applicable | 5 |
| Not evaluated | 10 |
| **Total** | **55** |

**What stands out:**

- The core interaction, structure and keyboard criteria are supported, and each has a test that guards it.
- **User-uploaded media is where the product falls short.** Images have a generic alternative, and uploaded video has no
  captions, transcript or audio description. Fixing this needs product features (an alternative-text field, a caption
  upload), not markup changes. The capstone's optional second ticket is one of them.
- **Ten criteria are "Not evaluated"**, all of them ones that need a person's judgement (reading order, link and heading
  quality, zoom, voice control). The manual scripts exist to close that gap.

## 1. Perceivable

| Criterion | Name | Level | Status | Evidence and notes |
| --- | --- | --- | --- | --- |
| 1.1.1 | Non-text Content | A | Partially supports | Interface images have text alternatives, and avatars are named for the person. **User-uploaded post images all use the generic alternative text "Post content"**, because authors have no field to describe an image (a known limitation, see the [audit log](AUDIT_LOG.md)). |
| 1.2.1 | Audio-only and Video-only (Prerecorded) | A | Does not support | Users can upload video, and there is no transcript or alternative mechanism. The page does not tell the author one is needed. |
| 1.2.2 | Captions (Prerecorded) | A | Does not support | Uploaded video plays in a native player with no caption track and no way to supply one. |
| 1.2.3 | Audio Description or Media Alternative (Prerecorded) | A | Does not support | No audio description or media alternative mechanism for uploaded video. |
| 1.2.4 | Captions (Live) | AA | Not applicable | No live media. |
| 1.2.5 | Audio Description (Prerecorded) | AA | Does not support | No audio description mechanism for uploaded video. |
| 1.3.1 | Info and Relationships | A | Supports | Landmarks, one top-level heading per page, labelled form fields and named articles. Checked by [axe scans](../../tests/e2e/accessibility-axe.spec.js), [component tests](../../frontend/src/tests/accessibility/a11y-regressions.test.jsx) and [audit log](AUDIT_LOG.md) (A11Y-001, 002, 015). Screen reader verification by a person is still to do. |
| 1.3.2 | Meaningful Sequence | A | Not evaluated | Reading order has not been reviewed against the visual order. |
| 1.3.3 | Sensory Characteristics | A | Not evaluated | Instructions have not been reviewed for reliance on shape, colour or position. |
| 1.3.4 | Orientation | AA | Supports | Nothing in the code restricts orientation. |
| 1.3.5 | Identify Input Purpose | AA | Supports | `autocomplete` tokens on every sign-in and registration field (A11Y-003), checked by [component tests](../../frontend/src/tests/accessibility/a11y-regressions.test.jsx) and the [behaviour tests](../../tests/e2e/accessibility-behavior.spec.js). |
| 1.4.1 | Use of Color | A | Not evaluated | Greyscale review (manual script CC-05) not yet done. The active Feed tab and the active reaction also expose their state in text (A11Y-015). |
| 1.4.2 | Audio Control | A | Supports | No audio plays automatically. Uploaded video uses native controls. |
| 1.4.3 | Contrast (Minimum) | AA | Supports | Axe `color-contrast` on every route, in light and dark themes and in several open states ([axe scans](../../tests/e2e/accessibility-axe.spec.js)), plus a unit test over every design-token pair (A11Y-016). Items axe marks "incomplete" still need measuring by hand (manual script CC-01). |
| 1.4.4 | Resize Text | AA | Not evaluated | Zoom to 200% by hand not yet done (manual script ZM-01, ZM-04). The 320 px reflow and text-spacing results below are encouraging. |
| 1.4.5 | Images of Text | AA | Supports | The interface contains no images of text. (User-uploaded images are user content.) |
| 1.4.10 | Reflow | AA | Supports | No horizontal scroll at 320 px on every route (A11Y-008), by [behaviour tests](../../tests/e2e/accessibility-behavior.spec.js) and axe at 320 px. |
| 1.4.11 | Non-text Contrast | AA | Not evaluated | Focus indicators measured at 5.59:1 (light) and 5.09:1 (dark). Borders of inputs, cards and other graphical objects have not been measured. |
| 1.4.12 | Text Spacing | AA | Supports | With line-height 1.5, letter-spacing 0.12em and word-spacing 0.16em applied, nothing was clipped on Feed, Settings, Profile or Login ([machine preview run](manual/runs/2026-10-04-machine-preview.md)). |
| 1.4.13 | Content on Hover or Focus | AA | Supports | The reaction picker is hoverable, persistent and dismissible with Escape (A11Y-014, A11Y-018), by [behaviour tests](../../tests/e2e/accessibility-behavior.spec.js). |

## 2. Operable

| Criterion | Name | Level | Status | Evidence and notes |
| --- | --- | --- | --- | --- |
| 2.1.1 | Keyboard | A | Supports | Every control is operable by keyboard, including the post menu, reaction picker and comment box ([behaviour tests](../../tests/e2e/accessibility-behavior.spec.js)). The drag-and-drop upload zone has a button alternative. |
| 2.1.2 | No Keyboard Trap | A | Supports | An 80-stop Tab walk of the Feed found no trap, and widgets close with Escape. |
| 2.1.4 | Character Key Shortcuts | A | Not applicable | There are no single-character shortcuts. |
| 2.2.1 | Timing Adjustable | A | Supports | The only time limit is a 24-hour sign-in session, which is longer than 20 hours (the 20 hour exception). |
| 2.2.2 | Pause, Stop, Hide | A | Supports | Nothing moves, blinks or updates automatically beyond short transitions. |
| 2.3.1 | Three Flashes or Below Threshold | A | Supports | Nothing flashes. |
| 2.4.1 | Bypass Blocks | A | Supports | A skip link and a `main` landmark (A11Y-010), by [behaviour tests](../../tests/e2e/accessibility-behavior.spec.js). |
| 2.4.2 | Page Titled | A | Supports | Every route has its own title (A11Y-009), by [behaviour tests](../../tests/e2e/accessibility-behavior.spec.js). |
| 2.4.3 | Focus Order | A | Supports | Focus moves in and returns when menus, editors and comment boxes open and close (A11Y-007), by [behaviour tests](../../tests/e2e/accessibility-behavior.spec.js). Whether the order feels logical needs a person (manual script KB-04). |
| 2.4.4 | Link Purpose (In Context) | A | Not evaluated | Link text has not been reviewed out of context (manual script CT-04). Post "View" links are named for their author. |
| 2.4.5 | Multiple Ways | AA | Not evaluated | Pages are reachable through the navigation bar and profile links. There is no search or site map, and this has not been assessed. |
| 2.4.6 | Headings and Labels | AA | Not evaluated | Heading and label quality has not been reviewed (manual script CT-03). |
| 2.4.7 | Focus Visible | AA | Supports | A 3 px focus ring on every control (A11Y-011, A11Y-012), by [behaviour tests](../../tests/e2e/accessibility-behavior.spec.js). |
| 2.4.11 | Focus Not Obscured (Minimum) | AA | Supports | An 80-stop Tab walk with the sticky navbar never hid a focused control, by [behaviour tests](../../tests/e2e/accessibility-behavior.spec.js). |
| 2.5.1 | Pointer Gestures | A | Supports | No path-based or multi-point gestures. |
| 2.5.2 | Pointer Cancellation | A | Supports | Pressing Repost, dragging off and releasing does not trigger it ([machine preview run](manual/runs/2026-10-04-machine-preview.md)). |
| 2.5.3 | Label in Name | A | Not evaluated | Voice control (manual script PT-05) not yet tested. Visible labels are contained in accessible names by design (for example "View post by ..." for "View"). |
| 2.5.4 | Motion Actuation | A | Not applicable | No function is triggered by device motion. |
| 2.5.7 | Dragging Movements | AA | Supports | The only dragging is the upload drop zone, and the Add Media button is a single-pointer alternative. |
| 2.5.8 | Target Size (Minimum) | AA | Supports | No control on the Feed or Settings is under 24 by 24 CSS px, by [behaviour tests](../../tests/e2e/accessibility-behavior.spec.js) and axe `target-size`. |

## 3. Understandable

| Criterion | Name | Level | Status | Evidence and notes |
| --- | --- | --- | --- | --- |
| 3.1.1 | Language of Page | A | Supports | `<html lang="en">`. |
| 3.1.2 | Language of Parts | AA | Partially supports | The interface is English. User posts in other languages are not marked up with their language. |
| 3.2.1 | On Focus | A | Supports | Nothing changes context when a control receives focus. |
| 3.2.2 | On Input | A | Supports | Changing a setting does not submit or navigate until the user presses Save. |
| 3.2.3 | Consistent Navigation | AA | Supports | One shared layout renders the same navigation on every signed-in page. |
| 3.2.4 | Consistent Identification | AA | Not evaluated | Naming of repeated controls has not been reviewed (manual script CT-06). |
| 3.2.6 | Consistent Help | A | Not applicable | There is no help mechanism. |
| 3.3.1 | Error Identification | A | Supports | Errors name the field and are announced (A11Y-004, A11Y-019), by [behaviour tests](../../tests/e2e/accessibility-behavior.spec.js) and [component tests](../../frontend/src/tests/accessibility/a11y-regressions.test.jsx). |
| 3.3.2 | Labels or Instructions | A | Supports | Every input has a label: visible on Login and Register, visually hidden on the post composer (A11Y-001). Persistent visible labels are good practice beyond what 3.3.2 strictly requires. |
| 3.3.3 | Error Suggestion | AA | Partially supports | Validation errors suggest a fix for the email field. Others, such as "Username already taken", say what is wrong but not how to fix it. |
| 3.3.4 | Error Prevention (Legal, Financial, Data) | AA | Supports | Deleting a post, removing a picture and deleting an account all ask for confirmation, and account deletion asks twice. |
| 3.3.7 | Redundant Entry | A | Not applicable | No multi-step flow asks for the same information twice. |
| 3.3.8 | Accessible Authentication (Minimum) | AA | Supports | No cognitive function test. Paste works, and fields carry `autocomplete` tokens ([behaviour tests](../../tests/e2e/accessibility-behavior.spec.js)). Password manager behaviour needs a person to confirm (manual script FM-05). |

## 4. Robust

| Criterion | Name | Level | Status | Evidence and notes |
| --- | --- | --- | --- | --- |
| 4.1.2 | Name, Role, Value | A | Supports | Named controls, exposed state (`aria-expanded`, `aria-pressed`), no nested interactive elements, unique ids, decorative emoji kept out of names (A11Y-005, 006, 015, 017, 020), by [axe scans](../../tests/e2e/accessibility-axe.spec.js) and [component tests](../../frontend/src/tests/accessibility/a11y-regressions.test.jsx). |
| 4.1.3 | Status Messages | AA | Supports | Errors use `role="alert"`, confirmations use `role="status"`, and a live region announces reactions, reposts, comments, deletions and page changes (A11Y-004, A11Y-013). The text is tested. **Whether it is spoken needs a person with a screen reader.** |

## Known limitations and next steps

1. **Run the manual scripts with a person.** Start with VoiceOver and NVDA, then the zoom, contrast and voice control scripts.
   Every "Not evaluated" row should be turned into a result.
2. **Add alternative text and captions for user-uploaded media.** These are the only "Does not support" rows.
3. **Test with disabled users.** No script replaces it.
4. **Re-issue this report** when the product changes, and keep the date current. A report is a snapshot.

## Reading a conformance report

If a vendor gives you one, check three things before you trust it: **who** evaluated the product (the vendor or someone
independent), **how** (automated tools alone cannot decide most criteria), and whether it contains any "Does not support" or
"Not evaluated" rows. A report with none of them is usually a sign that nobody looked closely.
