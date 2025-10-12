# DevContainer Configuration

This directory contains the configuration for GitHub Codespaces and VS Code DevContainers, providing a consistent, one-click development environment.

## What's Included

### Development Tools
- Python 3.11 with virtual environment
- Node.js 20 for frontend development
- Git for version control
- PostgreSQL (via docker-compose)

### VS Code Extensions
- **Python**: Language support, linting, testing
- **Black**: Python code formatting
- **Ruff**: Fast Python linter
- **ESLint**: JavaScript linting
- **Prettier**: JavaScript/React formatting
- **Playwright**: E2E test support
- **Tailwind CSS**: Styling support

### Automatic Setup
When the container starts, it automatically:
1. Creates Python virtual environment
2. Installs all Python dependencies
3. Installs all Node.js dependencies
4. Seeds the database with test data

## Usage

### GitHub Codespaces
1. Navigate to the repository on GitHub
2. Click "Code" → "Codespaces" → "Create codespace on main"
3. Wait for the environment to initialize (~2-3 minutes)
4. Start coding!

### VS Code DevContainers
1. Install the "Dev Containers" extension in VS Code
2. Open the project folder
3. Click "Reopen in Container" when prompted (or use Command Palette)
4. Wait for the container to build and initialize
5. Start coding!

## Starting the Services

The devcontainer automatically sets up everything, but you'll need to start the services:

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Run tests
cd backend
pytest -v
```

## Port Forwarding

The following ports are automatically forwarded:
- **8000**: Backend API (FastAPI)
- **5173**: Frontend Dev Server (Vite)
- **5432**: PostgreSQL Database

VS Code will notify you when services are running on these ports.

## Customization

### Adding Extensions
Edit `.devcontainer/devcontainer.json` and add extension IDs to the `extensions` array.

### Changing Python/Node Versions
Modify the `features` section in `devcontainer.json`:

```json
"features": {
  "ghcr.io/devcontainers/features/python:1": {
    "version": "3.12"
  },
  "ghcr.io/devcontainers/features/node:1": {
    "version": "22"
  }
}
```

### Adding Startup Commands
Edit `.devcontainer/post-create.sh` to add commands that run after container creation.

## Troubleshooting

### Container Won't Start
1. Ensure Docker is running
2. Try rebuilding: Command Palette → "Dev Containers: Rebuild Container"
3. Check Docker logs for errors

### Dependencies Not Installed
Run the post-create script manually:
```bash
bash .devcontainer/post-create.sh
```

### Port Already in Use
1. Stop conflicting services on your host machine
2. Or modify port numbers in `docker-compose.yml`

## Benefits

✅ **Consistent Environment**: Everyone uses the same tools and versions
✅ **Quick Onboarding**: New contributors can start in minutes
✅ **No Local Setup**: No need to install Python, Node, or PostgreSQL locally
✅ **Pre-configured IDE**: All necessary extensions and settings ready
✅ **Reproducible**: Identical environment on any machine or Codespace

## Requirements

- **For Local DevContainers**: VS Code + Dev Containers extension + Docker
- **For Codespaces**: GitHub account (free tier includes 60 hours/month)

## Learn More

- [VS Code DevContainers Docs](https://code.visualstudio.com/docs/devcontainers/containers)
- [GitHub Codespaces Docs](https://docs.github.com/en/codespaces)
- [devcontainer.json reference](https://containers.dev/implementors/json_reference/)

