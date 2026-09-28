import contextlib
import copy
import io
import json
from pathlib import Path
import unittest

from fom.canonical import canonicalize_text
from fom.cli import main
from fom.scope_resolution import resolve_status
from fom.semantic_diff import diff_texts, nonempty_diff


ROOT = Path(__file__).resolve().parents[1]


class ScopeResolutionTests(unittest.TestCase):
    def graph(self, body):
        return canonicalize_text(f'(fom demo (subgraph p (fact)) {body})')

    def test_existing_overlay_fixture_executes_its_expected_outcomes(self):
        graph = canonicalize_text((ROOT / 'tests/scope-overlay-shadow.fom').read_text(encoding='utf-8'))
        original = copy.deepcopy(graph)
        for scope, content, expected in (
            ('base', 'p-content', 'accept'), ('child', 'p-content', 'uncommitted'),
            ('child', 'q-content', 'accept'), ('merged', 'r-content', 'conflict'),
        ):
            with self.subTest(scope=scope, content=content):
                self.assertEqual(resolve_status(graph, scope, content)['status'], expected)
        shadow = resolve_status(graph, 'child', 'p-content')
        self.assertEqual(shadow['evidence'][0]['scope'], 'child')
        self.assertEqual(resolve_status(graph, 'merged', 'r-content')['alternatives'], ['accept', 'reject'])
        self.assertEqual(graph, original)

    def test_imports_and_nesting_do_not_inherit_status(self):
        graph = self.graph('''(scope base (accept p) (scope nested))
          (scope imported {:imports [base]})
          (scope disabled {:inherits-status-from base :inherit-mode :none})''')
        for name in ('nested', 'imported', 'disabled'):
            result = resolve_status(graph, name, 'p')
            self.assertEqual(result['status'], 'uncommitted')
            self.assertEqual(result['evidence'], [])

    def test_local_override_masks_inherited_conflict_and_propagates(self):
        graph = self.graph('''(scope a (accept p)) (scope b (reject p))
          (scope child {:inherits-status-from [a b] :inherit-mode :overlay} (uncommit p))
          (scope grandchild {:inherits-status-from child :inherit-mode :overlay})''')
        self.assertEqual(resolve_status(graph, 'grandchild', 'p')['status'], 'uncommitted')
        self.assertEqual(resolve_status(graph, 'grandchild', 'p')['evidence'][0]['scope'], 'child')

    def test_local_conflicts_are_not_overwritten(self):
        graph = self.graph('(scope s (accept p) (reject p))')
        self.assertEqual(resolve_status(graph, 's', 'p')['status'], 'conflict')

    def test_absence_is_not_a_conflict_but_explicit_shadow_is(self):
        for status, expected in (('', 'accept'), ('(uncommitted p)', 'conflict')):
            graph = self.graph(f'''(scope a (accept p)) (scope b {status})
              (scope child {{:inherits-status-from [a b] :inherit-mode :overlay}})''')
            self.assertEqual(resolve_status(graph, 'child', 'p')['status'], expected)

    def test_diamond_deduplicates_shared_evidence(self):
        graph = self.graph('''(scope a (accept p {:certainty :low}))
          (scope b {:inherits-status-from a :inherit-mode :overlay})
          (scope c {:inherits-status-from a :inherit-mode :overlay})
          (scope d {:inherits-status-from [b c] :inherit-mode :overlay})''')
        result = resolve_status(graph, 'd', 'p')
        self.assertEqual(len(result['evidence']), 1)
        self.assertEqual(result['evidence'][0]['qualifiers'], {'certainty': 'low'})

    def test_cycles_unsupported_modes_and_non_scope_bases_fail(self):
        for body in (
            '(scope s {:inherits-status-from s :inherit-mode :overlay} (accept p))',
            '(scope s {:inherits-status-from t :inherit-mode :overlay}) (scope t {:inherits-status-from s :inherit-mode :overlay})',
            '(scope s {:inherit-mode :selective})',
            '(scope s {:inherits-status-from p :inherit-mode :overlay})',
        ):
            with self.subTest(body=body), self.assertRaises(ValueError):
                resolve_status(self.graph(body), 's', 'p')

    def test_explicit_scope_inside_another_scope_and_shadow_alias(self):
        source = '(fom demo (subgraph p (fact)) (scope s) (scope t (uncommit s p)))'
        equivalent = '(fom demo (subgraph p (fact)) (scope s (uncommitted p)) (scope t))'
        self.assertEqual(canonicalize_text(source), canonicalize_text(equivalent))
        self.assertEqual(nonempty_diff(diff_texts(source, equivalent)), {})
        result = resolve_status(canonicalize_text(source), 's', 'p')
        self.assertEqual(result['evidence'][0]['value'], 'uncommitted')

    def test_cli_resolves_fixture(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main(['resolve', str(ROOT / 'tests/scope-overlay-shadow.fom'), 'child', 'p-content'])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out.getvalue())['status'], 'uncommitted')
