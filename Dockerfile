# Dockerfile for local-project-memory MCP server
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

# Copy source code
COPY src/ ./src/

# Create directories for memories
RUN mkdir -p .ai/context/memories

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the server
CMD ["python", "-m", "local_project_memory"]
