# Tech Context: {{PROJECT_NAME}}

> The technology choices, their pinned versions, the dev setup, and the operational constraints. Anything an engineer needs to be productive on day one — without re-deriving it from the codebase — lives here.
>
> Updated when a stack member is upgraded, swapped, or pinned. Mirrored in `package.json` / `pyproject.toml` / `Cargo.toml` (which are authoritative); this file is the human-readable summary.

---

## 1. Stack at a glance

| Layer | Choice | Version | ADR | Doctrine source |
|---|---|---|---|---|
| Frontend | | | | |
| Backend | | | | |
| Database | | | | |
| Auth | | | | |
| Hosting | | | | |
| CI / CD | | | | |
| Observability | | | | |
| Background jobs | | | | |
| Caching | | | | |
| Search | | | | |
| Email / notifications | | | | |
| Payments | | | | |
| File storage | | | | |
| Secrets | | | | |
| Code signing (desktop) | | | | |

## 2. Pinned versions (authoritative — copy from manifests)

```
# package.json (excerpt)
{{NPM_PINNED}}

# pyproject.toml (excerpt)
{{PIP_PINNED}}

# Cargo.toml (excerpt)
{{CARGO_PINNED}}
```

## 3. Local dev setup

The minimum to run this project locally. Aim for `git clone && <one command> && open localhost:<port>`.

```bash
# 1. Prerequisites
{{PREREQUISITES}}

# 2. Bootstrap
{{BOOTSTRAP_COMMAND}}

# 3. Run
{{RUN_COMMAND}}

# 4. Run tests
{{TEST_COMMAND}}
```

## 4. Environment variables

Listed by purpose, with defaults / where to obtain them. **Never commit `.env` files (Article IV).** Reference `.env.example` for the schema.

| Variable | Required | Purpose | Where to obtain |
|---|---|---|---|
| | | | |

## 5. External services

Every third-party API / service the project depends on, with auth method, rate limit, and incident channel.

| Service | Auth method | Rate limit | Status page | Incident channel |
|---|---|---|---|---|
| | | | | |

## 6. Dev-tool constraints

- **Node version:** {{NODE_VERSION}}  (`.nvmrc` / `.node-version`)
- **Python version:** {{PYTHON_VERSION}}  (`pyproject.toml::requires-python`)
- **Rust version:** {{RUST_VERSION}}  (`rust-toolchain.toml`)
- **OS targets:** {{OS_TARGETS}}
- **Browser targets:** {{BROWSER_TARGETS}}  (`browserslist`)
- **Editor extensions:** {{EDITOR_EXTENSIONS}}  (`.vscode/extensions.json`)

## 7. The freshness contract

`bequite freshness` runs against this stack on every `bequite stack` and quarterly via CI. A package is "fresh" iff:

- Last commit < 6 months
- No unfixed criticals (OSV scan)
- The vendor pricing tier this project assumed still exists
- Not in a recorded supply-chain incident (PhantomRaven, Shai-Hulud, Sept-8 attack, …)

When a package fails freshness, the project receives a freshness-warning receipt and the stack ADR enters `status: requires-review`.

**Last freshness sweep:** `{{LAST_FRESHNESS_SWEEP}}`
**Failures:** `{{FRESHNESS_FAILURES}}`
