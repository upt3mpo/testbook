/**
 * Accessibility tests with Playwright + axe-core (WCAG 2.2 AA + best-practice).
 *
 * Three groups:
 *   1. Every route in its default state, at desktop width.
 *   2. Interaction states a default-state scan never reaches: error messages,
 *      open menus, edit mode, open comment box. Several real defects only
 *      appear once the state is open (the edit textarea had no label; the login
 *      error failed contrast), so scanning only default pages misses them.
 *   3. The same routes at a 320 px phone width, where the layout differs.
 *
 * axe is one layer. It cannot see focus management, tab order, announcements or
 * reflow - those are in accessibility-behavior.spec.js. The tag list lives in
 * fixtures/a11y.js and is shared; read the comment there before changing it.
 *
 * Run with: npm run test:a11y   (or: npx playwright test accessibility)
 */

import { expect, test } from "@playwright/test";
import { expectNoA11yViolations } from "./fixtures/a11y.js";
import { resetDatabase, TEST_USERS } from "./fixtures/test-helpers.js";
import { AuthPage } from "./pages/AuthPage.js";

const PUBLIC_ROUTES = [
  { name: "Login", path: "/login" },
  { name: "Register", path: "/register" },
];

const username = TEST_USERS.sarah.username;
const AUTHENTICATED_ROUTES = [
  { name: "Feed", path: "/" },
  { name: "Profile", path: `/profile/${username}` },
  { name: "Followers", path: `/profile/${username}/followers` },
  { name: "Following", path: `/profile/${username}/following` },
  { name: "Settings", path: "/settings" },
];

async function loginAsSarah(page) {
  const auth = new AuthPage(page);
  await auth.gotoLogin();
  await auth.login(TEST_USERS.sarah.email, TEST_USERS.sarah.password);
  await auth.expectLoggedIn();
  await page.getByTestId("post-1").waitFor().catch(() => {});
}

/** Open the first seeded post's detail page; returns its path. */
async function openFirstPostDetail(page) {
  const link = page.locator('a[href^="/post/"]').first();
  const href = await link.getAttribute("href");
  await page.goto(href);
  await page.waitForLoadState("networkidle");
  return href;
}

async function settle(page) {
  await page.waitForLoadState("networkidle", { timeout: 5000 }).catch(() => {});
}

test.describe("Accessibility (axe-core) - routes", () => {
  test.beforeEach(async ({ page }) => {
    await resetDatabase(page);
  });

  for (const route of PUBLIC_ROUTES) {
    test(`${route.name} page`, async ({ page }, testInfo) => {
      await page.goto(route.path);
      await settle(page);
      await expectNoA11yViolations(page, testInfo, { name: route.name });
    });
  }

  for (const route of AUTHENTICATED_ROUTES) {
    test(`${route.name} page (authenticated)`, async ({ page }, testInfo) => {
      await loginAsSarah(page);
      await page.goto(route.path);
      await settle(page);
      await expectNoA11yViolations(page, testInfo, { name: route.name });
    });
  }

  test("Post detail page (authenticated)", async ({ page }, testInfo) => {
    await loginAsSarah(page);
    await openFirstPostDetail(page);
    await expectNoA11yViolations(page, testInfo, { name: "Post detail" });
  });
});

