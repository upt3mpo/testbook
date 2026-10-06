# Stage 0 Answer Keys

Read these **after** you have written your own answers. The point of each exercise is to
form your own view first and then compare. Several answers are judgement calls, and where
reasonable people differ the key says so.

## Exercise 0.1: what you should have observed

Wording and numbers can differ a little by browser and screen reader. What matters is that
you noticed the same underlying problem.

| Task | Broken page: what happens | Fixed page: what is different |
| --- | --- | --- |
| K1 Invisible Tab stops | From **React**, it takes **four** presses to reach **Comment**. Three of them land on controls you cannot see (Like, Love, Haha), and nothing visibly changes on screen | One press. Closed controls are not in the Tab order |
| K2 Lost focus | After choosing **Edit**, typing goes nowhere: focus fell back to the page because the Edit button disappeared. The same happens after **Cancel** | Typing goes straight into the edit box. After Cancel, focus returns to **Post options** |
| K3 Button inside a link | **View** has two Tab stops: the link, then the button inside it | One stop |
| S1 Silent error | The error appears on screen, but a screen reader says nothing. In the inspector there is no `alert` role | The error has the `alert` role, is announced, and focus moves to it |
| S2 Test id hides the bug | The menu button's only name is the ellipsis symbol (a reader may say "horizontal ellipsis" or similar), which says nothing about what it does | Named "Post options" |
| V1 Dark-mode contrast | White text on the button is about **3.45:1**, below the 4.5:1 needed, and is noticeably harder to read at low brightness | About **5.2:1**, which passes |
| V2 Placeholder as label | The word "Email" vanishes as soon as you type, so after a pause you cannot tell what the field is for | A visible label stays on screen |
| M1 Same title everywhere | The tab title never changes as you move between views, so many open tabs or a history list all look identical | The title follows the page ("Settings - Testbook") and the change is announced |

## Exercise 0.2: suggested mapping

Your wording will differ. Check that your **principle** and **criterion** are close, and that you
found a permanent, a temporary and a situational example.

| Task | People affected (permanent / temporary / situational) | POUR | WCAG criterion |
| --- | --- | --- | --- |
| K1 | Switch or keyboard-only user / wrist in a cast / broken trackpad or a kiosk with no mouse | Operable | 2.4.7 Focus Visible |
| K2 | Keyboard and screen reader users / hand injury, using only the keyboard / interrupted mid-task and loses their place | Operable | 2.4.3 Focus Order |
| K3 | Screen reader users, who hear the control twice / repetitive strain, wanting fewer keystrokes / (no clear situational case: an honest gap) | Robust | 4.1.2 Name, Role, Value |
| S1 | Blind and low-vision users / eye surgery recovery / listening with the screen off or looking away | Robust | 4.1.3 Status Messages |
| S2 | Blind users, and voice-control users who cannot say a name they cannot see / recovering from eye surgery / hands busy, using voice control | Robust | 4.1.2 Name, Role, Value |
| V1 | Low vision / tired or dilated eyes / glare or a dimmed battery-saver screen | Perceivable | 1.4.3 Contrast (Minimum) |
| V2 | Memory, attention and cognitive disabilities, dyslexia / concussion or fatigue / interrupted, or reading in a second language | Understandable | 3.3.2 Labels or Instructions (also 1.3.1) |
| M1 | Screen reader users (the title is read first), and people with cognitive disabilities / someone with eight tabs open / looking back through browser history | Operable | 2.4.2 Page Titled |

**On the curb cut (Step 4):** for K1 the fix helps everyone using a keyboard shortcut or a
broken trackpad. For V1 it helps everyone in sunlight. For S1 it helps anyone not looking at
the screen. Your own example is the right answer if it names people nobody listed when the
bug was written.

## Exercise 0.3: the prevention matrix

> **This is a judgement exercise.** "Earliest layer that could have prevented it" has more than
> one defensible answer for many rows. If yours differs, check that you can justify it in a
> sentence. The layer numbers are: 1 requirements and design, 2 components and design system,
> 3 code review and lint, 4 unit and component tests, 5 automated end-to-end tests, 6 manual
> testing, 7 real users.

