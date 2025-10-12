# Markdown Validation Guide

**Keeping documentation accurate and professional**

---

## 🎯 Overview

Testbook uses automated markdown validation to ensure documentation stays accurate, well-formatted, and free of broken links.

### What Gets Validated

**Linting (markdownlint):**
- Heading structure and hierarchy
- List formatting consistency
- Line length guidelines
- Proper spacing
- Code block formatting

**Link Checking (markdown-link-check):**
- Internal links (between docs)
- External links (to resources)
- Anchor links (#section-headings)
- Relative file paths

---

## 🚀 Usage

### Local Validation (Before Committing)

**Quick check:**
```bash
make check-markdown    # or: just check-markdown
```

**Lint only:**
```bash
make lint-markdown     # or: just lint-markdown
```

**Auto-fix issues:**
```bash
make fix-markdown      # or: just fix-markdown
```

**Manual script:**
```bash
bash scripts/check-markdown.sh
```

### CI Validation (Automatic)

The `.github/workflows/markdown-validation.yml` workflow automatically runs on:
- Every push to `main` or `develop` branches
- Every pull request
- When markdown files are modified

**Jobs:**
1. **markdown-lint** - Checks formatting and style
2. **markdown-link-check** - Validates all links
3. **markdown-report** - Generates summary

---

## 📦 Installation (Local Development)

### Install Tools

**Using npm (global):**
```bash
npm install -g markdownlint-cli markdown-link-check
```

**Using package.json (project):**
```bash
cd tests
npm install  # Includes markdown tools
```

**Verify installation:**
```bash
markdownlint --version
markdown-link-check --version
```

---

## ⚙️ Configuration

### markdownlint Config (`.markdownlint.json`)

```json
{
  "default": true,
  "MD013": { "line_length": 200 },
  "MD024": { "siblings_only": true },
  "MD033": false,
  "MD034": false
}
```

**Key settings:**
- `MD013`: Line length set to 200 (more lenient for code examples)
- `MD024`: Allow duplicate headings in different sections
- `MD033`: Allow inline HTML (needed for some formatting)
- `MD034`: Allow bare URLs in angle brackets

### Link Check Config (`.markdown-link-check.json`)

```json
{
  "ignorePatterns": [
    { "pattern": "^http://localhost" },
    { "pattern": "^https://localhost" }
  ],
  "timeout": "20s",
  "retryOn429": true,
  "aliveStatusCodes": [200, 206, 301, 302, 307, 308, 403, 429]
}
```

**Key settings:**
- Ignores localhost URLs (can't check in CI)
- Retries on rate limiting (429)
- Accepts redirects as valid
- 20s timeout for slow external sites

---

## 🔍 What Each Check Does

### Markdown Linting

**Checks:**
- ✅ Heading levels increment by one
- ✅ Consistent list markers (-, not *)
- ✅ Proper spacing around headings
- ✅ Code blocks have language specified
- ✅ No trailing spaces
- ✅ Files end with newline

**Example Issues:**
```markdown
# Heading 1

### Heading 3  ❌ Skipped level 2

## Heading 2  ✅ Correct
```

### Link Validation

**Checks:**
- ✅ Internal links exist (`docs/guide.md`)
- ✅ Anchor links exist (`#section-name`)
- ✅ External URLs are reachable
- ✅ Relative paths are correct

**Example Issues:**
```markdown
[Broken](docs/missing.md)        ❌ File doesn't exist
[Good](docs/INDEX.md)             ✅ File exists

[Broken](#week-1)                 ❌ Anchor doesn't exist
[Good](#section-1)                ✅ Anchor exists
```

---

## 🛠️ Fixing Common Issues

### Issue 1: Heading Level Skips

**Problem:**
```markdown
# Main Heading
### Subheading  ❌ Skipped H2
```

**Fix:**
```markdown
# Main Heading
## Subheading   ✅ Correct hierarchy
```

### Issue 2: Inconsistent List Markers

**Problem:**
```markdown
- Item 1
* Item 2  ❌ Mixed markers
- Item 3
```

**Fix:**
```markdown
- Item 1
- Item 2  ✅ Consistent
- Item 3
```

### Issue 3: Broken Anchor Links

**Problem:**
```markdown
[Jump to section](#week-1-introduction)  ❌ Anchor doesn't exist
```

**Fix:**
```markdown
[Jump to section](#section-1-introduction)  ✅ Correct anchor
```

### Issue 4: Trailing Spaces

**Problem:**
```markdown
This line has trailing spaces    ❌
```

**Fix:**
```bash
make fix-markdown  # Auto-fixes many issues
```

---

## 🎯 Best Practices

### When Writing Documentation

**1. Use consistent heading levels**
```markdown
# Title (H1)
## Section (H2)
### Subsection (H3)
```

**2. Use descriptive link text**
```markdown
❌ Click [here](link.md)
✅ Read the [installation guide](link.md)
```

**3. Test links before committing**
```bash
make check-markdown
```

**4. Keep lines reasonable**
- Aim for 80-120 characters per line
- Configuration allows up to 200 for code examples
- Break long lines for readability

**5. Use relative paths**
```markdown
❌ [Guide](/Users/danmanez/docs/guide.md)
✅ [Guide](docs/guide.md)
✅ [Guide](../docs/guide.md)
```

---

## 🚀 CI Integration

### How It Works

**Triggers:**
```yaml
on:
  push:
    branches: [main, develop]
    paths: ['**.md']
  pull_request:
    paths: ['**.md']
```

**Jobs:**
1. Checkout code
2. Install tools (markdownlint, markdown-link-check)
3. Run validation
4. Generate summary report

### Viewing Results

**In GitHub Actions:**
1. Go to Actions tab
2. Click on workflow run
3. View "Markdown Validation Summary"
4. Check job logs for details

**Pull Request Checks:**
- ✅ Green check = All markdown valid
- ❌ Red X = Issues found
- Click "Details" to see what failed

---

## 📊 Validation Report Example

```
✅ Markdown Linting: Passed
✅ Link Validation: Passed

### Files Checked
- Total Markdown files: 50
- Critical files validated: 5
- All links checked: 200+

### Summary
- Formatting issues: 0
- Broken links: 0
- Warnings: 0
```

---

## 🐛 Troubleshooting

### "markdownlint: command not found"

**Solution:**
```bash
npm install -g markdownlint-cli markdown-link-check
```

### "Too many links checked"

Some external sites rate-limit link checkers. Config already handles this with:
- Retry on 429 errors
- 20s timeout
- Accepts 403 (forbidden) as valid

### "False positives on localhost links"

Config ignores `http://localhost:*` URLs since they can't be checked in CI.

### "Anchor link not found" but it exists

Check capitalization and special characters:
```markdown
# Section 1: Introduction    → #section-1-introduction
# FAQ (Frequently Asked)     → #faq-frequently-asked
```

---

## 📚 Related Tools

### markdownlint

**Documentation:** https://github.com/DavidAnson/markdownlint

**Rules:** https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md

### markdown-link-check

**Documentation:** https://github.com/tcort/markdown-link-check

**Configuration:** https://github.com/tcort/markdown-link-check#config-file-format

---

## ✅ Checklist for Contributors

Before submitting documentation changes:

- [ ] Run `make check-markdown` locally
- [ ] Fix any linting issues
- [ ] Fix broken links
- [ ] Test anchor links work
- [ ] Ensure consistent formatting
- [ ] Check CI passes after push

---

## 🎯 Quick Reference

**Commands:**
```bash
make check-markdown    # Full validation
make lint-markdown     # Lint only
make fix-markdown      # Auto-fix issues
bash scripts/check-markdown.sh  # Manual run
```

**Files:**
- `.markdownlint.json` - Linting rules
- `.markdown-link-check.json` - Link check config
- `.github/workflows/markdown-validation.yml` - CI workflow
- `scripts/check-markdown.sh` - Local validation script

---

**📝 Keep documentation professional with automated validation! ✨**

