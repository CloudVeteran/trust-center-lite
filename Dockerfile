# Build stage: the -dev image has pip and a shell for installing packages
FROM cgr.dev/chainguard/python:latest-dev AS build
WORKDIR /app
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage: minimal image with no shell and no pip, runs as nonroot
FROM cgr.dev/chainguard/python:latest
WORKDIR /app
COPY --from=build /app/venv /app/venv
COPY app ./app
ENV PATH="/app/venv/bin:$PATH"
EXPOSE 8080
ENTRYPOINT ["/app/venv/bin/gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app.main:app"]