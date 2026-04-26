"""CLI entry point; extend with generate, validate, etc."""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(prog="appraisal-ai", description="AppraisalAI CLI")
    parser.add_argument("--version", action="store_true", help="print version and exit")
    args = parser.parse_args()
    if args.version:
        from appraisal_ai import __version__

        print(__version__)
        return
    parser.print_help()


if __name__ == "__main__":
    main()
