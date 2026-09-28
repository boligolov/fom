from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from fom.canonical import canonicalize_text
from fom.cli import main


COLLECTIONS = (
    "nodes", "relations", "scopes", "statuses", "deltas",
    "constraints", "subgraphs", "patterns",
)


class ProvenanceTests(unittest.TestCase):
    def test_locations_identify_distinct_anonymous_occurrences(self):
        source = (
            "(fom demo\n"
            "  (node anna)\n"
            "  (scope belief\n"
            "    (accept (home anna))\n"
            "    (accept (home anna))))\n"
        )
        result = canonicalize_text(source, "story.fom", include_provenance=True)
        origins = {p["target"]["ref"]: p for p in result["provenance"]}
        for record, line in zip(result["statuses"], (4, 5)):
            status_origin = origins[record["id"]]
            application_origin = origins[record["content"]["ref"]]
            self.assertEqual(status_origin["origin"], "status-form")
            self.assertEqual(status_origin["source"], {
                "path": "story.fom", "line": line, "column": 5,
                "end_line": line, "end_column": 25,
            })
            self.assertEqual(application_origin["origin"], "anonymous-application")
            self.assertEqual(application_origin["source"], {
                "path": "story.fom", "line": line, "column": 13,
                "end_line": line, "end_column": 24,
            })
        self.assertEqual(origins["anna"]["origin"], "declaration")
        self.assertEqual(origins["anna"]["source"]["line"], 2)
        self.assertEqual(len(result["relations"]), 2)

    def test_provenance_is_optional_and_does_not_change_graph(self):
        source = "(fom demo (node anna) (scope s (accept (home anna))))"
        plain = canonicalize_text(source)
        traced = canonicalize_text(source, "first.fom", include_provenance=True)
        moved = canonicalize_text("\n" + source, "second.fom", include_provenance=True)
        self.assertEqual(plain["provenance"], [])
        self.assertNotEqual(traced["provenance"], moved["provenance"])
        for result in (traced, moved):
            result["provenance"] = []
            self.assertEqual(plain, result)

    def test_every_emitted_corpus_record_has_one_origin(self):
        root = Path(__file__).resolve().parents[1]
        paths = sorted(
            path
            for directory in ("examples", "tests", "experiments/translation-retelling/gold")
            for path in (root / directory).rglob("*.fom")
        )
        self.assertTrue(paths)
        for path in paths:
            with self.subTest(path=path):
                source = path.read_text(encoding="utf-8")
                result = canonicalize_text(source, str(path), include_provenance=True)
                ids = [r["id"] for name in COLLECTIONS for r in result[name]]
                targets = [p["target"]["ref"] for p in result["provenance"]]
                self.assertCountEqual(ids, targets)
                self.assertEqual(len(targets), len(set(targets)))
                lines = source.splitlines()
                for origin in result["provenance"]:
                    loc = origin["source"]
                    self.assertEqual(loc["path"], str(path))
                    self.assertEqual(lines[loc["line"] - 1][loc["column"] - 1], "(")
                    self.assertEqual(lines[loc["end_line"] - 1][loc["end_column"] - 2], ")")

    def test_cli_emits_requested_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.fom"
            path.write_text("(fom demo (node anna))", encoding="utf-8")
            for option in ([], ["--provenance"]):
                with self.subTest(option=option):
                    output = io.StringIO()
                    with contextlib.redirect_stdout(output):
                        code = main(["canonical", str(path), *option])
                    self.assertEqual(code, 0)
                    result = json.loads(output.getvalue())
                    self.assertEqual(bool(result["provenance"]), bool(option))


if __name__ == "__main__":
    unittest.main()
