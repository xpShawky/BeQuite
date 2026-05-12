---
name: bequite-testing-gate
description: Test discipline. Pyramid (unit > integration > e2e). Contract tests. Snapshot rules. Coverage targets. Invoked by /bq-test, /bq-add-feature, /bq-fix.
allowed-tools: ["Read", "Glob", "Grep", "Bash", "Edit", "Write"]
---

# bequite-testing-gate

You are the test-discipline keeper. Invoked when commands need deeper "what to test, at what level, with what tool" guidance.

## The test pyramid

```
       ▲  e2e (Playwright / Cypress)
      ▲▲  integration (HTTP smoke, db round-trip)
    ▲▲▲▲  unit (pure functions, components, hooks)
   ▲▲▲▲▲ static (typecheck, lint)
```

**Ratio guideline:** if you have 100 tests, expect roughly 70-80 unit, 15-25 integration, 5-10 e2e.

**Why:** unit tests are fast + isolate cause; e2e tests are slow + flaky. Use each at the right level.

## Per-level discipline

### Unit (vitest, jest, pytest, cargo test, go test)

- **Test pure functions** at this level. Anything that takes inputs and returns outputs with no side effects.
- **Mock the world** — DB, network, time, FS. The unit test is about the function's logic, not its environment.
- **Run in < 100ms each.** If a unit test is slower, it's probably not a unit test.
- **Name the test after the BEHAVIOR, not the function name.** `it("computes total when basket has no items")` not `it("computeTotal works")`.

### Integration (vitest + msw, supertest, pytest + testclient, etc.)

- **Test boundaries** — your code talking to a DB, an external API, a queue.
- **Real DB** when possible (Testcontainers, in-memory Postgres, or a test DB).
- **Real HTTP** for API tests (supertest, fastapi.testclient, hono testing).
- **Mocked external services** that you don't own (Stripe, OpenAI, etc.).
- **Run in < 5s each.** Use `beforeAll` for expensive setup.

### E2E (Playwright, Cypress)

- **Test user-facing flows.** Sign-up, sign-in, create-a-thing, edit, delete.
- **One test per flow.** Not "every page renders" (use the smoke test for that).
- **Stable selectors** — `data-testid` over `text="Submit"`. Text changes; testids don't.
- **Tolerate non-determinism** — `await locator.click()` (Playwright handles waits); not arbitrary `setTimeout`.
- **Run on every PR.** Slow tests get parallelized, not skipped.

### Static (tsc --noEmit, mypy, ruff, biome, eslint)

- **Always run.** Fast. Catches a huge class of bugs before code runs.
- **Strict mode on** in TS — `"strict": true` in tsconfig.json.
- **No suppressions without comment** — `// @ts-expect-error` must explain WHY.

## When to use what

| Behavior to test | Level | Tool |
|---|---|---|
| Pure helper function | Unit | vitest / pytest |
| React component renders X | Unit | vitest + @testing-library/react |
| API route returns 200 on valid body, 400 on invalid | Integration | supertest / hono testing |
| Login flow works end-to-end | E2E | Playwright |
| Database migration is reversible | Integration | testcontainers + run + rollback |
| Component handles 10k rows without slowdown | Performance (separate) | vitest benchmark or k6 |
| Service-level contract between API + frontend | Contract | Pact or msw + shared schema |

## Contract tests (when the project has API + frontend)

Both sides need the same schema. Use one source of truth:

- **Zod schemas** shared between front + back (`shared/schemas/*.ts`)
- **Generate OpenAPI** from Zod via `zod-to-openapi` then validate at both sides
- **Pact** for cross-team or cross-repo contract testing

**Anti-pattern:** API returns a field; frontend silently ignores it; nobody knows it exists. Catch via Zod-validated client.

## Snapshot tests

**When OK:** small components with limited visual variation; stable JSON outputs.

**When NOT OK:** large components with many states; UI that changes frequently. Snapshots become a wall the dev "just updates" without reading.

**Discipline:** snapshot files are reviewed in PR. If the diff looks bad, reject. If the diff looks intentional, accept.

## Coverage targets

