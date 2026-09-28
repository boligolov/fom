import copy
import json
import unittest

from experiments.layered_architecture.adapter import lower
from experiments.layered_architecture.fixtures import CASES
from experiments.layered_architecture.run import HERE, run


class LayeredArchitectureTests(unittest.TestCase):
    def test_frozen_targets_survive_and_self_controls_are_empty(self):
        result = run()
        self.assertEqual(result['executable_cases'], 7)
        self.assertEqual(result['totals']['standalone'], 7)
        self.assertEqual(result['totals']['layered'], 7)
        for row in result['rows']:
            with self.subTest(case=row['case']):
                self.assertEqual(row['signatures']['standalone'], row['signatures']['layered'])
                self.assertTrue(all(not findings for findings in row['self_controls'].values()))
                counts = row['source_records']
                self.assertEqual(counts['layered_total'], counts['carrier'] + counts['overlay'])

    def test_static_commitment_and_attribution_survive_carrier_ablation(self):
        rows = run()['rows']
        retained = {r['case'] for r in rows if r['hits']['carrier_only']}
        self.assertEqual(retained, {'source-attribution', 'uncertain-train'})

    def test_report_is_reproducible(self):
        expected = json.loads((HERE / 'results.json').read_text(encoding='utf-8'))
        self.assertEqual(run(), expected)

    def test_dangling_overlay_reference_is_rejected(self):
        doc = copy.deepcopy(CASES[4]['source'])
        doc['overlay']['constraints'][0]['targets'].append('missing')
        with self.assertRaisesRegex(ValueError, 'unresolved'):
            lower(doc)

    def test_double_ownership_is_rejected(self):
        doc = copy.deepcopy(CASES[0]['source'])
        doc['overlay']['entities']['umbrella'] = 'object'
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            lower(doc)

    def test_carrier_cannot_depend_on_overlay(self):
        doc = copy.deepcopy(CASES[3]['source'])
        doc['carrier']['relations'].append({'id': 'leak', 'predicate': 'depends', 'roles': {'target': {'ref': 'initial-reading'}}})
        with self.assertRaisesRegex(ValueError, 'unresolved'):
            lower(doc)

    def test_unknown_fields_and_controls_are_not_silently_ignored(self):
        doc = copy.deepcopy(CASES[0]['source'])
        doc['carrier']['new_semantics'] = []
        with self.assertRaises(ValueError):
            lower(doc)
        doc = copy.deepcopy(CASES[0]['source'])
        doc['overlay']['constraints'][0]['kind'] = 'unimplemented'
        with self.assertRaises(ValueError):
            lower(doc)

    def test_lowering_does_not_mutate_inputs(self):
        original = copy.deepcopy(CASES)
        for case in CASES:
            for role in ('source', 'candidate'):
                lower(case[role])
        self.assertEqual(CASES, original)
