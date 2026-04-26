#!/usr/bin/env python3
"""Normalize a vendored Appendix G-style spreadsheet into appendix_g_mapping.csv.

Expected when ``vendor/uad/appendix_g.xlsx`` exists (column names are configurable
below; adjust to match your GSE export):

- CanonicalKey / legacy_xpath / uad36_xpath / cardinality / transform / severity / notes

If the spreadsheet is absent, exits 0 without modifying the committed CSV.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VENDOR_XLSX = REPO_ROOT / "vendor" / "uad" / "appendix_g.xlsx"
OUT_CSV = REPO_ROOT / "src" / "appraisal_ai" / "uad" / "data" / "appendix_g_mapping.csv"

# Map common header variants (edit when your vendor sheet differs)
HEADER_ALIASES = {
    "canonical_key": {"canonical_key", "canonicalkey", "canonical"},
    "legacy_xpath": {"legacy_xpath", "legacyxpath", "legacy path", "legacy_uad_xpath"},
    "uad36_xpath": {"uad36_xpath", "uad36xpath", "redesign_xpath", "uad 3.6 xpath"},
    "cardinality": {"cardinality", "card"},
    "transform": {"transform", "transform_rule"},
    "severity": {"severity", "mapping_severity"},
    "notes": {"notes", "comment", "remarks"},
}


def _normalize_header(cell: str) -> str:
    return cell.strip().lower().replace(" ", "_")


def _resolve_column(headers: list[str], aliases: dict[str, set[str]]) -> dict[str, int]:
    norm = [_normalize_header(h) for h in headers]
    out: dict[str, int] = {}
    for canonical, variants in aliases.items():
        for i, h in enumerate(norm):
            if h in variants:
                out[canonical] = i
                break
    return out


def main() -> int:
    if not VENDOR_XLSX.is_file():
        print(f"No vendor workbook at {VENDOR_XLSX}; leaving committed CSV unchanged.", file=sys.stderr)
        return 0

    try:
        import openpyxl
    except ImportError as e:
        print("openpyxl is required to read appendix_g.xlsx. Install dev extras: pip install -e '.[dev]'", file=sys.stderr)
        raise SystemExit(1) from e

    wb = openpyxl.load_workbook(VENDOR_XLSX, read_only=True, data_only=True)
    ws = wb.active
    rows_iter = ws.iter_rows(values_only=True)
    try:
        header_row = next(rows_iter)
    except StopIteration:
        print("Empty workbook.", file=sys.stderr)
        return 1

    headers = [str(c) if c is not None else "" for c in header_row]
    col_idx = _resolve_column(headers, HEADER_ALIASES)
    required = ("canonical_key", "legacy_xpath", "uad36_xpath", "cardinality", "transform", "severity")
    missing = [k for k in required if k not in col_idx]
    if missing:
        print(f"Could not resolve columns {missing} from headers {headers!r}. Edit HEADER_ALIASES.", file=sys.stderr)
        return 1

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["canonical_key", "legacy_xpath", "uad36_xpath", "cardinality", "transform", "severity", "notes"]
    out_rows: list[dict[str, str]] = []
    for row in rows_iter:
        if row is None or all(c is None or str(c).strip() == "" for c in row):
            continue

        def get(col: str) -> str:
            if col not in col_idx:
                return ""
            i = col_idx[col]
            v = row[i] if i < len(row) else None
            if v is None:
                return ""
            return str(v).strip()

        rec = {k: get(k) for k in fieldnames}
        if not rec["canonical_key"]:
            continue
        out_rows.append(rec)

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)

    print(f"Wrote {len(out_rows)} rows to {OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
