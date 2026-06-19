# kayak_data

The **metadata dataset** for [kayak](https://github.com/mousebrains/kayak_python)
(levels.wkcc.org) — the single source of truth for gauges, sources, reaches, and
their relationships. Split out of the code repo so high-churn data edits don't
churn `main` of the code repo (and so the code repo's `main` can be
branch-protected).

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
- **`regression/`** — published regression analyses (`<slug>.{md,svg,json}`) for
  the flow-estimation `calc_expression` formulas, keyed by
  `calc_expression.provenance_slug` and rendered to `/static/regression/` at build.
  See [`regression/README.md`](regression/README.md). The engine sanitizes them
  (markdown via `nh3`, SVG via a strict allowlist) at validate + build time.

Schema (table shape) lives in the **code** repo (`data/db/migrations/`), not here.

## How it changes

**Humans** edit metadata via a **PR** here (CI below gates it). A new row takes
the next id from `id_counters.csv` and bumps the counter (ids only ever
increment). See the code repo's
[`docs/PLAN_add_gauges_reaches.md`](https://github.com/mousebrains/kayak_python/blob/main/docs/PLAN_add_gauges_reaches.md).
A PR is now the **only** way `main` changes — the former nightly prod→dataset
snapshot (`snapshot_metadata.sh`) was retired in the engine's SA-teardown, and
there is no reverse sync from the live DB back to the dataset.

## How it's consumed

The code reads this directory via the `DATASET_DIR` env var (the local clone
path). `scripts/deploy.sh` pulls
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

`main` is **branch-protected**: the `validate` check is a **required gate** and
`enforce_admins` is on, so every change lands through a reviewed PR with green CI
(no direct pushes). The deploy-time `validate-dataset` in `scripts/deploy.sh` is
the second line of enforcement.
