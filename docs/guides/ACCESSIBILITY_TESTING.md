# ♿ Accessibility Testing Guide

**Making Testbook accessible to all users**

---

## 🎯 Why Accessibility Matters

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

## 📊 Accessibility Testing Pyramid

```
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

## 🧪 Testing Approaches in Testbook

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
import { axe } from 'vitest-axe';

it('Login page should have no accessibility violations', async () => {
  const { container } = render(<LoginPage />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
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
import AxeBuilder from '@axe-core/playwright';

test('Home page should not have accessibility violations', async ({ page }) => {
  await page.goto('http://localhost:3000/');

  const accessibilityScanResults = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
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

**Run:**
```bash
# Start the app first
cd frontend && npm run dev

# In another terminal
cd /path/to/testbook
npx lhci autorun
```

**Reports saved to:** `reports/lighthouse/`

---

## 🔍 What We Test For

### WCAG 2.1 Level AA Criteria

#### 1. **Perceivable**
- ✅ Alt text for all images
- ✅ Sufficient color contrast (4.5:1 for text)
- ✅ Text resizable to 200% without loss of content
- ✅ No information conveyed by color alone

#### 2. **Operable**
- ✅ All functionality available via keyboard
- ✅ No keyboard traps
- ✅ Skip links for navigation
- ✅ Clear focus indicators
- ✅ Sufficient time to read content

#### 3. **Understandable**
- ✅ Page language declared
- ✅ Consistent navigation
- ✅ Form labels and error messages
- ✅ Input assistance for errors

#### 4. **Robust**
- ✅ Valid HTML
- ✅ ARIA attributes used correctly
- ✅ Works with assistive technologies

---

## 🛠️ Tools We Use

### 1. axe-core
**What:** Industry-leading accessibility testing engine
**Coverage:** ~40% of WCAG issues
**Used in:** Component tests, E2E tests

**Install:**
```bash
npm install --save-dev @axe-core/playwright vitest-axe
```

### 2. Lighthouse
**What:** Google's web quality tool
**Coverage:** Performance + Accessibility + Best Practices + SEO
**Used in:** Performance baseline testing

**Install:**
```bash
npm install --save-dev @lhci/cli
```

### 3. eslint-plugin-jsx-a11y
**What:** Linter for React accessibility
**Coverage:** JSX-specific accessibility issues
**Used in:** ESLint checks during development

**Install:**
```bash
npm install --save-dev eslint-plugin-jsx-a11y
```

---

## 🚀 Running Tests

### Quick Check (All Accessibility Tests)
```bash
# Frontend component tests
cd frontend
npm test -- accessibility.test.jsx

# E2E accessibility tests
cd tests
npm run test:a11y

# Lighthouse audit
npx lhci autorun
```

### In CI/CD
All accessibility tests run automatically on every PR:
- Component-level (vitest-axe)
- E2E level (axe-playwright)
- Lighthouse scores checked

---

## 🐛 Common Issues & Fixes

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
<button><Icon /></button>
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

## 🧑‍🦯 Manual Testing Checklist

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

## 📈 Accessibility Scores

### Current Testbook Scores

| Page | axe-core Violations | Lighthouse Score |
|------|---------------------|------------------|
| Home | 0 | TBD |
| Register | 0 | TBD |
| Login | 0 | TBD |
| Feed | 0 | TBD |
| Profile | 0 | TBD |

**Goal:** 0 violations, 90+ Lighthouse score

---

## 💼 For Your Portfolio

When discussing accessibility in interviews:

**Example talking point:**
> "I implemented comprehensive accessibility testing for Testbook using a three-tier approach: component-level testing with vitest-axe, E2E testing with Playwright and axe-core for full WCAG 2.1 AA compliance, and Lighthouse CI for performance and accessibility baselines. I achieved zero accessibility violations across all key pages and maintained a 90+ Lighthouse accessibility score."

**Resume bullet:**
> • Implemented automated WCAG 2.1 AA accessibility testing using axe-core and Lighthouse CI, achieving zero violations across 5 key user flows and maintaining 90+ accessibility score

---

## 📚 Additional Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [axe-core Documentation](https://github.com/dequelabs/axe-core)
- [WebAIM Resources](https://webaim.org/)
- [A11y Project](https://www.a11yproject.com/)
- [Screen Reader Testing](https://webaim.org/articles/screenreader_testing/)

---

## ✅ Checklist for New Features

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

