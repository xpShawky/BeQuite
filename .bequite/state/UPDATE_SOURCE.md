# BeQuite update source configuration

Used by `/bq-update` to know where to fetch updates from.

---

**Source type:** github
**Repo URL or local path:** https://github.com/xpShawky/BeQuite.git
**Default branch:** main
**Default strategy:** safe (backup + merge; no overwrite of local edits)

## Pinned tag (optional)

Leave blank to track latest commits on default branch. Set to a tag (e.g.
`v3.0.0-alpha.9`) to pin to a stable release.

**Pinned tag:** (blank — tracks latest commits on main)

## Last update

- **Last checked:** never
- **Last updated:** never
- **Result:** seed file, no update yet

## Overrides

You can override per-run via `/bq-update` arguments:

```
/bq-update source=local path="../BeQuite-dev"
/bq-update source=github repo="xpShawky/BeQuite" branch=main
/bq-update source=github repo="xpShawky/BeQuite" tag=v3.0.0-alpha.9
```

These overrides don't change this file unless the user runs:

```
/bq-update source=github repo="..." save=true
```

## Notes

- For BeQuite contributors developing locally, set `source type` to `local` and point at your dev clone
- For production-stable installs, pin to a tag (so you don't get unintended updates from main)
- For the most-recent features, leave the pinned tag blank
