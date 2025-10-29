# DevContainer Configuration

This directory contains the configuration for VS Code DevContainers, providing a consistent local development environment for learning automation testing.

## What's Included

### Development Tools
- Python 3.13 with virtual environment
 - Node.js 24 for frontend development
- Git for version control
- Build tools for package compilation

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
4. Installs Playwright browsers
5. Seeds the database with test data
6. Generates placeholder images

## Usage

### Prerequisites
- Docker Desktop installed and running
- VS Code with "Dev Containers" extension installed

### Getting Started
1. Open this project folder in VS Code
2. When prompted, click "Reopen in Container" (or use Command Palette: "Dev Containers: Reopen in Container")
3. Wait for the container to build and initialize (~3-5 minutes first time)
4. Start coding and learning!

## Starting the Services

The devcontainer automatically sets up everything, but you'll need to start the services:

```bash
# Terminal 1: Backend
cd backend
source .venv/bin/activate
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
- **5432**: PostgreSQL (for future labs)

VS Code will notify you when services are running on these ports.

## Customization

### Adding Extensions
Edit `.devcontainer/devcontainer.json` and add extension IDs to the `extensions` array.

### Changing Python/Node Versions
Modify the base image in `.devcontainer/Dockerfile.dev` and the Node.js installation step.

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
✅ **Quick Onboarding**: Start learning in minutes without complex setup
✅ **No Local Setup**: No need to install Python, Node, or other dependencies
✅ **Pre-configured IDE**: All necessary extensions and settings ready
✅ **Isolated**: Container keeps learning environment separate from your system

## Requirements

- Docker Desktop (Windows, Mac, or Linux)
- VS Code with "Dev Containers" extension
- At least 4GB free RAM and 10GB disk space

## Learn More

- [VS Code DevContainers Docs](https://code.visualstudio.com/docs/devcontainers/containers)
- [devcontainer.json reference](https://containers.dev/implementors/json_reference/)
