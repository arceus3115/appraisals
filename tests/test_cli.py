import sys
from pathlib import Path

from appraisal_ai.cli import main


def test_cli_version(capsys):
    sys.argv = ["appraisal-ai", "--version"]
    main()
    out = capsys.readouterr().out.strip()
    assert out == "0.1.0"


def test_cli_uad_migrate(tmp_path: Path) -> None:
    fixtures = Path(__file__).resolve().parent / "fixtures" / "uad"
    inp = fixtures / "legacy_minimal.xml"
    outp = tmp_path / "out.xml"
    rep = tmp_path / "report.json"
    sys.argv = [
        "appraisal-ai",
        "uad",
        "migrate",
        "--from",
        "2.6",
        "--to",
        "3.6",
        "-i",
        str(inp),
        "-o",
        str(outp),
        "--report",
        str(rep),
    ]
    main()
    assert outp.is_file()
    assert "UAD36Example" in outp.read_text(encoding="utf-8")
    assert rep.is_file()
