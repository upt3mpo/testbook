/**
 * Accessibility behaviour tests (things axe-core cannot see).
 *
 * axe inspects one DOM snapshot. It cannot tell you where focus went after a
 * click, whether a message was announced, what the Tab order is, whether the
 * page scrolls sideways on a phone, or whether a sticky header covers the focused
 * control. Those need a real browser driven like a keyboard user, which is what
 * these tests do.
 *
 * Each test names the audit ID it guards (docs/a11y/AUDIT_LOG.md) and the WCAG
 * criterion. Contrast and anything else needing computed colour is covered by the
 * axe scans in accessibility-axe.spec.js.
 *
 * Run with: npm run test:a11y   (or: npx playwright test accessibility-behavior)
 */

import { expect, test } from '@playwright/test';
import { resetDatabase, TEST_USERS } from './fixtures/test-helpers.js';
import { AuthPage } from './pages/AuthPage.js';

async function loginAsSarah(page) {
  const auth = new AuthPage(page);
  await auth.gotoLogin();
  await auth.login(TEST_USERS.sarah.email, TEST_USERS.sarah.password);
  await auth.expectLoggedIn();
  await page
    .getByTestId('post-1')
    .waitFor()
    .catch(() => {});
}

/** A short, stable description of the focused element, for tab-order assertions. */
const focused = (page) =>
  page.evaluate(() => {
    const el = document.activeElement;
    return (
      el.getAttribute('data-testid') ||
      el.getAttribute('id') ||
      el.getAttribute('aria-label') ||
      el.tagName.toLowerCase()
    );
  });

/** The id of a seeded post that belongs to Sarah (so the menu button exists). */
const ownPostId = (page) => page.locator('[data-is-own-post="true"]').first().getAttribute('data-post-id');

