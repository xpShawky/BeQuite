# BeQuite Studio Marketing — Next.js 15 + R3F + Framer Motion
# Build:  docker build -t bequite-marketing -f studio/marketing/Dockerfile studio/marketing/
# Run:    docker run -p 3000:3000 bequite-marketing
#
# Or via docker-compose (recommended):
#   docker compose up marketing

# ------------------------------------------------------------------
# Stage 1: deps — install node_modules.
# ------------------------------------------------------------------
FROM node:20-bookworm-slim AS deps
WORKDIR /app

COPY package.json package-lock.json* ./

RUN npm install --no-audit --no-fund --prefer-offline

# ------------------------------------------------------------------
# Stage 2: builder — Next.js production build.
# ------------------------------------------------------------------
FROM node:20-bookworm-slim AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

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
ENV PORT=3000

RUN groupadd --system --gid 1001 nodejs && \
    useradd --system --uid 1001 --gid nodejs nextjs

COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./package.json
COPY --from=builder --chown=nextjs:nodejs /app/next.config.* ./
# MDX content for /docs route
COPY --from=builder --chown=nextjs:nodejs /app/content ./content

USER nextjs
EXPOSE 3000

HEALTHCHECK --interval=10s --timeout=3s --start-period=20s --retries=3 \
  CMD wget -q --spider http://localhost:3000/ || exit 1

CMD ["npm", "run", "start"]
