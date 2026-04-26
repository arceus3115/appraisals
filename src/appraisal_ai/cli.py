"""CLI entry point; extend with generate, validate, etc."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(prog="appraisal-ai", description="AppraisalAI CLI")
    parser.add_argument("--version", action="store_true", help="print version and exit")

    sub = parser.add_subparsers(dest="command")

    uad = sub.add_parser("uad", help="Uniform Appraisal Dataset utilities")
    uad_sub = uad.add_subparsers(dest="uad_command")

    mig = uad_sub.add_parser("migrate", help="Migrate XML between UAD 2.6-style legacy and UAD 3.6-style layouts")
    mig.add_argument("--from", dest="src_fmt", choices=["2.6", "3.6"], required=True, help="source format")
    mig.add_argument("--to", dest="dst_fmt", choices=["2.6", "3.6"], required=True, help="target format")
    mig.add_argument("--input", "-i", type=Path, required=True, help="input XML file path")
    mig.add_argument("--output", "-o", type=Path, required=True, help="output XML file path")
    mig.add_argument(
        "--mapping",
        type=Path,
        default=None,
        help="optional appendix_g_mapping.csv path (defaults to packaged starter CSV)",
    )
    mig.add_argument("--report", type=Path, default=None, help="write JSON migration report to this path")

    z = uad_sub.add_parser("zip", help="Build a UCDP-style appraisal ZIP (XML + PDF + optional images/)")
    z.add_argument("--xml", type=Path, required=True, help="UAD / MISMO XML file to place as appraisal.xml")
    z.add_argument("--pdf", type=Path, required=True, help="PDF report to place as report.pdf")
    z.add_argument("--images-dir", type=Path, default=None, help="optional directory packed under images/")
    z.add_argument("--output", "-o", type=Path, required=True, help="output .zip path")

    args = parser.parse_args()
    if args.version:
        from appraisal_ai import __version__

        print(__version__)
        return

    command = getattr(args, "command", None)
    uad_command = getattr(args, "uad_command", None)
    if command == "uad":
        if uad_command == "migrate":
            from appraisal_ai.uad.migrate import migrate_xml_bytes

            data = args.input.read_bytes()
            out, report = migrate_xml_bytes(
                data,
                args.src_fmt,
                args.dst_fmt,
                mapping_path=str(args.mapping) if args.mapping else None,
            )
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_bytes(out)
            if args.report is not None:
                args.report.parent.mkdir(parents=True, exist_ok=True)
                args.report.write_text(json.dumps(report.to_json_obj(), indent=2), encoding="utf-8")
            return
        if uad_command == "zip":
            from appraisal_ai.uad.zip_package import build_ucdp_style_zip

            build_ucdp_style_zip(
                xml_path=args.xml,
                pdf_path=args.pdf,
                output_zip=args.output,
                images_dir=args.images_dir,
            )
            return
        uad.print_help()
        return

    parser.print_help()


if __name__ == "__main__":
    main()
