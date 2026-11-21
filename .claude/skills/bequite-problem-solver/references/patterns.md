# Debugging patterns (2026-11-21)

## Symptom to likely cause

| Symptom | Check first |
|---|---|
| Works locally, fails in CI or a clean clone | untracked or gitignored files on your disk; env vars set only locally; runtime version; timezone and locale; case-sensitive paths |
| Works in dev, fails in prod | build-time env vars baked into the bundle; `NODE_ENV`-style branches; different database or data; CDN cache |
| Intermittent | race or shared state; order-dependent tests; network timeouts; clock |
| Only on Windows | path separators; CRLF line endings; shell builtins; file locks; long paths |
| Only on macOS | case-insensitive file system hiding a wrong-case import |
| Worked yesterday | lockfile diff; an unpinned dependency; an upstream API change; an expired token or certificate |
| "Permission denied" | file mode; container user; a hook or policy blocking the call |
| "Module not found" | the dependency not installed; ESM vs CJS resolution; wrong working directory |
| Memory grows | unbounded cache; listeners never removed; a loop collecting results |
| CORS error | the server does not echo the origin; the preflight route 404s; credentials with `*` |
| Button does nothing | no network request means client side: read the console; a prop or handler renamed in one place only |

## Environment difference checklist (passing vs failing)

Commit SHA · runtime versions (`node -v`, `python -V`) · OS · env var names (not values) · lockfile hash · untracked files (`git status --ignored`) · config files · data set · time and timezone · network access.

## Bisect script template

```bash
#!/usr/bin/env bash
# exit 0 = good, 1 = bad, 125 = cannot test this commit (skip)
npm ci --silent >/dev/null 2>&1 || exit 125
npm test -- --run tests/booking.test.ts >/dev/null 2>&1
```

```bash
git bisect start <bad-sha> <good-sha>
git bisect run ./bisect.sh
git bisect reset            # always return to the original branch
```

For a speed regression: `git bisect start --term-old fast --term-new slow`.

## Pitfalls (Google SRE, "Effective troubleshooting")

- Chasing symptoms that are not related to the failure.
- Changing the system in an unsafe way while testing a theory.
- Favouring an exotic theory over a common cause.
- Assuming the cause of the last incident is back.
- Taking a correlation for the cause.

## Shrinking a failing input (delta debugging, by hand)

1. Split the input (file, config, list of steps) in half.
2. Keep the half that still fails; if neither fails alone, split into quarters and test the complements.
3. Repeat until removing any single piece makes it pass.
4. Paste the minimal input into the log; it often names the cause by itself.
