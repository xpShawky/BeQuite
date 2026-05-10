# Inngest — Brief reference

> Quick reference for the **automation-architect** when the project uses Inngest. Also covers Trigger.dev + Pipedream as adjacent code-first platforms.

Inngest is **TypeScript-first, event-driven, serverless** durable execution. The strongest fit for TS SaaS apps that need background work without operating Temporal infrastructure.

---

## Why Inngest

- TypeScript-first SDK; first-class types for events + steps.
- Each `step.run()` is durable — automatic retry, automatic resume on crash.
- Replay any function from the dashboard.
- Event-driven — emit events; functions trigger on patterns.
- Step parallelism (`step.parallel()`), throttling (`concurrency`, `rateLimit`, `debounce`).
- AI primitives: `step.ai.infer()` with multiple model providers.
- Native fan-out + fan-in.

## Why NOT

- TypeScript-only at present (Python alpha).
- Smaller ecosystem vs n8n / Make.
- For non-engineer authors, no UX — pure code.
- Hosted (free tier; paid tiers per execution).

## Pricing (May 2026)

- **Free**: 50k function runs / mo.
- **Pro**: from $20/mo (1M runs).
- **Enterprise**: custom.

Verify with `bequite freshness`.

## Architecture

```
[Your app] ──emit("user.signed_up")──▶ [Inngest Cloud] ──▶ [Triggers function] ──▶ [Step 1, Step 2, ...]
                                                                                       (each durable)
```

## Function example

```typescript
import { Inngest } from 'inngest';

const inngest = new Inngest({ id: 'my-app' });

export const sendWelcome = inngest.createFunction(
  {
    id: 'send-welcome-email',
    concurrency: { limit: 100 },                    // max 100 parallel
    rateLimit: { limit: 10, period: '1s' },         // max 10/s upstream
    retries: 4,
    debounce: { period: '60s', key: 'event.data.userId' }, // dedup within 60s
  },
  { event: 'user.signed_up' },
  async ({ event, step }) => {
    await step.sleep('warm-up', '1m');
    const profile = await step.run('fetch-profile', async () => fetchProfile(event.data.userId));
    const subject = await step.ai.infer('compose-subject', {
      model: anthropic({ model: 'claude-sonnet-4-6' }),
      body: { messages: [{ role: 'user', content: `Welcome subject for ${profile.name}` }] },
    });
    await step.run('send-email', async () => sendEmail(profile.email, subject.text));
    await step.run('emit-followup', async () => inngest.send({ name: 'user.welcome.sent', data: { userId: event.data.userId } }));
  }
);
```

## Patterns

- **Idempotency**: events with `id` are deduped; steps within a function are idempotent on retry.
- **Retry**: automatic with exponential backoff. `retries` field on the function config.
- **Concurrency**: `concurrency.limit` per function or per key.
- **Rate limit**: `rateLimit` field — token-bucket pacing.
- **Debounce**: `debounce.period + key` for dedup over a window.
- **Fan-out**: `step.parallel([])` for true parallel; results awaited.
- **Failure handling**: `failureHandler` step — runs on max-retries-exceeded.
- **AI**: `step.ai.infer()` with provider abstraction.

## Adjacent platforms

### Trigger.dev (open-source alt to Inngest)

- TS-first; self-host or hosted.
- Tasks instead of functions; similar mental model.
- Strong free tier; less mature than Inngest as of 2026.
- Open-source (Apache 2.0).

### Pipedream (free-tier-generous + code-first + hosted)

- TS + Python steps in a hosted environment.
- 500+ pre-built sources / triggers.
- Free tier covers most personal use; HTTP egress quota.
- Less suited for high-volume production; better for power-user automation.

## When Inngest / Trigger.dev / Pipedream are wrong choices

- Non-engineer authors — use n8n / Make / Zapier.
- Mission-critical, week-long workflows — use Temporal (Inngest can do it but Temporal is more native).
- 1500+ vendor integrations needed — use Make.

## Verification (Doctrine `ai-automation` Rules → Inngest specifics)

- [ ] Rule 1 — Function source TS committed under `inngest/`.
- [ ] Rule 2 — Event IDs stable per business operation; step idempotency native.
- [ ] Rule 3 — `retries` config explicit; not unbounded.
- [ ] Rule 4 — Secrets via env; no hardcoded.
- [ ] Rule 5 — Run ID = native trace; OTel exporter optional.
- [ ] Rule 6 — Test fixtures in `tests/automation/inngest/` using `inngest-test`.
- [ ] Rule 7 — `failureHandler` emits to Sentry / Slack.
- [ ] Rule 8 — Event schemas with Zod (`new EventSchemas().fromZod({...})`).
- [ ] Rule 9 — AI agent flows with iteration cap + cost-tracker step.
- [ ] Rule 10 — `rateLimit` config matches upstream API.
- [ ] Rule 11 — Function ID with version suffix on breaking change; old function deprecated gracefully.
- [ ] Rule 12 — Daily run cost via Inngest dashboard + custom logger to observability.

## References

- Inngest docs: https://www.inngest.com/docs
- Trigger.dev docs: https://trigger.dev/docs
- Pipedream docs: https://pipedream.com/docs
- Inngest GitHub: https://github.com/inngest/inngest
- Inngest test: https://www.inngest.com/docs/sdk/testing
