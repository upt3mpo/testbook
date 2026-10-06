# 🧪 Lab 2: Testing Real Functions

**Estimated Time:** 75 minutes (45 minutes of core steps and a 30 minute accessibility step)<br>
**Difficulty:** Beginner<br>
**Language:** 🐍 Python<br>
**Prerequisites:** Lab 1 completed

**💡 Need JavaScript instead?** Try [Lab 2: Testing Real Functions (JavaScript)](LAB_02_Testing_Real_Functions_JavaScript.md)!

**What This Adds:** Move from testing simple examples to testing real production code - learn to test actual functions that handle authentication, password hashing, and other critical application logic.

---

<h2 id="what-youll-learn">🎯 What You'll Learn</h2>

- Test real Testbook functions
- Test password hashing
- Test authentication
- Use pytest fixtures
- Understand test coverage
- Test a pure function with boundary values, and why that matters for accessibility

---

<h2 id="step-by-step-instructions">📋 Step-by-Step Instructions</h2>

### Step 1: Explore Real Functions (10 minutes)

**Open the file:** `backend/auth.py`

**Find these functions:**

```python
def get_password_hash(password):
    """Hash a password for storing."""
    # Uses bcrypt to securely hash passwords

def verify_password(plain_password, hashed_password):
    """Verify a password against a hash."""
    # Checks if password matches the hash
```

**Understand:** These are REAL functions used in Testbook!

✅ **Checkpoint:** You understand what these functions do

### Step 2: Look at Existing Tests (10 minutes)

**Open:** `backend/tests/unit/test_auth.py`

**Find this test:**

```python
def test_password_is_hashed(self):
    """Test that password hashing produces a different string."""
    # Arrange
    password = "TestPassword123!"

    # Act
    hashed = get_password_hash(password)

    # Assert
    assert hashed != password
    assert len(hashed) > len(password)
    assert hashed.startswith("$2b$")  # bcrypt format
```

**Notice:**

- Clear comments (Arrange, Act, Assert)
- Multiple assertions checking different things
- Tests what the function actually does

✅ **Checkpoint:** You understand the test structure

### Step 3: Run the Test (5 minutes)

```bash
cd backend
pytest tests/unit/test_auth.py::TestPasswordHashing::test_password_is_hashed -v
```

**You should see:**

```text
tests/unit/test_auth.py::TestPasswordHashing::test_password_is_hashed PASSED ✓
```

**Try running all password tests:**

```bash
pytest tests/unit/test_auth.py::TestPasswordHashing -v
```

✅ **Checkpoint:** All password hashing tests pass

### Step 4: Write Your Own Password Test (15 minutes)

**Challenge:** Test that the same password produces different hashes

**Why?** Bcrypt uses a "salt" so the same password hashes differently each time (more secure!)

**Add this test to `tests/unit/test_auth.py` in the `TestPasswordHashing` class:**

```python
def test_same_password_different_hashes(self):
    """
    Test that hashing the same password twice gives different results.

    This is a critical security test - bcrypt uses a random salt for each hash,
    so the same password should produce different hashes every time.
    This prevents rainbow table attacks and makes passwords more secure.
    """
    # Arrange: Use a strong password for testing
    password = "MyPassword123!"

    # Act: Hash the same password twice
    # Each call to get_password_hash() generates a new random salt
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)

    # Assert: The hashes should be different due to different salts
    assert hash1 != hash2, "Same password should produce different hashes due to salt"

    # But both hashes should still verify correctly with the original password
    # This proves the salt doesn't break password verification
    assert verify_password(password, hash1) is True, "First hash should verify correctly"
    assert verify_password(password, hash2) is True, "Second hash should verify correctly"
```

**Run your test:**

```bash
pytest tests/unit/test_auth.py::TestPasswordHashing::test_same_password_different_hashes -v
```

✅ **Checkpoint:** Your test passes!

### Step 5: Test Password Verification (15 minutes)

**Challenge:** Test that wrong passwords are rejected

**Add this test:**

