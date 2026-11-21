<div align="center">

# BeQuite

**A workflow pack for Claude Code that makes the agent research and plan before it builds, and prove its work before it says done.**

**Version:** `1.0.0` · MIT · by [@xpShawky](https://github.com/xpShawky)

<a href="commands.md"><img alt="55 commands" src="https://img.shields.io/badge/slash_commands-55-7c3aed?style=flat-square"></a>
<a href="#skills"><img alt="38 skills" src="https://img.shields.io/badge/skills-38-10b981?style=flat-square"></a>
<img alt="zero runtime deps" src="https://img.shields.io/badge/runtime_deps-0-0ea5e9?style=flat-square">
<img alt="markdown only" src="https://img.shields.io/badge/install-markdown_only-f59e0b?style=flat-square">

</div>

---

## What it is

BeQuite is a set of slash commands, skills, subagents and hooks for Claude Code, written in plain markdown with a few small scripts. It gives every piece of work the same path: find out what is true, choose between real options, get a yes on the plan, build it in small steps, have something independent check it, and write down what happened. A project keeps its memory in a `.bequite/` folder, so the next session (or the next model) starts where the last one stopped.

It also covers work that is not code. A film studio directs motion pieces from studied references. A content studio goes from what is moving in a niche to a packaged post that waits for your yes. An agent team works a ticket board on a schedule, inside a token budget, with an editor that can reject a draft.

## The workflow

```
 0 up to date   1 orient   2 references   3 research   4 options board
 (update check) (memory)   (creative work) (dated sources) (built from what you have)
        |                                                        |
        v                                                        v
 10 write back  <-  9 verify  <-  8 guard  <-  7 build  <-  6 approval  <-  5 plan
 (log, lessons)    (evidence)    (second pass) (one task at a time)  (your yes)
```

Every command is an entry point into this one pipeline ([PIPELINE.md](.claude/bequite/docs/architecture/PIPELINE.md)). `/bq-auto` runs all of it for one intent; `/bq-feature`, `/bq-fix`, `/bq-motion` and `/bq-content` preset the stages; the phase commands (`/bq-plan`, `/bq-verify` and the rest) run one stage by hand. A missing gate stops the command and names the step that has to come first. Some steps always wait for you: deleting things, touching production or a shared database, secrets, paid services, a release, and for creative work the script, the style and the render plan.

## Five-minute start

As a plugin:

```
/plugin marketplace add xpShawky/BeQuite
/plugin install bequite@bequite
```

Plugin commands carry the plugin's name: `/bequite:bq-auto`, `/bequite:bq-plan`. The hooks are on from the start.

With the script installer, inside the project you want to work on:

```powershell
# Windows
irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.ps1 | iex
```

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.sh | bash
```

Then, in Claude Code:

```
/bequite                                  the menu: where the project stands and the next three commands
/bq-doctor                                checks the environment and records what this machine can do
/bq-auto feature "Add a booking page"     one feature through the whole pipeline
/bq-suggest "what I want to do"           not sure where to start
```

The installer copies the commands, skills, subagents, docs and hooks into `.claude/`, adds a `.bequite/` scaffold and a section in `CLAUDE.md`. Your project memory is never overwritten, not by a re-install and not by an update.

**Coming from v4?** Run the installer once more with `--force` (`$env:BEQUITE_FORCE=1` on Windows). v4 has no update check, so it cannot move itself to v1; from v1 on, updates are automatic.

## Packs

| Pack | Commands | Skills | For |
|---|---|---|---|
| **core** | 45 | 26 | the engineering pipeline, memory, research, review and verification, the agent team, the harness commands |
| **studio** | 5 | 10 | films (`/bq-motion`), decks (`/bq-presentation`), content (`/bq-content`, `/bq-watch`, `/bq-dna`) |
| **business** | 5 | 2 | offers and proposals (`/bq-offer`), earning routes, jobs, turning work into a product |

All three install by default. To install fewer: `install-bequite.sh --packs core,studio`, or `$env:BEQUITE_PACKS="core"` before the PowerShell line. Core is always included and the choice is remembered for updates. What each pack holds: [core](.claude/bequite/docs/packs/core.md), [studio](.claude/bequite/docs/packs/studio.md), [business](.claude/bequite/docs/packs/business.md).

## What keeps it honest

- **Evidence before done.** A claim of done needs the command, its exit code and the output, or the word `UNVERIFIED:` with a reason. The Stop hook refuses a "done" that has neither, and one that leans on "should work" or "probably fixed".
- **Independent checks.** `bq-verifier` re-runs the evidence without having built the work; `bq-red-team` attacks risky plans and diffs. On this repository, the verifier found five stale pointers that the self-check had missed; both the pointers and the check were fixed.
- **Memory at every session start.** The SessionStart hook hands the agent the active work, its open gates, the last run, the five newest lessons and your taste rules before the first message.
- **A self-check in CI.** `python scripts/bq_check.py` checks installer safety, the plugin, the command contract, every path and command a file cites, counts, gates, packs and stale model names. Releases run it in strict mode.

## The human test

Creative work in BeQuite starts from real references, not from a model's defaults: sites, films, posts and decks people made, measured before anything is drafted. Before delivery it is checked against lists of things that make work look machine-made (for pages and decks, among others: decorative gradients, "01 / 02 / 03" section labels, thin body text under all-bold headings, coloured left-border note boxes). Writing in someone's voice is learned from their real samples and checked with a blind pick. When you correct the agent ("no, not like that"), the correction goes to an inbox, and `/bq-taste` turns it into a rule you approve, with the example that caused it.

## Off-label uses

People use the same pipeline for things that are not software:

- **A film without spending Claude credits.** A chat model (ChatGPT, Gemini or Claude) writes a kinetic-type film as JSON from six short files; the BQ Kinetic panel builds it in After Effects and makes a contact sheet the model reviews. In our test ChatGPT directed a 15-second intro in five rounds without a single edit to its JSON. See [examples/chat-directed-kinetic-film](examples/chat-directed-kinetic-film/).
- **A content desk.** `/bq-content radar` finds what is moving in a niche, with links and numbers; `study` measures the top five videos' format; `script` writes in your voice; `package` checks every platform limit; nothing is posted without a yes per post.
- **An agent team in a folder.** `/bq-team` runs six roles (chief, scout, analyst, writer, editor, producer) on heartbeats with a token cap per role. One post through the full team cost about 634,000 tokens in our first test, which is why heartbeats are off until you turn them on.
- **Selling the work.** `/bq-offer` builds an honest offer, a proposal for one client or a minimum digital system for a local business; `/bq-productize` turns a finished project into a product from its own evidence.

## Staying up to date

Every command starts with a short update check (at most once an hour). When the version published on GitHub differs from yours, BeQuite backs up its own files, updates them and carries on with your command; offline it simply continues. Set `**Auto update:** off` in `.bequite/state/UPDATE_SOURCE.md` to be told instead, and run `/bq-update` when you want. Plugin installs update through `/plugin`.

## Commands

The full list with arguments is in [commands.md](commands.md); `/bq-help` prints it inside Claude Code. The most used:

| Need | Command |
|---|---|
| start here | `/bequite`, `/bq-suggest "<goal>"` |
| one feature or fix | `/bq-feature "<title>"`, `/bq-fix "<symptom>"` |
| run a whole intent | `/bq-auto <intent> "<task>"` |
| check before shipping | `/bq-verify`, then `/bq-release` |
| a film, a deck, a post | `/bq-motion`, `/bq-presentation`, `/bq-content` |
| understand a video | `/bq-watch "<link>"` |
| a standing team | `/bq-team init` |
| watch the spend | `/bq-budget set 500k tokens` |

## Skills

38 skills hold the procedures: architecture and research, backend, database, security, DevOps and release, testing and debugging, a frontend design system with its quality checks, localization for Arabic and right-to-left layouts, automation (official API first, Scrapling as the scraping default), delegation between models, the human-taste and writing-voice skills, the film team (director, kinetic type, sound and voice, render pipeline), the content skills, the agent team, and the business skills. All but six of them were rewritten for v1 and name their sources and the date they were last checked; six still have to be brought up to that rule (the four film skills, the skill auditor and the updater). Registry: [SKILL_REGISTRY.md](templates/bequite/skills/SKILL_REGISTRY.md).

## Docs and contributing

Reference docs live in `.claude/bequite/docs/` (architecture, specs, runbooks, decisions). [CONTRIBUTING.md](CONTRIBUTING.md) explains how to change the pack and keep the self-check green; [CHANGELOG.md](CHANGELOG.md) lists what changed. BeQuite is MIT licensed.
