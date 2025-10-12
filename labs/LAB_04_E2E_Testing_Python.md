# 🧪 Lab 4: End-to-End Testing with Playwright (Python)

**Estimated Time:** 90 minutes
**Difficulty:** Intermediate
**Language:** 🐍 Python
**Prerequisites:** Labs 1-3 completed, Python 3.11+ installed

**Note:** There's also a [JavaScript version](LAB_04_E2E_Testing_JavaScript.md) that follows the same structure!

---

## 🎯 What You'll Learn

- Write E2E tests with Playwright (Python)
- Test in a real browser
- Select elements with data-testid
- Test complete user flows
- See tests run visually!

---

## 📋 Step-by-Step Instructions

### Step 1: Setup Playwright (10 minutes)

```bash
cd tests/e2e-python
pip install -r requirements.txt
playwright install chromium
```

**Wait for installation...**

✅ **Checkpoint:** Run `playwright --version` and see version number

### Step 2: Make Sure Testbook is Running (5 minutes)

**In a separate terminal:**

```bash
# macOS/Linux
./start-dev.sh

# Windows
start-dev.bat
```

This launches the backend API on `http://localhost:8000` and the frontend UI on `http://localhost:3000`.

**Verify:** Open <http://localhost:3000> in your browser – you should see Testbook!

✅ **Checkpoint:** Testbook loads in your browser

### Step 3: Watch a Test Run! (10 minutes)

**Run an existing test in HEADED mode (you'll see the browser!):**

```bash
cd tests/e2e-python
pytest test_auth.py::TestAuthentication::test_login_success -v --headed
```

**🎬 What you'll see:**

- Browser window opens automatically
- Form fields fill themselves
- Buttons click themselves
- Test passes or fails

**This is E2E testing magic!** ✨

✅ **Checkpoint:** You watched a test run in the browser

### Step 4: Run in SLOW MOTION (15 minutes)

**This is even cooler - you can see each step!**

```bash
pytest test_auth.py::TestAuthentication::test_login_success -v --headed --slowmo=1000
```

**What happens:**

- Test runs slowly (1 second per action)
- You can see what's being filled
- You can see what's being clicked
- Much easier to understand!

**Try it:**

- Watch the email field fill in
- Watch the password field fill in
- Watch the submit button click
- See the page navigate

✅ **Checkpoint:** You used slow motion mode

### Step 5: Understand Selectors (15 minutes)

**Open:** `tests/e2e-python/test_auth.py`

**Find:**

```python
page.fill('[data-testid="login-email"]', user["email"])
```

**This means:**

- `page.fill()` - Type into an input field
- `[data-testid="login-email"]` - Find element by its test ID
- `user["email"]` - The value to type

**Why `data-testid`?**

- Specifically for testing
- Won't change if CSS changes
- Clear and reliable

**Other selectors you'll use:**

```python
page.click('[data-testid="login-submit"]')
page.locator('[data-testid="navbar"]').is_visible()
page.fill('[data-testid="create-post-textarea"]', 'My post')
```

✅ **Checkpoint:** You understand how to find elements

### Step 6: Write Your First E2E Test! (35 minutes)

**Create:** `tests/e2e-python/test_my_first.py`

```python
from playwright.sync_api import Page, expect

def test_my_first_e2e_login_and_create_post(page: Page):
    """My first E2E test - Login and create post"""
    # Step 1: Go to Testbook
    page.goto('http://localhost:3000')

    # Step 2: Login
    page.fill('[data-testid="login-email"]', 'sarah.johnson@testbook.com')
    page.fill('[data-testid="login-password"]', 'Sarah2024!')
    page.click('[data-testid="login-submit"]')

    # Step 3: Wait for page to load
    expect(page.locator('[data-testid="navbar"]')).to_be_visible()

    # Step 4: Create a post
    page.fill('[data-testid="create-post-textarea"]', 'My first E2E test post!')
    page.click('[data-testid="create-post-submit"]')

    # Step 5: Verify post appears
    page.wait_for_timeout(1000)  # Wait for post to appear
    first_post = page.locator('[data-testid-generic="post-item"]').first
    expect(first_post).to_contain_text('My first E2E test post!')

    print('✅ Test passed! Post created successfully!')
```

**Run your test in headed mode (watch it work!):**

```bash
pytest test_my_first.py -v --headed
```

**🎬 Watch the magic:**

- Browser opens
- Form fills automatically
- Login happens
- Post is created
- Test verifies result

✅ **Checkpoint:** YOUR first E2E test runs and passes!

---

## 🎓 What You Learned

- ✅ How to write E2E tests with Playwright (Python)
- ✅ How to select elements with data-testid
- ✅ How to interact with the UI (fill, click)
- ✅ How to verify results (expect, to_be_visible, to_contain_text)
- ✅ How powerful automated testing is!

---

## 💪 Practice Challenges

### Challenge 1: Test Logout

Write a test that:

1. Logs in
2. Clicks logout button
3. Verifies user is logged out (login form visible)

**Hint:** Logout button test-id is `navbar-logout-button`

### Challenge 2: Test Registration

Write a test that:

1. Goes to registration page
2. Fills all fields (use unique email!)
3. Submits
4. Verifies auto-login (navbar appears)

**Hint:** Use `/register` route

### Challenge 3: Test Reaction

Write a test that:

1. Logs in
2. Hovers over react button on first post
3. Clicks like emoji
4. Verifies emoji appears in button

**Hint:** Use `.hover()` method

---

## 🐛 Troubleshooting

**Problem:** `page.goto: net::ERR_CONNECTION_REFUSED`
**Solution:** Make sure the dev servers are running (`./start-dev.sh`) so the frontend is available on <http://localhost:3000> and the API on <http://localhost:8000>

**Problem:** `Timeout waiting for element`
**Solution:** Check the data-testid is correct, or add longer timeout

**Problem:** `Test fails randomly`
**Solution:** Add `page.wait_for_timeout(500)` after actions

---

## ✅ Lab Completion Checklist

- [ ] Playwright installed successfully
- [ ] Watched test run in headed mode
- [ ] Used slow motion mode
- [ ] Wrote `test_my_first.py` and it passes
- [ ] Understand selectors and interactions
- [ ] Completed at least 1 practice challenge

---

## 🎯 Pro Tips

**Tip 1:** Always run in headed mode while developing

```bash
pytest test_my_first.py -v --headed
```

**Tip 2:** Use slow motion when test fails

```bash
pytest test_my_first.py -v --headed --slowmo=1000
```

**Tip 3:** Pause execution to inspect

```python
page.pause()  # Add this line anywhere in your test
```

(Browser pauses and you can click around manually!)

---

## 🆚 Python vs JavaScript?

**Both versions of this lab teach the same concepts!**

| Aspect | Python (this lab) | JavaScript |
|--------|------------------|------------|
| **Syntax** | Synchronous, clean | Async/await |
| **Best For** | Python developers, backend teams | JS developers, frontend teams |
| **Features** | Identical | Identical |
| **Speed** | Same | Same |

**Choose based on your comfort level!** Both are excellent.

---

**🎉 You're now writing E2E tests! This is professional-level testing!**

**Next Lab:** [Lab 5: Test Data Management](labs/LAB_05_Test_Data_Management.md)
