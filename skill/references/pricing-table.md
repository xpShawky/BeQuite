# Pricing reference (vendored, May 2026 snapshot)

> Hard-coded snapshot used as `bequite freshness` + `bequite cost` offline fallback when the live pricing fetch (`cli/bequite/pricing.py`, v0.8.1) cannot reach vendor pages. Marked `stale=True` whenever read from this file vs from the 24h cache.
>
> **Maintenance:** when a vendor's pricing changes, regenerate this file via the `bequite` maintainer command (lands in v0.15.0). Manually verify quarterly; record the verification in `state/pricing-verifications.log` (created on first verify).
>
> **Source of truth:** the vendor's pricing page, fetched at runtime via `cli/bequite/pricing.py`. This file is the *fallback* — it must be kept current, but the live cache wins when both exist and the cache is < 24h old.

## Models — per-1M-token rates (input / output)

### Anthropic (https://anthropic.com/pricing)
| Model | Input USD/1M | Output USD/1M |
|---|---|---|
| claude-opus-4-7 | 15.00 | 75.00 |
| claude-sonnet-4-6 | 3.00 | 15.00 |
| claude-haiku-4-5 | 0.80 | 4.00 |

### OpenAI (https://openai.com/pricing)
| Model | Input USD/1M | Output USD/1M |
|---|---|---|
| gpt-5 | 12.00 | 50.00 |
| gpt-5-mini | 0.50 | 2.00 |
| gpt-4.1 | 3.00 | 12.00 |
| gpt-4.1-mini | 0.40 | 1.60 |
| o3 | 10.00 | 40.00 |
| o3-mini | 1.50 | 6.00 |

### Google (https://ai.google.dev/pricing)
| Model | Input USD/1M | Output USD/1M |
|---|---|---|
| gemini-2.5-pro | 1.25 | 10.00 |
| gemini-2.5-flash | 0.30 | 2.50 |
| gemini-2.5-flash-lite | 0.10 | 0.40 |

### DeepSeek (https://api-docs.deepseek.com/quick_start/pricing)
| Model | Input USD/1M | Output USD/1M |
|---|---|---|
| deepseek-chat | 0.27 | 1.10 |
| deepseek-coder | 0.27 | 1.10 |
| deepseek-reasoner | 0.55 | 2.19 |

### Ollama (local)
| Model | Input USD/1M | Output USD/1M |
|---|---|---|
| (any local model) | 0.00 | 0.00 |

## Hosting — flat / metered (May 2026)

### Vercel (https://vercel.com/pricing)
| Tier | Price | Notes |
|---|---|---|
| Hobby | $0 | Hard 300s function timeout. |
| Pro | $20/user/mo | Functions configurable to 800s. |
| Enterprise | custom | SLA + dedicated. |

### Cloudflare Workers (https://www.cloudflare.com/plans/)
| Tier | Price | Notes |
|---|---|---|
| Free | $0 | 100k requests/day. |
| Paid | $5/mo | 10M requests/mo + $0.50/M after. |
| Workers Unbound | usage-based | CPU-time billed. |

### Render / Fly.io / Railway
| Tier | Price | Notes |
|---|---|---|
| Render Hobby | $0 | sleeps after 15min. |
| Render Pro | $7/mo per service | always-on. |
| Fly Hobby | $0 | small allowance. |
| Fly Pro | $29/mo | + per-CPU pricing. |
| Railway | $5/mo + usage | $0.000463/GB-hr CPU. |

## Auth — flat / metered

### Clerk (https://clerk.com/pricing)
| Tier | Price | Notes |
|---|---|---|
| Hobby | $0 | 50k MAU. |
| Pro | $25/mo + $0.02/MAU | |
| Enterprise | custom | SAML / SSO / org controls. |

### Auth0 (https://auth0.com/pricing)
| Tier | Price | Notes |
|---|---|---|
| Free | $0 | 7,500 MAU; 25 enterprise connections. |
| B2C Essentials | $35/mo | |
| Enterprise | custom | |

### Better-Auth
- Self-hosted; MIT-licensed; **$0 / use** plus your hosting cost.

### Supabase Auth
- Bundled with Supabase Postgres tier.

## Database — per-instance / metered

### Supabase (https://supabase.com/pricing)
| Tier | Price | Notes |
|---|---|---|
| Free | $0 | 500MB DB; 2 paused projects. |
| Pro | $25/mo | 8GB DB + bandwidth. |
| Team | $599/mo | SOC 2 + multi-region. |

### Neon (https://neon.com/pricing)
| Tier | Price | Notes |
|---|---|---|
| Free | $0 | 0.5GB DB. |
| Launch | $19/mo | 10GB. |
| Scale | $69/mo | 50GB. |

### Convex (https://convex.dev/pricing)
| Tier | Price | Notes |
|---|---|---|
| Starter | $0 | small writes/sec. |
| Pro | $25/mo per dev. |

## Last verified

- 2026-05-10 — Initial vendored snapshot from `bequite freshness` runs at v0.4.3.
- (Future updates appended here by `bequite update-pricing` maintainer command.)

## Cross-references

- Live pricing fetch module: `cli/bequite/pricing.py` (v0.8.1).
- Cost ledger: `cli/bequite/cost_ledger.py` (v0.8.0).
- Provider adapters: `cli/bequite/providers/` (v0.8.0).
- Stop-cost-budget hook: `skill/hooks/stop-cost-budget.sh` (v0.3.0).
- Freshness probe: `cli/bequite/freshness.py` (v0.4.3).
