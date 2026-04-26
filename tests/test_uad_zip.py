from __future__ import annotations

import zipfile
from pathlib import Path

from appraisal_ai.uad.zip_package import build_ucdp_style_zip


def test_build_ucdp_style_zip_flat_files(tmp_path: Path) -> None:
    xml = tmp_path / "a.xml"
    pdf = tmp_path / "b.pdf"
    out = tmp_path / "out.zip"
    xml.write_bytes(b"<root/>")
    pdf.write_bytes(b"%PDF-1.4 minimal")

    build_ucdp_style_zip(xml_path=xml, pdf_path=pdf, output_zip=out)

    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
    assert "appraisal.xml" in names
    assert "report.pdf" in names


def test_build_ucdp_style_zip_includes_images(tmp_path: Path) -> None:
    xml = tmp_path / "a.xml"
    pdf = tmp_path / "b.pdf"
    imgs = tmp_path / "imgs"
    imgs.mkdir()
    (imgs / "front.jpg").write_bytes(b"fakejpg")
    sub = imgs / "interior"
    sub.mkdir()
    (sub / "kitchen.png").write_bytes(b"fakepng")
    out = tmp_path / "out.zip"
    xml.write_bytes(b"<root/>")
    pdf.write_bytes(b"%PDF-1.4")

    build_ucdp_style_zip(xml_path=xml, pdf_path=pdf, output_zip=out, images_dir=imgs)

    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
    assert "images/front.jpg" in names
    assert "images/interior/kitchen.png" in names
