from __future__ import annotations

import argparse
import json
from pathlib import Path

from .canonical import canonicalize_text
from .semantic_diff import diff_texts, nonempty_diff
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


def cmd_diff(source: str, candidate: str, as_json: bool = False) -> int:
    source_path = Path(source)
    candidate_path = Path(candidate)

    try:
        result = nonempty_diff(
            diff_texts(
                source_path.read_text(encoding="utf-8"),
                candidate_path.read_text(encoding="utf-8"),
                str(source_path),
                str(candidate_path),
            )
        )
    except (OSError, ValueError) as exc:
        print(f"fom diff: {exc}")
        return 2

    if as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif not result:
        print("no differences in the currently supported dimensions")
    else:
        for dimension, changes in result.items():
            print(f"{dimension}:")
            for change in changes:
                details = ", ".join(
                    f"{key}={value}"
                    for key, value in change.items()
                    if key != "status"
                )
                suffix = f" ({details})" if details else ""
                print(f"  {change['status']}{suffix}")

    return 0


def cmd_canonical(path: str) -> int:
    source_path = Path(path)

    try:
        result = canonicalize_text(
            source_path.read_text(encoding="utf-8"),
            str(source_path),
        )
    except (OSError, ValueError) as exc:
        print(f"fom canonical: {exc}")
        return 2

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


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

    diff = sub.add_parser(
        "diff",
        help="compare two FoM files using the currently supported semantic dimensions",
    )
    diff.add_argument("source")
    diff.add_argument("candidate")
    diff.add_argument("--json", action="store_true")

    canonical = sub.add_parser(
        "canonical",
        help="emit first-pass canonical FoM graph as JSON",
    )
    canonical.add_argument("path")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "check":
        return cmd_check(
            args.paths,
            args.warnings_as_errors,
        )

    if args.command == "diff":
        return cmd_diff(
            args.source,
            args.candidate,
            args.json,
        )

    if args.command == "canonical":
        return cmd_canonical(args.path)

    return 2
