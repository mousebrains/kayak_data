# kayak_data

The **metadata snapshot** for [kayak](https://github.com/mousebrains/kayak_python)
(levels.wkcc.org) — the single source of truth for gauges, sources, reaches, and
their relationships. Split out of the code repo so high-churn data edits and the
nightly prod snapshot don't churn `main` of the code repo (and so the code repo's
`main` can be branch-protected).

## Contents

- **`*.csv`** — the 15 metadata tables + `id_counters.csv` (the per-type stable-id
  high-water marks). These are the authoritative metadata: a fresh DB is rebuilt
  from them, and `levels sync-metadata` applies a reviewed diff to the live DB by
  stable id.
- **`reaches.json`** — `reach.geom` (excluded from `reach.csv`: large,
  machine-generated, not regenerable on prod). Applied with
  `import_metadata.py --geom-only`.
- **`reaches-gradient.json`** — `reach.gradient_profile`, same rationale.
  Applied with `--gradient-only`.

Schema (table shape) lives in the **code** repo (`data/db/migrations/`), not here.

## How it changes

- **Humans** edit metadata via a **PR** here (CI below gates it). A new row takes
  the next id from `id_counters.csv` and bumps the counter (ids only ever
  increment). See the code repo's
  [`docs/PLAN_add_gauges_reaches.md`](https://github.com/mousebrains/kayak_python/blob/main/docs/PLAN_add_gauges_reaches.md).
- **The prod host** auto-commits the nightly metadata snapshot to `main` here
  (`scripts/snapshot_metadata.sh`), reconciling editor-approved prod-direct edits
  back into the CSVs.

## How it's consumed

The code reads this directory via the `DATASET_DIR` env var (the local clone
path; the former `METADATA_DIR` is a deprecated alias). `scripts/deploy.sh` pulls
this repo, then `levels sync-metadata` applies the CSV diff and
`import_metadata.py --geom-only/--gradient-only` applies the JSONs.

## CI

`.github/workflows/validate.yml` checks out the **kayak engine pinned by
`dataset.yaml`'s `engine_test_ref`** — read from the PR's **base** commit, so a PR
can't weaken its own validator by editing the pin — and runs the engine's
authoritative `levels validate-dataset`. That enforces the full dataset contract:
id-counter invariants (ids unique per table, every id `< next_id`, plus retired-id
reuse / high-water vs `retired_ids.yaml`), foreign keys, geometry/gradient shape,
and complete-projection file presence. It then runs an `init-db → sync-metadata →
no-op sync-metadata → build` smoke against a throwaway DB. (This replaced the old
stdlib `validate.py`, which only checked CSV parsing + id-counters.)

The check runs on every PR and push for visibility, but is **not yet a required
gate** — branch protection here waits until the nightly snapshot's direct push to
`main` is removed (engine plan slice SA); enforcement until then is PR-CI
visibility plus the deploy-time `validate-dataset` in `scripts/deploy.sh`.
