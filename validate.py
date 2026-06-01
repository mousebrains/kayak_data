#!/usr/bin/env python3
"""Standalone integrity check for the kayak_data metadata snapshot.

Pure stdlib — no dependency on the kayak package — so kayak_data's CI can gate its
own edit-PRs without checking out the (private) code repo. Mirrors the code repo's
``tests/test_id_counters.py``:

  - every ``<table>.csv`` named in ``id_counters.csv`` parses and has id rows,
  - ids are unique per table,
  - each table's ``next_id`` is strictly above its max existing id (so a deleted
    base-62 handle is never reused).

Exit 0 on success; prints the first failures and exits 1 otherwise.
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
COUNTERS = HERE / "id_counters.csv"


def _counters() -> dict[str, int]:
    with COUNTERS.open(encoding="utf-8") as fh:
        return {row["table"]: int(row["next_id"]) for row in csv.DictReader(fh)}


def _ids(table: str) -> list[int]:
    with (HERE / f"{table}.csv").open(encoding="utf-8") as fh:
        return [int(row["id"]) for row in csv.DictReader(fh) if (row.get("id") or "").strip()]


def main() -> int:
    errors: list[str] = []

    # Every CSV parses (header + rows readable).
    for csv_path in sorted(HERE.glob("*.csv")):
        try:
            with csv_path.open(encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                if reader.fieldnames is None:
                    errors.append(f"{csv_path.name}: empty / headerless")
                    continue
                for _ in reader:
                    pass
        except (OSError, csv.Error) as exc:
            errors.append(f"{csv_path.name}: unreadable ({exc})")

    # id_counters invariants.
    for table, nxt in _counters().items():
        ids = _ids(table)
        if not ids:
            errors.append(f"{table}.csv (in id_counters.csv) has no id rows")
            continue
        dups = {i for i, c in Counter(ids).items() if c > 1}
        if dups:
            errors.append(f"{table}.csv has duplicate ids: {sorted(dups)}")
        hi = max(ids)
        if hi >= nxt:
            errors.append(f"{table}: next_id={nxt} <= max id {hi} (stale counter / id-reuse risk)")

    if errors:
        print("kayak_data validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("kayak_data validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