| Audit ID | What went wrong | Earliest prevention | Default axe scan? | First found by (in our history) |
| --- | --- | --- | --- | --- |
| A11Y-001 | Inputs labelled only by a placeholder | Layer 2: a field component that cannot be created without a label | No: axe accepts a placeholder as a name | Reading the markup during the audit |
| A11Y-002 | Edit textarea with no name | Layer 2: the same field component | Partly: only with the edit box open | Layer 5: axe scanning the edit state |
| A11Y-003 | No `autocomplete` tokens | Layer 3: a review checklist or lint for auth forms | No: axe does not flag an absent token | Reading the code, while preparing the 3.3.8 checks |
| A11Y-004 | Error not announced, and failed contrast | Layer 2: an `Alert` component | Partly: contrast only, and only with the error showing | Layer 5: axe on the error state (announcement: manual) |
| A11Y-005 | A button inside a link | Layer 2: a link-styled-as-button component | Partly: only through a WCAG 2.2 rule the old suite did not enable | Layer 5: scripted browser checks |
| A11Y-006 | Icon-only and state-less menu buttons | Layer 2: an icon-button component that requires a name | No: a glyph counts as a name | Layer 5: a scripted check for unnamed controls |
| A11Y-007 | Focus lost when something closes | Layer 2: a menu or disclosure component that manages focus | No | Layer 5: scripted focus checks |
| A11Y-008 | Horizontal scroll at 320 px | Layer 1: a 320 px requirement in the definition of done | No | Layer 5: a scripted overflow check |
| A11Y-009 | The same page title on every route | Layer 2: a routing convention that requires a title | No: a title exists | Layer 5: scripted title checks |
| A11Y-010 | No skip link | Layer 1: the layout template includes one | No | Reviewing the page structure |
| A11Y-011 | Focus outline removed | Layer 2: a global focus style in the design tokens (or a lint rule) | No | Layer 5: a computed-style check |
| A11Y-012 | Hidden controls still in the Tab order | Layer 3: code review of the hiding technique | No | Reading the CSS |
| A11Y-013 | No live region anywhere | Layer 1: "how is this change announced?" asked at design time | No | Searching the code for live regions |
| A11Y-014 | Hover and click fought over one state | Layer 2: a single-writer disclosure component | No | A keyboard test that behaved inconsistently |
| A11Y-015 | Active tab shown by colour only | Layer 2: a toggle component that exposes its state | No | Writing the screen reader script |
| A11Y-016 | Dark-mode contrast failures | Layer 1: colour tokens by role, and "every theme" in the definition of done | Partly: yes if you scan dark mode | Layer 5: axe in dark theme |
| A11Y-017 | Duplicate ids from the fix for A11Y-006 | Layer 3: review (use a generated id) | Partly: reported as "incomplete" | Layer 5: axe |
| A11Y-018 | Hover content not dismissible | Layer 1: review against WCAG 1.4.13 when adding hover reveal | No | Writing the zoom and hover script |

### The totals

| Question | Count |
| --- | --- |
| Defects a default axe scan could have caught on its own | **0 of 18**. The original suite reported zero violations |
| Defects axe could catch with states, themes or the WCAG 2.2 tag | 5 of 18 (002, 004, 005, 016, 017), and only partly |
| Defects that could have been prevented at layers 1 to 3 | **18 of 18**: 5 at layer 1, 10 at layer 2, 3 at layer 3 |
| Defects that needed layer 5 or later to find | The majority, found by scripted browser checks, reading, or writing the manual scripts |

### What to take from it

- **Layer 2 dominates.** Ten of the eighteen are best prevented by a shared component that makes
  the right thing the only easy thing. That is a design-system decision, not a testing one.
- **Tools are blind to most of it.** Thirteen of eighteen are invisible to axe in any state,
  because they depend on time, on judgement, or on what a screen reader does.
- **Prevention is cheap and testing is not free.** Every one of these could have been stopped
  earlier. And the ones testing did find needed browser-driven checks, not a simple scan.

### Common questions

- *"Isn't this hindsight?"* Partly, and that is fine. Hindsight is how teams learn what to
  add to a definition of done. The point is the pattern, not blame.
- *"So is testing pointless?"* No. Testing found all 18, and it keeps them from coming back.
  It is the last line of defence, not the first.

## Exercise 0.3, Step 5: acceptance criteria

A strong set covers these ideas, in your own words. Check each of yours is **testable**.

- Keyboard operation and visible, managed focus
- A visible, persistent label for every input
- Announcements for changes that have no visible message
- Errors that explain and are announced
- Every theme, and 400% zoom or 320 px width
- A distinct page title per route
- A meaningful name for every control, including icon-only ones

If a criterion cannot be failed, it is a wish, not a criterion.
