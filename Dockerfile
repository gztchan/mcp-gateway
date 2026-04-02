# MCP Local Proxy - 需要 Python 与 Node.js（用于 npx 子进程）
FROM node:22-bookworm-slim AS node
FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y curl wget git gcc libpq-dev python3-dev

# 从 node 镜像复制 node/npm/npx
COPY --from=node /usr/local/bin/node /usr/local/bin/
COPY --from=node /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
    && ln -s /usr/local/lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

COPY . .

EXPOSE 9090

ENV UV_WORKSPACE_ROOT=/app

ENV UV_ENV=production

RUN uv sync --all-packages --no-editable

CMD ["uv", "run", "poe", "deploy"]
