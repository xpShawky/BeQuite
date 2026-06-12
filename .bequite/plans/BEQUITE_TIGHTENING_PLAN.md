# BeQuite Tightening Plan (from the alpha.23 audits, 2026-06-12)

Improvements that were NOT safe/cheap enough to patch inline. Source audits: BEST_PRACTICE · DUPLICATION_AND_CONFLICT · GENERIC_OUTPUT_RISK · quality matrix. Safe patches already applied this pass: C11 status flip (6 surfaces) · AGENTS.md-as-standard rewrite in cross-agent docs · offers/ scaffold · Slidev verified-candidate note · monetization journey updated with C11.

## P0 — none open

(Everything P0-grade found by the audits was patched in-pass.)

## P1 — next maintenance pass

| Item | What | Why deferred |
|---|---|---|
| problem-solver worked example | add one full reproduce→bisect→root-cause walkthrough to the skill | content-writing task, better done with a real bug as the example (pairs with first live /bq-fix) |
| multi-model-planning phasing refresh | update its phase/mode references to the current 4-mode + contract system | needs a careful read of the full 200+ line skill; not a one-line patch |
| `skill/` heavy-era root dir | add a DEPRECATED-pointer README inside it, or move to docs/legacy | touching retired assets = user decision (mild destructive risk) |
| Live trials (the big one) | first real runs of C5/C3/C11 etc. | user-initiated by definition; every audit names this as the dominant quality unknown |

## P2 — on demand / with live use

OWASP citation refresh at next security run · frontend reference refresh at next FE build · product-strategist pricing section on first pricing use · V1 argument procedure blocks (13, build on first demand) · USING runbook walkthrough refresh after first capability live run · presentation tool comparison refresh at first deck build (Slidev already verified).

## Watch-items (no action, monitored)

Conventional-enforcement gap (models can ignore instructions; hooks + Guard Pass are the mitigations — revisit if live trials show drift) · data-product↔C7 merge-watch · NEXT_COMMAND_LOG learning loop (needs accumulated entries before tuning).

**Rule:** items graduate from this plan via the normal maintenance/feature workflows; nothing here authorizes a build by itself.
