import unittest

from fom.validator import validate_text


class ValidatorTests(unittest.TestCase):
    def test_valid_minimal_document(self):
        src = """
        (fom demo
          (node anna {:type :person})
          (node bob {:type :person})
          (rel r1 loves [anna bob]))
        """

        result = validate_text(src)

        self.assertFalse(
            result.errors,
            result.diagnostics,
        )

    def test_old_relation_syntax_fails(self):
        src = """
        (fom demo
          (node anna {:type :person})
          (node bob {:type :person})
          (rel loves {:left anna :right bob}))
        """

        result = validate_text(src)

        self.assertTrue(
            any(
                d.code == "F110"
                for d in result.errors
            )
        )

    def test_unresolved_reference_fails(self):
        src = """
        (fom demo
          (node anna {:type :person})
          (rel r1 sees {:actor anna :object apple}))
        """

        result = validate_text(src)

        self.assertTrue(
            any(
                "apple" in d.message
                for d in result.errors
            )
        )

    def test_duplicate_id_fails(self):
        src = """
        (fom demo
          (node x)
          (node x))
        """

        result = validate_text(src)

        self.assertTrue(
            any(
                d.code == "F011"
                for d in result.errors
            )
        )

    def test_bound_variable_passes(self):
        src = """
        (fom demo
          (node students {:type :group})
          (node book {:type :object})
          (pattern p [?x]
            (where (member-of ?x students))
            (require (read ?x book))))
        """

        result = validate_text(src)

        self.assertFalse(
            result.errors,
            result.diagnostics,
        )

    def test_unbound_variable_fails(self):
        src = """
        (fom demo
          (node book {:type :object})
          (constraint c (> ?x 1)))
        """

        result = validate_text(src)

        self.assertTrue(
            any(
                d.code == "F200"
                for d in result.errors
            )
        )


if __name__ == "__main__":
    unittest.main()
