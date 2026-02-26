# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.10.6 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# Install deps first
COPY pyproject.toml uv.lock README.md LICENSE.txt ./
RUN uv sync --frozen --no-dev --no-install-project

# Now copy source and do the final sync (installs the project itself)
COPY aibolit ./aibolit
RUN uv sync --frozen --no-dev

FROM python:3.14-slim

# Create a non-root user and group
RUN groupadd --system appgroup \
    && useradd --system --gid appgroup --no-create-home appuser

WORKDIR /app

COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appgroup /app/aibolit /app/aibolit

ENV PATH="/app/.venv/bin:$PATH"
ENV VIRTUAL_ENV=/app/.venv

USER appuser

ENTRYPOINT ["aibolit"]
CMD ["--help"]