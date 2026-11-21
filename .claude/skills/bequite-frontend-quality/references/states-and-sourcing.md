# Real states, component sourcing, per-feature checklist (2026-11-21)

## Real states (each one reachable and looked at in the browser)

| State | Pass |
|---|---|
| Empty | says what goes here and offers the one action that fills it ("Add your first patient") |
| Loading | skeleton for content, spinner only for an action; falls back to an error state if it hangs (pick a limit, for example 10 s) |
| Error | says what failed and what to do next, in the user's words; a retry where retrying helps |
| Success | confirms what happened, where the result is |
| Partial and long | 1 item, 10x the designed amount, very long names, RTL text |

Reach each state by stubbing the API in the browser tool or with a test fixture, then screenshot it.

## Honest data

- A chart or counter labelled live is fed by real data. Demo data is labelled as demo.
- Placeholder names, emails and dates look like real ones from the product's market, never lorem ipsum.

## Component sourcing order

1. The project's own components (extend before adding).
2. An open-source kit the project already uses, copied into the repo where the kit works that way (for example shadcn/ui registries; its MCP server can browse and install registry items).
3. A reference component studied from 21st.dev, mobbin.com or refero.design, rebuilt in the project's tokens (learn the manner, do not paste foreign styles).
4. Custom, when 1 to 3 do not fit.

Check licences of anything copied; check versions in the registry this session.

## Per-feature checklist

- [ ] Rendered and screenshotted at desktop and 375 x 812
- [ ] Tell sweep run; hits fixed or justified
- [ ] Empty, loading, error, success states shown
- [ ] No invented data
- [ ] Every new button clicked; focus visible on tab
- [ ] Contrast and target size checked on the rendered page
- [ ] No new font, colour or radius outside the tokens without a DNA note