test.describe("Accessibility (axe-core) - interaction states", () => {
  test.beforeEach(async ({ page }) => {
    await resetDatabase(page);
  });

  test("Login with an error message showing", async ({ page }, testInfo) => {
    await page.goto("/login");
    await page.getByLabel("Email").fill("nobody@example.com");
    await page.getByLabel("Password").fill("wrong-password");
    await page.getByRole("button", { name: "Log In" }).click();
    await page.getByRole("alert").waitFor();
    // Catches the error text failing contrast (A11Y-004).
    await expectNoA11yViolations(page, testInfo, { name: "Login error" });
  });

  test("Register with an error message showing", async ({ page }, testInfo) => {
    await page.goto("/register");
    await page.getByLabel("Email").fill(TEST_USERS.sarah.email); // already taken
    await page.getByLabel(/^Username/).fill("someone");
    await page.getByLabel("Display Name").fill("Someone");
    await page.getByLabel("Password").fill("Password123!");
    await page.getByRole("button", { name: "Sign Up" }).click();
    await page.getByRole("alert").waitFor();
    await expectNoA11yViolations(page, testInfo, { name: "Register error" });
  });

  test("Feed with a post menu open", async ({ page }, testInfo) => {
    await loginAsSarah(page);
    await page.getByRole("button", { name: "Post options" }).first().click();
    await expectNoA11yViolations(page, testInfo, { name: "Post menu open" });
  });

  test("Feed with a post in edit mode", async ({ page }, testInfo) => {
    await loginAsSarah(page);
    await page.getByRole("button", { name: "Post options" }).first().click();
    await page.getByRole("button", { name: /Edit/ }).click();
    await page.getByRole("textbox", { name: "Edit post content" }).waitFor();
    // Catches the unlabeled edit textarea (A11Y-002).
    await expectNoA11yViolations(page, testInfo, { name: "Post edit mode" });
  });

  test("Feed with a comment box open", async ({ page }, testInfo) => {
    await loginAsSarah(page);
    await page.getByRole("button", { name: "Comment" }).first().click();
    await page.getByRole("textbox", { name: "Write a comment" }).waitFor();
    await expectNoA11yViolations(page, testInfo, { name: "Comment box open" });
  });

  test("Feed with a reaction picker open", async ({ page }, testInfo) => {
    await loginAsSarah(page);
    await page.getByRole("button", { name: "React" }).first().click();
    await page.getByRole("button", { name: "Like" }).first().waitFor();
    await expectNoA11yViolations(page, testInfo, { name: "Reaction picker open" });
  });
});

test.describe("Accessibility (axe-core) - phone width (320px)", () => {
  test.use({ viewport: { width: 320, height: 700 } });

  test.beforeEach(async ({ page }) => {
    await resetDatabase(page);
  });

  for (const route of PUBLIC_ROUTES) {
    test(`${route.name} page`, async ({ page }, testInfo) => {
      await page.goto(route.path);
      await settle(page);
      await expectNoA11yViolations(page, testInfo, { name: `${route.name} @320` });
    });
  }

  for (const route of AUTHENTICATED_ROUTES) {
    test(`${route.name} page (authenticated)`, async ({ page }, testInfo) => {
      await loginAsSarah(page);
      await page.goto(route.path);
      await settle(page);
      await expectNoA11yViolations(page, testInfo, { name: `${route.name} @320` });
    });
  }
});

test.describe("Accessibility (axe-core) - dark theme", () => {
  // The theme is a per-user setting, so go through the real Settings flow rather
  // than poking data-theme. The original suite never scanned dark mode, and it hid
  // real contrast failures (white text on the dark accent colour was 3.45:1).
  test.beforeEach(async ({ page }) => {
    await resetDatabase(page);
    await loginAsSarah(page);
    await page.goto("/settings");
    await page.getByLabel("Theme").selectOption("dark");
    await page.getByRole("button", { name: /save/i }).click();
    await page.getByRole("status").waitFor();
    await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  });

  for (const route of AUTHENTICATED_ROUTES) {
    test(`${route.name} page`, async ({ page }, testInfo) => {
      await page.goto(route.path);
      await settle(page);
      await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
      await expectNoA11yViolations(page, testInfo, { name: `${route.name} (dark)` });
    });
  }

  test("Post detail page", async ({ page }, testInfo) => {
    await page.goto("/");
    await openFirstPostDetail(page);
    await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
    await expectNoA11yViolations(page, testInfo, { name: "Post detail (dark)" });
  });

  test("Feed with the reaction picker open", async ({ page }, testInfo) => {
    await page.goto("/");
    await page.getByRole("button", { name: "React", exact: true }).first().click();
    await page.getByRole("button", { name: "Like", exact: true }).first().waitFor();
    await expectNoA11yViolations(page, testInfo, { name: "Reaction picker (dark)" });
  });
});
