# Zapier — Brief reference

> Quick reference for the **automation-architect** when the project uses Zapier. Pair with `references/patterns.md`.

Zapier is the **simplest** automation platform for marketing / sales / ops teams. 7000+ apps, the easiest UX in the market. Trade-off: per-task pricing scales fast; weak for complex branching; limited code escape hatch.

---

## Why Zapier

- 7000+ apps — broadest integration library on the market.
- Easiest UX for non-engineer authors.
- "Code by Zapier" (JS / Python) for glue logic.
- Multi-step zaps + Paths (branching).

## Why NOT

- Per-task pricing scales fast.
- No real source-code escape hatch (Code steps are limited).
- Limited error handling at scale (auto-replay is enterprise-only).
- No deep AI orchestration; native AI actions exist but no agent / tool-calling primitive.
- Vendor lock-in.

## Pricing (May 2026 — verify with `bequite freshness`)

- **Free**: 100 tasks/mo, single-step zaps.
- **Pro**: $19.99/mo (750 tasks).
- **Team**: $69/mo (2k tasks).
- **Company / Enterprise**: custom.

A "task" = one successful zap step.

## Source-of-truth: zapier-platform-cli

Multi-step zaps export via `zapier-platform-cli`. Custom integrations build with `zapier convert <zap-id> ./zaps/<slug>` then commit.

For UI-built zaps (the 99% case), there's no clean export — workaround: document the zap shape in `docs/automation/zaps/<slug>.md` (manual mirror).

## Patterns

- **Idempotency**: "Filter by Zapier" step "only continue if X" — but races in vendor APIs aren't preventable. Prefer search-then-create.
- **Retry**: automatic up to 3 retries (Pro+); not configurable.
- **Branch**: "Paths by Zapier" (Pro+) — multi-path with conditions.
- **Loop**: "Looping by Zapier" (Pro+) — limited; sequential only.
- **Code**: "Code by Zapier" — JS/Python step. Use for shape transforms, not load-bearing logic.
- **Filter**: "Filter by Zapier" — drops items that don't match conditions, preventing wasted tasks.

## AI

Native AI actions for OpenAI / Anthropic. For agent-style flows, Zapier is weaker than n8n / Inngest; consider chaining Code steps + AI actions, but expect verbosity.

## When Zapier is the wrong choice

- Complex branching (> 3-deep) — use n8n or Make.
- AI agent loops — use n8n.
- Cost optimisation at scale — self-hosted n8n is ~free per execution.
- Mission-critical durable workflows — Temporal.

## Verification (Doctrine `ai-automation` Rules → Zapier specifics)

- [ ] Rule 1 — Document each Zap in `docs/automation/zaps/<slug>.md` (workaround for no-export); link to the Zap URL.
- [ ] Rule 2 — Filter step + search-then-create pattern.
- [ ] Rule 3 — Auto-retry enabled (Pro+); document max attempts.
- [ ] Rule 4 — Connections via Zapier auth, never hardcoded; document required scopes.
- [ ] Rule 5 — Trace ID via custom HTTP step (POST to logging endpoint).
- [ ] Rule 6 — Test fixtures in `tests/automation/zaps/<slug>/` (sample webhook payloads).
- [ ] Rule 7 — Error route to webhook → Slack / Sentry.
- [ ] Rule 8 — Filter step on entry validates required fields.
- [ ] Rule 9 — AI steps with budget (Code by Zapier counter); limited circuit breaker support.
- [ ] Rule 10 — Vendor rate limits respected via Schedule + Wait steps.
- [ ] Rule 11 — Old zap turned off; new zap created (no in-place upgrade).
- [ ] Rule 12 — Daily task count via Zapier dashboard; alarm via Webhook to monitoring.

## References

- Docs: https://zapier.com/help
- CLI: https://github.com/zapier/zapier-platform-cli
- Pricing: https://zapier.com/pricing
- Custom integration developer docs: https://platform.zapier.com/
