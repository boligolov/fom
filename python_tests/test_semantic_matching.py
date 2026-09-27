from __future__ import annotations

import unittest

from fom.alignment import align_node_aliases
from fom.parser import parse
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

    def test_unique_node_structure_allows_id_independent_match(self):
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
          (node person-1 {:type :person})
          (node person-2 {:type :person})

          (rel relation-z greets
            {:actor person-1
             :target person-2}))
        """

        self.assertEqual(
            nonempty_diff(diff_texts(source, candidate)),
            {},
        )

    def test_ambiguous_same_type_nodes_are_not_guessed(self):
        source = parse(
            """
            (fom source
              (node anna {:type :person})
              (node bob {:type :person}))
            """
        )

        candidate = parse(
            """
            (fom candidate
              (node person-1 {:type :person})
              (node person-2 {:type :person}))
            """
        )

        source_aliases, candidate_aliases = align_node_aliases(
            source,
            candidate,
        )

        self.assertEqual(source_aliases, {})
        self.assertEqual(candidate_aliases, {})


if __name__ == "__main__":
    unittest.main()
