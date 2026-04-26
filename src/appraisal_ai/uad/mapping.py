from __future__ import annotations

import csv
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Literal

Transform = Literal["identity", "uppercase", "lowercase"]
Severity = Literal["lossless", "approximate", "unsupported"]
Cardinality = Literal["1:1", "1:n", "n:1"]


@dataclass(frozen=True)
class MappingRow:
    canonical_key: str
    legacy_xpath: str
    uad36_xpath: str
    cardinality: str
    transform: Transform | str
    severity: Severity | str
    notes: str


def default_mapping_csv_bytes() -> bytes:
    return resources.files("appraisal_ai.uad.data").joinpath("appendix_g_mapping.csv").read_bytes()


def load_mapping_rows(csv_bytes: bytes | None = None) -> list[MappingRow]:
    raw = default_mapping_csv_bytes() if csv_bytes is None else csv_bytes
    text = raw.decode("utf-8").splitlines()
    reader = csv.DictReader(text)
    rows: list[MappingRow] = []
    for r in reader:
        if not r.get("canonical_key"):
            continue
        rows.append(
            MappingRow(
                canonical_key=r["canonical_key"].strip(),
                legacy_xpath=r["legacy_xpath"].strip(),
                uad36_xpath=r["uad36_xpath"].strip(),
                cardinality=(r.get("cardinality") or "1:1").strip(),
                transform=(r.get("transform") or "identity").strip(),
                severity=(r.get("severity") or "lossless").strip(),
                notes=(r.get("notes") or "").strip(),
            )
        )
    return rows


def load_mapping_rows_from_path(path: Path) -> list[MappingRow]:
    return load_mapping_rows(path.read_bytes())