```python
def test_wrong_password_fails(self):
    """
    Test that wrong password doesn't verify.

    This test ensures that our password verification is working correctly -
    only the exact password that was hashed should verify successfully.
    Wrong passwords should be rejected, even if they're similar.
    """
    # Arrange: Set up correct and wrong passwords
    correct_password = "CorrectPassword123!"
    wrong_password = "WrongPassword456!"

    # Create a hash from the correct password
    hashed = get_password_hash(correct_password)

    # Act & Assert: Test both scenarios
    # The correct password should verify successfully
    assert verify_password(correct_password, hashed) is True, "Correct password should verify"

    # The wrong password should be rejected
    assert verify_password(wrong_password, hashed) is False, "Wrong password should be rejected"
```

**Run it:**

```bash
pytest tests/unit/test_auth.py::TestPasswordHashing::test_wrong_password_fails -v
```

✅ **Checkpoint:** Test passes and verifies security works!

---

### Step 6: A function that decides who can read your page (30 minutes)

**Accessibility thread.** Some of the most valuable functions to test are small and pure. One
of them decides whether people with low vision can read your text.

**Why it matters.** The *contrast ratio* between text and its background is a number. WCAG
requires at least **4.5:1** for normal text. Testbook's dark theme once failed this: white text
on the blue button was **3.46:1**, and nobody noticed because nobody had checked dark mode. A
unit test over the numbers would have caught it before a user ever saw it. You can read the
whole story in [Case 5 of the worked examples](../../../docs/a11y/WORKED_EXAMPLES.md).

**Get the function.** Testbook's backend has no colour code, so you are given one. Copy the
starter file into your backend:

```bash
cp learn/stage_1_unit/exercises/starter_files/contrast.py backend/contrast.py
```

**Open it** and read it. It converts each colour to a *relative luminance* between 0 (black) and
1 (white) using the formula in the WCAG definition, and returns
`(lighter + 0.05) / (darker + 0.05)`. You do not need to memorise the maths. You need to test that
it gives the right answers.

```python
def contrast_ratio(colour_a, colour_b): ...      # 1 to 21
def passes_aa(foreground, background, large_text=False): ...   # True or False
```

> **Do not look at `learn/solutions/LAB_02_contrast_solution.py` yet.** That is the reference
> version of the tests you are about to write.

**Create your own test file:** `backend/tests/test_contrast_lab.py`

**Start with this and complete it:**

```python
import pytest
from contrast import contrast_ratio, hex_to_rgb, passes_aa


class TestContrastRatio:
    def test_black_on_white_is_21(self):
        # Arrange / Act / Assert: the WCAG definition says the maximum ratio is 21.
        assert contrast_ratio("#000000", "#ffffff") == pytest.approx(21, abs=1e-5)

    # TODO 1: a colour on itself is 1:1.

    # TODO 2: the answer must not depend on which colour is the foreground.
```

**Now write these tests yourself:**

1. **Known values.** Use `@pytest.mark.parametrize` to check these real Testbook colour pairs.
   Compare with `pytest.approx(expected, abs=0.005)`, never `==`: floating-point maths is not
   exact.

   | Foreground | Background | Expected ratio |
   | --- | --- | --- |
   | `#ffffff` | `#2d88ff` | 3.46 (the dark-theme bug) |
   | `#ffffff` | `#1668d9` | 5.23 (the fix) |
   | `#ffffff` | `#1264d0` | 5.59 |

2. **The boundary.** Boundary values are where bugs live, and this function has a sharp one.
   Check that `#767676` on white **passes** AA and `#777777` on white **fails**. To your eye the
   two greys are identical. Their ratios are 4.54 and 4.48, on either side of 4.5. Also assert
   that the failing ratio is **less than 4.5 but more than 4.4**, to prove it is not being
   rounded: WCAG treats 4.499 as a fail, not as "close enough".

3. **Large text.** Check that the 3.46:1 pair fails for normal text and **passes** with
   `large_text=True`, because large text only needs 3:1.

4. **Bad input.** `hex_to_rgb` should raise `ValueError` for `""`, `"#12"`, `"blue"` and `None`.
   Use `parametrize` with `pytest.raises(ValueError)`.

**Run your tests:**

```bash
cd backend
pytest tests/test_contrast_lab.py -v
```

✅ **Checkpoint:** all your tests pass.

**Now compare** with `learn/solutions/LAB_02_contrast_solution.py`. Did you cover something it
does not, or miss something it covers?

### Step 7: Check the real design (optional challenge, 10 to 15 minutes)

