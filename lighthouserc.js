module.exports = {
  ci: {
    collect: {
      startServerCommand: 'cd frontend && npm run dev',
      url: [
        'http://localhost:3000/',
        'http://localhost:3000/register',
        'http://localhost:3000/login',
      ],
      startServerReadyPattern: 'Local:',
      numberOfRuns: 3,
    },
    upload: {
      target: 'filesystem',
      outputDir: './reports/lighthouse',
      reportFilenamePattern: '%%PATHNAME%%-%%DATETIME%%-report.%%EXTENSION%%',
    },
    assert: {
      preset: 'lighthouse:recommended',
      assertions: {
        'categories:performance': ['warn', { minScore: 0.7 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
        'categories:best-practices': ['warn', { minScore: 0.8 }],
        'categories:seo': ['warn', { minScore: 0.8 }],
      },
    },
  },
};
