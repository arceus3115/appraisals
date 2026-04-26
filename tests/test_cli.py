from appraisal_ai.cli import main


def test_cli_version(capsys):
    import sys

    sys.argv = ["appraisal-ai", "--version"]
    main()
    out = capsys.readouterr().out.strip()
    assert out == "0.1.0"
