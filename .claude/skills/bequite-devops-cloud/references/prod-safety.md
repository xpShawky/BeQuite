# Production safety: servers, migrations, runbook, cost (2026-11-21)

These are hard human gates from the project rules. The agent may prepare, test on a copy and print commands; the user runs them.

## Servers and VPS

The agent never executes, even in auto mode:

- SSH sessions that change state on a production host
- `rm -rf`, `systemctl stop|restart|disable`, package upgrades on production
- edits under `/etc/`, Nginx or other proxy config, TLS certificate operations
- user or SSH key changes, firewall rules, DNS records

The agent may, after the user allows it: read logs (`journalctl -u <svc> --since "1 hour ago"`, `tail`), read status (`systemctl status`), read resources (`df -h`, `free -m`, `ss -tlnp`).

## Database migrations on shared or production databases

Pause for the user before any migration that is unreviewed, contains `DROP`, `ALTER COLUMN TYPE`, `RENAME` or a backfill, or is estimated over one minute. The agent: generates it, runs it on a fresh DB and on a copy, times it, writes the rollback (often "roll forward"), prints the command. Per-PR scratch databases may be migrated automatically.

## Deploy runbook template (`docs/runbooks/DEPLOY.md` in the project)

```markdown
# Deploy runbook
## Before
- [ ] CI green on the commit to deploy (link)
- [ ] Migration reviewed and timed on a copy (or none)
- [ ] New env vars set in production (names only)
- [ ] Rollback written: previous build id / roll-forward plan
## Deploy
1. Trigger (who, how)
2. Watch errors and latency for 30 minutes, compared with the previous hour
## Roll back if
- error rate above baseline x2, or p95 latency above <n> ms, or a failed health check
## After
- [ ] Health checks green · [ ] key user flow tried by hand · [ ] status page updated if users saw it
```

## Canary (Google SRE workbook, "Canarying releases")

- Send a small share of traffic to the new version and compare it with the control at the same time, not with yesterday.
- Watch a dozen or fewer signals that users feel: error rate by status code, latency percentiles. CPU alone is a weak signal.
- One canary at a time; length matched to how often you release.

## Cost ceilings

| Item | Rule |
|---|---|
| Platform plan limits (functions, bandwidth, storage, email) | alert at 80% |
| LLM API | hard cap per user per day and per month for the project; requests over the cap are refused |
| Background jobs | max duration and memory; killed beyond |
| Paid services | adding one is a hard human gate with the price stated |

## Secrets

- Names in `.env.example`, values only in the platform's secret store and the local `.env` (gitignored).
- Prefer short-lived credentials (OIDC) over stored keys.
- Rotate on exposure, on staff leaving, and on the provider's advice; record each secret's owner and rotation path in `SECURITY.md`.
