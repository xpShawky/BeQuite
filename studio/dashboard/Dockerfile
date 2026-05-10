# BeQuite Studio Dashboard — Next.js 15
# Build:  docker build -t bequite-dashboard -f studio/dashboard/Dockerfile studio/dashboard/
# Run:    docker run -p 3001:3001 bequite-dashboard
#
# Or via docker-compose (recommended):
#   docker compose up dashboard
#
# Two env namespaces:
#   BEQUITE_API_BASE             — server-side (Next.js server components).
#                                  Defaults to http://api:3002 (docker-compose
#                                  service name) so the dashboard's loadProject()
#                                  fetches inside the docker network.
#   NEXT_PUBLIC_BEQUITE_API_BASE — client-side (browser EventSource for live
#                                  updates). Defaults to http://localhost:3002
#                                  (host-published port) so the browser can
#                                  reach the API from outside docker.

# ------------------------------------------------------------------
# Stage 1: deps — install node_modules.
# ------------------------------------------------------------------
FROM node:20-bookworm-slim AS deps
WORKDIR /app

COPY package.json package-lock.json* ./

# npm install (lockfile present) or npm install (no lockfile).
RUN npm install --no-audit --no-fund --prefer-offline

# ------------------------------------------------------------------
# Stage 2: builder — Next.js production build.
# ------------------------------------------------------------------
FROM node:20-bookworm-slim AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# NEXT_PUBLIC_* are baked into the bundle at build time. Setting it here
# makes the browser-side EventSource hit http://localhost:3002 (host port).
ARG NEXT_PUBLIC_BEQUITE_API_BASE=http://localhost:3002
ENV NEXT_PUBLIC_BEQUITE_API_BASE=$NEXT_PUBLIC_BEQUITE_API_BASE

ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

RUN npm run build

# ------------------------------------------------------------------
# Stage 3: runner — production image.
# ------------------------------------------------------------------
FROM node:20-bookworm-slim AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3001

# Server-side API base (used by server components / loadProject()).
# Override in docker-compose for service-name resolution.
ENV BEQUITE_API_BASE=http://api:3002
ENV BEQUITE_DASHBOARD_MODE=http

# Non-root user for safety.
RUN groupadd --system --gid 1001 nodejs && \
    useradd --system --uid 1001 --gid nodejs nextjs

COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./package.json
COPY --from=builder --chown=nextjs:nodejs /app/next.config.* ./

USER nextjs
EXPOSE 3001

# Healthcheck via Node's built-in fetch (Node 20+). No wget/curl needed.
HEALTHCHECK --interval=10s --timeout=3s --start-period=25s --retries=5 \
  CMD node -e "fetch('http://localhost:3001/').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"

CMD ["npm", "run", "start"]
