# Multi-stage Dockerfile: build, test, then produce a lean runtime image

# Stage 1: build & test
FROM python:3.11-slim AS builder
WORKDIR /app

# Build-time argument with default version label
ARG VERSION=latest
LABEL version="$VERSION"
LABEL maintainer="tzvimlif@gmail.com"

# Copy dependencies and install runtime deps + pytest for testing
COPY src/requirements.txt .
# Install both app dependencies and pytest for test stage
RUN pip install --no-cache-dir -r requirements.txt pytest

# Copy application code and tests
COPY src/ .

# Ensure src/ is on PYTHONPATH for tests
ENV PYTHONPATH=/app

# Run tests; if any fail, build stops here
RUN pytest tests/


# Stage 2: production image
FROM python:3.11-slim
WORKDIR /app

# Copy installed packages from builder (adjust path if needed)
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy only application code
COPY src/app.py src/server.py ./

# Expose application port
EXPOSE 5000

# Command to run the service
CMD ["python", "server.py"]
