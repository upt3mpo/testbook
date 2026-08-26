---
name: Bug Report
about: Report a bug or issue with Testbook
title: '[BUG] '
labels: bug
assignees: ''
---

<!--
Template Version: 2.0
Last Updated: October 2025
-->

## 🐛 Bug Description

A clear and concise description of what the bug is.

## 📋 Steps to Reproduce

1. Go to '...'
2. Run command '...'
3. Click on '...'
4. See error

## ✅ Expected Behavior

What you expected to happen.

## ❌ Actual Behavior

What actually happened.

## 🖼️ Screenshots

If applicable, add screenshots to help explain your problem.

## 💻 Environment

**Platform:**
- [ ] macOS
- [ ] Linux
- [ ] Windows

**Details:**
- OS Version: [e.g. macOS 14, Windows 11, Ubuntu 22.04]
- Python Version: [e.g. 3.13.0]
- Node Version: [e.g. 24.0.0]
- Browser (if E2E test related): [e.g. Chrome 120]

## 📝 Additional Context

Add any other context about the problem here.

**Which lab/section were you working on?**
[e.g. LAB_01, backend tests, frontend unit tests, E2E]

**Error messages or logs (redact secrets):**
```
Paste relevant snippets only (no secrets, tokens, or .env values)
```

## 🔍 Have you checked?

- [ ] I've searched existing issues for this problem
- [ ] I've checked the [FAQ](../../docs/guides/FAQ.md)
- [ ] I've checked [RUNNING_TESTS.md](../../docs/guides/RUNNING_TESTS.md)
- [ ] I've checked [DEBUGGING_GUIDE.md](../../docs/reference/DEBUGGING_GUIDE.md)
- [ ] I've checked [TROUBLESHOOTING.md](../../docs/reference/TROUBLESHOOTING.md)

## 🧪 Minimal Reproduction (if applicable)

Commands used (copy/paste):

```
# Backend
cd backend && pytest -v

# Frontend
cd frontend && npm test

# E2E
cd tests && npx playwright test
```
