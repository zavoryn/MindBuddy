# =============================================================================
# MindBuddy — Multi-stage Dockerfile
# =============================================================================
#
# Quick start:
#   docker build -t mindbuddy .
#   docker run -it --rm \
#     -e ANTHROPIC_API_KEY=sk-ant-... \
#     -v $(pwd):/workspace \
#     mindbuddy
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1: Builder — install package into venv
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /build

# Copy package source
COPY pyproject.toml README.md ./
COPY mindbuddy/ ./mindbuddy/

# Install into a clean venv (keeps final image small)
RUN python -m venv /opt/mindbuddy-venv && \
    /opt/mindbuddy-venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/mindbuddy-venv/bin/pip install --no-cache-dir .

# ---------------------------------------------------------------------------
# Stage 2: Runtime — minimal image with only the venv
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

LABEL org.opencontainers.image.title="MindBuddy"
LABEL org.opencontainers.image.description="A lightweight terminal coding assistant — the agent that grows with you"
LABEL org.opencontainers.image.source="https://github.com/zavoryn/MindBuddy"

# Create non-root user for security
RUN groupadd --gid 1000 mindbuddy && \
    useradd --uid 1000 --gid mindbuddy --create-home --shell /bin/bash mindbuddy

# Copy venv from builder
COPY --from=builder /opt/mindbuddy-venv /opt/mindbuddy-venv

# Make mindbuddy available on PATH
ENV PATH="/opt/mindbuddy-venv/bin:${PATH}"

# Create persistent data directories
RUN mkdir -p /home/mindbuddy/.mindbuddy/memory /home/mindbuddy/.mindbuddy/skills && \
    chown -R mindbuddy:mindbuddy /home/mindbuddy/.mindbuddy

# Default workspace
RUN mkdir -p /workspace && chown mindbuddy:mindbuddy /workspace
WORKDIR /workspace

# Environment defaults (override at runtime)
ENV MINDBUDDY_LOG_LEVEL=WARNING \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    MINDBUDDY_CONTAINER=docker

# Health check: verify the CLI entry point works
HEALTHCHECK --interval=60s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import mindbuddy; print(mindbuddy.__version__)" || exit 1

# Switch to non-root user
USER mindbuddy

# Default entry: interactive CLI mode
ENTRYPOINT ["mindbuddy"]
CMD ["--help"]
