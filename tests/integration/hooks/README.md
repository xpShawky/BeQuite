# tests/integration/hooks/

Integration tests for the 10 BeQuite hooks. Each hook gets:

- **Positive fixtures** under `fixtures/<hook>/allow/` — input that should be allowed (exit 0).
- **Negative fixtures** under `fixtures/<hook>/block/` — input that should be blocked (exit 2).
- **Test runner** at `run-hook-tests.sh` (drafted v0.6.0 alongside the validation mesh).

## Running locally

```bash
# Once v0.6.0 ships, the runner is:
./tests/integration/hooks/run-hook-tests.sh
```

Pre-v0.6.0, manual smoke:

```bash
# Allow path: should exit 0
echo '{"tool_name": "Edit", "tool_input": {"new_string": "const greeting = \"hello\";"}}' \
  | bash skill/hooks/pretooluse-secret-scan.sh
echo "exit: $?"   # expect 0

# Block path: should exit 2
echo '{"tool_name": "Edit", "tool_input": {"new_string": "const apiKey = \"sk-ant-api03-FAKEFORTESTONLY-LOREMIPSUMDOLORSITAMETCONSECTETUR-FAKEFAKE\";"}}' \
  | bash skill/hooks/pretooluse-secret-scan.sh
echo "exit: $?"   # expect 2
```

## Hook → fixture map

| Hook | Allow fixtures | Block fixtures |
|---|---|---|
| `pretooluse-secret-scan.sh` | `fixtures/secret-scan/allow/`: clean code, env-var refs | `fixtures/secret-scan/block/`: AWS keys, GitHub tokens, Anthropic keys, Stripe keys, JWTs, Slack tokens, RSA private keys |
| `pretooluse-block-destructive.sh` | `fixtures/block-destructive/allow/`: `rm /tmp/foo`, `git status`, `npm install` | `fixtures/block-destructive/block/`: `rm -rf /`, `git push --force`, `DROP DATABASE`, `terraform destroy`, `:(){:|:&};:` |
| `pretooluse-verify-package.sh` | `fixtures/verify-package/allow/`: real packages (lodash, requests, serde) | `fixtures/verify-package/block/`: hallucinated package names, PhantomRaven targets (allowlist seeded with known-bad samples) |
| `posttooluse-format.sh` | `fixtures/format/`: language-mixed; no exit-2 case | n/a (warn-only) |
| `posttooluse-lint.sh` | `fixtures/lint/`: clean code | n/a (warn-only) |
| `posttooluse-audit.sh` | `fixtures/audit/clean/`: tokens-only design | `fixtures/audit/block/`: hardcoded `font-family: Inter` outside tokens |
| `stop-verify-before-done.sh` | `fixtures/stop-verify/allow/`: concrete completion ("ran `pytest`; exit 0; 12/12 pass") | `fixtures/stop-verify/block/`: weasel words ("should pass", "probably works", "I think it works") |
| `sessionstart-load-memory.sh` | always exit 0 | n/a (advisory print) |
| `sessionstart-cost-budget.sh` | always exit 0 | n/a (advisory print) |
| `stop-cost-budget.sh` | `fixtures/cost-budget/under/`: 50% ceiling | `fixtures/cost-budget/over/`: 100% ceiling without override |

## Acceptance criteria (v0.3.0)

- All 10 hooks executable (`chmod +x` applied — verified on POSIX; Windows uses Git Bash).
- Hook-protocol contract obeyed: read JSON from stdin, exit 0/2, errors to stderr.
- Each hook's blocking fixture exits 2; allow fixture exits 0.
- `template/.claude/settings.json` wires all hooks under the correct event matchers (PreToolUse / PostToolUse / Stop / SessionStart).

## CI integration (v0.6.0+)

The runner runs in `.github/workflows/ci.yml` on every push touching `skill/hooks/**` or `tests/integration/hooks/**`.
