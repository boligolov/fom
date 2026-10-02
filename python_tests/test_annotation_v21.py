import copy
import json
import unittest

from experiments.annotation_v21.prepare import HERE, PREVIOUS, prepare, validate_response
from experiments.annotation_v21.review_response import review


class AnnotationV21Tests(unittest.TestCase):
    def setUp(self):
        self.artifacts = prepare()
        self.packet = self.artifacts['blind/packet.json']
        self.response = copy.deepcopy(self.artifacts['blind/response-template.json'])
        self.response.update(annotator='synthetic test', model_or_background='fixture', prior_exposure='fixture')
        for item, source in zip(self.response['items'], self.packet['items']):
            item['summary'] = 'Synthetic schema test, not semantic annotation'
            item['commitments'] = [dict(id='C01', claim='fixture', evidence=[source['source']],
                scope='fixture', source_status='inferred', preservation=dict(
                    decision='required', object='available reading', rationale='synthetic test'))]

    def test_sources_order_and_policy_unchanged(self):
        old = json.loads((PREVIOUS / 'blind/packet.json').read_text(encoding='utf-8'))
        self.assertEqual(old['items'], self.packet['items'])
        self.assertEqual(old['translation_policy'], self.packet['translation_policy'])

    def test_reproducible_artifacts(self):
        for name, expected in self.artifacts.items():
            self.assertEqual(json.loads((HERE / name).read_text(encoding='utf-8')), expected)

    def test_status_does_not_determine_obligation(self):
        for status in self.packet['commitment_fields']['source_status']:
            for decision in ('required', 'optional', 'unresolved'):
                with self.subTest(status=status, decision=decision):
                    c = self.response['items'][0]['commitments'][0]
                    c['source_status'] = status
                    c['preservation']['decision'] = decision
                    self.assertEqual(validate_response(self.response, self.packet), [])

    def test_reject_legacy_fields_bad_evidence_and_missing_rationale(self):
        for defect in ('legacy', 'evidence', 'rationale', 'version', 'duplicate'):
            response = copy.deepcopy(self.response)
            c = response['items'][0]['commitments'][0]
            if defect == 'legacy':
                c['required'] = True
            elif defect == 'evidence':
                c['evidence'] = ['NOT A SOURCE QUOTE']
            elif defect == 'rationale':
                del c['preservation']['rationale']
            elif defect == 'version':
                response['version'] = '2.0'
            else:
                response['items'][-1] = copy.deepcopy(response['items'][0])
            with self.subTest(defect=defect):
                self.assertTrue(validate_response(response, self.packet))

    def test_collected_responses_when_present(self):
        for path in (HERE / 'responses').glob('*.json'):
            with self.subTest(response=path.name):
                self.assertEqual(validate_response(json.loads(path.read_text(encoding='utf-8')), self.packet), [])

    def test_delivery_report_reproduces_raw_response(self):
        self.assertEqual(json.loads((HERE / 'coordinator/delivery-report.json').read_text(encoding='utf-8')), review())
