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

## Index

One file set per fit (target ← predictor(s)); the link is the write-up, with
sibling `.svg`/`.json` alongside. The `provenance_slug` is the filename stem. See
each report for the full fit, diagnostics, and the deployed `calc_expression`.

### Willamette basin (Oregon)

- [`calapooia_14172000_from_mohawk_wiley_thomas.md`](calapooia_14172000_from_mohawk_wiley_thomas.md)
  — Calapooia at Holley (retired USGS 14172000) ← Mohawk 14165000 + Wiley 14187000 +
  Thomas 14188800 (multi-linear, r²=0.985).
- [`mckenzie_14159000_from_vida_trailbridge_sfrainbow_sfcougar_lookout.md`](mckenzie_14159000_from_vida_trailbridge_sfrainbow_sfcougar_lookout.md)
  — McKenzie at McKenzie Bridge (retired USGS 14159000) ← five upstream gauges
  (Vida, Trail Br Dam, SF Rainbow, SF Cougar, Lookout). Lead/lag:
  [`mckenzie_14159000_leadlag.md`](mckenzie_14159000_leadlag.md).
- [`horse_14159100_from_sfcougar_trailbridge.md`](horse_14159100_from_sfcougar_trailbridge.md)
  — Horse Cr nr McKenzie Bridge (USGS 14159100, 1969–2023 record gap) ← SF Cougar
  14159200 + Trail Br 14158850. Lead/lag:
  [`horse_14159100_leadlag.md`](horse_14159100_leadlag.md).
- [`salmon_14146500_from_nfmf.md`](salmon_14146500_from_nfmf.md)
  — Salmon Cr nr Oakridge (retired USGS 14146500) ← NFMF Willamette 14147500
  (linear, r²=0.952). Lead/lag: [`salmon_14146500_leadlag.md`](salmon_14146500_leadlag.md).

### Clackamas basin (Oregon)

- [`fishcreek_14209700_stage_rating.md`](fishcreek_14209700_stage_rating.md)
  — Fish Creek nr Three Lynx (USGS 14209700): same-gauge stage→discharge rating
  `Q = 6.192·(h−2.45)^3.288` (discharge ended 2024-11-27; USGS retired the rating).
  Continuous-record fit, log-log r²=0.998; validated by recent gaugings (−1% bias),
  the 1999 confluence bracket, and a live Three Lynx cross-check.
