---
description: Turn a finished, evidenced piece of work into something sellable - a service offer, a template or skill pack, a case study built only from the work's own evidence, landing copy, a five-minute demo script and a price test - with the sales channel checked for the seller's country. Business pack. Honest by contract - no invented results, no income promises.
---

# /bq-productize - finished work into a product

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

`/bq-offer` packages an idea; `/bq-productize` starts from work that already exists and already has proof. The proof is the product's strongest asset, so it is the only source for claims.

## Syntax

```
/bq-productize <work-id>                    # e.g. /bq-productize 0001
/bq-productize <work-id> as=service|template|skill|course|case-study
/bq-productize <work-id> lang=ar|en
```

## Preconditions

- The source work is closed: its `gates.md` shows the verify gate passed, and its `evidence.md` has entries. If not, refuse and name the missing gate.
- Nothing is published, listed, priced live or sent: BeQuite drafts; the user publishes (hard human gate).

## Honesty rules (refusal-grade)

- Every result in the case study quotes an entry from the source work's `evidence.md` (command and output, before and after, the number). No entry, no claim.
- No income or results promise. A guarantee covers only what the seller controls (redo, response time, refund terms).
- Client names, private data and other people's work never appear without written permission.
- Market and price claims come from pages read in this run (`bequite-researcher`), else `UNVERIFIED:`.

## Steps (after contract steps 1 to 7)

1. **Inventory.** Read the source work: `spec.md`, `plan.md`, `evidence.md`, `log.md`, the outputs. List what is reusable: code, prompts, skills, templates, a workflow, a measured result, a before-and-after.
2. **Pick the shape** with the user (offer the options with one line each; recommend one):
   - **service**: "I do this for you" (sellable this week; needs only proof);
   - **template or skill pack**: the reusable parts, cleaned (needs three evidenced uses before it is sold as a product: the same promotion rule the forge command uses);
   - **course or workshop**: the method, taught;
   - **case study only**: proof for an existing offer.
   Default when unsure: service first, then the template once three clients have used it.
3. **Strip and generalise** (template and skill shapes): remove secrets, client data and machine paths; make the parts run in an empty folder; a skill follows the open Agent Skills format (`name`, `description`, `SKILL.md` under 500 lines, `references/`, `scripts/`). Test it in a scratch folder; paste the run.
4. **Case study** `CASE_STUDY.md`: problem, constraint, what was done, the result with its evidence quotes, what it cost in time. Short. In the user's voice (writing DNA if present).
5. **Offer** (`product-strategist` rules): who it is for, the job, the alternative, why this, deliverables and exclusions, three tiers named by buyer type, anchored to the cost of the alternative.
6. **Channel check** for the seller's country, on each platform's own pages: can the seller be paid out, by which method, with which minimum and fee? Write the table in `CHANNELS.md` with URLs and dates. Never pick a channel with no verified payout.
7. **Landing copy and demo:** `LANDING.md` (headline from the job, proof block from the case study, tiers, one call to action) and `DEMO_SCRIPT.md` (what to show in five minutes, in order, using the real work). Both pass the human test (side by side with three real references, tell sweep) before delivery.
8. **Price test** `PRICE_TEST.md`: the first price, the cheapest test (five conversations, a pre-sale, a waitlist with the price shown), the signal that would change it, a review date.
9. **Route** with Next Command Recommendations.

## Writes

`.bequite/work/<new-id>/product/` : `INVENTORY.md`, `CASE_STUDY.md`, `OFFER.md`, `CHANNELS.md`, `LANDING.md`, `DEMO_SCRIPT.md`, `PRICE_TEST.md`, and `package/` for a template or skill pack. Plus the contract's write-back files.

## Skill routing

product-strategist (offer, price, risk) · make-money (channel and payout checks) · researcher (live pages) · anti-hallucination (claims) · human-taste (landing and demo) · writing-dna (voice) · localization-rtl (Arabic output) · presentation-builder (if a deck is wanted).

## Worked example (dry run on work 0002, 2026-11-21)

Source: work 0002 (the BeQuite v5 relaunch). Reusable: the five-track parallel task pack (`plan.md`, `tasks.md`), per-track evidence files, the Egypt payout verification method.

- Shape: **service** ("I set up a verified AI coding workflow in your repo in two days"), because the pack itself is free and open; the template comes after three client uses.
- Case study evidence: "13 skills rewritten from dated sources; every Egypt payout claim read on the platform's own page; self-check green before every commit" (each line quotes `evidence-C345.md`).
- Channels for a seller in Egypt (verified 2026-11-21): Khamsat and Mostaql pay out to Egyptian banks from $250 (PayPal from $25); Gumroad's payout for Egypt did not render (`UNVERIFIED:`); Lemon Squeezy excluded (closed to new sign-ups, shutting down 31 March 2027); Claude's plugin marketplace has no paid listings, so the pack stays free and the service is what is sold.

## Next Command Recommendations (typical)

- Source work not closed -> `/bq-verify` on it first.
- Shape is a pitch to one client -> `/bq-offer proposal`.
- Wants a deck for the demo -> `/bq-presentation`.
- Wants the landing page built -> `/bq-feature landing`.
