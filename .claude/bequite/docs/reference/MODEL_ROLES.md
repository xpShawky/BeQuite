# Model roles

BeQuite names roles, never models. Commands and skills say "strong model", "balanced model" or "fast model"; this file is the only place that maps a role to the models of the day. When models change, edit this file and nothing else. `scripts/bq_check.py` fails on a versioned model name anywhere else in the pack.

last_verified: 2026-11-21

| Role | Use it for | Claude family (2026-11) | Other vendors |
|---|---|---|---|
| strong | architecture, plans, research synthesis, judgment calls, security review, red-team, the final pass | Fable 5.2, Opus 5.5 | the vendor's flagship reasoning model |
| balanced | implementation from an approved plan, most commands, rewriting to a spec | Opus 5.5, Sonnet 5.5 | the vendor's mid tier |
| fast | sweeps, extraction, formatting, scouts, evals, blind-pick tests | Haiku 5.5, Sonnet 5.5 | the vendor's small model |

## Rules

1. BeQuite recommends a role per task; it never switches the user's model. Report the model actually running.
2. Effort is separate from the role: high for plans, security and final passes; default for implementation; low for sweeps.
3. In multi-model planning, use whatever flagship models the user has. BeQuite does not rank vendors.
4. A cost figure tied to a model is an estimate; mark it `UNVERIFIED:` unless it comes from the vendor's current price page.
