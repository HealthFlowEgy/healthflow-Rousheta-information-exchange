# GitHub Actions Workflows

Due to GitHub App permissions, the CI/CD workflow files need to be added manually through the GitHub web interface or with proper authentication.

## Workflow Files to Add

### 1. ci.yml - CI/CD Pipeline

Create `.github/workflows/ci.yml` with the following jobs:
- **test**: Run tests with PostgreSQL and Redis services
- **lint**: Code quality checks (Black, Flake8, isort)
- **docker**: Build Docker image
- **security**: Security scanning (Bandit, Safety)

### 2. docker-publish.yml - Docker Build and Publish

Create `.github/workflows/docker-publish.yml` to:
- Build and push Docker images to GitHub Container Registry
- Tag images with version, branch, and SHA
- Support multi-platform builds (linux/amd64, linux/arm64)

### 3. dependency-update.yml - Dependency Updates

Create `.github/workflows/dependency-update.yml` to:
- Run weekly on Mondays
- Update Python dependencies
- Create pull requests automatically

## Manual Setup Instructions

1. Go to your repository on GitHub
2. Click on "Actions" tab
3. Click "New workflow"
4. Click "set up a workflow yourself"
5. Copy the content from the workflow files in this directory
6. Commit directly to the main branch

## Workflow Files Location

The complete workflow files are available in the repository at:
- `docs/workflows/ci.yml`
- `docs/workflows/docker-publish.yml`
- `docs/workflows/dependency-update.yml`

Copy these files to `.github/workflows/` directory through the GitHub web interface.

## Required Secrets

No additional secrets are required. The workflows use:
- `GITHUB_TOKEN` (automatically provided by GitHub Actions)

## Permissions

The workflows require the following permissions:
- `contents: read` - To checkout code
- `packages: write` - To push Docker images to GHCR

These are configured in each workflow file.
