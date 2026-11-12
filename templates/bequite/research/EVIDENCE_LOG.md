# Evidence Log

> **Durable verification evidence** — the file backing `bequite-anti-hallucination`'s evidence-over-claims rule. Every "works / done / passes" claim in a long run records its proof here so it survives compaction and feeds `/bq-verify`, `/bq-review`, and audits. Short runs may paste evidence inline instead; long runs MUST externalize here.
>
> Created alpha.19 (Fable Strengthening Pass). Per `.claude/bequite/docs/architecture/CONTEXT_ENGINEERING_STRATEGY.md` + execution contract step 8.

---

## Entry format

```markdown
## <ISO 8601 UTC> — <claim being evidenced>
**Claim:** <e.g. "build passes after the auth fix">
**Command:** `<exact command>`
**Exit code:** <n>
**Key output:** <the lines that prove the claim — trimmed, not the whole log>
**Verified by:** <command run live this session | UNVERIFIED — reason>
**Related:** <file:line / task ID / gate>
```

Rules:
- One claim per entry. No entry → the claim is `UNVERIFIED:` and must be labeled so in any report.
- Trim output to the proving lines; link big logs by path instead of pasting.
- Never log secret values — reference by key name.
- Prune: archive entries for shipped releases into `EVIDENCE_LOG-<version>.md` at release time.

---

## Entries (newest at top)

(none yet - entries are added newest at top as work happens)
