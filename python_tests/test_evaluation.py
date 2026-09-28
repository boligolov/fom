import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest

from fom.canonical import canonicalize_text
from fom.cli import main
from fom.evaluation import evaluate_constraints


FIXTURES = Path(__file__).resolve().parents[1] / 'tests/fixtures/evaluation'


class EvaluationTests(unittest.TestCase):
    def graph(self, body='', requirement='(unknown p {:scope s})', strength='required'):
        return canonicalize_text(f'''(fom demo
          (subgraph p (fact)) (scope s {body})
          (constraint c {{:strength :{strength}}} {requirement}))''')

    def test_fixture_detects_removed_shadow_even_when_constraints_are_deleted(self):
        source = canonicalize_text((FIXTURES / 'source.fom').read_text())
        candidate = canonicalize_text((FIXTURES / 'corrupted.fom').read_text())
        original = copy.deepcopy((source, candidate))
        self.assertEqual(evaluate_constraints(source)['outcome'], 'PASS')
        result = evaluate_constraints(source, candidate)
        self.assertEqual(result['outcome'], 'FAIL')
        rows = {r['constraint']: r for r in result['results']}
        self.assertEqual(rows['keep-secret-unknown']['outcome'], 'VIOLATED')
        self.assertEqual(rows['retain-known-status']['outcome'], 'SATISFIED')
        self.assertEqual(rows['keep-secret-unknown']['resolved']['evidence'][0]['scope'], 'base')
        self.assertEqual((source, candidate), original)

    def test_status_matrix_and_unknown(self):
        for actual in ('accept', 'reject', 'uncommitted'):
            for expected in ('accept', 'reject', 'uncommitted'):
                with self.subTest(actual=actual, expected=expected):
                    graph = self.graph(f'({actual} p)', f'(status-is p {{:scope s :value :{expected}}})')
                    self.assertEqual(evaluate_constraints(graph)['outcome'], 'PASS' if actual == expected else 'FAIL')
        self.assertEqual(evaluate_constraints(self.graph())['outcome'], 'PASS')
        self.assertEqual(evaluate_constraints(self.graph('(reject p)'))['outcome'], 'FAIL')

    def test_conflict_does_not_satisfy_unknown(self):
        result = evaluate_constraints(self.graph('(accept p) (reject p)'))
        self.assertEqual(result['outcome'], 'FAIL')
        self.assertEqual(result['results'][0]['resolved']['status'], 'conflict')

    def test_unsupported_required_constraints_never_pass(self):
        for requirement in ('(fixed-unknown p)', '(preserve p)',
                            '(unknown p {:scope s :audience :reader})'):
            with self.subTest(requirement=requirement):
                result = evaluate_constraints(self.graph(requirement=requirement))
                self.assertEqual(result['outcome'], 'INDETERMINATE')
                self.assertFalse(result['complete'])

    def test_bad_contract_is_error(self):
        for requirement in ('(status-is p {:scope s :value :maybe})',
                            '(unknown p {:scope p})'):
            self.assertEqual(evaluate_constraints(self.graph(requirement=requirement))['outcome'], 'ERROR')
        self.assertEqual(evaluate_constraints(self.graph(strength='preferred'))['outcome'], 'ERROR')

    def test_anonymous_cross_document_target_is_unsupported(self):
        result = evaluate_constraints(self.graph(requirement='(unknown (fact) {:scope s})'))
        self.assertEqual(result['outcome'], 'INDETERMINATE')

    def test_missing_candidate_scope_or_target_is_violation(self):
        for text in ('(fom candidate (subgraph p (fact)))', '(fom candidate (scope s))'):
            result = evaluate_constraints(self.graph(), canonicalize_text(text))
            self.assertEqual(result['outcome'], 'FAIL')

    def test_optional_violations_do_not_block_required_pass(self):
        graph = self.graph('(accept p)', '(status-is p {:scope s :value :accept})')
        optional = self.graph('(accept p)', strength='optional')['constraints'][0]
        optional['id'] = 'optional'
        graph['constraints'].append(optional)
        result = evaluate_constraints(graph)
        self.assertEqual(result['outcome'], 'PASS')
        self.assertEqual(result['results'][1]['outcome'], 'VIOLATED')

    def test_empty_and_optional_only_contracts_are_not_applicable(self):
        self.assertEqual(evaluate_constraints(canonicalize_text('(fom empty)'))['outcome'], 'NOT_APPLICABLE')
        self.assertEqual(evaluate_constraints(self.graph(strength='optional'))['outcome'], 'NOT_APPLICABLE')

    def test_known_violation_and_optional_unsupported_keep_honest_summary(self):
        graph = self.graph('(accept p)')
        unsupported = self.graph(requirement='(fixed-unknown p)')['constraints'][0]
        unsupported['id'] = 'unsupported'
        graph['constraints'].append(unsupported)
        result = evaluate_constraints(graph)
        self.assertEqual(result['outcome'], 'FAIL')
        self.assertFalse(result['complete'])
        graph['statuses'][0]['value'] = 'uncommitted'
        self.assertEqual(evaluate_constraints(graph)['outcome'], 'INDETERMINATE')
        unsupported['strength'] = 'optional'
        result = evaluate_constraints(graph)
        self.assertEqual(result['outcome'], 'PASS')
        self.assertFalse(result['complete'])

    def test_invalid_inheritance_cannot_produce_a_pass(self):
        graph = canonicalize_text('''(fom demo (subgraph p (fact))
          (scope s {:inherits-status-from s :inherit-mode :overlay})
          (constraint c (unknown p {:scope s})))''')
        self.assertEqual(evaluate_constraints(graph)['outcome'], 'ERROR')

    def test_cli_exit_codes_distinguish_pass_fail_and_incomplete(self):
        with tempfile.TemporaryDirectory() as directory:
            unsupported = Path(directory) / 'unsupported.fom'
            unsupported.write_text('(fom demo (node n) (constraint c (fixed-unknown n)))')
            cases = (
                ([str(FIXTURES / 'source.fom')], 0, 'PASS'),
                ([str(FIXTURES / 'source.fom'), str(FIXTURES / 'corrupted.fom')], 1, 'FAIL'),
                ([str(unsupported)], 2, 'INDETERMINATE'),
            )
            for args, expected_code, expected_outcome in cases:
                with self.subTest(args=args):
                    output = io.StringIO()
                    with contextlib.redirect_stdout(output):
                        code = main(['evaluate', *args])
                    self.assertEqual(code, expected_code)
                    self.assertEqual(json.loads(output.getvalue())['outcome'], expected_outcome)
