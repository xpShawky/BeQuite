# skill/references/package-allowlist.md

> Known-good packages for `pretooluse-verify-package.sh` + `cli/bequite/audit.py` + `cli/bequite/freshness.py`. Append-only; remove only via ADR.
>
> Format: one package per backtick-wrapped entry. Ecosystem prefix optional (auto-detected from manifest):
> `<pkg>` for npm; `pypi:<pkg>` for PyPI; `cargo:<pkg>` for Rust crates. Lines starting with `#` are comments and ignored.

## Ecosystem-agnostic well-known names

`anthropic`
`openai`
`google-genai`

## npm — stack matrix favourites (post brief reconciliation)

`next`
`react`
`react-dom`
`hono`
`fastify`
`@nestjs/core`
`tailwindcss`
`@radix-ui/themes`
`shadcn`
`zod`
`drizzle-orm`
`@prisma/client`
`prisma`
`@supabase/supabase-js`
`better-auth`
`@clerk/clerk-sdk-node`
`@playwright/test`
`@playwright/mcp`
`@21st-dev/magic`
`@upstash/context7-mcp`
`vitest`
`turbo`
`pnpm`
`storybook`
`bullmq`
`inngest`
`temporalio`
`@temporalio/client`
`@temporalio/worker`
`n8n`

## PyPI — stack matrix favourites

`pypi:fastapi`
`pypi:pydantic`
`pypi:click`
`pypi:typer`
`pypi:rich`
`pypi:httpx`
`pypi:anthropic`
`pypi:openai`
`pypi:google-genai`
`pypi:hatchling`
`pypi:setuptools`
`pypi:pip`
`pypi:uvicorn`
`pypi:gunicorn`
`pypi:sqlalchemy`
`pypi:alembic`
`pypi:psycopg`
`pypi:asyncpg`
`pypi:redis`
`pypi:pytest`
`pypi:pytest-asyncio`
`pypi:pytest-cov`
`pypi:ruff`
`pypi:black`
`pypi:mypy`
`pypi:pyright`
`pypi:cryptography`
`pypi:tomli`
`pypi:dvc`
`pypi:mlflow`
`pypi:wandb`

## Rust crates — stack matrix favourites

`cargo:tokio`
`cargo:reqwest`
`cargo:serde`
`cargo:serde_json`
`cargo:clap`
`cargo:anyhow`
`cargo:thiserror`
`cargo:tracing`
`cargo:tauri`
`cargo:tauri-plugin-keyring`
`cargo:keyring`

## Known-DEPRECATED — DO NOT add as fresh

These are listed for reference only. `bequite freshness` flags them as `stale-block`.

# tauri-plugin-stronghold       — deprecated; removed in Tauri v3 (use tauri-plugin-keyring)
# roo-code                       — host shutting down 2026-05-15

## Adding a package

1. Verify package exists in the relevant registry (`npm view <pkg>` / `pip index versions <pkg>` / `cargo search <pkg>`).
2. Run `bequite freshness --package <name> --ecosystem <eco>`; verdict must be `fresh`.
3. Append the line above (with the right ecosystem prefix).
4. Commit with message `chore(allowlist): add <pkg> (rationale: ...)`.

## Removing a package

Removal requires an ADR documenting:
- Why this package is no longer trusted.
- What replacement is being adopted.
- Migration plan for existing usages.

Then this file gets a delete commit referencing the ADR.
