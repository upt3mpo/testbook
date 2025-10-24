# Course Restructure Backup and Migration Mapping

## Current File Structure (Before Restructure)

### Stage 1: Unit Tests

- LAB_01_Your_First_Test_Python.md
- LAB_01_Your_First_Test_JavaScript.md
- LAB_02_Testing_Real_Functions_Python.md
- LAB_02_Testing_Real_Functions_JavaScript.md
- LAB_02.5_Understanding_Fixtures_Python.md
- LAB_02.5_Understanding_Fixtures_JavaScript.md
- LAB_DEBUG_01_Reading_Errors_JavaScript.md
- LAB_DEBUG_01_Reading_Errors_Python.md
- LAB_DEBUG_02_Fixing_Broken_Tests_JavaScript.md
- LAB_DEBUG_02_Fixing_Broken_Tests_Python.md

### Stage 2: Integration Tests

- LAB_03_Testing_API_Endpoints_JavaScript.md
- LAB_03_Testing_API_Endpoints_Python.md
- LAB_04_Component_Testing_Vitest.md
- LAB_05_Test_Data_Management_JavaScript.md
- LAB_05_Test_Data_Management_Python.md

### Stage 3: API & E2E Testing

- LAB_04_E2E_Testing_JavaScript.md
- LAB_04_E2E_Testing_Python.md
- LAB_04B_Advanced_E2E_JavaScript.md
- LAB_04B_Advanced_E2E_Python.md
- LAB_06B_Advanced_Component_Testing_Python.md
- LAB_06C_Frontend_Integration_Testing_Python.md
- LAB_07_Playwright_Deep_Dive_JavaScript.md
- LAB_07_Playwright_Deep_Dive_Python.md

### Stage 4: Performance & Security

- LAB_06_Testing_With_Rate_Limits_JavaScript.md
- LAB_06_Testing_With_Rate_Limits_Python.md

## Migration Mapping

### Stage 1 Changes

- LAB*02.5_Understanding_Fixtures*_ → LAB*03_Fixtures_And_Test_Data*_
- LAB*DEBUG_01*_ + LAB*DEBUG_02*_ → LAB*04_Debugging_And_Error_Handling*\* (consolidated)

### Stage 2 Changes

- LAB*03_Testing_API_Endpoints*_ → LAB*05_API_Endpoint_Testing*_
- LAB_04_Component_Testing_Vitest.md → LAB_06_Component_Testing_JavaScript.md
- LAB*05_Test_Data_Management*_ → LAB*07_Test_Data_Management*_
- LAB_06B_Advanced_Component_Testing_Python.md → LAB_06_Advanced_API_Testing_Python.md (moved from Stage 3)
- LAB_06C_Frontend_Integration_Testing_Python.md → LAB_08_Contract_Testing_Foundations_Python.md (moved from Stage 3)
- NEW: LAB_08_Contract_Testing_Foundations_JavaScript.md

### Stage 3 Changes

- LAB*04_E2E_Testing*_ → LAB*09_Basic_E2E_Playwright*_
- LAB*04B_Advanced_E2E*_ → LAB*10_Advanced_E2E_Patterns*_
- LAB*07_Playwright_Deep_Dive*_ → LAB*11_Cross_Browser_Testing*_
- NEW: LAB*12_E2E_Test_Organization*\*

### Stage 4 Changes

- LAB*06_Testing_With_Rate_Limits*_ → LAB*15_Rate_Limiting_Production*_
- NEW: LAB_13_Load_Testing_k6.md
- NEW: LAB*14_Security_Testing_OWASP*\*

## Files to Delete

- LAB*DEBUG_01*\* (content moved to Lab 4)
- LAB*DEBUG_02*\* (content moved to Lab 4)

## Cross-Reference Updates Required

- All "Next Lab" links
- All "Prerequisites" references
- All stage README lab listings
- All internal lab references
- Testing pyramid visualizations

## Backup Created: $(date)
