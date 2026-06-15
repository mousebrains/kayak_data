# Stage→discharge rating: Fish Creek nr Three Lynx (USGS 14209700)

**Status:** analysis complete; `calc_expression` deployment **pending**. This report
is an *orphan* (no `provenance_slug` references it yet) — that is a known non-fatal
`validate-dataset` warning until the Fish Creek flow calc is added. Supersedes an
earlier field-measurement-only fit (see *Superseded fits*).

**Goal:** Fish Creek's USGS gauge (`14209700`, on reach `3f` / id 201) reports **gage
height only** — USGS stopped publishing discharge after 2024-11-27 and retired the
rating (stage feed flagged ~2026-01-23). Reconstruct a stage→discharge rating so a
`calc_expression` can turn the live stage into CFS (and feed the Roaring surrogate —
see [`roaring_from_fishcreek.md`](roaring_from_fishcreek.md)).

This is **not** the standard `gauge_pair_linear.py` regression (estimate one gauge
from others); it is a same-gauge rating curve fit to the gauge's own paired
stage+discharge record. Done as ad-hoc analysis (USGS APIs); the script-generated
`.svg`/`.json` sidecars are not produced — generate them before wiring a calc to this
slug, or the deploy validator will require them.

## The rating

> **Q = 6.192 · (h − 2.45)^3.288**   (h = gage height ft, Q = cfs)

- log-log **r² = 0.998**, relative RMSE **5.9%** vs stage-binned medians.
- Fit on **119,623** paired 15-min observations, **2021-06-09 → 2024-11-27**
  (the full extent of the gauge's paired stage+discharge record — see *Data*),
  by stage-binned medians (0.05 ft bins, ≥20 obs) so the fit is equal-weighted
  across the flow range and the median absorbs rating-shift scatter.
- Well-constrained **3.5–8 ft (~10–1700 cfs)** — covers everything runnable.
  Above ~9 ft it extrapolates (the 2021–24 window had no major flood); both this
  fit and the old gauging fit over-read the lone 1996 extreme (11.8 ft / 7540 cfs)
  by ~25%, far above any boatable level.

| stage (ft) | 4.0 | 4.25 | 5.0 | 6.0 | 7.0 | 8.0 |
|---|---|---|---|---|---|---|
| Q (cfs) | 26 | 42 | 134 | 399 | 903 | 1734 |

Current (2026-06-14): **4.28 ft → ~45 cfs**.

## Data

All USGS site `14209700`, `parameterCd` as noted.

| Series | Extent | Notes |
|---|---|---|
| Discharge `00060` (daily + IV) | 1989-08-18 → **2024-11-27** | hard end; USGS pulled the rating |
| Gage height `00065` (IV) | 2021-06-09 → 2026-01-23+ | continues past the discharge end |
| Gage height `00065` (daily) | 2024-11-27 → 2026-06-14 | the live feed we now serve |
| Field gaugings (`00060`+`00065`) | 1994–2024, **121 pairs** | independent measured stage/Q |

The paired continuous (stage AND discharge) record that the rating is fit to runs
**only to 2024-11-27** — the 2025/2026 IV files carry stage but no discharge column.
Everything served since is therefore stage→rating extrapolation.

## Validation — three independent lines

1. **Recent field gaugings (2021+, n=19):** the continuous fit sits at **−1.0% bias,
   13% RMSE** against independent measured discharge; the old 30-year gauging fit is
   **−18% / 30%** (it over-reads current flows — the channel shifted). This is why the
   continuous fit, not the gaugings, is the rating.
2. **1999 confluence mass-balance bracket** (see
   [`roaring_from_fishcreek.md`](roaring_from_fishcreek.md) for the geography): USGS
   gauged two mainstem sites straddling *only* the Fish Creek confluence as same-trip
   pairs — `14209710` (below) − `14209670` (above) = Fish Creek outflow. Four
   concurrent days match Fish Creek's own gauge within **3–4%** (the 4th is a 6-cfs
   differencing-noise gap at low flow). Confirms `14209700` measures Fish Creek
   correctly — the discharge record underpinning the rating is sound.
3. **Three Lynx live cross-check:** Clackamas above Three Lynx (`14209500`, live,
   1989–2026) is a continuous proxy (FishCk ≈ 0.077·ThreeLynx, r²=0.86 — coarse). A
   *rating-independent* shift test (Fish Creek stage vs Three Lynx flow, matched
   flow bins, pre/post the 2026-01-23 cutoff) shows **mean stage shift −0.024 ft** —
   no discontinuous jump. Today: rating 45 cfs vs proxy 36 cfs, consistent at summer
   low within the proxy's ±20–30%.

