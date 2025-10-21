/**
 * Global setup for Playwright tests
 * Runs once before all tests
 */

async function globalSetup(config) {
  console.log("=" * 70);
  console.log("🎭 Welcome to Testbook E2E Testing!");
  console.log("Running browser automation tests with Playwright");
  console.log("Chrome | JavaScript | Page Object Model");
  console.log("Tip: Use --headed to see browser, --debug to step through");
  console.log("=" * 70);
}

export default globalSetup;
