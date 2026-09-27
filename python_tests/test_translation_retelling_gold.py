from __future__ import annotations

import tomllib
import unittest
from pathlib import Path

from fom.semantic_diff import diff_texts, nonempty_diff
from fom.validator import validate_path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = (
    ROOT
    / "experiments"
    / "translation-retelling"
    / "gold"
    / "expected.toml"
)


class TranslationRetellingGoldTests(unittest.TestCase):
    def setUp(self):
        self.cases = tomllib.loads(
            MANIFEST.read_text(encoding="utf-8")
        )["case"]

    def test_gold_files_are_structurally_valid(self):
        for case in self.cases:
            for key in ("source", "candidate"):
                with self.subTest(case=case["name"], role=key):
                    path = ROOT / case[key]
                    result = validate_path(path)
                    self.assertFalse(
                        result.errors,
                        "\n".join(
                            diagnostic.render()
                            for diagnostic in result.errors
                        ),
                    )

    def test_expected_corruptions_are_detected(self):
        for case in self.cases:
            with self.subTest(case=case["name"]):
                source_path = ROOT / case["source"]
                candidate_path = ROOT / case["candidate"]

                result = nonempty_diff(
                    diff_texts(
                        source_path.read_text(encoding="utf-8"),
                        candidate_path.read_text(encoding="utf-8"),
                        str(source_path),
                        str(candidate_path),
                    )
                )

                changes = result.get(case["dimension"], [])
                statuses = {change["status"] for change in changes}

                self.assertIn(
                    case["status"],
                    statuses,
                    f"{case['name']}: {result}",
                )


if __name__ == "__main__":
    unittest.main()
