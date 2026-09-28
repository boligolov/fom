from __future__ import annotations

import unittest

from fom.canonical import canonicalize_text


class CanonicalizerTests(unittest.TestCase):
    def test_generated_ids_do_not_collide_with_later_declarations(self):
        source = """
        (fom demo
          (node anna {:type :person})
          (scope belief
            (accept (home anna))
            (reject (away anna)))
          (subgraph reserved
            (node _anon-0001)
            (rel _anon-0002 home [anna])
            (node _status-0001)
            (rel _status-0002 away [anna])))
        """
        canonical = canonicalize_text(source)
        collections = (
            "nodes", "relations", "scopes", "statuses", "deltas",
            "constraints", "subgraphs", "patterns",
        )
        ids = [record["id"] for name in collections for record in canonical[name]]
        self.assertEqual(len(ids), len(set(ids)))

        relations = {record["id"]: record for record in canonical["relations"]}
        for status, predicate in zip(canonical["statuses"], ("home", "away")):
            relation = relations[status["content"]["ref"]]
            self.assertTrue(relation["generated"])
            self.assertEqual(relation["predicate"], predicate)
        self.assertEqual(canonical, canonicalize_text(source))

    def test_nested_applications_keep_distinct_references(self):
        canonical = canonicalize_text("""
        (fom demo
          (node anna)
          (node _anon-0001)
          (scope belief (accept (possible (home anna)))))
        """)
        relations = {record["id"]: record for record in canonical["relations"]}
        outer = relations[canonical["statuses"][0]["content"]["ref"]]
        inner = relations[outer["args"]["arg0"]["ref"]]
        self.assertEqual(outer["predicate"], "possible")
        self.assertEqual(inner["predicate"], "home")
        self.assertNotEqual(outer["id"], inner["id"])
        self.assertNotIn("_anon-0001", relations)

    def test_scope_shorthand_matches_explicit_status(self):
        shorthand = """
        (fom demo
          (node anna {:type :person})
          (subgraph content
            (rel r1 home {:person anna}))
          (scope belief
            {:owner anna}
            (accept content
              {:certainty :high})))
        """

        explicit = """
        (fom demo
          (node anna {:type :person})
          (subgraph content
            (rel r1 home {:person anna}))
          (scope belief
            {:owner anna})
          (accept belief content
            {:certainty :high}))
        """

        self.assertEqual(
            canonicalize_text(shorthand),
            canonicalize_text(explicit),
        )

    def test_pattern_variables_are_alpha_normalized(self):
        left = """
        (fom demo
          (node students {:type :group})
          (node book {:type :object})
          (pattern p [?x]
            (where
              (member-of ?x students))
            (require
              (read ?x book))))
        """

        right = """
        (fom demo
          (node students {:type :group})
          (node book {:type :object})
          (pattern p [?student]
            (where
              (member-of ?student students))
            (require
              (read ?student book))))
        """

        self.assertEqual(
            canonicalize_text(left),
            canonicalize_text(right),
        )

    def test_map_key_order_is_nonsemantic(self):
        left = """
        (fom demo
          (node anna {:type :person})
          (node bob {:type :person})
          (rel r1 transfer
            {:source anna
             :recipient bob}))
        """

        right = """
        (fom demo
          (node anna {:type :person})
          (node bob {:type :person})
          (rel r1 transfer
            {:recipient bob
             :source anna}))
        """

        self.assertEqual(
            canonicalize_text(left),
            canonicalize_text(right),
        )

    def test_anonymous_application_is_reified(self):
        source = """
        (fom demo
          (node anna {:type :person})
          (scope belief
            {:owner anna}
            (accept
              (home anna))))
        """

        canonical = canonicalize_text(source)

        generated = [
            relation
            for relation in canonical["relations"]
            if relation["generated"]
        ]

        self.assertEqual(len(generated), 1)
        self.assertEqual(generated[0]["predicate"], "home")
        self.assertEqual(
            canonical["statuses"][0]["content"],
            {"ref": generated[0]["id"]},
        )


if __name__ == "__main__":
    unittest.main()
