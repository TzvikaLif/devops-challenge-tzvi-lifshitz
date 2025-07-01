# INSTRUCTIONS.md

## Prerequisites

* **Git** and a Unix‑style shell (bash) or Windows Git Bash
* **jq** Install jq using the system package manager (e.g., apt-get install jq or brew install jq).
* **Docker** installed and running
* **Python 3.11** and `pip`
* **AWS credentials** loaded from your `.env` file (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`)
* **AWS CLI** (optional; used only for identity verification)

---

## 1. Clone the Repository

```bash
git clone https://github.com/TzvikaLif/devops-challenge-tzvi-lifshitz.git
cd devops-challenge-tzvi-lifshitz
```

---

## 2. Configure Environment Variables

1. Copy the template:

   ```bash
   cp .env.template .env
   ```
2. Edit `.env` and set:

   ```dotenv
   AWS_ACCESS_KEY_ID=...
   AWS_SECRET_ACCESS_KEY=...
   AWS_REGION=...
   DYNAMODB_TABLE=your-table-name
   CODE_NAME=your-secret-key
   DOCKER_HUB_REPO=youruser/devops-challenge
   PROJECT_URL=https://github.com/youruser/devops-challenge-tzvi-lifshitz
   ```
3. Load variables into your shell:

   ```bash
   export $(grep -v '^#' .env | xargs)
   ```

---

## 3. Run Test Suite

Verify functionality before running the app:

```bash
pytest src/tests -q
```

---

## 4. Run the Flask App (AWS DynamoDB)

> **Note:** The DynamoDB table must already exist and contain the required items.

1. (Optional) **Verify AWS identity**:

   ```bash
   aws sts get-caller-identity
   ```
2. **Install Python dependencies & start the server**:

   ```bash
   pip install -r src/requirements.txt
   python src/server.py
   ```
3. **Health check**:

   ```bash
   curl http://127.0.0.1:5000/health
   ```
4. **Retrieve secret**:

   ```bash
   curl http://127.0.0.1:5000/secret
   ```

---

## 5. Run with Docker Compose

This brings up the Flask app (and any other services) in one command:

```bash
# Ensure .env is present and correct
docker-compose up -d
```

Check the health endpoint:

```bash
curl http://127.0.0.1:5000/health
```

---

## 6. Build and Run with Docker

1. **Build the image**:

   ```bash
   docker build -t $DOCKER_HUB_REPO .
   ```
2. **Run the container**:

   ```bash
   docker run --rm -p 5000:5000 --env-file .env $DOCKER_HUB_REPO
   ```
3. **Verify**:

   ```bash
   curl http://127.0.0.1:5000/health
   ```

---

## 7. CI/CD with GitHub Actions

On pushes to `main`, Actions will:

1. Install dependencies and run tests.
2. Build Docker images (commit SHA & `latest`).
3. Log in and push to Docker Hub (using GitHub secrets).

Just push and watch the **Actions** tab.
