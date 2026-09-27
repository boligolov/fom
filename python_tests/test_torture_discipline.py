from __future__ import annotations

import tomllib
import unittest
from pathlib import Path

from fom.model import Atom, Expr, ListExpr, MapExpr, VectorExpr
from fom.parser import parse


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tests" / "discipline.toml"

STRUCTURAL_HEADS = {
    "fom",
    "node",
    "rel",
    "subgraph",
    "scope",
    "delta",
    "constraint",
    "pattern",
    "where",
    "require",
    "bind",
    "accept",
    "reject",
    "add",
    "remove",
    "update",
    "connect",
    "disconnect",
    "identify",
    "activate",
    "deactivate",
    "uncommit",
}


def symbol(expr: Expr) -> str | None:
    if isinstance(expr, Atom) and expr.kind == "symbol":
        return str(expr.value)
    return None


def collect_predicates(expr: Expr) -> list[str]:
    out: list[str] = []

    def walk(node: Expr) -> None:
        if isinstance(node, Atom):
            return

        if isinstance(node, VectorExpr):
            for child in node.items:
                walk(child)
            return

        if isinstance(node, MapExpr):
            for _, child in node.items:
                walk(child)
            return

        if not node.items:
            return

        head = symbol(node.items[0])

        if head == "rel" and len(node.items) >= 3:
            predicate = symbol(node.items[2])
            if predicate:
                out.append(predicate)
            for child in node.items[3:]:
                walk(child)
            return

        if head and head not in STRUCTURAL_HEADS:
            out.append(head)

        for child in node.items[1:]:
            walk(child)

    walk(expr)
    return out


class TortureDisciplineTests(unittest.TestCase):
    def test_phenomenon_labels_are_not_predicates(self):
        manifest = tomllib.loads(MANIFEST.read_text(encoding="utf-8"))

        failures: list[str] = []

        for case in manifest["test"]:
            path = ROOT / case["path"]
            root = parse(path.read_text(encoding="utf-8"))
            predicates = collect_predicates(root)

            forbidden = [
                fragment.lower()
                for fragment in case["forbid_predicate_fragments"]
            ]

            for predicate in predicates:
                normalized = predicate.lower()
                hits = [
                    fragment
                    for fragment in forbidden
                    if fragment in normalized
                ]
                if hits:
                    failures.append(
                        f"{case['path']}: predicate '{predicate}' "
                        f"contains forbidden phenomenon label(s): {hits}"
                    )

        self.assertFalse(
            failures,
            "\n".join(failures),
        )


if __name__ == "__main__":
    unittest.main()
