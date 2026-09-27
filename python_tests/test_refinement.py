from __future__ import annotations

import unittest

from fom.refinement import find_refinement_matches


class RefinementTests(unittest.TestCase):
    def test_transfer_control_refinement_matches(self):
        source = """
        (fom source
          (node anna {:type :person})
          (node bob {:type :person})
          (node book {:type :object})

          (rel transfer transfer-control
            {:source anna
             :theme book
             :recipient bob}))
        """

        candidate = """
        (fom candidate
          (node anna {:type :person})
          (node bob {:type :person})
          (node book {:type :object})

          (rel before controls-before
            {:holder anna
             :theme book})

          (rel after controls-after
            {:holder bob
             :theme book}))
        """

        matches = find_refinement_matches(source, candidate)

        self.assertEqual(len(matches), 1)
        self.assertEqual(
            matches[0].source_relation_id,
            "transfer",
        )
        self.assertEqual(
            set(matches[0].candidate_relation_ids),
            {"before", "after"},
        )

    def test_missing_required_refinement_relation_does_not_match(self):
        source = """
        (fom source
          (node anna {:type :person})
          (node bob {:type :person})
          (node book {:type :object})

          (rel transfer transfer-control
            {:source anna
             :theme book
             :recipient bob}))
        """

        candidate = """
        (fom candidate
          (node anna {:type :person})
          (node bob {:type :person})
          (node book {:type :object})

          (rel before controls-before
            {:holder anna
             :theme book}))
        """

        self.assertEqual(
            find_refinement_matches(source, candidate),
            [],
        )

    def test_wrong_role_binding_does_not_match(self):
        source = """
        (fom source
          (node anna {:type :person})
          (node bob {:type :person})
          (node book {:type :object})

          (rel transfer transfer-control
            {:source anna
             :theme book
             :recipient bob}))
        """

        candidate = """
        (fom candidate
          (node anna {:type :person})
          (node bob {:type :person})
          (node book {:type :object})

          (rel before controls-before
            {:holder bob
             :theme book})

          (rel after controls-after
            {:holder anna
             :theme book}))
        """

        self.assertEqual(
            find_refinement_matches(source, candidate),
            [],
        )


if __name__ == "__main__":
    unittest.main()