- [`roaring_from_fishcreek.md`](roaring_from_fishcreek.md)
  — Roaring River (reach 32; historical USGS 14209600) ← **0.95 × Fish Creek**
  drainage-area surrogate (DA 0.94 / boating-season bridge 0.97), replacing the
  dam-regulated Oak Grove Fork stand-in. No direct regression (Roaring's 1966–68
  record doesn't overlap Fish Creek).

### Rogue (Oregon)

- [`rogue_14328000_from_14330000.md`](rogue_14328000_from_14330000.md)
  — Rogue above Prospect (USGS 14328000, retired 2024-06-09) ← Rogue below Prospect
  14330000 (single-linear, n=8599). Lead/lag:
  [`rogue_14328000_leadlag.md`](rogue_14328000_leadlag.md).

### Oregon Coast

- [`drift_alsea_14306600_from_14306500.md`](drift_alsea_14306600_from_14306500.md)
  — Drift Cr (Alsea) at take-out ← Alsea nr Tidewater 14306500 (linear,
  drainage-area scaled from retired USGS 14306600).
- [`nf_alsea_14306100_from_14306500.md`](nf_alsea_14306100_from_14306500.md)
  — NF Alsea ← Alsea nr Tidewater 14306500 (linear; retired USGS 14306100, r²=0.956).
  Lead/lag: [`nf_alsea_14306100_leadlag.md`](nf_alsea_14306100_leadlag.md).
- [`sf_alsea_14306200_from_14306500.md`](sf_alsea_14306200_from_14306500.md)
  — SF Alsea ← Alsea nr Tidewater 14306500 (linear; retired USGS 14306200).
- [`sunshine_14304350_from_14305500.md`](sunshine_14304350_from_14305500.md)
  — Sunshine Cr at confluence ← Siletz at Siletz 14305500 (linear; retired USGS
  14304350). Lead/lag: [`sunshine_14304350_leadlag.md`](sunshine_14304350_leadlag.md).
- [`smith_14323100_from_siuslaw_sfcoquille.md`](smith_14323100_from_siuslaw_sfcoquille.md)
  — Smith River nr Gardiner (retired USGS 14323100, 1973) ← Siuslaw nr Mapleton
  14307620 + SF Coquille at Powers 14325000 (multi-linear, quadratic on the Siuslaw,
  r²=0.937).

### Salmon River basin (Idaho)

- [`efsf_13312000_from_johnson_stibnite.md`](efsf_13312000_from_johnson_stibnite.md)
  — EFSF Salmon below the Johnson Cr confluence: calibrated estimate of the EFSF
  above the confluence (retired USGS 13312000) + live Johnson Cr, replacing the
  uncalibrated Johnson + Stibnite sum (r²=0.980).
- [`sfsalmon_13314300_from_krassel_johnson_whitebird.md`](sfsalmon_13314300_from_krassel_johnson_whitebird.md)
  — SF Salmon at mouth nr Mackay Bar (retired USGS 13314300, 1993–2003) ← Krassel
  13310700 + Johnson Cr 13313000 + White Bird 13317000 (r²=0.996). Lead/lag:
  [`sfsalmon_13314300_leadlag.md`](sfsalmon_13314300_leadlag.md) — **the one fit with
  a real deployable sub-daily gain** (see the table below).
- [`secesh_13313500_from_johnson_whitebird.md`](secesh_13313500_from_johnson_whitebird.md)
  — Secesh nr Burgdorf (retired USGS 13313500) ← Johnson Cr 13313000 + White Bird
  13317000 (multi-linear).

### Lower Columbia / SW Washington

- [`sftoutle_14241500_from_tower_eflewis.md`](sftoutle_14241500_from_tower_eflewis.md)
  — SF Toutle at Toutle (retired USGS 14241500) ← Toutle at Tower Rd 14242580
  (downstream mass-balance) + EF Lewis 14222500. Lead/lag:
  [`sftoutle_14241500_leadlag.md`](sftoutle_14241500_leadlag.md).
- [`coweeman_14245000_from_eflewis.md`](coweeman_14245000_from_eflewis.md)
  — Coweeman nr Kelso (retired USGS 14245000, 1984) ← EF Lewis 14222500 (quadratic).
  **Out-of-era validated** against the independent WA Ecology 26C075 telemetry record
  (2006–19): bias −1.1%, r²=0.891.
- [`green_14240800_from_tower_tilton.md`](green_14240800_from_tower_tilton.md)
  — Green River (Toutle drainage) ab Beaver Cr (retired USGS 14240800) ← Toutle at
  Tower Rd 14242580 (mass-balance) + Tilton 14236200 (multi-linear).

## Sub-daily lead/lag

A daily-mean fit averages away the sub-daily travel time between gauges. The
`<slug>_leadlag.{md,svg,json}` companions measure that timing from USGS **unit
values** resampled to a **30-min** grid: lags from a first-difference
cross-correlation, gain tested with a **block-bootstrap CI** (grid residuals are
~0.97 autocorrelated, so the bare RMSE difference is far less precise than its
decimals suggest). They are **diagnostic only** — the calculator reads
contemporaneous `LatestObservation` values and cannot apply a lag.

The key distinction is **full vs deployable** alignment: *full* shifts every
predictor to its best lag (including downstream gauges to a *future* reading — real
timing signal, but non-causal look-ahead); *deployable (causal)* shifts only
upstream (+τ) predictors (a *past* reading, usable in a real-time nowcast). The lag
sign is timing, not geography — +τ is usually upstream travel time, but shared
diurnal-melt phase can give a geographically downstream gauge a +τ peak; the causal
split is unaffected.

| reach (target) | lag | full gain (95% CI, cfs) | deployable | verdict |
|---|---|---|---|---|
| McKenzie Bridge 14159000 | TB +1.5h, Vida −2.5h | +2.2% [+0.5, +3.2] ✓ | +0.1% [−3.2, +2.5] | real, look-ahead only |
| Rogue a. Prospect 14328000 | −0.5h (downstream) | +0.3% [+0.2, +0.6] ✓ | 0 (no upstream) | real, look-ahead only |
| Sunshine 14304350 | −3.0h (downstream) | +10.7% [+2.1, +7.2] ✓ | 0 (no upstream) | real, look-ahead only |
| Salmon 14146500 | −0.5h (downstream) | +0.5% [−0.0, +0.8] | 0 (no upstream) | unresolved |
| NF Alsea 14306100 | −3.5h (downstream) | [−1.1, +30.7] | 0 (no upstream) | unresolved |
| Horse Cr 14159100 | none resolvable | — | — | no sub-daily lag |
| SF Salmon Mackay Bar 13314300 | Krassel +3.0h, Johnson +5.0h, White Bird +1.0h (all +τ/causal) | +21.1% [+41.7, +66.8] ✓ | **+21.1% [+41.7, +66.8] ✓** | **deployable gain — the first real one** |
| SF Toutle 14241500 | Tower Rd −2.5h (downstream), EF Lewis 0.0h | +8.8% [+8.9, +23.5] ✓ | 0 (no +τ predictor) | real, look-ahead only |

**Result:** for every reach analysed before 2026-06 the *deployable* sub-daily gain
was nil — those calc gauges are estimated from downstream or co-located gauges, so
what timing signal existed was downstream look-ahead, not real-time-usable. **SF
Salmon at Mackay Bar broke the pattern**: every donor carries a +τ (past-reading,
causal) lag — Krassel and Johnson are upstream travel time (3–5 h), White Bird is
geographically downstream mainstem but its +1 h is shared diurnal-melt phase — and
the deployable gain is +21.1% with a CI excluding zero. The calculator still reads
contemporaneous values (no lag support), so that gain is *unrealised*; it would
justify a time-offset reference form in the engine's calculator if more
upstream-donor fits accumulate.

Not feasible (target has no sub-hourly record, or predictors don't overlap it):
Calapooia 14172000, SF Alsea 14306200, Drift Cr Alsea 14306600, Smith 14323100,
Secesh 13313500, EFSF 13312000, Kalama 14223500, Coweeman 14245000, Green 14240800.

## Conventions

- **One fit per file.** A new fit (different window or predictor set) goes in a new
  file with a date/version suffix — don't overwrite an existing analysis.
- **Mark superseded fits in the heading** rather than deleting them; they document
  the previous calc's provenance. The `calc_expression.csv` row (keyed by
  `provenance_slug`) is the permanent record; the report is the contemporary
  justification.

## Provenance

- **Source:** copied from the `kayak_python` engine repo's `docs/regression/` at
  commit `6d291fd7bf418be8bc5a5a98ebe3e7acc6c77cd3` (dataset-separation slice S2 —
  the reports became dataset content). In slice S2-E3 the engine copy was deleted
  and the reports' internal `docs/regression/` self-references were rewritten to the
  dataset-relative `regression/`; otherwise the reports are as generated.
- **License:** `CC-BY-NC-4.0` (this dataset's license). The underlying gauge data
  is USGS daily-mean streamflow (public domain); the analysis write-ups and plots
  are the project's own work.
- **How they're generated:** `kayak_python`
  [`scripts/regression/`](https://github.com/mousebrains/kayak_python/tree/main/scripts/regression)
  (`gauge_pair_linear.py` + `gauge_lead_lag.py`) — dev-only tools (USGS API +
  regression stack). The engine validates and sanitizes every file here at `levels
  validate-dataset` and at build time, so a report served to the public is never
  trusted verbatim.
