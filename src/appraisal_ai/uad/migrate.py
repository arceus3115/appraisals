from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from lxml import etree

from appraisal_ai.uad.canonical import CanonicalAppraisal
from appraisal_ai.uad.mapping import MappingRow, load_mapping_rows
from appraisal_ai.uad.xml_paths import get_path_text, parse_xml, serialize_xml, set_path_text

Format = Literal["2.6", "3.6"]


def _apply_transform(transform: str, value: str) -> str:
    t = transform.strip().lower()
    if t in ("", "identity"):
        return value
    if t == "uppercase":
        return value.upper()
    if t == "lowercase":
        return value.lower()
    return value


@dataclass
class MigrationReport:
    direction: str
    populated_canonical_keys: list[str] = field(default_factory=list)
    warnings: list[dict[str, Any]] = field(default_factory=list)
    skipped_unsupported: list[str] = field(default_factory=list)
    missing_source_paths: list[dict[str, str]] = field(default_factory=list)

    def to_json_obj(self) -> dict[str, Any]:
        return {
            "direction": self.direction,
            "populated_canonical_keys": self.populated_canonical_keys,
            "warnings": self.warnings,
            "skipped_unsupported": self.skipped_unsupported,
            "missing_source_paths": self.missing_source_paths,
        }


def _read_xpath(row: MappingRow, source: Format) -> str:
    return row.legacy_xpath if source == "2.6" else row.uad36_xpath


def _write_xpath(row: MappingRow, target: Format) -> str:
    return row.legacy_xpath if target == "2.6" else row.uad36_xpath


def xml_bytes_to_canonical(
    data: bytes,
    source: Format,
    rows: list[MappingRow],
    report: MigrationReport,
) -> CanonicalAppraisal:
    root = parse_xml(data)
    flat: dict[str, str | None] = {}
    for row in rows:
        if str(row.severity).lower() == "unsupported":
            report.skipped_unsupported.append(row.canonical_key)
            continue
        src_xp = _read_xpath(row, source)
        raw = get_path_text(root, src_xp)
        if raw is None:
            if str(row.severity).lower() == "lossless":
                report.missing_source_paths.append({"canonical_key": row.canonical_key, "xpath": src_xp})
            continue
        flat[row.canonical_key] = _apply_transform(str(row.transform), raw)

    canon = CanonicalAppraisal.from_flat(flat)
    report.populated_canonical_keys = sorted(canon.to_flat().keys())
    for row in rows:
        if str(row.severity).lower() == "approximate" and row.canonical_key in canon.to_flat():
            report.warnings.append(
                {
                    "code": "approximate_mapping",
                    "canonical_key": row.canonical_key,
                    "message": "Value derived from an approximate (non-lossless) mapping row.",
                }
            )
    return canon


def canonical_to_xml_bytes(
    canon: CanonicalAppraisal,
    target: Format,
    rows: list[MappingRow],
    _report: MigrationReport,
) -> bytes:
    flat = canon.to_flat()
    write_rows = [r for r in rows if str(r.severity).lower() != "unsupported"]
    if not write_rows:
        msg = "No supported mapping rows"
        raise ValueError(msg)

    first_xp = _write_xpath(write_rows[0], target)
    parts = [p for p in first_xp.strip().split("/") if p]
    if not parts:
        msg = f"Invalid xpath {first_xp!r}"
        raise ValueError(msg)
    root_tag = parts[0]
    root = etree.Element(root_tag)

    for row in write_rows:
        wx = _write_xpath(row, target)
        val = flat.get(row.canonical_key)
        if val is None:
            continue
        set_path_text(root, wx, val)

    return serialize_xml(root)


def migrate_xml_bytes(
    data: bytes,
    source: Format,
    target: Format,
    *,
    mapping_path: str | None = None,
) -> tuple[bytes, MigrationReport]:
    if source == target:
        msg = "source and target must differ"
        raise ValueError(msg)
    rows = load_mapping_rows(Path(mapping_path).read_bytes()) if mapping_path else load_mapping_rows()
    direction = f"{source}_to_{target}"
    report = MigrationReport(direction=direction)
    canon = xml_bytes_to_canonical(data, source, rows, report)
    out = canonical_to_xml_bytes(canon, target, rows, report)
    return out, report
