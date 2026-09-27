from __future__ import annotations

import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS = (
    ROOT
    / "experiments"
    / "translation-retelling"
    / "corpus"
    / "cases.toml"
)

KNOWN_DIMENSIONS = {
    "content",
    "fixed_unknown",
    "resolution",
    "source_attribution",
    "epistemic_status",
    "inference_path",
    "explicitness",
    "disclosure",
    "coactivation",
    "function",
    "salience",
    "focus",
    "social_state",
    "attempted_vs_actual",
    "indeterminacy",
    "form",
}


class ExperimentCorpusTests(unittest.TestCase):
    def setUp(self):
        self.data = tomllib.loads(
            CORPUS.read_text(encoding="utf-8")
        )
        self.cases = self.data["case"]

    def test_case_ids_are_unique(self):
        ids = [case["id"] for case in self.cases]
        self.assertEqual(len(ids), len(set(ids)))

    def test_required_fields_exist(self):
        required = {
            "id",
            "source_language",
            "target_language",
            "source",
            "valid",
            "corrupted",
            "expected_dimensions",
            "note",
        }

        for case in self.cases:
            with self.subTest(case=case.get("id")):
                self.assertTrue(
                    required.issubset(case),
                    required - set(case),
                )

    def test_valid_and_corrupted_variants_differ(self):
        for case in self.cases:
            with self.subTest(case=case["id"]):
                self.assertNotEqual(
                    case["valid"].strip(),
                    case["corrupted"].strip(),
                )

    def test_expected_dimensions_use_known_vocabulary(self):
        for case in self.cases:
            with self.subTest(case=case["id"]):
                unknown = (
                    set(case["expected_dimensions"])
                    - KNOWN_DIMENSIONS
                )
                self.assertFalse(unknown, unknown)

    def test_pilot_has_multiple_failure_classes(self):
        covered = {
            dimension
            for case in self.cases
            for dimension in case["expected_dimensions"]
        }
        self.assertGreaterEqual(len(covered), 8)


if __name__ == "__main__":
    unittest.main()
