# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13.0

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.

FROM python:${PYTHON_VERSION}-slim AS prod-deps
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

FROM python:${PYTHON_VERSION}-slim AS dev-deps
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    --mount=type=bind,source=requirements-dev.txt,target=requirements-dev.txt \
    python -m pip install -r requirements-dev.txt

FROM python:${PYTHON_VERSION}-slim AS base
ARG IMAGE_VERSION
ENV IMAGE_VERSION=$IMAGE_VERSION
# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1
WORKDIR /app
# Copy the source code into the container.
COPY . .
# Expose the port that the application listens on.
EXPOSE 8000

FROM base AS test
ENV APP_ENV=test
COPY --from=dev-deps /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
WORKDIR /app
CMD ["python3", "-m", "pytest", "tests", "--junitxml=/reports/junit.xml", "--cov=src", "--cov-report=xml:/reports/coverage.xml"]

FROM base AS final
ENV APP_ENV=production
COPY --from=prod-deps /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
WORKDIR /app
# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
# Change the ownership of the application to the non-privileged user.
RUN chown -R appuser:appuser /app
# Switch to the non-privileged user to run the application.
USER appuser
# Run the application.
CMD ["python3", "-m", "fastapi", "run", "src/main.py", "--proxy-headers", "--port", "8000"]
# CMD ["python3", "-m", "uvicorn", "src.main:app", "--host=0.0.0.0", "--port=8000"]

# Add a healthcheck to monitor the application's status.
HEALTHCHECK CMD python -c "import http.client; conn = http.client.HTTPConnection('localhost', 8000); conn.request('GET', '/health'); res = conn.getresponse(); exit(0 if res.status == 200 else 1)"