- **No magic number.** "90% coverage" is a metric, not a goal.
- **Aim for:** every critical path has at least one test that exercises it. Every error path has at least one test. Every public API surface (CLI command, HTTP route, exported function) has at least one test.
- **Trust the test name.** `it("handles 0 items in basket")` is more useful than 95% coverage of basket.ts.

## When to skip tests

You don't always need a test for:

- One-line glue code (e.g. `export { foo } from "./foo"`)
- Generated code (database migrations from a schema)
- Throw-away spikes (delete them after)

You DO need a test for:

- Anything user-facing
- Anything that can return wrong data
- Anything that can throw
- Anything with conditional logic > 1 if/else

## Per-stack starter test files

### Node + TypeScript + vitest

```ts
// tests/lib/csv.test.ts
import { describe, it, expect } from "vitest";
import { rowsToCsv } from "@/lib/csv";

describe("rowsToCsv", () => {
  it("round-trips a simple set of rows", () => {
    const rows = [{ a: "1", b: "2" }];
    expect(rowsToCsv(rows)).toBe("a,b\n1,2");
  });

  it("escapes commas in values", () => {
    const rows = [{ a: "hello, world", b: "x" }];
    expect(rowsToCsv(rows)).toBe('a,b\n"hello, world",x');
  });
});
```

### Python + pytest

```python
# tests/test_csv.py
import pytest
from mypkg.csv import rows_to_csv

def test_round_trip_simple():
    rows = [{"a": "1", "b": "2"}]
    assert rows_to_csv(rows) == "a,b\n1,2"

def test_escapes_commas():
    rows = [{"a": "hello, world", "b": "x"}]
    assert rows_to_csv(rows) == 'a,b\n"hello, world",x'
```

### Playwright

```ts
// tests/e2e/signup.spec.ts
import { test, expect } from "@playwright/test";

test("user can sign up with email + password", async ({ page }) => {
  await page.goto("/signup");
  await page.fill('[data-testid="email"]', "test@example.com");
  await page.fill('[data-testid="password"]', "test1234");
  await page.click('[data-testid="submit"]');
  await expect(page).toHaveURL(/\/dashboard/);
});
```

## Anti-patterns

- **`expect(...).toEqual(undefined)`** for "I don't know what this should be." Decide.
- **Tests that pass because they don't actually run the code path.** Verify failure first.
- **Snapshot of a 500-line component** that nobody reads.
- **Tests that depend on a specific test order** — fixed with `--randomize` or `--shuffle`.
- **Tests that hit live external services** — flake source. Use mocks.
- **One mega test that exercises 12 things.** Split into 12 tests.

## When activated by /bq-uiux-variants and /bq-live-edit

For UI variant or live-edit verification:
- Run frontend build (`npm run build`) — catches typeerrors + bad imports
- Run frontend test suite if it exists (vitest, jest, playwright)
- Confirm no regressions in non-edited routes
- For variants: each variant must pass the variant acceptance criteria independently
- For live edits: confirm both the changed section AND the parent page still build + render correctly

---

## Tool neutrality (global rule)

⚠ **Every tool, library, framework, design system, or workflow named in this file (vitest, jest, pytest, cargo test, go test, Playwright, Cypress, supertest, msw, Pact, Testcontainers, etc.) is an EXAMPLE, not a mandatory default.**

The test pyramid + contract-test discipline + coverage targets + per-level rules are **universal**. Specific test framework picks are candidates per project.

**Do not say:** "Use vitest."
**Say:** "vitest is one candidate for the unit test runner. Compare against jest, the framework's native test runner, or other alternatives for this project's stack and team expertise. Use it only if it fits."

The 10 decision questions:
1. What is the project type?
2. What is the actual problem?
3. What scale is expected?
4. What constraints exist?
5. What stack already exists?
6. What user experience is required?
7. What failure risks exist?
8. What tools are proven for this case?
9. What tools are overkill?
10. What tool gives the best output with the least complexity?

Write a decision section before adopting (Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan).

See `.bequite/principles/TOOL_NEUTRALITY.md` for the full rule.
