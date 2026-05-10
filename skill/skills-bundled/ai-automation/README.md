# skill/skills-bundled/ai-automation/

> Bundled expert skill for BeQuite. Loaded automatically when the `ai-automation` Doctrine is active. Provides deep per-platform expertise (n8n, Make, Zapier, Temporal, Inngest, patterns) to the **automation-architect** persona.
>
> Vendored, not live-pulled. Update via PR; pin commit at `.pinned-commit` for reproducibility.

## What this skill provides

- **Platform expertise** in `references/`: n8n, Make.com, Zapier, Temporal, Inngest, Trigger.dev, Pipedream, AWS Step Functions.
- **Cross-platform patterns** in `references/patterns.md`: idempotency, retry/backoff/jitter, dead-letter, fan-out, batching, circuit breakers, AI-agent chains, prompt-injection mitigations, schema-at-the-edge, observability propagation.
- **Workflow templates** in `templates/` (planned for v0.6.x): example n8n flows + Make scenarios for common patterns (lead routing, AI summarisation, e-commerce order, billing reconciliation).
- **Slash commands** in `commands/` (planned): `/bequite.automation.design-flow`, `/bequite.automation.audit-flow`, `/bequite.automation.simulate-flow`.

## When this skill loads

The skill loads when `state/project.yaml::active_doctrines` contains `ai-automation` (or any fork like `ai-automation-no-code-only`, `ai-automation-llm-agent-heavy`).

## How the automation-architect uses it

The `automation-architect` persona at `skill/agents/automation-architect.md` references this skill's `references/<platform>.md` files when:

- Researching platform options (P0).
- Drafting the platform ADR (P1).
- Designing the per-flow spec (P2).
- Implementing flow exports (P5).
- Validating against the Doctrine's 10 gates (P6).

## Layering with other skills

This skill stacks cleanly with **Impeccable** (frontend) when the automation has an admin UI / dashboard. The frontend-designer authors the UI; the automation-architect owns the backend flow.

This skill **does not replace** the platform vendors' own docs — it captures the *opinionated, BeQuite-aligned* knowledge needed to make good choices fast and avoid common traps.

## Versioning

This bundled skill versions independently from BeQuite. Update via PR. Major bumps require an ADR (similar to Constitution v1.0.0 → v1.0.1 process).

- Current version: `1.0.0`
- Pinned commit (when applicable): see `.pinned-commit`

## License

MIT. Original content authored by Ahmed Shawky (xpShawky) and BeQuite contributors.
