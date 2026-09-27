from __future__ import annotations

import unittest

from fom.semantic_diff import diff_texts, nonempty_diff


class SemanticMatchingTests(unittest.TestCase):
    def test_relation_and_subgraph_ids_are_nonsemantic(self):
        source = """
        (fom source
          (node anna {:type :person})
          (node bob {:type :person})

          (subgraph source-content
            (rel relation-a greets
              {:actor anna
               :target bob}))

          (scope shared
            (accept source-content)))
        """

        candidate = """
        (fom candidate
          (node anna {:type :person})
          (node bob {:type :person})

          (subgraph completely-different-fragment-id
            (rel totally-different-relation-id greets
              {:target bob
               :actor anna}))

          (scope shared
            (accept completely-different-fragment-id)))
        """

        self.assertEqual(
            nonempty_diff(diff_texts(source, candidate)),
            {},
        )

    def test_relation_id_rename_does_not_hide_real_change(self):
        source = """
        (fom source
          (node anna {:type :person})
          (node bob {:type :person})

          (rel relation-a greets
            {:actor anna
             :target bob}))
        """

        candidate = """
        (fom candidate
          (node anna {:type :person})
          (node bob {:type :person})

          (rel other-id insults
            {:actor anna
             :target bob}))
        """

        diff = nonempty_diff(diff_texts(source, candidate))

        statuses = {
            change["status"]
            for change in diff.get("content", [])
        }

        self.assertIn("LOST", statuses)
        self.assertIn("INVENTED", statuses)


if __name__ == "__main__":
    unittest.main()
