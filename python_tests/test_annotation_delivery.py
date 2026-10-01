import copy
import json
import unittest

from experiments.annotation_v2.review_responses import HERE, delivery_report, validate_response


class AnnotationDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.packet = {'items': [{'id': 'P01', 'source': 'The train left.'}]}
        self.response = {
            'annotator': 'test', 'model_or_background': 'synthetic schema test',
            'prior_exposure': 'none', 'items': [{
                'id': 'P01', 'summary': 'Train departure', 'elapsed_seconds': None,
                'unresolved': [], 'alternatives': [], 'policy_assumptions': [],
                'commitments': [{'id': 'C01', 'claim': 'Train departure is stated.',
                                 'evidence': ['The train left.'], 'scope': 'narrator',
                                 'status': 'explicit', 'required': True}],
            }],
        }

    def test_valid_delivery_does_not_assert_semantic_correctness(self):
        self.assertEqual(validate_response(self.response, self.packet), [])

    def test_wrong_quote_missing_case_and_duplicate_ids_are_rejected(self):
        wrong_quote = copy.deepcopy(self.response)
        wrong_quote['items'][0]['commitments'][0]['evidence'] = ['The train arrived.']
        missing_case = copy.deepcopy(self.response)
        missing_case['items'] = []
        duplicate_id = copy.deepcopy(self.response)
        duplicate_id['items'].append(copy.deepcopy(duplicate_id['items'][0]))
        for response in (wrong_quote, missing_case, duplicate_id):
            self.assertTrue(validate_response(response, self.packet))

    def test_uncertain_timings_stay_null_and_bad_types_are_rejected(self):
        response = copy.deepcopy(self.response)
        response['items'][0]['elapsed_seconds'] = 'approximately ten'
        self.assertTrue(validate_response(response, self.packet))
        response['items'][0]['elapsed_seconds'] = None
        response['items'][0]['commitments'][0]['required'] = 'yes'
        self.assertTrue(validate_response(response, self.packet))

    def test_checked_in_raw_responses_and_delivery_hashes(self):
        expected = json.loads((HERE / 'coordinator/delivery-report.json').read_text(encoding='utf-8'))
        actual = delivery_report()
        self.assertEqual(actual, expected)
        self.assertTrue(all(not row['errors'] for row in actual['responses']))
        self.assertFalse(actual['semantic_agreement_measured_by_this_script'])

    def test_review_ledger_covers_packet_and_cites_real_commitments(self):
        ledger = json.loads((HERE / 'coordinator/review-ledger.json').read_text(encoding='utf-8'))
        packet = json.loads((HERE / 'blind/packet.json').read_text(encoding='utf-8'))
        self.assertCountEqual([i['id'] for i in ledger['items']], [i['id'] for i in packet['items']])
        for letter in ('a', 'b'):
            response = json.loads((HERE / f'responses/annotator-{letter}.json').read_text(encoding='utf-8'))
            identifiers = {i['id']: {c['id'] for c in i['commitments']} for i in response['items']}
            for item in ledger['items']:
                self.assertTrue(set(item[f'{letter}_refs']) <= identifiers[item['id']])
                self.assertTrue(set(item['outcomes']) <= {
                    'aligned', 'granularity', 'coverage', 'boundary', 'contradiction', 'unresolved',
                })
