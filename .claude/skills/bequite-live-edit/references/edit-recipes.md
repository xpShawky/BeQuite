# Edit recipes: detection, change locus, failures, rollback (2026-11-21)

## Stack and dev server

| Signal | Stack | Usual dev command and port |
|---|---|---|
| `next` in `package.json`, `app/` or `pages/` | Next.js | `npm run dev`, 3000 |
| `nuxt.config.*` | Nuxt | `npm run dev`, 3000 |
| `svelte.config.js`, `src/routes/` | SvelteKit | `npm run dev`, 5173 |
| `vite.config.*` + `react` or `vue` | Vite app | `npm run dev`, 5173 |
| `astro.config.*` | Astro | `npm run dev`, 4321 |
| `index.html` only | static | `python -m http.server <port>` |

Read the real script in `package.json`; ports above are defaults, not facts about the project. Vite-based stacks hot-reload modules and keep app state through framework plugins (React Fast Refresh, Vue SFC); a full reload resets state.

## Finding the source of a visible section

1. Grep the visible text: `grep -rn "Book a slot" src app components`.
2. Read the element's attributes in the browser (`id`, `data-*`, class names); grep those.
3. Component names in the route file (top-level children of the page component).
4. Translations: the text may live in a locale file; edit the string there, not the component.

## Change locus

| Request | Change |
|---|---|
| Text | the component or the content/locale file |
| One section's spacing, size, layout | the component's classes or styles |
| The same value wrong everywhere | the token (with a DNA note) |
| Responsive break | the component's breakpoint rules; prefer fluid (`clamp`, `minmax`) over more breakpoints |
| Colour or contrast | the token if systemic, else the component; re-check the ratio |
| Missing state | the component plus the data hook that feeds it |
| Accessibility | the element (label, role, focus style, alt) |

Never: rewrite the page for a one-section request, add a library for a small edit, refactor neighbours, change tokens without a note.

## Failures

| Failure | Action |
|---|---|
| Dev server will not start | read the error; ask for missing env or services; do not invent values |
| Section ambiguous | one question with the candidates |
| Build or tests red after the edit | restore the logged snippet, retry smaller |
| Neighbour section moved | restore, scope the selector, retry |
| No visual tier available | manual steps for the user; mark `UNVERIFIED:` |
| Three failed attempts | stop and report |

## Rollback

- The log entry holds the old snippet; restoring it with an edit is the undo.
- Uncommitted single-file change: `git restore <file>` (or `git checkout -- <file>`) after confirming no other edits in that file are wanted.
- Never use bare `git stash` in shared worktrees; it can collide with other sessions.
