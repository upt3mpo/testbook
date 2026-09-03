// @ts-check
import { defineConfig, devices } from "@playwright/test";

/**
 * Playwright configuration for visual regression tests, kept separate
 * from playwright.config.js on purpose: the main suite asserts on
 * behavior (does clicking this button do the right thing) and runs on
 * every push/PR; this one asserts on pixels (does this page still look
 * the way it's supposed to) and only runs on the schedule in
 * .github/workflows/visual-regression.yml. Sharing one config would
 * mean either running slow, flake-prone screenshot comparisons on
 * every PR, or disabling screenshot assertions for the whole suite -
 * neither is what either kind of test actually needs.
 *
 * See docs/guides/VISUAL_REGRESSION.md for what these tests cover, why
 * the CI runner version is pinned, and how to update baselines.
 *
 * @see https://playwright.dev/docs/test-snapshots
 */
export default defineConfig({
  testDir: "./visual-tests",
  snapshotDir: "./visual-snapshots",

  /* Screenshot comparisons are slower and more failure-prone than the
     main suite's behavioral assertions - keep the timeout generous. */
  timeout: 30 * 1000,

  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: 1,

  reporter: [
    ["html", { outputFolder: "playwright-report-visual", open: "never" }],
    ["list"],
  ],

  expect: {
    toHaveScreenshot: {
      // 2% pixel difference allowed, to absorb minor antialiasing
      // differences without masking a real visual regression. This is
      // a starting point, not a tuned constant - if a specific page
      // turns out to need a different tolerance (a page with a lot of
      // text is more antialiasing-sensitive than one that's mostly flat
      // color), override it per-test rather than loosening this default
      // for everyone.
      maxDiffPixelRatio: 0.02,
    },
  },

  use: {
    baseURL: process.env.BASE_URL || "http://localhost:3000",
    // Font rendering must be pixel-consistent between the run that
    // captured the baseline and every run comparing against it -
    // hinting can otherwise vary in ways that have nothing to do with
    // an actual visual change.
    launchOptions: {
      args: ["--font-render-hinting=none"],
    },
  },

  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
      // Chromium only, deliberately - cross-browser rendering
      // differences (font metrics, subpixel antialiasing) would show up
      // as "failures" that are really just Firefox not being Chrome,
      // not an actual regression. The main E2E suite already covers
      // cross-browser behavior; this one is single-browser by design.
    },
  ],

  webServer: undefined,
});
