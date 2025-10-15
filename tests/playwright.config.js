// @ts-check
import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright configuration for Testbook E2E tests.
 *
 * @see https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  testDir: './e2e',

  /* Maximum time one test can run */
  timeout: 30 * 1000,

  /* Run tests in files in parallel */
  fullyParallel: false,

  /* Fail the build on CI if you accidentally left test.only in the source code */
  forbidOnly: !!process.env.CI,

  /* Retry on CI only */
  retries: process.env.CI ? 2 : 0,

  /* Run tests sequentially for better stability (database resets between tests) */
  workers: 1,

  /* Reporter to use */
  reporter: [
    // HTML report with open: 'never' prevents auto-opening browser
    // To view report manually: npx playwright show-report
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['list']
  ],

  /* Shared settings for all projects */
  use: {
    /* Base URL to use in actions like `await page.goto('/')` */
    // IMPORTANT: Port 3000 is for development mode (start-dev.sh)
    // Use PORT 8000 only if running production mode (start.sh)
    baseURL: process.env.BASE_URL || 'http://localhost:3000',

    /* Collect trace when retrying the failed test */
    trace: 'on-first-retry',

    /* Screenshot on failure */
    screenshot: 'only-on-failure',

    /* Video on failure */
    video: 'retain-on-failure',
  },

  /* Configure projects for major browsers */
  // NOTE: CI only runs 'chromium' (via --project=chromium flag) for speed
  // Run locally with all browsers: npx playwright test
  // Run specific browser: npx playwright test --project=firefox
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },

    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },

    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },

    /* Test against mobile viewports */
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  /* Run your local dev server before starting the tests */
  // NOTE: Disabled - students should manually run ./start-dev.sh
  // This ensures both frontend (port 3000) and backend (port 8000) are running
  webServer: undefined,

  // If you want auto-start, use this (requires start-dev.sh running):
  // webServer: process.env.CI ? undefined : {
  //   command: '../start-dev.sh',
  //   url: 'http://localhost:3000',
  //   reuseExistingServer: true,
  //   timeout: 120 * 1000,
  // },
});

