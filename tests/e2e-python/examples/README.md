# 🧪 E2E Python Examples

## Example tests demonstrating advanced patterns from Lab 4B

These tests showcase the patterns taught in [Lab 4B: Advanced E2E Python](../../../learn/stage_3_api_e2e/exercises/LAB_10_Advanced_E2E_Patterns_Python.md).

---

## 📁 Files

- `test_page_objects_example.py` - Page Object Model examples
- `test_api_ui_combined_example.py` - Combined API + UI validation patterns

---

## 🚀 Running the Examples

### Prerequisites

1. Backend and frontend must be running:

```bash
./start-dev.sh
```

1. Install Python dependencies:

```bash
cd tests/e2e-python
pip install -r requirements.txt
playwright install chromium
```

### Run All Examples

**macOS/Linux:**

```bash
cd tests/e2e-python
HEADLESS=false pytest examples/ -v -m examples
```

**Windows (PowerShell - Recommended):**

```powershell
cd tests/e2e-python
$env:HEADLESS="false"; pytest examples/ -v -m examples
```

### Run Specific Examples

**macOS/Linux:**

```bash
# Page Object Model examples
HEADLESS=false pytest examples/test_page_objects_example.py -v

# API + UI combined examples
HEADLESS=false pytest examples/test_api_ui_combined_example.py -v
```

**Windows (PowerShell - Recommended):**

```powershell
# Page Object Model examples
$env:HEADLESS="false"; pytest examples/test_page_objects_example.py -v

# API + UI combined examples
$env:HEADLESS="false"; pytest examples/test_api_ui_combined_example.py -v
```

---

## 📚 What These Examples Demonstrate

### Page Object Model

- Reusable page classes
- Selector centralization
- Maintainable test code
- Professional organization

### Combined API + UI Testing

- Fast test setup using API
- UI verification of API actions
- API verification of UI changes
- Python's unique advantage for full-stack testing

---

## 💡 Key Takeaways

**Page Objects make tests:**

- ✅ More readable
- ✅ Easier to maintain
- ✅ Reusable across tests
- ✅ Professional quality

**API + UI patterns enable:**

- ✅ 10-100x faster test setup
- ✅ More reliable assertions
- ✅ Same language for both layers
- ✅ Reduced UI flakiness

---

## 🎓 Learn More

- [Lab 4B: Advanced E2E Python](../../../learn/stage_3_api_e2e/exercises/LAB_10_Advanced_E2E_Patterns_Python.md) -
  Full tutorial
- [Section 8: Advanced E2E Patterns](../../../learn/stage_3_api_e2e/README.md#advanced-e2e-patterns) -
  Comprehensive guide
- [Testing Comparison](../../../docs/guides/TESTING_COMPARISON_PYTHON_JS.md) -
  Python vs JavaScript
