# BeQuite — root Makefile (Unix one-command surface).
#
# Same surface as `npm run *` (root package.json) and `bequite *` (CLI),
# for users who prefer make.

.PHONY: help dev dev-detach stop status install verify typecheck test-py test-e2e clean

# Default target: print help
help:
	@echo "BeQuite — Make targets"
	@echo ""
	@echo "  make dev          Bring up the Studio stack via Docker Compose"
	@echo "  make dev-detach   Same, in background"
	@echo "  make stop         Stop the Studio stack"
	@echo "  make status       Probe localhost:3000/3001/3002"
	@echo ""
	@echo "  make install      Install all npm dependencies (api, dashboard, marketing, tests/e2e)"
	@echo "  make typecheck    Run tsc --noEmit on api, dashboard, marketing"
	@echo "  make test-py      Run the Python integration suite"
	@echo "  make test-e2e     Run the Playwright suite (requires running stack)"
	@echo "  make verify       Run everything (typecheck + py tests + e2e tests)"
	@echo ""
	@echo "  make clean        Remove all node_modules directories"
	@echo ""
	@echo "Or use the BeQuite CLI directly:"
	@echo "  bequite dev       Same as 'make dev' (Docker if available)"
	@echo "  bequite status    Same as 'make status'"
	@echo "  bequite quickstart Print friendly onboarding"

dev:
	docker compose up --build

dev-detach:
	docker compose up --build -d

stop:
	docker compose down

status:
	@bequite status 2>/dev/null || (echo "bequite CLI not on PATH. Falling back to curl checks..."; \
	  curl -sS -o /dev/null -w "API       %{http_code} %{url_effective}\n" http://localhost:3002/healthz ; \
	  curl -sS -o /dev/null -w "DASHBOARD %{http_code} %{url_effective}\n" http://localhost:3001/ ; \
	  curl -sS -o /dev/null -w "MARKETING %{http_code} %{url_effective}\n" http://localhost:3000/ )

install:
	@echo "==> Installing studio/api deps"
	cd studio/api && npm install --no-audit --no-fund
	@echo "==> Installing studio/dashboard deps"
	cd studio/dashboard && npm install --no-audit --no-fund
	@echo "==> Installing studio/marketing deps"
	cd studio/marketing && npm install --no-audit --no-fund
	@echo "==> Installing tests/e2e deps"
	cd tests/e2e && npm install --no-audit --no-fund

typecheck:
	@echo "==> tsc --noEmit (api)"
	cd studio/api && npx tsc --noEmit
	@echo "==> tsc --noEmit (dashboard)"
	cd studio/dashboard && npx tsc --noEmit
	@echo "==> tsc --noEmit (marketing)"
	cd studio/marketing && npx tsc --noEmit

test-py:
	cd cli && python -m pytest tests/ -q

test-e2e:
	cd tests/e2e && npx playwright test

verify: typecheck test-py test-e2e

clean:
	rm -rf studio/api/node_modules
	rm -rf studio/dashboard/node_modules
	rm -rf studio/marketing/node_modules
	rm -rf tests/e2e/node_modules
