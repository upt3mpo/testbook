# Project Roadmap

This document tracks technical debt, planned improvements, and future changes for the Testbook project.

## 🚨 High Priority

### ESLint 9 Migration

**Status:** Planned
**Priority:** Low (cosmetic warnings only)
**Effort:** 4-6 hours
**Impact:** Eliminates deprecation warnings

**Current State:**

- ESLint 8.57.1 with deprecation warnings
- Warnings are cosmetic and don't affect functionality
- All plugins work correctly

**Required Work:**

1. **Convert configuration system:**

   - Migrate from `.eslintrc.json` to `eslint.config.js` (flat config)
   - Rewrite configuration syntax completely
   - Test all rules still work correctly

2. **Update plugin versions:**

   - `eslint-plugin-react` - ensure ESLint 9 compatibility
   - `eslint-plugin-jsx-a11y` - ensure ESLint 9 compatibility
   - `eslint-plugin-react-hooks` - ensure ESLint 9 compatibility
   - `eslint-plugin-vitest-globals` - ensure ESLint 9 compatibility

3. **Update build scripts:**

   - Modify `package.json` scripts if needed
   - Update any CI/CD configurations
   - Test with new configuration system

4. **Testing:**
   - Verify all linting rules work correctly
   - Test in all environments (Windows, WSL, Docker)
   - Ensure no new warnings or errors

**Why Not Now:**

- Warnings are cosmetic only
- No learning value for students
- Significant time investment for minimal benefit
- Plugin ecosystem still catching up with ESLint 9

**When to Do:**

- When ESLint 8.x reaches end-of-life
- When all plugins have stable ESLint 9 support
- During a major project maintenance cycle

---

## 🔧 Medium Priority

### Frontend Dependency Updates

**Status:** Mostly Complete
**Priority:** Low
**Effort:** 1-2 hours remaining
**Impact:** Security updates, performance improvements

**Completed:**

- ✅ Updated `eslint-config-prettier` to v10.1.8
- ✅ Updated `jsdom` to v27.0.1
- ✅ Updated `msw` to v2.11.6
- ✅ Updated `@lhci/cli` to v0.15.1
- ✅ Updated `@playwright/test` to v1.56.1
- ✅ Updated `@vitejs/plugin-react` to v4.7.0
- ✅ Updated `vite` to v5.4.21
- ✅ **Fixed all npm deprecation warnings** (rimraf, glob, inflight)
- ✅ **Reduced security vulnerabilities** from 12 to 4

**Remaining Work:**

1. **Major version updates:**

   - React 18.3.1 → 19.2.0 (breaking changes)
   - React Router 6.30.1 → 7.9.4 (breaking changes)
   - Vite 5.4.20 → 7.1.11 (breaking changes)
   - Vitest 1.6.1 → 3.2.4 (breaking changes)

2. **Testing required:**
   - Test all components with React 19
   - Update routing code for React Router 7
   - Verify Vite 7 build process
   - Test Vitest 3 test runner

**Why Not Now:**

- Breaking changes require significant testing
- Learning focus should be on testing concepts
- Current versions work perfectly

**When to Do:**

- During major project maintenance
- When security vulnerabilities are found
- When new features require newer versions

---

## 📚 Low Priority

### Documentation Improvements

**Status:** Ongoing
**Priority:** Low
**Effort:** 1-2 hours each
**Impact:** Better user experience

**Planned:**

1. **Create platform-specific setup guides:**

   - macOS setup guide (MACOS_SETUP.md)
   - Linux setup guide (LINUX_SETUP.md)
   - Address platform-specific installation issues
   - Provide comprehensive troubleshooting for each OS

2. **Add more troubleshooting scenarios:**

   - Windows Defender blocking Node.js
   - Antivirus software interference
   - Corporate proxy issues
   - WSL networking problems
   - macOS-specific issues (Xcode tools, Homebrew, permissions)
   - Linux distribution-specific issues (package managers, Python paths)

3. **Create video tutorials:**

   - Windows setup walkthrough
   - macOS setup walkthrough
   - Linux setup walkthrough
   - Common error resolution
   - Testing concepts explanation

4. **Add accessibility testing:**
   - Screen reader compatibility
   - Keyboard navigation testing
   - Color contrast validation

---

## 🐛 Known Issues

### Minor Issues

1. **Windows path handling** - Some edge cases with spaces in paths
2. **WSL networking** - Occasional port binding issues

### Workarounds

- All issues have documented workarounds
- No impact on learning experience
- Solutions provided in troubleshooting guide

---

## 📋 Maintenance Schedule

### Monthly

- [ ] Check for security updates
- [ ] Review dependency warnings
- [ ] Update documentation if needed

### Quarterly

- [ ] Evaluate major dependency updates
- [ ] Review technical debt priorities
- [ ] Plan maintenance windows

### Annually

- [ ] Major dependency upgrades
- [ ] Architecture review
- [ ] Performance optimization

---

## 🎯 Decision Criteria

**When to prioritize technical debt:**

- ✅ Security vulnerabilities found
- ✅ Functionality broken
- ✅ Learning experience impacted
- ✅ Maintenance becomes difficult

**When to defer:**

- ❌ Cosmetic warnings only
- ❌ No learning value
- ❌ Significant effort for minimal benefit
- ❌ Breaking changes require extensive testing

---

## 📝 Notes

- **Learning Focus:** This project prioritizes teaching testing concepts over perfect tooling
- **Stability First:** Working code is more valuable than latest versions
- **Documentation:** All issues are documented with workarounds
- **Community:** Contributions welcome for any of these improvements

---

_Last Updated: December 2024_
_Next Review: January 2025_
