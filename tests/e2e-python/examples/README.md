# 🧪 E2E Python Examples

**Example tests demonstrating advanced patterns from Lab 4B**

These tests showcase the patterns taught in [Lab 4B: Advanced E2E Python](../../../labs/LAB_04B_Advanced_E2E_Python.md).

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

2. Install Python dependencies:
```bash
cd tests/e2e-python
pip install -r requirements.txt
playwright install chromium
```

### Run All Examples

```bash
cd tests/e2e-python
pytest examples/ -v --headed -m examples
```

### Run Specific Examples

```bash
# Page Object Model examples
pytest examples/test_page_objects_example.py -v --headed

# API + UI combined examples
pytest examples/test_api_ui_combined_example.py -v --headed
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

- [Lab 4B: Advanced E2E Python](../../../labs/LAB_04B_Advanced_E2E_Python.md) - Full tutorial
- [Section 8: Advanced E2E Patterns](../../../docs/course/SECTION_08_ADVANCED_E2E_PATTERNS.md) - Comprehensive guide
- [Testing Comparison](../../../docs/guides/TESTING_COMPARISON_PYTHON_JS.md) - Python vs JavaScript

