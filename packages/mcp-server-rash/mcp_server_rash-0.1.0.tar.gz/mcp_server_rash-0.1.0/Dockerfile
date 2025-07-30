FROM python:3.11-slim

WORKDIR /app

# Install uv for package management
RUN pip install --no-cache-dir uv

# Install the mcp-server-qdrant package
RUN uv pip install --system --no-cache-dir mcp-server-rash

# Expose the default port for SSE transport
EXPOSE 8000

# Set environment variables with defaults that can be overridden at runtime
ENV LYZR_API_KEY=""
ENV LYZR_USER_ID=""
ENV LYZR_AGENT_ID=""

# Run the server with SSE transport
CMD uvx mcp-server-rash
