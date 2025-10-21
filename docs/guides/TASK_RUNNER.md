# Task Runner Guide

Testbook provides unified task runners to simplify common development operations.

## Available Task Runners

We provide **two** task runner options:

1. **Make** (`Makefile`) - Traditional, widely available
2. **Just** (`justfile`) - Modern, user-friendly alternative

Both provide identical functionality. Choose the one you prefer!

---

## Quick Start

### Using Make (Traditional)

```bash
# Show all available commands
make help

# Setup project
make setup

# Start development
make start

# Run tests
make test
```

### Using Just (Modern)

```bash
# Install just: https://github.com/casey/just
brew install just  # macOS
cargo install just # Rust
choco install just # Windows

# Show all available commands
just

# Setup project
just setup

# Start development
just start

# Run tests
just test
```

---

## Common Commands

### Setup & Installation

```bash
make install          # Install all dependencies
make install-backend  # Backend only
make install-frontend # Frontend only
make install-tests    # Test tools only
make setup            # Full setup + database seed
```

### Development

```bash
make start            # Start both backend + frontend
make start-backend    # Backend only (port 8000)
make start-frontend   # Frontend only (port 3000)
```

### Testing

```bash
make test             # All tests
make test-backend     # Backend unit/API tests
make test-frontend    # Frontend component tests
make test-e2e         # E2E tests (Playwright)
make test-security    # Security tests
make test-performance # Performance tests (k6)
make test-contract    # API contract tests
make coverage         # Generate coverage report
```

### Code Quality

```bash
make lint             # Lint all code
make lint-backend     # Backend linting
make lint-frontend    # Frontend linting
make format           # Format all code
```

### Database

```bash
make reset-db         # Reset database
make seed             # Seed with test data
```

### Docker

```bash
make docker-up        # Start services
make docker-down      # Stop services
```

### Cleanup

```bash
make clean            # Remove temp files
make clean-all        # Deep clean (includes dependencies)
```

---

## Why Use Task Runners?

### ❌ Without Task Runners

```bash
# Have to remember multiple commands
cd backend
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uvicorn main:app --reload

# In another terminal
cd frontend
npm run dev

# In another terminal for tests
cd backend
source .venv/bin/activate  # Windows: .venv\Scripts\activate
TESTING=true pytest -v  # Windows (PowerShell): $env:TESTING="true"; pytest -v
```

### ✅ With Task Runners

```bash
# One simple command
make start

# Run tests easily
make test

# Everything's automated
make setup
```

---

## Benefits

### 1. **Simplified Commands**

Replace complex multi-step commands with simple shortcuts.

### 2. **Cross-Platform**

Works consistently across macOS, Linux, and Windows.

### 3. **Documentation**

Self-documenting - `make help` or `just` shows all commands.

### 4. **Error Prevention**

Reduces typos and mistakes in complex commands.

### 5. **Onboarding**

New contributors can start immediately without memorizing commands.

### 6. **CI/CD Integration**

Use same commands locally and in CI pipelines.

---

## Which Task Runner Should I Use?

### Use **Make** if

- ✅ You're familiar with Make
- ✅ You want maximum compatibility (Make is everywhere)
- ✅ You don't want to install additional tools

### Use **Just** if

- ✅ You want modern, clean syntax
- ✅ You prefer better error messages
- ✅ You're okay installing one extra tool

Both work identically - it's purely personal preference!

---

## Examples

### Full Setup From Scratch

```bash
# Clone the repo
git clone https://github.com/upt3mpo/testbook.git
cd testbook

# Complete setup (dependencies + database)
make setup

# Start development
make start
```

### Daily Development Workflow

```bash
# Morning: start servers
make start

# Make code changes...

# Run tests
make test

# Check linting
make lint

# Clean up at end of day
make clean
```

### Before Committing

```bash
# Format code
make format

# Run all tests
make test

# Check coverage
make coverage

# Lint code
make lint
```

### Running Specific Test Types

```bash
# API tests only
make test-backend

# Frontend tests only
make test-frontend

# E2E tests
make test-e2e

# Security audit
make test-security

# Performance benchmarks
make test-performance
```

---

## Customization

### Adding Custom Commands

Edit `Makefile` or `justfile` to add your own shortcuts:

**Makefile:**

```makefile
.PHONY: my-command
my-command:
 @echo "Running custom command..."
 cd backend && ./my-script.sh
```

**justfile:**

```just
# My custom command
my-command:
    #!/usr/bin/env bash
    echo "Running custom command..."
    cd backend && ./my-script.sh
```

---

## Troubleshooting

### Make Issues

**"make: command not found"**

```bash
# macOS
xcode-select --install

# Ubuntu/Debian
sudo apt-get install build-essential

# Windows
choco install make
```

**"No rule to make target"**

- Check you're in the project root directory
- Verify command name with `make help`

### Just Issues

**"just: command not found"**

```bash
# Install just
brew install just      # macOS
cargo install just     # Rust
choco install just     # Windows
```

**Syntax errors**

- Just uses shell scripts in recipes
- Ensure you have bash available

---

## CI/CD Integration

Use the same commands in GitHub Actions:

```yaml
- name: Setup project
  run: make setup

- name: Run tests
  run: make test

- name: Generate coverage
  run: make coverage
```

---

## Learn More

- **Make Tutorial**: <https://makefiletutorial.com/>
- **Just Documentation**: <https://github.com/casey/just>
- **Project Scripts**: See `scripts/` directory for platform-specific alternatives

---

## Without Task Runners

If you prefer not to use task runners, you can still use the original shell scripts:

- `start-dev.sh` / `start-dev.bat` - Start development servers
- `reset-database.sh` / `reset-database.bat` - Reset database
- `run-all-tests.sh` - Run all tests

See [README.md](../../README.md#development-vs-production-mode) for details.

---

**Bottom Line**: Task runners are optional but highly recommended for a better developer experience!