test.describe('Accessibility behaviour', () => {
  test.beforeEach(async ({ page }) => {
    await resetDatabase(page);
  });

  test('login: Tab order is email, password, submit, create-account (2.4.3)', async ({ page }) => {
    await page.goto('/login');
    const order = [];
    for (let i = 0; i < 4; i++) {
      await page.keyboard.press('Tab');
      order.push(await focused(page));
    }
    expect(order).toEqual([
      'login-email-input',
      'login-password-input',
      'login-submit-button',
      'create-account-button',
    ]);
  });

  test('login: the whole form works by keyboard alone (2.1.1)', async ({ page }) => {
    await page.goto('/login');
    await page.keyboard.press('Tab');
    await page.keyboard.type(TEST_USERS.sarah.email);
    await page.keyboard.press('Tab');
    await page.keyboard.type(TEST_USERS.sarah.password);
    await page.keyboard.press('Enter');
    await expect(page.getByTestId('navbar')).toBeVisible();
  });

  test('A11Y-003/3.3.8: password fields accept paste', async ({ page }) => {
    await page.goto('/login');
    const blocked = await page.getByLabel('Password').evaluate((el) => {
      const event = new Event('paste', { bubbles: true, cancelable: true });
      el.dispatchEvent(event);
      return event.defaultPrevented;
    });
    expect(blocked).toBe(false);
  });

  test('A11Y-004: a failed login is announced and takes focus (4.1.3, 2.4.3)', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel('Email').fill('nobody@example.com');
    await page.getByLabel('Password').fill('wrong-password');
    await page.keyboard.press('Enter');

    const alert = page.getByRole('alert');
    await expect(alert).toBeVisible();
    // Focus must not fall back to <body> when the submit button re-enables.
    await expect(alert).toBeFocused();
  });

  test('A11Y-009: every route has its own title (2.4.2)', async ({ page }) => {
    await page.goto('/login');
    await expect(page).toHaveTitle('Log In - Testbook');
    await page.goto('/register');
    await expect(page).toHaveTitle('Sign Up - Testbook');

    await loginAsSarah(page);
    await expect(page).toHaveTitle('Home - Testbook');
    await page.goto('/settings');
    await expect(page).toHaveTitle('Settings - Testbook');
    await page.goto(`/profile/${TEST_USERS.sarah.username}`);
    await expect(page).toHaveTitle(`${TEST_USERS.sarah.displayName} (@sarahjohnson) - Testbook`);
    await page.goto(`/profile/${TEST_USERS.sarah.username}/followers`);
    await expect(page).toHaveTitle('Followers of @sarahjohnson - Testbook');
    await page.goto(`/profile/${TEST_USERS.sarah.username}/following`);
    await expect(page).toHaveTitle('People @sarahjohnson follows - Testbook');
    await page.goto('/post/1');
    await expect(page).toHaveTitle(/^Post by .+ - Testbook$/);
  });

  test('A11Y-013: client-side navigation is announced (4.1.3)', async ({ page }) => {
    await loginAsSarah(page);
    await page.getByTestId('navbar-settings-link').click();
    await expect(page.getByTestId('live-region')).toHaveText('Settings - Testbook');
  });

  test('A11Y-010: a skip link is the first Tab stop and moves focus to main (2.4.1)', async ({ page }) => {
    await loginAsSarah(page);
    await page.keyboard.press('Tab');
    const skip = page.getByRole('link', { name: 'Skip to main content' });
    await expect(skip).toBeFocused();
    await expect(skip).toBeVisible(); // not just focusable - visible once focused

    await page.keyboard.press('Enter');
    await expect(page.locator('main')).toBeFocused();
  });

  test('A11Y-011: inputs show a focus indicator (2.4.7, 1.4.11)', async ({ page }) => {
    await page.goto('/login');
    await page.keyboard.press('Tab'); // keyboard focus, so :focus-visible applies
    const style = await page.getByLabel('Email').evaluate((el) => {
      const s = getComputedStyle(el);
      return { style: s.outlineStyle, width: parseFloat(s.outlineWidth) };
    });
    expect(style.style).not.toBe('none');
    expect(style.width).toBeGreaterThanOrEqual(2);
  });

  test('A11Y-008: no horizontal scroll at 320px (1.4.10)', async ({ page }) => {
    await page.setViewportSize({ width: 320, height: 700 });
    await loginAsSarah(page);
    for (const path of ['/', '/settings', `/profile/${TEST_USERS.sarah.username}`, '/post/1']) {
      await page.goto(path);
      await page.waitForLoadState('networkidle');
      const overflow = await page.evaluate(
        () => document.documentElement.scrollWidth - document.documentElement.clientWidth
      );
      expect(overflow, `${path} overflows by ${overflow}px`).toBeLessThanOrEqual(0);
    }
  });

  test('A11Y-012: closed reaction pickers add no Tab stops (2.4.7)', async ({ page }) => {
    await loginAsSarah(page);
    await page.mouse.click(5, 300); // park focus at the top of the page
    const stops = [];
    for (let i = 0; i < 40; i++) {
      await page.keyboard.press('Tab');
      stops.push(await focused(page));
    }
    expect(stops.filter((id) => id.includes('-reaction-'))).toEqual([]);
  });

  test('A11Y-006: the reaction picker opens and closes by keyboard (2.1.1)', async ({ page }) => {
    await loginAsSarah(page);
    // exact: true - "React" would otherwise also match "Your reaction: like. Change reaction"
    const react = page.getByRole('button', { name: 'React', exact: true }).first();
    await react.focus();
    await page.keyboard.press('Enter');
    await expect(react).toHaveAttribute('aria-expanded', 'true');
    // Wait until the picker is actually visible (it fades in) before tabbing: a
    // sighted keyboard user sees it open first, and Tab skips hidden controls.
    const like = page.getByRole('button', { name: 'Like', exact: true }).first();
    await expect(like).toBeVisible();

    await page.keyboard.press('Tab');
    await expect(like).toBeFocused();

    await page.keyboard.press('Escape');
    await expect(react).toHaveAttribute('aria-expanded', 'false');
    await expect(react).toBeFocused();
  });

  test('A11Y-014: a real mouse click opens the picker and aria-expanded agrees', async ({ page }) => {
    await loginAsSarah(page);
    const react = page.getByRole('button', { name: 'React', exact: true }).first();
    await react.click(); // Playwright hovers, then clicks, like a real pointer
    await expect(react).toHaveAttribute('aria-expanded', 'true');
    await expect(page.getByRole('button', { name: 'Like', exact: true }).first()).toBeVisible();

    // Moving the pointer away must not close it; clicking elsewhere does.
    await page.mouse.move(0, 0);
    await expect(react).toHaveAttribute('aria-expanded', 'true');
    await page.mouse.click(5, 300);
    await expect(react).toHaveAttribute('aria-expanded', 'false');
  });

  test('A11Y-017: no duplicate ids on the feed (4.1.2, aria-controls targets)', async ({ page }) => {
    await loginAsSarah(page);
    // The seed data has reposts, which embed the original post: a second copy of
    // a post already on the page. Any id derived from the post id would collide.
    await expect(page.locator('[data-is-repost="true"]').first()).toBeVisible();
    const duplicates = await page.evaluate(() => {
      const seen = new Map();
      for (const el of document.querySelectorAll('[id]')) {
        seen.set(el.id, (seen.get(el.id) || 0) + 1);
      }
      return [...seen].filter(([, count]) => count > 1).map(([id]) => id);
    });
    expect(duplicates).toEqual([]);
  });

  test('A11Y-015: the active Feed tab is exposed to assistive technology', async ({ page }) => {
    await loginAsSarah(page);
    const all = page.getByRole('button', { name: 'See All' });
    const following = page.getByRole('button', { name: 'Following' });
    await expect(all).toHaveAttribute('aria-pressed', 'true');
    await following.click();
    await expect(following).toHaveAttribute('aria-pressed', 'true');
    await expect(all).toHaveAttribute('aria-pressed', 'false');
  });

  test('A11Y-018: Escape dismisses a hover-revealed picker without moving the pointer (1.4.13)', async ({ page }) => {
    await loginAsSarah(page);
    const react = page.getByRole('button', { name: 'React', exact: true }).first();
    const like = page.getByRole('button', { name: 'Like', exact: true }).first();

    await react.hover(); // hover only: no click, no focus
    await expect(like).toBeVisible(); // revealed by hover (CSS :hover)

    // Hoverable: the pointer can travel onto the picker without it vanishing.
    await like.hover();
    await expect(like).toBeVisible();

    // Dismissible: Escape hides it while the pointer stays exactly where it is.
    await page.keyboard.press('Escape');
    await expect(like).toBeHidden();

    // Moving away and back brings it back.
    await page.mouse.move(0, 0);
    await react.hover();
    await expect(like).toBeVisible();
  });

  test('A11Y-019: a validation error from the API shows a readable alert, not a blank page (3.3.1)', async ({
    page,
  }) => {
    // "a@b" passes the browser's own email check but the API rejects it with a 422 whose
    // `detail` is a LIST of objects. Rendering that list used to crash React and blank the page.
    const pageErrors = [];
    page.on('pageerror', (error) => pageErrors.push(error.message));

    await page.goto('/register');
    await page.getByLabel('Email').fill('a@b');
    await page.getByLabel(/^Username/).fill('zed');
    await page.getByLabel('Display Name').fill('Zed');
    await page.getByLabel('Password').fill('Password1!');
    await page.getByRole('button', { name: 'Sign Up' }).click();

    const alert = page.getByRole('alert');
    await expect(alert).toBeVisible();
    await expect(alert).toContainText('valid email address');
    // The page is still there: a crash would have removed the whole form.
    await expect(page.getByRole('heading', { name: 'Create Account' })).toBeVisible();
    expect(pageErrors).toEqual([]);
  });

  test('2.4.11: the sticky navbar never fully covers the focused element', async ({ page }) => {
    await loginAsSarah(page);
    await page.mouse.click(5, 300);
    const navBottom = await page.getByTestId('navbar').evaluate((el) => el.getBoundingClientRect().bottom);

    for (let i = 0; i < 80; i++) {
      await page.keyboard.press('Tab');
      const { id, bottom } = await page.evaluate(() => {
        const el = document.activeElement;
        return {
          id: el.getAttribute('data-testid') || el.tagName,
          bottom: el.getBoundingClientRect().bottom,
        };
      });
      // Entirely above the navbar's bottom edge means entirely hidden behind it
      // (or scrolled off); allow the navbar's own links, which sit inside it.
      const insideNavbar = await page.evaluate(() => !!document.activeElement.closest('[data-testid="navbar"]'));
      if (!insideNavbar) {
        expect(bottom, `${id} is hidden behind the navbar`).toBeGreaterThan(navBottom);
      }
    }
  });

  test.describe('focus management in the post card (2.4.3)', () => {
    test('A11Y-007: Edit focuses the textarea; Cancel returns to the menu button', async ({ page }) => {
      await loginAsSarah(page);
      const id = await ownPostId(page);
      const menu = page.getByTestId(`post-${id}-menu-button`);

      await menu.click();
      await expect(menu).toHaveAttribute('aria-expanded', 'true');
      await page.getByTestId(`post-${id}-edit-button`).click();
      await expect(page.getByTestId(`post-${id}-edit-textarea`)).toBeFocused();

      await page.getByTestId(`post-${id}-cancel-button`).click();
      await expect(menu).toBeFocused();
    });

    test('A11Y-007: Escape closes the post menu and returns focus to its button', async ({ page }) => {
      await loginAsSarah(page);
      const id = await ownPostId(page);
      const menu = page.getByTestId(`post-${id}-menu-button`);

      await menu.click();
      await page.keyboard.press('Escape');
      await expect(page.getByTestId(`post-${id}-dropdown`)).toBeHidden();
      await expect(menu).toBeFocused();
    });

    test('A11Y-007: deleting a post parks focus on <main> and announces it', async ({ page }) => {
      page.on('dialog', (dialog) => dialog.accept());
      await loginAsSarah(page);
      const id = await ownPostId(page);

      await page.getByTestId(`post-${id}-menu-button`).click();
      await page.getByTestId(`post-${id}-delete-button`).click();

      await expect(page.getByTestId(`post-${id}`)).toHaveCount(0);
      await expect(page.locator('main')).toBeFocused();
      await expect(page.getByTestId('live-region')).toHaveText('Post deleted');
    });
  });

  test('A11Y-013: reacting, reposting and commenting are announced (4.1.3)', async ({ page }) => {
    await loginAsSarah(page);
    const live = page.getByTestId('live-region');
    // A plain post, not a repost: a repost embeds its original, which repeats the
    // original's data-testids on the same page.
    const post = page.locator('[data-post-id][data-is-repost="false"]').first();
    const id = await post.getAttribute('data-post-id');

    // Scoped to this one post: ids repeat when a repost embeds its original.
    await post.getByTestId(`post-${id}-react-button`).click();
    await post.getByTestId(`post-${id}-reaction-like`).click();
    await expect(live).toHaveText(/Reacted with like|Reaction removed/);

    await post.getByTestId(`post-${id}-comment-button`).click();
    await expect(post.getByTestId(`post-${id}-comment-input`)).toBeFocused();
    await page.keyboard.type('Nice post');
    await page.keyboard.press('Enter');
    await expect(live).toHaveText('Comment posted');
    await expect(post.getByTestId(`post-${id}-comment-button`)).toBeFocused();
  });

  test('2.5.8: interactive controls on the feed are at least 24x24 CSS px', async ({ page }) => {
    await loginAsSarah(page);
    const tooSmall = await page.evaluate(() =>
      [...document.querySelectorAll('button, a[href], input, textarea, select')]
        .map((el) => ({ el, r: el.getBoundingClientRect() }))
        .filter(({ r }) => r.width > 0 && r.height > 0 && (r.width < 24 || r.height < 24))
        .map(
          ({ el, r }) =>
            `${el.tagName} ${el.getAttribute('data-testid') || ''} ${Math.round(r.width)}x${Math.round(r.height)}`
        )
    );
    expect(tooSmall).toEqual([]);
  });
});
