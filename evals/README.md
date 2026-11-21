# BeQuite evals

Scenarios that check the pack's promises; run with `/bq-eval run`. One file per scenario under `evals/<skill>/`; results in `evals/results/<date>.md`. A scenario that passed in the last passing run and fails now is a regression, and `/bq-release` refuses while one is open. This folder tests BeQuite itself and is not installed into projects.
