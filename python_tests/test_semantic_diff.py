from __future__ import annotations

import tomllib
import unittest
from pathlib import Path

from fom.semantic_diff import diff_texts, nonempty_diff


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tests" / "diff-fixtures.toml"


class SemanticDiffFixtureTests(unittest.TestCase):
    def test_declared_corruptions_are_detected(self):
        manifest = tomllib.loads(
            MANIFEST.read_text(encoding="utf-8")
        )

        for case in manifest["case"]:
            with self.subTest(case=case["name"]):
                source_path = ROOT / case["source"]
                candidate_path = ROOT / case["candidate"]

                diff = nonempty_diff(
                    diff_texts(
                        source_path.read_text(encoding="utf-8"),
                        candidate_path.read_text(encoding="utf-8"),
                        str(source_path),
                        str(candidate_path),
                    )
                )

                changes = diff.get(case["dimension"], [])
                statuses = {change["status"] for change in changes}

                self.assertIn(
                    case["status"],
                    statuses,
                    f"{case['name']}: {diff}",
                )

    def test_source_against_itself_has_no_diff(self):
        path = ROOT / "tests" / "fixtures" / "corruption" / "source.fom"
        text = path.read_text(encoding="utf-8")

        self.assertEqual(
            nonempty_diff(
                diff_texts(
                    text,
                    text,
                    str(path),
                    str(path),
                )
            ),
            {},
        )


if __name__ == "__main__":
    unittest.main()
