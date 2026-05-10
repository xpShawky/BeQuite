# BeQuite Studio API — Hono on Bun
# Build:  docker build -t bequite-api -f studio/api/Dockerfile studio/api/
# Run:    docker run -p 3002:3002 -v $(pwd):/workspace bequite-api
#
# Or via docker-compose (recommended):
#   docker compose up api

# ------------------------------------------------------------------
# Stage 1: deps — install node_modules with Bun's package manager.
# ------------------------------------------------------------------
FROM oven/bun:1.1 AS deps
WORKDIR /app

# Copy manifest only first for layer caching. If package.json hasn't changed,
# Docker reuses this layer on rebuild.
COPY package.json ./
COPY package-lock.json* ./
COPY bun.lockb* ./

# bun install reads package.json. Compatible with either lockfile shape.
RUN bun install --frozen-lockfile 2>/dev/null || bun install

# ------------------------------------------------------------------
# Stage 2: runner — production image.
# ------------------------------------------------------------------
FROM oven/bun:1.1 AS runner
WORKDIR /app

# Copy dependencies from the deps stage.
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/package.json ./package.json

# Copy source code (filtered by .dockerignore).
# README.md intentionally NOT copied — .dockerignore excludes *.md to keep
# the runtime image minimal. Docs live in the repo, not the container.
COPY src ./src
COPY tsconfig.json ./tsconfig.json

# Default ports + env. Override via docker-compose.yml or `docker run -e ...`.
ENV PORT=3002
ENV BEQUITE_AUTH_MODE=local-dev
ENV NODE_ENV=production

# The workspace is mounted at /workspace by docker-compose. The API
# reads from BEQUITE_WORKSPACE_ROOT — set explicitly in compose so it
# matches the volume mount target.
ENV BEQUITE_WORKSPACE_ROOT=/workspace

EXPOSE 3002

# Healthcheck so docker-compose can know when the API is up before
# starting dashboard. Uses Bun's built-in fetch (no wget/curl required;
# oven/bun base images don't include them).
HEALTHCHECK --interval=10s --timeout=3s --start-period=15s --retries=5 \
  CMD bun -e "fetch('http://localhost:3002/healthz').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"

CMD ["bun", "run", "src/index.ts"]
