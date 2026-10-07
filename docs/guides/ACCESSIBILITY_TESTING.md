# Accessibility Testing Guide

**Making Testbook accessible to all users**

---

<h2 id="why-accessibility-matters">Why Accessibility Matters</h2>

**Legal Requirements:**

- ADA (Americans with Disabilities Act) compliance required for many websites
- WCAG 2.1 AA is the international standard
- Non-compliance can result in lawsuits and fines

**Ethical & Business Reasons:**

- 15% of the global population has some form of disability
- Accessible design benefits everyone (better UX)
- Improves SEO and mobile experience
- Demonstrates inclusive company values

---

<h2 id="accessibility-testing-pyramid">Accessibility Testing Pyramid</h2>

```text
     Manual Testing (60%)
    - Screen readers
    - Keyboard navigation
    - Real user testing
   ↑
   |
  Automated Testing (40%)
 - axe-core
 - Lighthouse
 - WCAG validators
```

**Both are essential!** Automation catches obvious issues, manual testing catches context and flow.

---

<h2 id="testing-approaches-in-testbook">Testing Approaches in Testbook</h2>

### 1. Unit-Level Accessibility (Frontend Component Tests)

**Location:** `frontend/src/tests/accessibility/accessibility.test.jsx`

**What it tests:**

- Component-level WCAG compliance
- ARIA attributes
- Form labels
- Semantic HTML

**Run:**

```bash
cd frontend
npm test -- accessibility.test.jsx
```

**Example test:**

```jsx
import { axe } from "vitest-axe";

it("Login page should have no accessibility violations", async () => {
  const { container } = renderWithRouter(<LoginPage />);
  const results = await axe(container, {
    rules: { "color-contrast": { enabled: false } }, // needs canvas, unavailable in jsdom
  });
  expect(results.violations).toEqual([]);
});
```

---

### 2. E2E Accessibility (Playwright + axe-core)

**Location:** `tests/e2e/accessibility-axe.spec.js`

**What it tests:**

- Full page WCAG 2.1 AA compliance
- Navigation flows
- Authenticated pages
- Dynamic content

**Run:**

```bash
cd tests
npm run test:a11y
```

**Example test:**

```javascript
import AxeBuilder from "@axe-core/playwright";

test("Home page should not have accessibility violations", async ({ page }) => {
  await page.goto("http://localhost:3000/");

  const accessibilityScanResults = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
    .analyze();

  expect(accessibilityScanResults.violations).toEqual([]);
});
```

---

### 3. Performance & Accessibility (Lighthouse CI)

**Configuration:** `lighthouserc.js` (root directory)

**What it tests:**

- Overall accessibility score (0-100)
- Performance metrics
- Best practices
- SEO

It audits **six pages, including the signed-in ones** (Feed, Post detail, Profile,
Settings). Lighthouse starts every run logged out, and the app redirects a logged-out visit
to `/login`, so `tests/lighthouse/login.cjs` signs in first (a Lighthouse CI
`puppeteerScript`). The accessibility score must be at least 0.95; performance, best
practices and SEO only warn.

**Run:**

```bash
# Start the app first (./start-dev.sh), with seeded data
make lighthouse            # or: cd tests && npm run lighthouse
```

**Reports saved to:** `tests/reports/lighthouse/` (HTML and JSON)

---

<h2 id="what-we-test-for">What We Test For</h2>

### WCAG 2.1 Level AA Criteria

#### 1. **Perceivable**

- Alt text for all images
- Sufficient color contrast (4.5:1 for text)
- Text resizable to 200% without loss of content
- No information conveyed by color alone

#### 2. **Operable**

- All functionality available via keyboard
- No keyboard traps
- Skip links for navigation
- Clear focus indicators
- Sufficient time to read content

#### 3. **Understandable**

- Page language declared
- Consistent navigation
- Form labels and error messages
- Input assistance for errors

#### 4. **Robust**

- Valid HTML
- ARIA attributes used correctly
- Works with assistive technologies

---

<h2 id="tools-we-use">Tools We Use</h2>

### 1. axe-core

**What:** Industry-leading accessibility testing engine
**Coverage:** ~40% of WCAG issues
**Used in:** Component tests, E2E tests

**Install:** (already a devDependency in this repo — `@axe-core/playwright` in `tests/package.json`, `vitest-axe` in `frontend/package.json`)

```bash
npm install --save-dev @axe-core/playwright vitest-axe
```

### 2. Lighthouse

**What:** Google's web quality tool
**Coverage:** Performance + Accessibility + Best Practices + SEO
**Used in:** Performance baseline testing

