# Contributing to BeQuite

BeQuite is markdown plus a few small scripts. A change is done when the self-check is green, the catalogs agree with the files, and anything you claim works has been run.

## Before every commit

```bash
python3 scripts/bq_check.py          # must end with no FAIL (warnings are allowed on branches)
bash scripts/test_update.sh          # only when bq-update.sh or an installer changed
```

CI runs both, plus an install with each installer. A `v*.*.*` tag runs `bq_check.py --strict` (warnings fail too) and creates the GitHub Release. Only the owner pushes tags. Every BeQuite install updates itself to a new release, so a release goes out to everyone.

## The rules the check enforces

- **The command contract.** Every action command carries the three-line block between `<!-- bq:contract -->` markers. Don't edit it by hand: change `CONTRACT_BODY` in `scripts/bq_check.py`, then run `python3 scripts/bq_check.py --fix contract`.
- **Installers.** `install-bequite.ps1` stays pure ASCII with no BOM, no `param()` or `CmdletBinding`, and no `exit`, because it runs through `irm | iex`. Shell scripts (`.claude/hooks/*.sh`, `.claude/bequite/bin/*.sh`, `install-bequite.sh`) use LF endings and a bash shebang. `bq-update.sh` keeps its whole body in `main()` and ends with `main "$@"` then `exit 0`. When an installer changes, test both end to end: bash with `--from-local`, and PowerShell through `[Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes(...)) | iex`.
- **Never build a sed or regex program from file contents.** Values from memory files go through `ENVIRON` in awk, and `$` is escaped in .NET replacement strings.
- **Counts and catalogs.** The numbers of commands and skills in `README.md`, `commands.md`, `CLAUDE.md` and the catalogs must match the folders.
- **Packs.** Every command and skill outside core is listed in `.claude/bequite/PACKS.txt`, and the pack column of `COMMAND_ID_MAP.md` and `SKILL_REGISTRY.md` agrees with it.
- **References.** Every path and `bq-*.md` file a document cites must exist.
- **Versions.** `VERSION`, both installers' fallback, `.claude-plugin/plugin.json` and the newest `CHANGELOG.md` release agree.
- **Models.** Name roles (strong, balanced, fast) from `MODEL_ROLES.md`, not model versions.

## Adding a command or a skill

1. Justify the shape first. Should it be a command, an argument of an existing command, or a skill (`FEATURE_TYPE_TAXONOMY.md`)? Most new ideas are a mode of an existing command.
2. In the same commit, update `COMMAND_ID_MAP.md` or `SKILL_REGISTRY.md` and `SKILL_ROUTER.md`, plus `ORCHESTRATION_MAP.md`, `commands.md`, `README.md`, `/bq-help`, the `/bequite` menu and `CHANGELOG.md`. Studio and business entries also go in `PACKS.txt`.
3. A skill names its sources and the date they were last checked (`last_verified`), and keeps to the size budget the check warns about.
4. Add at least one scenario under `evals/<skill>/` (see `evals/README.md`).
5. A new gate goes in `templates/bequite/state/WORKFLOW_GATES.md` (project) or `templates/bequite/work/_template/gates.md` (work) before anything uses it.

## Removing or renaming a file

Add its path (relative to `.claude/`) to `.claude/bequite/REMOVED.txt`. Installers and updates then move the old copy to `.bequite/backups/`, and never delete it. A hook that a user's settings still run is kept.

## What never goes in the repo

- Third-party media: reference films, frames, audio, fonts. `motion-library/` media is ignored, and only breakdowns are tracked.
- Secrets, tokens and account details, including the `LOCAL_CAPABILITIES` notes of anyone's machine.
- A project's `.bequite/` memory. This repo's own `.bequite/` is local only.

## Writing style for the pack

Plain, short, checkable. Every rule a skill states should be something a reviewer can test. A completion claim carries the command, its exit code and the output, or the word `UNVERIFIED:`. "Should work", "probably" and "seems to" are refused by the Stop hook.