A function test is good. A test that applies the function to **your real design** is better.

**The task.** Write a test that reads Testbook's real colours from `frontend/src/index.css` and
checks that every text and background pair meets 4.5:1 in **both** the light and dark themes.

**Hints:**

- The colours are CSS custom properties such as `--text-primary: #050505;`. The `:root` block
  holds the light theme. The `[data-theme='dark']` block overrides some of them for dark mode;
  anything it does not redefine falls back to the light value.
- A regular expression such as `(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{3,6})` pulls out the pairs.
- Use `@pytest.mark.parametrize` over the pairs, and over the two themes.
- A good failure message names the pair, both colours, the ratio and the theme.

**Pairs to check:** `--text-primary` on `--bg-primary` and `--bg-secondary`; `--text-secondary` on
both; `--accent-color` on `--bg-primary` (links); white on `--accent-fill` (the primary button);
`--error-text` on `--bg-primary`.

**Then break it on purpose.** In the dark theme block, change `--accent-fill: #1668d9;` to
`--accent-fill: #2d88ff;` (the colour the bug used). Your test should fail and name the pair.
Undo with `git checkout frontend/src/index.css`.

The reference version is at the bottom of `learn/solutions/LAB_02_contrast_solution.py`.

> **Python and JavaScript differ here.** The repository's own guard for these tokens is a
> JavaScript test (`frontend/src/tests/accessibility/tokens.test.js`), because the frontend owns
> the CSS. JavaScript learners read and run it. Python learners write their own version of it, so
> the Python track gets the extra practice of parsing a file and parametrising over themes.

**What you just saw.** This is a *unit test*, layer 4 on the
[prevention ladder](../../stage_0_inclusion_first/README.md#the-prevention-ladder). It runs in
milliseconds, needs no browser, and would have caught a bug that a full browser test missed for
months.

<h2 id="what-you-learned">🎓 What You Learned</h2>

- ✅ How to test real application functions
- ✅ How password hashing works
- ✅ Why security testing matters
- ✅ How to write tests that verify security
- ✅ How to navigate existing test code

---

## 💪 Practice Exercises

Try these on your own:

### Exercise 1: Edge Cases

Test password hashing with:

- Empty string
- Very long password (1000 characters)
- Password with special characters: `!@#$%^&*()`
- Unicode password: `密码123`

### Exercise 2: Multiple Assertions

Write one test that:

- Hashes a password
- Verifies hash is different than password
- Verifies hash length > 50 characters
- Verifies hash starts with "$2b$"
- Verifies the password verifies correctly

### Exercise 3: Explore More

Find and run tests for:

- JWT tokens (`tests/unit/test_auth.py`)
- User models (`tests/unit/test_models.py`)
- Try to understand what each test does

---

<h2 id="troubleshooting">🐛 Troubleshooting</h2>

**Problem:** `ModuleNotFoundError: No module named 'auth'`
**Solution:** Make sure you're in the `backend/` directory and venv is activated

**Problem:** `Test not found`
**Solution:** Check file name starts with `test_` and function starts with `test_`

**Problem:** `Import errors`
**Solution:** Run `pip install -r requirements.txt`

---

<h2 id="lab-completion-checklist">✅ Lab Completion Checklist</h2>

Before moving to Lab 3, ensure you:

- [ ] Successfully ran existing password tests
- [ ] Wrote `test_same_password_different_hashes` and it passes
- [ ] Wrote `test_wrong_password_fails` and it passes
- [ ] Understand Arrange-Act-Assert pattern
- [ ] Can explain why password hashing matters
- [ ] Wrote `test_contrast_lab.py`, including the `#767676` / `#777777` boundary test, and it passes
- [ ] Can explain why a 4.48:1 pair fails even though it looks the same as a 4.54:1 pair
- [ ] (Optional) Wrote a test that checks the real design tokens in both themes

---

Answer these to solidify your learning:

1. **Why do we hash passwords instead of storing them plainly?**
2. **Why does the same password produce different hashes?**
3. **What would happen if password verification was broken?**
4. **Why is it important to test security functions?**

---

**🎉 Great job! You're testing real security code!**

**Next Lab:** [Lab 3: Testing API Endpoints (Python)](LAB_03_Fixtures_And_Test_Data_Python.md)
