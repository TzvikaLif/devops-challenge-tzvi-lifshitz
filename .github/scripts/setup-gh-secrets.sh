#!/usr/bin/env bash
set -e

if ! command -v gh &>/dev/null; then
  cat <<EOF
ERROR: GitHub CLI (gh) is required but not found in your PATH.
Please install it before running this script:

  • macOS:     brew install gh
  • Ubuntu:    sudo apt-get update && sudo apt-get install gh
  • Windows:   winget install --id GitHub.cli
  • Or see:    https://cli.github.com/manual/installation

EOF
  exit 1
fi

# Load your local .env
export $(grep -v '^#' .env | xargs)

# Push Docker Hub creds into GitHub secrets
gh secret set DOCKER_USERNAME --body "$DOCKER_USERNAME"
gh secret set DOCKER_PASSWORD --body "$DOCKER_PASSWORD"
echo "Docker Hub credentials stored as GitHub secrets."