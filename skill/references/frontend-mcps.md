# Frontend MCP wiring (May 2026)

> The three MCPs Doctrine `default-web-saas` recommends, plus tweakcn, plus context7. Loaded on demand by the **frontend-designer** persona during P5. Cross-referenced from `skill/skills-bundled/impeccable/SKILL.md`.

## 1. shadcn Registry MCP — built-in to shadcn CLI v3+

### Purpose

Add shadcn components by name without leaving the agent loop. The MCP is exposed by the official `shadcn` CLI v3+ (released late 2024); no separate package required.

### Wiring

In a project's `.claude/settings.json` or equivalent host config:

```json
{
  "mcpServers": {
    "shadcn": {
      "command": "npx",
      "args": ["-y", "shadcn@latest", "registry:mcp"]
    }
  }
}
```

### Usage

The frontend-designer invokes:

```
mcp shadcn list
mcp shadcn add button
mcp shadcn add data-table
```

Components install into the project's configured directory (typically `components/ui/`). All shadcn components are MIT-licensed copy-paste; full ownership.

### When to use

- Adding any "standard" UI component (button, input, card, dialog, dropdown, select, checkbox, toast, etc.).
- Adding shadcn blocks (full sections like dashboard, sign-in form, settings layout).
- When you want copy-paste components you can modify freely.

### When NOT to use

- For fully custom components (use Magic MCP or hand-author).
- For animation-heavy components (consider Aceternity/Magic UI).

### Cost

Free. No API key.

---

## 2. 21st.dev Magic MCP — `@21st-dev/magic`

### Purpose

Generate component variations from a natural-language prompt. Useful for *unfamiliar* component shapes — when shadcn doesn't have it and you'd rather not hand-author from scratch.

### Wiring

```json
{
  "mcpServers": {
    "magic-21st": {
      "command": "npx",
      "args": ["-y", "@21st-dev/magic@latest"],
      "env": {
        "TWENTY_FIRST_API_KEY": "${TWENTY_FIRST_API_KEY}"
      }
    }
  }
}
```

### API key

- Required. Sign up at https://21st.dev/.
- Tier as of May 2026: free tier with daily quota; paid tiers for higher throughput.
- Store key in your env-loader (Doppler / Infisical / `.env` excluded from repo).
- BeQuite hook `pretooluse-secret-scan.sh` blocks accidental commits of the key.

### Usage

The frontend-designer invokes via slash:

```
/ui a multi-select dropdown with chips and async search
```

The MCP returns multiple component variations. The designer picks one, integrates with the project's tokens (Impeccable's `craft` command).

### When to use

- Unusual component shapes (complex selectors, custom data-vis primitives, AI-chat-input style components).
- When shadcn / Aceternity / Origin UI don't have it.
- When you need multiple variations to compare quickly.

### When NOT to use

- For standard components (use shadcn).
- For exact-spec layouts (prompts produce variations, not pixel-perfect specs).
- When offline or air-gapped (see `claude-code-full` vs `api-portable` skill modes; v0.14.0 docs).

### Cost

Per-prompt token spend on 21st.dev side; respect the project's cost ceiling.

---

## 3. context7 MCP — Upstash, version-pinned docs

### Purpose

Pull library documentation pinned to the version you're actually using. Solves the "Claude knows the API for v3 but you're on v5" rot.

### Wiring

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

### Usage

```
mcp context7 use shadcn/ui
mcp context7 ask "How do I customize the data-table sorting?"
mcp context7 use radix-ui/react-dropdown-menu@2.0.6
```

The MCP loads the version's docs directly into context.

### When to use

- Before invoking any unfamiliar library API.
- When troubleshooting why a documented API isn't working (you might be on a different version).
- When choosing between version-pinned alternatives.

### When NOT to use

- For libraries context7 doesn't index (rare; check before assuming).
- When you can read the local README more cheaply.

### Cost

Free tier as of May 2026. No API key.

---

## 4. tweakcn — visual theme editor (NOT an MCP)

### Purpose

Generate a `tokens.css` / theme JSON visually, then drop into shadcn. Pair with the BeQuite `tokens.css.tpl` template to seed a deliberate theme.

### Usage

1. Visit https://tweakcn.com/.
2. Tweak the theme visually.
3. Export as JSON or CSS.
4. Merge exported tokens into project's `tokens.css` (use Impeccable `extract` command to incorporate).
5. Document the theme rationale in `tokens.css` comment per Doctrine Rule 2.

### When to use

- Project kickoff (P1/P2 — establishing brand tokens).
- Brand refresh.
- When a designer is providing a visual brief but not raw tokens.

### Cost

Free.

---

## 5. Cross-MCP playbook

### Project kickoff sequence

1. **tweakcn** — visualize the brand palette + radii + typography.
2. Export to `tokens.css` (use BeQuite's `tokens.css.tpl` as the base; merge tweakcn's color values).
3. **context7** — pin shadcn / Tailwind / Next versions; load docs for the actually-installed versions.
4. **shadcn registry MCP** — add base components into the project (Button, Input, Card, Dialog, Form).
5. Manual review: confirm `tokens.css` reflects the theme; confirm shadcn components inherit tokens correctly.

### Adding a custom component during P5

1. Search shadcn / Aceternity / Magic UI / Origin UI first.
2. If nothing fits, **Magic MCP** with a precise prompt.
3. Pick a variation; integrate with project's tokens.
4. Run `bequite design audit`; iterate.

### Refreshing during a stack-bump

1. **context7** — pull the new version's docs.
2. Run `bequite freshness` to confirm no breaking changes in unsupported direction.
3. **shadcn registry MCP** — re-add components if the registry has updates.
4. Run `bequite design audit` to confirm visual regression-free.

## Anti-patterns when wiring frontend MCPs

- **Letting Magic MCP define the tokens.** It returns generated styles; treat them as suggestions, not authority. Your `tokens.css` remains the source of truth.
- **Letting context7 substitute for reading the actual code.** The docs lag the code; verify behavior in the running app before trusting.
- **Skipping tweakcn for "I'll pick a color later."** Tokens get hardcoded once; later is harder.

## Cross-references

- **Bundled Impeccable:** `skill/skills-bundled/impeccable/`
- **Tokens template:** `skill/templates/tokens.css.tpl`
- **Frontend stack:** `skill/references/frontend-stack.md`
- **Doctrine:** `skill/doctrines/default-web-saas.md`
- **Designer persona:** `skill/agents/frontend-designer.md`
- **Slash commands:** `skill/commands/design-audit.md`, `skill/commands/impeccable-craft.md`
