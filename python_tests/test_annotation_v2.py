import copy
import json
import tomllib
import unittest

from experiments.annotation_v2.prepare import CORPUS, HERE, build_packets, prepare, validate_proposal


class AnnotationV2Tests(unittest.TestCase):
    def setUp(self):
        self.corpus = tomllib.loads(CORPUS.read_text(encoding='utf-8'))['case']
        self.proposal = tomllib.loads((HERE / 'commitments.toml').read_text(encoding='utf-8'))

    def test_source_evidence_and_complete_case_coverage(self):
        validate_proposal(self.proposal, self.corpus)
        self.assertEqual(len(self.proposal['case']), 10)

    def test_unknown_evidence_and_duplicate_requirements_are_rejected(self):
        for corrupt in ('evidence', 'duplicate'):
            proposal = copy.deepcopy(self.proposal)
            rows = proposal['case'][0]['requirements']
            if corrupt == 'evidence':
                rows[0]['evidence'] = ['This is not in the source.']
            else:
                rows.append(copy.deepcopy(rows[0]))
            with self.assertRaises(ValueError):
                validate_proposal(proposal, self.corpus)

    def test_designer_fields_never_flow_into_blind_packet(self):
        packet, response, key = build_packets(self.corpus, self.proposal['translation_policy'])
        altered = copy.deepcopy(self.corpus)
        for case in altered:
            for field in ('valid', 'corrupted', 'note', 'expected_dimensions', 'secret_hint'):
                case[field] = 'LEAK_SENTINEL'
        again, _, _ = build_packets(altered, self.proposal['translation_policy'])
        self.assertEqual(packet, again)
        self.assertNotIn('LEAK_SENTINEL', json.dumps(again))
        for item in packet['items']:
            self.assertEqual(set(item), {'id', 'source', 'source_language', 'target_language'})
        source_by_id = {c['id']: c['source'] for c in self.corpus}
        mapping = {m['blind_id']: m['source_id'] for m in key['mapping']}
        self.assertEqual(len(mapping), 10)
        for item in packet['items']:
            self.assertEqual(item['source'], source_by_id[mapping[item['id']]])
        self.assertEqual([i['id'] for i in packet['items']], [i['id'] for i in response['items']])

    def test_no_fake_annotations_or_timings(self):
        _, response, _ = build_packets(self.corpus, self.proposal['translation_policy'])
        self.assertIsNone(response['annotator'])
        for item in response['items']:
            self.assertEqual(item['commitments'], [])
            self.assertIsNone(item['elapsed_seconds'])

    def test_checked_in_packets_are_reproducible(self):
        for name, expected in prepare().items():
            actual = json.loads((HERE / name).read_text(encoding='utf-8'))
            self.assertEqual(actual, expected)
