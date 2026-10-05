/**
 * Lighthouse CI configuration.
 *
 * Run with the app already up (start-dev.sh, or `make start`) and a seeded
 * database; from the repo root: `cd tests && npm run lighthouse`.
 *
 * The signed-in pages (Feed, Post detail, Profile, Settings) are audited through
 * tests/lighthouse/login.cjs, which signs in first. Lighthouse alone cannot reach
 * them: it starts logged out and the app redirects to /login.
 *
 * Lighthouse is a regression guard for the accessibility *score*, not a
 * substitute for the axe and behaviour suites. It runs a subset of axe's rules.
 */
const path = require('path');

module.exports = {
  ci: {
    collect: {
      url: [
        'http://localhost:3000/login',
        'http://localhost:3000/register',
        'http://localhost:3000/',
        'http://localhost:3000/post/1',
        'http://localhost:3000/profile/sarahjohnson',
        'http://localhost:3000/settings',
      ],
      // lhci joins this onto the current directory, so compute it relative to wherever lhci
      // is run from (the repo root, or tests/ via `npm run lighthouse`).
      puppeteerScript: path.relative(process.cwd(), path.resolve(__dirname, 'tests/lighthouse/login.cjs')),
      numberOfRuns: 1,
      settings: {
        // Keep the signed-in session between the login script and the audit.
        disableStorageReset: true,
        onlyCategories: ['accessibility', 'best-practices', 'seo', 'performance'],
      },
    },
    upload: {
      target: 'filesystem',
      outputDir: './reports/lighthouse',
      reportFilenamePattern: '%%PATHNAME%%-%%DATETIME%%-report.%%EXTENSION%%',
    },
    assert: {
      assertions: {
        // The score is the gate. Individual audits are covered by axe.
        'categories:accessibility': ['error', { minScore: 0.95 }],
        'categories:performance': ['warn', { minScore: 0.7 }],
        'categories:best-practices': ['warn', { minScore: 0.8 }],
        'categories:seo': ['warn', { minScore: 0.8 }],
      },
    },
  },
};
