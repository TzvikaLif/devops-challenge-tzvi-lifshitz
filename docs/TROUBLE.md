# TROUBLE.md

This document outlines the main difficulties encountered during development and how each was resolved.

## Fresh Laptop Environment Setup

**Difficulty:** Beginning on a freshly rebooted laptop without any prerequisite tools blocked initial progress.

**Solution:**

* Installed Docker Desktop and verified it launched correctly.
* Installed Visual Studio Code and added recommended extensions (Python, Docker).
* Installed Git, configured global username/email, and set up SSH keys for GitHub access.
* Installed AWS CLI and configured credentials to match the `.env` file

---

## DynamoDB Access Denied

**Difficulty:** The provided AWS credentials resulted in an AccessDenied error when attempting to read from the DynamoDB table.

**Solution:**

* Created a personal test DynamoDB table with the correct key schema and seeded it with sample data.
* Updated the `.env` file to point to the new test table for development and testing.
* Documented this workaround in `TROUBLE.md` to ensure reproducible tests without relying on restricted credentials.

---

## Verification Script Dependency

**Difficulty:** The provided `verification.sh` script uses `jq` but the tool wasn’t installed on the fresh environment.

**Solution:**

* Installed `jq` using the system package manager (e.g., `apt-get install jq` or `brew install jq`).
* Added a note in `INSTRUCTIONS.md` to install `jq` as a prerequisite for running verification scripts.

---

## CI/CD Platform Change

**Difficulty:** Upon opening a Travis CI account, discovered that Travis no longer offers a free tier, and I had zero experience with both Travis CI and GitHub Actions.

**Solution:**

* Switched to GitHub Actions, which supports free usage for public repositories.
* Created a basic GitHub Actions workflow to handle testing, building, and publishing Docker images, despite initial inexperience.
* Documented the GitHub Actions setup in `INSTRUCTIONS.md` and `SUMMARY.md` to guide future users.
