# Approvals

Every publish, every spend over a cap and every "the editor rejected it twice" decision waits here as
`A-xxxx.md` with `status: pending`. Only the owner changes the status:

- `python <skill>/scripts/heartbeat.py decide --team <team> --approval A-0001 --yes` (or `--no --note "why"`)
- `/bq-team approve A-0001` / `/bq-team decline A-0001 "why"`
- the Approve / Decline buttons from the Telegram bridge (`/bq-operator`)

An approved publish only copies the package to `outbox/`. The publish step asks again for each post.
