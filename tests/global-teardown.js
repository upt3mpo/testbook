/**
 * Global teardown for Playwright tests
 * Runs once after all tests complete
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function globalTeardown(config) {
  // Check if tests passed by looking at the results

  try {
    const resultsPath = path.join(__dirname, "test-results", "results.json");
    if (fs.existsSync(resultsPath)) {
      const results = JSON.parse(fs.readFileSync(resultsPath, "utf8"));
      const stats = results.stats || {};

      if (stats.failed === 0 && stats.passed > 0) {
        console.log(`
🎉 Congratulations! All E2E Tests Passed! 🎉

You're mastering browser automation! Your application works perfectly.

Next steps:
  - View test report: npx playwright show-report
  - Run backend tests: cd ../backend && pytest -v
  - Run frontend tests: cd ../frontend && npm test
  - Check coverage: pytest --cov --cov-report=html

Keep up the great work! 🚀
        `);
      } else if (stats.failed > 0) {
        console.log(`
Some E2E Tests Failed

Debug tips:
  - Use --headed to see what's happening
  - Use --debug to step through tests
  - Check screenshots in test-results/
  - View report: npx playwright show-report
        `);
      }
    }
  } catch (error) {
    // If we can't read results, just continue
    console.log("E2E tests completed");
  }
}

export default globalTeardown;
