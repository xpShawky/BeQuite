# BeQuite update source configuration

Used by the automatic update check (`.claude/bequite/bin/bq-update.sh`, step 1 of every BeQuite command) and by `/bq-update`.

---

**Source type:** github
**Repo URL or local path:** https://github.com/xpShawky/BeQuite.git
**Default branch:** main
**Auto update:** on

## Automatic updates

Every BeQuite command first runs the update check (at most once an hour; a failed install is retried once a day). It installs, by itself, only:

- the latest **published GitHub Release** of the official repo (`xpShawky/BeQuite`). A release exists only after the owner tags a version and the strict self-check passes, so a push to `main` never reaches your project on its own;
- the **Pinned tag** below, when one is set;
- for `Source type: local`, the **last commit** of a BeQuite clone at an absolute path outside this project (never its uncommitted files).

Any other repo, a path inside this project, or a value that does not validate is reported and never run; use `/bq-update` for those.

When a new version is installed, BeQuite first copies `.claude/commands`, the BeQuite skills, `.claude/bequite`, `.claude/hooks`, `.claude/agents`, `CLAUDE.md`, `commands.md` and the version file into `.bequite/backups/<time>-v<old>/`. Pack files are replaced by the new version's copies, so an edit you made to a BeQuite command or skill is in that backup, not in the new file. If the install does not finish, the previous files are copied back. Your `.bequite/` memory is never overwritten. Offline, it says "skipped" and the work goes on.

Set **Auto update** to `off` to be told about new releases instead, then run `/bq-update` yourself (it merges around your edits file by file).

## Pinned tag (optional)

Leave blank to follow the latest release. Set a release tag (for example `v1.0.0`) to stay on it; BeQuite then installs exactly that tag.

**Pinned tag:** (blank: follows the latest release)

## Overrides

`/bq-update` takes per-run arguments (it does not change this file unless you add `save=true`):

```
/bq-update source=local path="C:/dev/BeQuite"
/bq-update source=github repo="xpShawky/BeQuite" tag=v1.0.0
/bq-update source=github repo="xpShawky/BeQuite" branch=main
```

`branch=` installs unreleased commits. It is for BeQuite contributors, and only by hand; the automatic check never follows a branch.