**Install:** (already a devDependency in `tests/package.json`)

```bash
npm install --save-dev @lhci/cli
```

### 3. eslint-plugin-jsx-a11y

**What:** Linter for React accessibility
**Coverage:** JSX-specific accessibility issues
**Used in:** ESLint checks during development

**Install:** (already a devDependency in `frontend/package.json`)

```bash
npm install --save-dev eslint-plugin-jsx-a11y
```

---

<h2 id="running-tests">Running Tests</h2>

### Quick Check (All Accessibility Tests)

```bash
# Frontend component tests
cd frontend
npm test -- accessibility.test.jsx

# E2E accessibility tests
cd tests
npm run test:a11y

# Lighthouse audit
make lighthouse

# Everything automated (component + E2E)
make test-a11y
```

### In CI/CD

Accessibility tests run automatically on every PR:

- Component-level (vitest-axe plus the regression tests), in `frontend-tests.yml`
- E2E level (axe-core via `@axe-core/playwright`, plus the behaviour specs) and
  Lighthouse, in the dedicated `accessibility.yml` workflow, which uploads the Playwright
  report (with the axe violation JSON) and the Lighthouse reports as artifacts
- The full `e2e-tests.yml` run also executes the same specs

---

<h2 id="common-issues-fixes">Common Issues & Fixes</h2>

### Issue: "Form elements must have labels"

**Bad:**

```jsx
<input type="email" placeholder="Email" />
```

**Good:**

```jsx
<label htmlFor="email">Email</label>
<input id="email" type="email" placeholder="your@email.com" />
```

---

### Issue: "Images must have alt text"

**Bad:**

```jsx
<img src="profile.jpg" />
```

**Good:**

```jsx
<img src="profile.jpg" alt="John Doe profile picture" />
```

---

### Issue: "Insufficient color contrast"

**Bad:**

```css
color: #999; /* Light gray on white = 2.85:1 */
background: #fff;
```

**Good:**

```css
color: #595959; /* Dark gray on white = 4.6:1 */
background: #fff;
```

