from __future__ import annotations

import json
from pathlib import Path

import pytest

from appraisal_ai.uad.mapping import load_mapping_rows
from appraisal_ai.uad.migrate import migrate_xml_bytes
from appraisal_ai.uad.xml_paths import get_path_text, parse_xml

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "uad"


def test_migrate_legacy_to_uad36_paths() -> None:
    src = (FIXTURES / "legacy_minimal.xml").read_bytes()
    out, report = migrate_xml_bytes(src, "2.6", "3.6")
    assert report.direction == "2.6_to_3.6"
    root = parse_xml(out)
    assert get_path_text(root, "/UAD36Example/Collateral/SubjectProperty/AddressLineText") == "100 Elm St"
    assert get_path_text(root, "/UAD36Example/Collateral/Valuation/MarketValueAmount") == "350000"
    assert "subject_address_line" in report.populated_canonical_keys


def test_migrate_uad36_to_legacy_paths() -> None:
    src = (FIXTURES / "uad36_minimal.xml").read_bytes()
    out, report = migrate_xml_bytes(src, "3.6", "2.6")
    assert report.direction == "3.6_to_2.6"
    root = parse_xml(out)
    assert get_path_text(root, "/LegacyUADExample/SubjectProperty/AddressLineText") == "200 Oak Ave"
    assert get_path_text(root, "/LegacyUADExample/Appraisal/OpinionOfMarketValueAmount") == "425000"


def test_roundtrip_preserves_canonical_values() -> None:
    src = (FIXTURES / "legacy_minimal.xml").read_bytes()
    mid, _ = migrate_xml_bytes(src, "2.6", "3.6")
    back, rep2 = migrate_xml_bytes(mid, "3.6", "2.6")
    a = parse_xml(src)
    b = parse_xml(back)
    for xp in (
        "/LegacyUADExample/SubjectProperty/AddressLineText",
        "/LegacyUADExample/SubjectProperty/CityName",
        "/LegacyUADExample/Appraisal/OpinionOfMarketValueAmount",
    ):
        assert get_path_text(a, xp) == get_path_text(b, xp)


def test_custom_mapping_csv(tmp_path: Path) -> None:
    csv_path = tmp_path / "m.csv"
    csv_path.write_text(
        "canonical_key,legacy_xpath,uad36_xpath,cardinality,transform,severity,notes\n"
        "subject_address_line,/LegacyUADExample/SubjectProperty/AddressLineText,"
        "/UAD36Example/Collateral/SubjectProperty/AddressLineText,1:1,identity,lossless,\n",
        encoding="utf-8",
    )
    src = (FIXTURES / "legacy_minimal.xml").read_bytes()
    out, _ = migrate_xml_bytes(src, "2.6", "3.6", mapping_path=str(csv_path))
    root = parse_xml(out)
    assert get_path_text(root, "/UAD36Example/Collateral/SubjectProperty/AddressLineText") == "100 Elm St"


def test_unsupported_row_skipped(tmp_path: Path) -> None:
    csv_path = tmp_path / "m.csv"
    csv_path.write_text(
        "canonical_key,legacy_xpath,uad36_xpath,cardinality,transform,severity,notes\n"
        "subject_address_line,/LegacyUADExample/SubjectProperty/AddressLineText,"
        "/UAD36Example/Collateral/SubjectProperty/AddressLineText,1:1,identity,lossless,\n"
        "extra_field,/LegacyUADExample/Unknown,/UAD36Example/Unknown,1:1,identity,unsupported,test\n",
        encoding="utf-8",
    )
    rows = load_mapping_rows(csv_path.read_bytes())
    assert any(r.canonical_key == "extra_field" and r.severity == "unsupported" for r in rows)
    src = (FIXTURES / "legacy_minimal.xml").read_bytes()
    _, report = migrate_xml_bytes(src, "2.6", "3.6", mapping_path=str(csv_path))
    assert "extra_field" in report.skipped_unsupported


def test_approximate_mapping_emits_warning(tmp_path: Path) -> None:
    csv_path = tmp_path / "m.csv"
    csv_path.write_text(
        "canonical_key,legacy_xpath,uad36_xpath,cardinality,transform,severity,notes\n"
        "subject_address_line,/LegacyUADExample/SubjectProperty/AddressLineText,"
        "/UAD36Example/Collateral/SubjectProperty/AddressLineText,1:1,identity,approximate,\n",
        encoding="utf-8",
    )
    src = (FIXTURES / "legacy_minimal.xml").read_bytes()
    _, report = migrate_xml_bytes(src, "2.6", "3.6", mapping_path=str(csv_path))
    assert any(w.get("code") == "approximate_mapping" for w in report.warnings)


def test_migrate_same_format_raises() -> None:
    src = (FIXTURES / "legacy_minimal.xml").read_bytes()
    with pytest.raises(ValueError, match="source and target must differ"):
        migrate_xml_bytes(src, "2.6", "2.6")


def test_report_json_serializable(tmp_path: Path) -> None:
    src = (FIXTURES / "legacy_minimal.xml").read_bytes()
    _, report = migrate_xml_bytes(src, "2.6", "3.6")
    json.dumps(report.to_json_obj())
