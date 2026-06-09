# Regression reports

Published regression analyses for the flow-estimation `calc_expression` formulas
in this dataset. Each fit has three files, keyed by the calc's `provenance_slug`
(see `calc_expression.csv`):

- `<slug>.md` — the write-up (goal, fit, coefficients, residual diagnostics)
- `<slug>.svg` — the residual-scatter plot
- `<slug>.json` — the machine-readable fit summary

The site links these from a gauge's description page (rendered to
`/static/regression/<slug>.html` at build). Some fits also carry a
`<slug>_leadlag.{md,svg,json}` companion (sub-daily lead/lag timing), linked from
the main report.

## Provenance

- **Source:** copied verbatim from the `kayak_python` engine repo's
  `docs/regression/` at commit `6d291fd7bf418be8bc5a5a98ebe3e7acc6c77cd3`
  (dataset-separation slice S2 — the reports become dataset content).
- **License:** `CC-BY-NC-4.0` (this dataset's license). The underlying gauge data
  is USGS daily-mean streamflow (public domain); the analysis write-ups and plots
  are the project's own work.
- **How they're generated:** `kayak_python`
  [`scripts/regression/`](https://github.com/mousebrains/kayak_python/tree/main/scripts/regression)
  (`gauge_pair_linear.py` + `gauge_lead_lag.py`) — dev-only tools (USGS API +
  regression stack). The engine validates and sanitizes every file here at `levels
  validate-dataset` and at build time, so a report served to the public is never
  trusted verbatim.
