# 📜 Frontend Scripts

**Utility scripts for development and testing**

---

## fetch-schema.js

Fetches the OpenAPI schema from the running FastAPI backend for use in contract testing (Lab 6C).

### Usage

```bash
# Basic usage (assumes backend on localhost:8000)
node scripts/fetch-schema.js

# Custom API URL
API_URL=https://api.testbook.com node scripts/fetch-schema.js
```

### Prerequisites

- Backend must be running (`./start-dev.sh`)
- Backend must be accessible on the specified URL

### Output

- Creates `src/test/openapi-schema.json`
- Shows endpoint count and API stats

### When to Run

- Before starting Lab 6C
- After backend API changes
- Before running contract tests

**Learn more:** [Lab 6C: Frontend Integration & Contract Testing](../../labs/LAB_06C_Frontend_Integration_Testing.md)

