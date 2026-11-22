# BeQuite changelog

Format: [Keep a Changelog v1.1](https://keepachangelog.com/en/1.1.0/). Versioning: [Semantic Versioning](https://semver.org/). The history before the v1 relaunch is in [docs/history/CHANGELOG-before-v1.md](docs/history/CHANGELOG-before-v1.md).

## [1.0.0] - unreleased (release candidate; the owner tags it)

BeQuite relaunched. One pipeline instead of a pile of commands, three packs, a plugin, hooks that hold the rules, subagents where they pay, and skills rewritten from dated sources.

### Added
- **The pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`): up to date, orient, references (creative work), research, options board, plan, approval, build, guard, verify, write back. `/bq-auto`, `/bq-feature`, `/bq-fix`, `/bq-motion` and `/bq-content` are routes into it; each command carries a three-line pointer instead of an eight-line contract.
- **Plugin** (`.claude-plugin/plugin.json`, `marketplace.json`): install with `/plugin marketplace add xpShawky/BeQuite` then `/plugin install bequite@bequite`. `claude plugin validate .` passes.
- **Hooks**: SessionStart injects the active work, open gates, the last run, the five newest lessons, the taste rules and the capability summary; Stop refuses a "done" with no evidence or with a banned weasel word; UserPromptSubmit logs the user's corrections to `TASTE_INBOX.md`. Automatic in the plugin, opt-in for script installs (`/bq-hooks`).
- **Subagents** (`agents/`): `bq-researcher`, `bq-verifier`, `bq-red-team`, `bq-scout`, with the cost rule in the orchestrator (a subagent only when the reading is wider than five sources, a check must be independent, or the output would flood the context).
- **Packs**: core (45 commands, 26 skills), studio (5, 10), business (5, 2). `install-bequite.sh --packs core,studio` or `$env:BEQUITE_PACKS`; the choice is remembered for updates.
- **Automatic updates**: every command first runs `.claude/bequite/bin/bq-update.sh` (hourly); when a new official GitHub Release is published (the owner tags it and the strict self-check passes), it backs up, installs that release from one clone, puts the old files back if anything fails, and carries on; a push to `main` never reaches users by itself; other repos and paths inside the project are reported, never run; offline it continues; memory is never overwritten. `scripts/test_update.sh` tests this path in CI. Pack files a version removes are moved to `.bequite/backups/`, never deleted.
- **Content studio** (studio): `/bq-content` (radar, study, script, produce, package, queue, from-work, brand-kit, community, course), `/bq-watch`, `/bq-dna`; skills `bequite-video-intel`, `bequite-trend-radar`, `bequite-format-dna`, `bequite-hooks-and-copy`, `bequite-publish-prep`.
- **Agent team** (core): `/bq-team` (roles on heartbeats, per-role budgets, an editor that can reject, approvals before any post or spend) and `/bq-operator` (a Telegram bridge with an allow-list, read-only runs and Approve/Decline); skill `bequite-agent-team` with its ledger and 56 offline tests.
- **Harness commands** (core): `/bq-budget` (a credit ceiling per work), `/bq-taste` (corrections into DNA rules, saved only on a yes), `/bq-forge` (a proven procedure becomes a skill after three evidenced uses), `/bq-eval` (scenarios per skill; scripted ones cost nothing, model ones run on the fast model).
- **`bequite-human-taste`** (core): creative work starts from studied human references and passes the human test.
- **BQ Kinetic** in `bequite-kinetic-type`: a chat model directs kinetic type as JSON and an After Effects panel builds it; ChatGPT directed a 15-second film in five rounds without a single edit to its JSON.
- **`/bq-productize`** (business): finished work into a sellable asset built from its own evidence.
- **Capability inventory**: `/bq-doctor` writes `.bequite/state/CAPABILITIES.md`; every plan's options board is built from it.
- `bq_check.py`: nine checks that fail the run (installer safety, plugin JSON and version, shell scripts LF and bash, packs against the catalogs, command files cited by name, skill-relative paths, git-ignored paths) and two that warn (size budgets, skill sources).

### Changed
- 21 skills rewritten to the v1 rubric with dated sources (engineering, frontend, research and context, business, writing); the orchestrator absorbed the routing table and the operating card.
- `/bq-auto` 527 to 102 lines; `/bq-feature` 288 to 55; `/bq-fix` 406 to 55.
- Model names replaced by roles (strong, balanced, fast) in one file, `MODEL_ROLES.md`.
- Ten small capability commands folded into modes of `/bq-knowledge`, `/bq-content` and `/bq-offer`.

### Removed
- The seven phase redirects (`/bq-now`, `/bq-p0` to `/bq-p5`).
- Six skills merged into `bequite-delegation`, `bequite-automation` and `bequite-orchestrator`.
- The PowerShell version of the Stop hook (the bash hook covers Windows through Git Bash).

### Upgrading from v4
Run the installer once with `--force` (`$env:BEQUITE_FORCE=1` on Windows): v4 has no update check, so it cannot update itself to v1. After that, updates are automatic. Your `.bequite/` memory is never overwritten.
