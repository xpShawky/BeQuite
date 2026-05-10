# tests/integration/audit/

Integration tests for `bequite audit` (cli/bequite/audit.py).

## Smoke

```bash
python -m cli.bequite.audit --repo .
```

Expected: zero `block` findings on the BeQuite repo itself (it eats its own food). `warn` findings about Inter font in the Constitution v1.0.1 amendment text are acceptable (the Constitution discusses Inter; it doesn't *use* it).

## Fixture-based tests (drafted v0.6.0+ when CI runner ships)

Each fixture is a minimal repo skeleton + expected findings.

```
tests/integration/audit/fixtures/
├── clean/                            — should produce zero findings
│   ├── state/project.yaml
│   ├── apps/web/src/Foo.tsx          (no Inter, no nested cards, no env reads)
│   └── ...
├── secrets-in-source/
│   └── apps/api/src/config.ts        (literal AKIA... → expect block finding)
├── nested-cards/
│   └── apps/web/src/Bar.tsx          (.card inside .card → expect block)
├── inter-without-reason/
│   └── apps/web/src/styles.css       (font-family: Inter without comment → warn)
├── env-reads/
│   └── apps/api/src/secrets.py       (open(".env") → expect block)
├── ai-automation-secret-in-flow/
│   └── .n8n/workflows/lead.json      (sk-ant-... in JSON → expect block)
└── library-telemetry-no-gate/
    └── packages/sdk/src/telemetry.ts (fetch to /telemetry without config gate → block)
```

## Per-rule expected output

| Fixture | Rule | Severity | Count |
|---|---|---|---|
| `clean` | (none) | n/a | 0 |
| `secrets-in-source` | `iron-law-iv-secrets/aws-akia` | block | 1 |
| `nested-cards` | `default-web-saas-rule-4-nested-cards` | block | 1 |
| `inter-without-reason` | `default-web-saas-rule-2-inter-no-reason` | warn | 1 |
| `env-reads` | `iron-law-iv-env-reads` | block | 1 |
| `ai-automation-secret-in-flow` | `ai-automation-rule-4-flow-secret/anthropic-key` | block | 1 |
| `library-telemetry-no-gate` | `library-package-rule-7-telemetry` | block | 1 |

## Running on the BeQuite repo itself

```bash
cd /path/to/bequite
python -m cli.bequite.audit
```

The repo's own active Doctrines (`library-package`, `cli-tool`, `mena-bilingual`) drive which rule packs run. Frontend Doctrine rules don't run on BeQuite-itself (no frontend). The audit is currently a zero-block, zero-warn pass when the Constitution amendment text is excluded from the Inter scan (it's Markdown discussing Inter, not code using it — `default-web-saas` Doctrine isn't loaded for BeQuite-itself, so the rule doesn't fire).
