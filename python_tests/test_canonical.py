from __future__ import annotations

import unittest

from fom.canonical import canonicalize_text


class CanonicalizerTests(unittest.TestCase):
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
