# Test levels and starters (verified 2026-11-21)

Sizes follow "Software Engineering at Google", chapter 11. Locator and assertion rules follow the Playwright best-practices page and Testing Library's query priority.

## Levels

| Level | Allowed | Typical runtime | Use for |
|---|---|---|---|
| Static | type-check, lint | seconds for the repo | whole classes of bugs before anything runs |
| Small (unit) | one process; no network, disk, sleep or clock unless faked | milliseconds | pure logic, parsers, reducers, components rendered in isolation |
| Medium (integration) | one machine: real database (container or local), HTTP on localhost | under a few seconds each | routes, queries, migrations, queues |
| Large (end-to-end) | browser, deployed or full local stack | seconds to minutes | a few key user flows: sign-up, checkout, the main task |
| Contract | a shared schema checked on both sides | fast | API and client agreeing on shapes |

Rough mix by test count: 80% small, 15% medium, 5% large.

## What goes where

| Behaviour | Level |
|---|---|
| Helper returns the right value for edge inputs | small |
| Component shows the error text when the prop says so | small |
| `POST /bookings` returns 422 with a problem-details body | medium |
| Migration runs up on an empty database and on seeded data | medium |
| A user signs up and lands on the dashboard | large |
| Client and server agree on the booking schema | contract |

## Query and locator priority (UI)

`getByRole` (with `name`) → `getByLabelText` → `getByPlaceholderText` → `getByText` → `getByDisplayValue` → `getByAltText` / `getByTitle` → `getByTestId` (last resort). If an element has no accessible role or name, that is often an accessibility bug: report it.

## Snapshot tests

Fine for small, stable output (a serialised config, a short JSON response). Not for large components: reviewers stop reading the diff. Every snapshot change is read in review.

## Starters

Vitest:

```ts
import { describe, it, expect } from "vitest";
import { toCsv } from "../src/csv";

describe("toCsv", () => {
  it("quotes values that contain a comma", () => {
    expect(toCsv([{ a: "hello, world", b: "x" }])).toBe('a,b\n"hello, world",x');
  });
});
```

pytest:

```python
from mypkg.csv import to_csv

def test_quotes_values_that_contain_a_comma():
    assert to_csv([{"a": "hello, world", "b": "x"}]) == 'a,b\n"hello, world",x'
```

Playwright:

```ts
import { test, expect } from "@playwright/test";

test("a visitor can book a slot", async ({ page }) => {
  await page.goto("/book");
  await page.getByLabel("Email").fill("sara@example.com");
  await page.getByRole("button", { name: "Book 10:30" }).click();
  await expect(page.getByRole("heading", { name: "Booking confirmed" })).toBeVisible();
});
```

## Anti-patterns

- `expect(x).toBeDefined()` where the real value is known.
- A test that never ran the code path (no failing "before").
- `sleep(2000)` instead of waiting for a condition.
- One test checking twelve things; split it.
- Tests that call live third-party services.
- Retries configured to make a flaky test green.
