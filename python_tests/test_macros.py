import unittest

from fom.canonical import canonicalize_text
from fom.macros import expand_macros
from fom.parser import parse
from fom.semantic_diff import diff_texts, nonempty_diff
from fom.validator import validate_text


class SelfMacroTests(unittest.TestCase):
    def test_explicit_status_scope_supports_forward_declaration(self):
        source = '(fom demo (node anna) (accept s (home (self))) (scope s {:center anna}))'
        shorthand = '(fom demo (node anna) (scope s {:center anna} (accept (home (self)))))'
        self.assertEqual(canonicalize_text(source), canonicalize_text(shorthand))
        self.assertEqual(nonempty_diff(diff_texts(source, shorthand)), {})

    def test_self_matches_explicit_center_in_canonical_and_diff(self):
        source = '(fom demo (node anna) (scope s {:center anna} (accept (home (self)))))'
        explicit = source.replace('(self)', 'anna')
        self.assertEqual(canonicalize_text(source), canonicalize_text(explicit))
        self.assertEqual(nonempty_diff(diff_texts(source, explicit)), {})
        self.assertEqual(nonempty_diff(diff_texts(explicit, source)), {})

    def test_nested_scopes_use_local_center_and_restore_outer(self):
        source = '''(fom demo (node anna) (node bob)
          (scope outer {:center anna}
            (scope inner {:center bob} (accept (home (self))))
            (accept (home (self)))))'''
        result = canonicalize_text(source)
        relations = {r['id']: r for r in result['relations']}
        targets = {s['scope']['ref']: relations[s['content']['ref']]['args']['arg0']
                   for s in result['statuses']}
        self.assertEqual(targets, {'inner': {'ref': 'bob'}, 'outer': {'ref': 'anna'}})

    def test_invalid_self_fails_validation_and_canonicalization(self):
        bodies = (
            '(rel r home [(self)])',
            '(scope s {:owner anna} (accept (home (self))))',
            '(scope s {:center anna} (scope t (accept (home (self)))))',
            '(scope s {:center anna} (accept (home (self anna))))',
            '(scope s {:center :anna} (accept (home (self))))',
        )
        for body in bodies:
            with self.subTest(body=body):
                source = f'(fom demo (node anna) {body})'
                self.assertTrue(any(d.code == 'M001' for d in validate_text(source).errors))
                with self.assertRaises(ValueError):
                    canonicalize_text(source)

    def test_unresolved_center_is_not_licensed_by_expansion(self):
        source = '(fom demo (scope s {:center missing} (accept (home (self)))))'
        self.assertTrue(any(d.code == 'F300' for d in validate_text(source).errors))

    def test_provenance_records_substitution_without_inventing_a_relation(self):
        source = '(fom demo (node anna) (scope s {:center anna} (accept (home (self)))))'
        result = canonicalize_text(source, 'self.fom', include_provenance=True)
        expansion, = result['macro_provenance']
        self.assertEqual(expansion['macro'], 'self')
        self.assertEqual(expansion['target'], {'ref': 'anna'})
        loc = expansion['source']
        self.assertEqual(source[loc['column'] - 1:loc['end_column'] - 1], '(self)')
        self.assertEqual([r['predicate'] for r in result['relations']], ['home'])
        self.assertNotIn('macro_provenance', canonicalize_text(source))

    def test_expansion_is_idempotent_and_preserves_open_predicates(self):
        source = '(fom demo (node anna) (scope s {:center anna} (accept (again (home (self))))))'
        root, first = expand_macros(parse(source))
        twice, second = expand_macros(root)
        self.assertEqual(root, twice)
        self.assertEqual(len(first), 1)
        self.assertEqual(second, [])
        self.assertIn('again', [r['predicate'] for r in canonicalize_text(source)['relations']])

    def test_scope_center_does_not_leak_to_sibling(self):
        source = '(fom demo (node anna) (scope s {:center anna}) (scope t (accept (home (self)))))'
        self.assertTrue(validate_text(source).errors)
