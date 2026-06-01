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

The code reads this directory via the `METADATA_DIR` env var (the local clone
path). `scripts/deploy.sh` pulls this repo, then `levels sync-metadata` applies the
CSV diff and `import_metadata.py --geom-only/--gradient-only` applies the JSONs.

## CI

`validate.py` (run by `.github/workflows/validate.yml`) checks every CSV parses and
the `id_counters.csv` invariants hold (ids unique per table; every id `< next_id`)
— the same guarantee as the code repo's `tests/test_id_counters.py`, with no
dependency on the kayak package.