## Continuous drift (channel aggradation)

Channel shifts are continuous in time (floods are the discontinuous exception), so
the right test is the **trend of stage-at-fixed-discharge**, not a date split. From
the 2021–2024 paired record:

| Three Lynx-equiv. band | drift |
|---|---|
| 30–60 cfs (summer low) | ~0 ft/yr |
| 100–160 cfs (≈median) | +0.05 ft/yr |
| 250–400 cfs (moderate) | +0.055 ft/yr |

Gradual aggradation at mid/moderate flows, negligible at baseflow. Carried to *now*
(~2.5 yr past the data center), the rating likely **over-reads current mid flows by
~0.1–0.15 ft of stage ≈ 10–15%**, and is accurate at summer low. We cannot see drift
past 2024-11 (no discharge), so 2025–26 is extrapolated — likely why USGS retired the
rating. **The rating has a shelf life:** re-anchor when new gaugings/discharge appear,
and re-rate immediately after any major flood.

## `calc_expression` row (when deployed)

A `Calculation` source on **gauge 34** (Fish Creek), so reach 201 also gains a CFS
value. The ref `14209700::gauge` resolves to gauge 34's latest stage (its USGS source
166); `max(…,0)` floors the power base so stage below the 2.45-ft offset can't raise a
negative number to a fractional power.

```
data_type:       flow
expression:      round(6.192 * max(14209700::gauge - 2.45, 0) ** 3.288, 0)
time_expression: 14209700::gauge
note:            same-gauge stage->discharge rating, power law Q=6.192*(h-2.45)^3.288. Fit n=119623 paired 15-min obs 2021-06..2024-11 (discharge ends 2024-11-27), binned-median, log-log r2=0.998. Validated: recent gaugings -1% bias, 1999 confluence bracket within 3-4%, live Three Lynx cross-check no shift. ~0.05 ft/yr mid-flow aggradation -> re-check after floods / when USGS re-rates. See regression/fishcreek_14209700_stage_rating.md.
provenance_slug: fishcreek_14209700_stage_rating
```

Authoring: add the source to `sources.yaml` (`agency: Calculation`), `levels
generate-sources`, add the `calc_expression.csv` row (stable id from
`id_counters.csv`), and the `.svg`/`.json` sidecars, then `sync-metadata`.

## Future — if USGS resumes publishing discharge

`fetch-usgs-ogc` fetches `00060/00065/00010` for **any** USGS source, keyed on the
source row, not on a flag. Source 166 (`14209700`, agency USGS) already exists, so the
**moment USGS republishes `00060`, fetch will auto-ingest real Fish Creek flow** onto
gauge 34 — alongside the calc flow. Gauge 34 would then carry **two** flow values
(real + rating-derived), and which wins the gauge-level "latest flow" is undefined.

**Action when that happens:** retire the Fish Creek flow calc — remove its
`sources.yaml` entry, `generate-sources`, `sync-metadata --allow-deletes`. Gauge 34
then serves the real USGS flow, and the Roaring surrogate (which reads
`14209700::flow`) automatically switches to the real flow with no further change. Watch
for the transition via the gauge audit (a USGS gauge that starts reporting flow again)
or a periodic check of `14209700` for `00060`.

## Superseded fits

- **Field-measurement-only power law `Q = 4.87·(h−2.23)^3.34`** (121 gaugings,
  1994–2024). Replaced 2026-06: it spans 30 years of channel change and over-reads
  *current* flows by ~18% (−18% bias vs 2021+ gaugings). Kept here for provenance.

## Reproduce

Not the standard script — ad-hoc from USGS web services:

```
# paired continuous (rating fit input):
https://waterservices.usgs.gov/nwis/iv/?format=rdb&sites=14209700&parameterCd=00060,00065&startDT=<yr>&endDT=<yr>
# field gaugings (validation):
https://api.waterdata.usgs.gov/ogcapi/v0/collections/field-measurements/items?monitoring_location_id=USGS-14209700&f=json
# confluence bracket: USGS-14209670 (above) / USGS-14209710 (below) field-measurements
# live cross-check proxy: 14209500 (Clackamas above Three Lynx Creek), 00060 daily
```