**Tool:** Use [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

---

### Issue: "Button must have accessible name"

**Bad:**

```jsx
<button>
  <Icon />
</button>
```

**Good:**

```jsx
<button aria-label="Close dialog">
  <Icon />
</button>
```

---

### Issue: "Heading levels should increase by one"

**Bad:**

```jsx
<h1>Main Title</h1>
<h3>Subsection</h3> {/* Skipped h2 */}
```

**Good:**

```jsx
<h1>Main Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
```

---

## Manual Testing Checklist

> **Full scripted suite:** this checklist is the short version. The step-by-step manual
> tests, with expected results and a run sheet, are in
> [`docs/a11y/manual/`](../a11y/manual/README.md). Start there.

### Keyboard Navigation

- [ ] Tab through all interactive elements
- [ ] No keyboard traps
- [ ] Skip links work
- [ ] Clear focus indicators visible
- [ ] Can close modals with Escape

### Screen Reader Testing

- [ ] Test with NVDA (Windows) or VoiceOver (Mac)
- [ ] All images have meaningful alt text
- [ ] Form errors announced
- [ ] Page title accurate
- [ ] Landmarks identified

### Zoom Testing

- [ ] Test at 200% zoom
- [ ] No horizontal scrolling
- [ ] All content readable
- [ ] Buttons/links still usable

---

## Accessibility Scores

### Current Testbook Scores

Real numbers from a pre-merge accessibility review (see "Known Application
Accessibility State" below for the full story, including what this table
doesn't cover):

| Page | axe-core Violations (WCAG + best-practice) | Lighthouse Score |
| --- | --- | --- |
| Login | 0 | 100 |
| Register | 0 | 100 |
| Feed | 0 | 100 |
| Post Detail | 0 | 100 |
| Profile | 0 | 100 |
| Settings | 0 | 100 |

**Goal:** 0 violations, 95+ Lighthouse score - met on every page. The signed-in pages are
measured by Lighthouse through a login script (`tests/lighthouse/login.cjs`). A
Lighthouse score of 100 does not mean the page is accessible: it runs a subset of axe's
rules, and several real defects (see `docs/a11y/AUDIT_LOG.md`) passed it. Treat it as a
regression guard.

---

## Known Application Accessibility State

A pre-merge accessibility review (2026-09) audited every real page in the
app - Login, Register, Feed, Post Detail, Profile, Settings - with axe-core
run directly (`axe.run()`, no tag filter), not just through the existing
`accessibility-axe.spec.js` suite. That distinction matters: it's the reason
this review found real bugs the existing, passing test suite had missed.

### What was found and fixed

The existing `accessibility-axe.spec.js` suite scoped its checks to
`['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']` and had been reporting zero
violations. That was a true result, but a narrower one than it sounds: four
real structural issues existed on every page, and none of them map to a
specific WCAG success criterion, so none of them were in scope for that tag
filter.

- **No `<main>` landmark anywhere in the app.** Every page's content sat
  directly under the page root with no landmark region wrapping it - a
  screen reader user has no way to jump straight to the page's main content
  and skip repeated navigation chrome. Fixed by wrapping the shared
  authenticated layout's content in a `<main>` element
  ([App.jsx](../../frontend/src/App.jsx)'s `PrivateLayout`) and changing
  Login and Register's outermost container from a `<div>` to a `<main>`
  (both are pure element-tag changes - the CSS targets the existing class
  names, not the tag, so nothing visual changed).
- **Feed, Post Detail, and Profile had no `<h1>`.** A screen reader user
  navigating by heading has no way to identify what page they're on. Fixed
  by adding a visually-hidden `<h1>` (a new `.sr-only` utility class in
  [index.css](../../frontend/src/index.css)) to Feed and Post Detail, and by
  promoting Profile's existing `<h2>` display-name heading to `<h1>` - it
  already was the page's real headline, just at the wrong level.
- **Heading order skipped a level on Post Detail and Profile** once the new
  `<h1>`s existed and made the skip visible (`heading-order` couldn't flag
  an `<h1>`-to-`<h3>` jump when there was no `<h1>` to jump from). Fixed by
  changing Post Detail's "Comments" heading and Profile's "Posts" heading
  from `<h3>` to `<h2>`.

All four were moderate-severity, none critical or serious, and none were
intentional teaching examples - they were genuine oversights. A re-run with
axe-core's default rule set (WCAG plus best-practice rules) found 0
violations across all six audited pages after the fix.

### The test-suite gap, and why it was closed here too

Fixing the app without also fixing why the existing suite missed this would
leave the same blind spot in place for the next regression. `landmark-one-main`,
`region`, `page-has-heading-one`, and `heading-order` are all tagged
`best-practice` in axe-core, not any WCAG tag - confirmed directly against
this repo's own `axe-core` package (`axe.getRules()`), not assumed.
`accessibility-axe.spec.js` now includes `'best-practice'` in its tag list,
so this exact class of issue - a missing landmark, a missing top-level
heading, a broken heading order - will fail CI going forward instead of
passing silently. If you're extending this suite to a new page, keep the
tag list as-is; narrowing it back to WCAG-only tags would reopen this gap.

### What's still not covered

- **Screen reader testing has not been done by a person yet.** The scripted manual suite
  is in [`docs/a11y/manual/`](../a11y/manual/README.md). Automated tools catch a
  meaningful chunk of WCAG issues but not all of them; whether live-region announcements
  are actually *spoken* can only be checked with a real screen reader.

---

## For Your Portfolio

When discussing accessibility in interviews:

**Example talking point:**

> "I implemented comprehensive accessibility testing for Testbook using a three-tier approach: component-level testing with vitest-axe, E2E testing with Playwright and axe-core for full WCAG 2.1 AA compliance, and Lighthouse CI for performance and accessibility baselines. I achieved zero accessibility violations across all key pages and maintained a 90+ Lighthouse accessibility score."

**Resume bullet:**

> • Implemented automated WCAG 2.1 AA accessibility testing using axe-core and Lighthouse CI, achieving zero violations across 5 key user flows and maintaining 90+ accessibility score

---

<h2 id="additional-resources">Additional Resources</h2>

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [axe-core Documentation](https://github.com/dequelabs/axe-core)
- [WebAIM Resources](https://webaim.org/)
- [A11y Project](https://www.a11yproject.com/)
- [Screen Reader Testing](https://webaim.org/articles/screenreader_testing/)

---

<h2 id="checklist-for-new-features">Checklist for New Features</h2>

When adding new features, ensure:

- [ ] All images have alt text
- [ ] Forms have proper labels
- [ ] Color contrast meets 4.5:1
- [ ] Keyboard navigation works
- [ ] ARIA attributes added where needed
- [ ] Component accessibility test written
- [ ] E2E accessibility test updated
- [ ] Manual keyboard testing performed
- [ ] Tested with screen reader (if possible)

---

**Remember:** Accessibility is not a "nice to have" — it's a requirement, both legally and ethically. Good accessibility makes the app better for everyone!
