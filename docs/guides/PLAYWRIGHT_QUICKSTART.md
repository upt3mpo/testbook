# 🎭 Playwright Quick Start

**Get your first browser test running in under 10 minutes**

This is the fast on-ramp to Playwright in Testbook. It doesn't replace the
full references — [`tests/e2e/README.md`](../../tests/e2e/README.md) (JavaScript)
and [`tests/e2e-python/README.md`](../../tests/e2e-python/README.md) (Python) —
it's the thing to read first, before you need those.

Testbook ships **two parallel Playwright suites that test the same app**: one
in JavaScript (`tests/e2e/`), one in Python (`tests/e2e-python/`). Pick
whichever matches the language track you're on, or run both — Playwright's
API is nearly identical in either language, which is itself a useful thing to
notice.

---

## What Playwright actually does

Playwright drives a real browser (Chromium by default here) the way a user
would: it opens pages, clicks buttons, fills in forms, and reads back what's
on screen. That's the difference from the API tests elsewhere in this repo —
those call the backend directly; Playwright tests go through the actual UI,
so they catch things API tests can't (a button that's disabled, a form that
doesn't submit, a redirect that never happens).

---

## Prerequisites

You need the app running **with the backend in `TESTING=true` mode**. A
plain `./start-dev.sh` leaves `TESTING` unset, which disables the dev-only
`/api/dev/reset` endpoint the tests use to reset state between runs — skip
this and a chunk of the suite will fail or skip with 403s.

```bash
# Terminal 1: backend, in testing mode
cd backend
source .venv/bin/activate      # Windows: .venv\Scripts\activate
TESTING=true uvicorn main:app --reload --port 8000

# Terminal 2: frontend
cd frontend
npm run dev
```

Leave both running. Confirm they're up:

```bash
curl http://localhost:8000/api/health   # {"status":"healthy"}
curl http://localhost:3000              # returns the app's HTML
```

---

## JavaScript track

```bash
# Terminal 3
cd tests
npm install
npx playwright install chromium   # one-time browser download

# Run the suite
npm test
```

That runs every spec in `tests/e2e/` against Chromium. A few other entry
points worth knowing:

```bash
npm run test:headed        # watch the browser while it runs
npm run test:ui            # Playwright's interactive UI mode — great for debugging
npx playwright test auth.spec.js          # just one file
npx playwright test --grep "login"        # just tests matching a name
```

After a run, open the HTML report (screenshots + traces for anything that
failed):

```bash
npx playwright show-report
```

### Your first JS test

Here's the shape every test in `tests/e2e/` follows — log in, do something,
assert on what changed:

```javascript
import { test, expect } from "@playwright/test";
import { loginUser } from "./fixtures/test-helpers.js";
import { TEST_USERS } from "./fixtures/test-helpers.js";

test("user can create a post", async ({ page }) => {
  await loginUser(page, TEST_USERS.sarah.email, TEST_USERS.sarah.password);

  await page.click('[data-testid="create-post"]');
  await page.fill('[data-testid="post-content"]', "My first Playwright test!");
  await page.click('[data-testid="submit-post"]');

  await expect(page.locator('[data-testid="post-content"]').first()).toContainText(
    "My first Playwright test!"
  );
});
```

`data-testid` attributes are the anchor for nearly every selector in this
repo — grep the frontend source for `data-testid` if you need to find one
that isn't in `fixtures/test-helpers.js` already.

---

## Python track

```bash
# Terminal 3
cd tests/e2e-python
pip install -r requirements.txt        # or: uv pip install -r requirements.txt
playwright install chromium            # one-time browser download

# Run the suite
pytest -v
```

Useful variations:

```bash
HEADLESS=false pytest -v                        # watch the browser
HEADLESS=false SLOW_MO=1000 pytest -v           # …and slow it down to actually see it
pytest test_auth.py -v                          # just one file
pytest test_auth.py::TestAuthentication::test_login_success -v   # just one test
```

### Your first Python test

Same shape as the JS version — this project's Python suite uses fixtures
from `conftest.py` for login and page setup:

```python
def test_create_post(page, login_as):
    login_as("sarah")

    page.click('[data-testid="create-post"]')
    page.fill('[data-testid="post-content"]', "My first Playwright test!")
    page.click('[data-testid="submit-post"]')

    assert "My first Playwright test!" in page.locator(
        '[data-testid="post-content"]'
    ).first.text_content()
```

---

## Troubleshooting the first run

| Symptom | Likely cause |
| --- | --- |
| Every test times out waiting for navigation | Backend isn't running with `TESTING=true` — see Prerequisites above |
| `Executable doesn't exist` / browser not found | Run `playwright install chromium` in the right directory (`tests/` for JS, `tests/e2e-python/` for Python — each has its own browser cache) |
| `ECONNREFUSED` / connection errors | Frontend or backend isn't actually up on port 3000 / 8000 — check the two `curl` commands above |
| Tests pass individually but fail run together | The suite resets the database between tests via `/api/dev/reset`; if you're running two suites against the same backend at once, they'll stomp on each other's data — run one suite at a time |

For anything not covered here, the full guides have deeper troubleshooting
sections: [`tests/e2e/README.md`](../../tests/e2e/README.md) and
[`tests/e2e-python/README.md`](../../tests/e2e-python/README.md).

---

## Where to go next

- **Structured lessons:** [Stage 3: API & E2E Testing](../../learn/stage_3_api_e2e/) walks through Playwright concepts (locators, the Page Object Model, auto-waiting) step by step, with exercises.
- **Command reference:** [`docs/reference/QUICK_REFERENCE_PLAYWRIGHT.md`](../reference/QUICK_REFERENCE_PLAYWRIGHT.md) — a one-page cheat sheet once you're past the basics.
- **Running everything else:** [`docs/guides/RUNNING_TESTS.md`](RUNNING_TESTS.md) covers backend, frontend, performance, and security tests too.
