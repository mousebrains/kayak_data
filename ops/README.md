# ops/ — WKCC-regional operational inputs and tools

Moved from the engine repo (`kayak_python` `scripts/` +
`src/kayak/data/audit_ignore.yaml` at `d23bc19`) by dataset-separation
S3g + decision D3: these encode *this* deployment's region (which HUC4s
to download, which providers to harvest, which audit candidates we've
judged not-useful, what the WKCC host audit checks), so they belong to
the dataset, not the engine surface. Generic provider clients and
geometry tools stay engine-side.

| File | Purpose |
|---|---|
| `audit_ignore.yaml` | Suppressions for the engine's `scripts/audit_gauges.py` — read automatically from `DATASET_DIR/ops/audit_ignore.yaml` (schema documented in-file) |
| `fetch_nhd.sh` | Download the OR/WA/ID/NV/CA NHD state GPKGs + NHDPlus HR HUC4s; **destination is a required argument** — pass the engine checkout's `Trace-cache/NHD/` (the engine's `extract_*.sh` scripts read it there) |
| `harvest_wa_ecology.py` | Harvest WA Ecology flow-station metadata into the gauge-metadata cache |
| `fetch_usbr_pn_sites.py` | USBR Pacific-Northwest (hydromet) site catalog → gauge-metadata cache |
| `fetch_usbr_rise_sites.py` | USBR RISE site catalog (PNW cross-referencing) → gauge-metadata cache |
| `audit-t30.sh` | WKCC host audit (tails nginx/fail2ban/auth/mail logs, checks certs/backups); host-specific, to be superseded by S7's parameterized status checks |

The Python tools resolve the gauge-metadata cache via
`$GAUGE_METADATA_CACHE`, falling back to the sibling-clone convention
(`../kayak/Gauge-metadata-cache/gauges.db` relative to this repo's
parent — holds on both the dev box and prod). None of these run in the
production pipeline; they are operator/dev tools.
