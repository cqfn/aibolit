# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

FROM python:3.11-slim

ENV UV_VERSION=0.7.13
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PATH="/root/.local/bin:/app/.venv/bin:${PATH}"

RUN apt-get update \
    && apt-get install --yes --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf "https://astral.sh/uv/${UV_VERSION}/install.sh" | sh

WORKDIR /app

COPY pyproject.toml uv.lock README.md LICENSE.txt ./
COPY aibolit ./aibolit

RUN uv sync --frozen --no-dev

ENTRYPOINT ["aibolit"]
CMD ["--help"]
