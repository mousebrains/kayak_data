# Frozen migration history (regional data)

These are the **data-only** schema migrations (`INSERT`/`UPDATE`/`DELETE` on
metadata tables) from the WKCC "wire-via-migration" era (engine migrations
≤ 0074), copied **byte-for-byte** out of the engine repo when the engine's active
migration history was made schema-only (dataset-separation **S9b**).

They are **frozen audit only** — nothing runs or reads them:

- The live DB already applied them; their effect is the current metadata, which now
  lives in this repo's CSVs (`levels sync-metadata` is the apply path now).
- A fresh database builds its schema from the engine's SQLAlchemy models
  (`create_all`) and never replays regional data migrations, so a new region does
  **not** inherit WKCC's gauges/reaches/calc fits from these files.
- The engine's `levels validate-dataset` ignores this directory (it reads the
  root-level `*.csv` + JSON sidecars, not `history/`).

`manifest.csv` records each file's `version,filename,sha256` plus its
`origin_path` and the `engine_commit` it was copied from, so the copy is
verifiable against engine history. Mixed schema+data migrations (`0003`, `0028`,
`0051`) were **not** copied here — their schema effect is engine-relevant, so they
stay frozen in the engine repo (`legacy/migrations_frozen/`).
