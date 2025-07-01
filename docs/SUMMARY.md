# SUMMARY.md

*This project was developed with massive assistance from ChatGPT.*

This document walks through each step of the project’s development process, including design decisions, implementation details, and how components fit together.

---

## 1. Project Setup

1. **Repository Initialization**

   * Created a new Git repository (`devops-challenge-tzvi-lifshitz`) to track all infrastructure-as-code (IaC), application code, and documentation.
   * Organized folder structure:

     * `src/` for application source and tests
     * `docker-compose.yml` and `Dockerfile` at root
     * Documentation files (`INSTRUCTIONS.md`, `SUMMARY.md`, `TROUBLE.md`)

2. **Environment Configuration**

   * Added a `.env.template` to outline required environment variables.
   * Ensured secure handling of secrets by excluding `.env` from version control (`.gitignore`).

---

## 2. Application Development

1. **Flask Application (`src/app.py` & `src/server.py`)**

   * `app.py` defines `create_app()`, which initializes the Flask app and loads configuration from environment variables:

     * `AWS_REGION`, `DYNAMODB_TABLE`, `CODE_NAME` for DynamoDB access
     * `DOCKER_HUB_REPO`, `PROJECT_URL` for health endpoint metadata
   * Inside `create_app()`, DynamoDB is configured via `boto3.resource("dynamodb", region_name=region)` and the target table is instantiated with `dynamodb.Table(table_name)`.
   * Two routes are registered:

     * **`/health`**: returns JSON with `status`, `container` (from `DOCKER_HUB_REPO`), and `project` (from `PROJECT_URL`).
     * **`/secret`**: uses `table.get_item(Key={"code_name": code_key})` to fetch the secret code, handles `ClientError` by logging and returning HTTP 500, and returns 404 if no `secret_code` is found.
   * `server.py` simply imports and runs the Flask app on `0.0.0.0:5000`, enabling Docker port mapping.

---

## 3. Testing Strategy

1. **Unit & Integration Tests**

   * Utilized `pytest` with Flask’s `test_client` to simulate HTTP requests.
   * Mocked DynamoDB using the `moto` library to isolate tests from AWS.

2. **Final Test File Details**

   * Located in `src/tests`, the test file imports `create_app` and configures environment variables via `monkeypatch`.
   * Defines a `FakeTable` to simulate successful and empty DynamoDB responses.
   * Patches `boto3.resource` to ensure tests do not call AWS.
   * Tests include:

     * `test_health`: checks `/health` status, container, and project values.
     * `test_secret_success`: verifies the endpoint returns a mocked secret.
     * `test_secret_not_found`: asserts a 404 status when no item is found.

3. **CI Integration**

   * Integrated test execution into GitHub Actions to run `pytest` on each push to `main`.

---

## 4. Containerization

1. **Dockerfile**

   * Based on Python 3.11 slim image.

   * Uses a multi-stage build: a **builder** stage installs dependencies and runs tests (`pytest`), then a **final** stage copies only the application code and installed packages for a minimal runtime image.

   * Installs dependencies and sets the default command to start the Flask app.

   * Based on Python 3.11 slim image.

   * Installs dependencies and sets the default command to start the Flask app.

2. **Docker Compose**

   * Single-command launch for the Flask app with environment injection.
   * Simplifies local development and testing setups.

---

## 5. CI/CD Pipeline

1. **GitHub Actions Workflow**

   * **Secrets Configuration:** Ensure you’ve added your Docker Hub credentials (`DOCKER_HUB_USERNAME` and `DOCKER_HUB_TOKEN`) as encrypted GitHub repository secrets so the workflow can authenticate and push images.
   * **Trigger:** pushes to the `main` branch.
   * **Jobs:**

     * **Test:** Installs dependencies and runs `pytest` to validate functionality.
     * **Build & Publish:** Builds the Docker image and tags it with both the short commit SHA and `latest`, then logs in to Docker Hub and pushes both tags using GitHub Secrets.
       :\*\* Builds the Docker image and tags it with both the short commit SHA and `latest`, then logs in to Docker Hub and pushes both tags using GitHub Secrets.
