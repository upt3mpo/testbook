# 🛠️ Testbook Scripts

Utility scripts for development and maintenance.

---

## 📝 Markdown Validation

### check-markdown.sh / check-markdown.bat

**Purpose:** Validate all markdown files in the project for linting issues and broken links.

**When to use:**

- Before committing documentation changes
- Before creating a pull request
- To verify all links work
- To maintain markdown quality

### Quick Start

**macOS/Linux:**

```bash
./scripts/check-markdown.sh
```

**Windows:**

```bat
scripts\check-markdown.bat
```

### What It Checks

1. **Markdown Linting**

   - Consistent heading styles
   - Proper list formatting
   - Code block syntax
   - Line endings
   - And more...

2. **Link Validation**
   - All internal links work
   - External links are accessible (with retries)
   - Relative paths are correct
   - Anchor links are valid

### First Time Setup

The script will automatically install required tools:

- `markdownlint-cli` - For markdown linting
- `markdown-link-check` - For link validation

**Manual installation:**

```bash
npm install -g markdownlint-cli markdown-link-check
```

### Auto-fix Common Issues

Many markdown linting issues can be auto-fixed:

```bash
# Auto-fix all files
markdownlint --fix '**/*.md' --ignore node_modules --ignore venv

# Fix specific file
markdownlint --fix README.md
```

### Configuration Files

**`.markdownlint.json`** - Linting rules

- Controls which markdown rules are enforced
- Customize to match project style

**`.markdown-link-check.json`** - Link checking config

- Ignores localhost URLs
- Configures retries and timeouts
- Handles rate limiting

---

## 🔧 Configuration

### Markdown Linting Rules

Edit `.markdownlint.json` to customize:

```json
{
  "default": true,
  "MD013": false,  // Disable line length check
  "MD033": false,  // Allow inline HTML
  ...
}
```

**Common rules:**

- `MD013` - Line length (disabled for flexibility)
- `MD033` - Inline HTML (allowed for badges, etc.)
- `MD024` - Duplicate headings (only check siblings)
- `MD041` - First line heading (disabled for flexibility)

### Link Checking Configuration

Edit `.markdown-link-check.json` to customize:

```json
{
  "ignorePatterns": [{ "pattern": "^http://localhost" }],
  "timeout": "20s",
  "retryOn429": true
}
```

---

## 🚀 CI/CD Integration

Markdown validation runs automatically in GitHub Actions when:

- Markdown files are changed
- Pull requests are created
- Code is pushed to main/develop branches

**Workflow:** `.github/workflows/markdown-validation.yml`

### CI Behavior

- **Markdown linting:** Must pass (blocking)
- **Link validation:** Informational (non-blocking for most files)
- **Critical files:** README.md and learn/README.md must have valid links

---

## 📊 Understanding Results

### Successful Run

```text
✅ Markdown linting passed!
✅ Link validation passed!
All markdown validation checks passed!
You're good to commit! 🚀
```

### Failed Linting

```text
❌ Markdown linting found issues

README.md:45 MD022/blanks-around-headings
README.md:67 MD031/blanks-around-fences

Run 'markdownlint --fix **/*.md' to auto-fix some issues
```

**Fix:** Run the auto-fix command or manually correct the issues.

### Broken Links

```text
❌ README.md has broken links

FILE: README.md
[✖] https://example.com/broken → 404
```

**Fix:** Update or remove the broken link.

---

## 💡 Tips

### Pre-commit Hook

Add to your workflow to catch issues early:

```bash
# .git/hooks/pre-commit
#!/bin/bash
./scripts/check-markdown.sh
```

### VS Code Integration

Install extensions for real-time validation:

- `DavidAnson.vscode-markdownlint` - Markdown linting
- `yzhang.markdown-all-in-one` - Markdown productivity

### Common Fixes

**Multiple blank lines:**

```bash
markdownlint --fix **/*.md
```

**Inconsistent list markers:**

- Use `-` for unordered lists (dashes)
- Use `1.` for ordered lists

**Heading structure:**

- Only one H1 (`#`) per file
- Don't skip heading levels (H1 → H3)

---

## 🐛 Troubleshooting

### "Command not found: markdownlint"

**Solution:**

```bash
npm install -g markdownlint-cli markdown-link-check
```

### "npm: command not found"

**Solution:** Install Node.js from <https://nodejs.org/>

### Too many link check failures

**Solutions:**

1. Check your internet connection
2. Some sites rate-limit (retries will help)
3. Add problematic domains to `.markdown-link-check.json` ignore patterns
4. Run again - transient network issues are common

### Permission denied (macOS/Linux)

**Solution:**

```bash
chmod +x scripts/check-markdown.sh
```

---

## 🔗 Related Documentation

- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [GitHub Actions Workflows](../.github/workflows/) - CI/CD setup
- [markdownlint documentation](https://github.com/DavidAnson/markdownlint)
- [markdown-link-check documentation](https://github.com/tcort/markdown-link-check)

---

## 📝 Future Scripts

Potential additions to this directory:

- Database migration scripts
- Test data generation
- Code generation utilities
- Deployment helpers

**Suggestions welcome!** See [CONTRIBUTING.md](../CONTRIBUTING.md)

---

**Keep your documentation clean!** 📝✨
