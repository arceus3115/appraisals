from __future__ import annotations

import zipfile
from pathlib import Path


def build_ucdp_style_zip(
    *,
    xml_path: Path,
    pdf_path: Path,
    output_zip: Path,
    images_dir: Path | None = None,
) -> None:
    """Assemble a UCDP-style appraisal ZIP (XML + PDF + optional images folder).

    Layout (conventional):
    - ``appraisal.xml`` at archive root (caller supplies the logical UAD 3.6 payload file).
    - ``report.pdf`` at archive root.
    - ``images/`` optional directory of image files referenced by the report.
    """

    output_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(xml_path, arcname="appraisal.xml")
        zf.write(pdf_path, arcname="report.pdf")
        if images_dir is not None and images_dir.is_dir():
            for p in sorted(images_dir.rglob("*")):
                if p.is_file():
                    rel = Path("images") / p.relative_to(images_dir)
                    zf.write(p, arcname=str(rel).replace("\\", "/"))
