from __future__ import annotations

import argparse
from pathlib import Path

from .validator import validate_path


def iter_fom(paths: list[str]) -> list[Path]:
    out: list[Path] = []

    for raw in paths:
        path = Path(raw)

        if path.is_dir():
            out.extend(
                sorted(
                    item
                    for item in path.rglob("*.fom")
                    if item.is_file()
                )
            )
        elif path.suffix == ".fom" and path.is_file():
            out.append(path)

    return sorted(set(out))


def cmd_check(
    paths: list[str],
    warnings_as_errors: bool = False,
) -> int:
    files = iter_fom(paths)

    if not files:
        print("fom: no .fom files found")
        return 2

    errors = 0
    warnings = 0

    for path in files:
        result = validate_path(path)

        for diagnostic in result.diagnostics:
            print(diagnostic.render())

        errors += len(result.errors)
        warnings += len(result.warnings)

    print(
        f"checked {len(files)} file(s): "
        f"{errors} error(s), {warnings} warning(s)"
    )

    return (
        1
        if errors or (warnings_as_errors and warnings)
        else 0
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fom")
    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    check = sub.add_parser(
        "check",
        help="parse and validate FoM Text files",
    )
    check.add_argument(
        "paths",
        nargs="+",
        help=".fom files or directories",
    )
    check.add_argument(
        "--warnings-as-errors",
        action="store_true",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "check":
        return cmd_check(
            args.paths,
            args.warnings_as_errors,
        )

    return 2
