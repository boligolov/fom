"""Prepare blind-at-delivery packets; never dispatch or fabricate annotations."""
import hashlib
import json
from pathlib import Path
import random
import tomllib

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CORPUS = ROOT / 'experiments/translation-retelling/corpus/cases.toml'


def digest(text):
    return hashlib.sha256(text.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def validate_proposal(proposal, corpus):
    sources = {c['id']: c['source'] for c in corpus}
    cases = proposal['case']
    if len(cases) != len(sources) or {c['id'] for c in cases} != set(sources):
        raise ValueError('proposal must cover each source case exactly once')
    for case in cases:
        seen = set()
        if not case['requirements'] or not case['do_not_infer'] or not case['open_questions']:
            raise ValueError('missing requirements or uncertainty boundaries')
        for requirement in case['requirements']:
            if requirement['key'] in seen:
                raise ValueError('duplicate requirement key')
            seen.add(requirement['key'])
            if requirement['basis'] not in ('text', 'policy'):
                raise ValueError('unknown requirement basis')
            if not requirement['evidence'] or any(
                not quote or quote not in sources[case['id']] for quote in requirement['evidence']
            ):
                raise ValueError('evidence must quote the actual source')


def build_packets(corpus, translation_policy):
    order = list(corpus)
    random.Random(20261001).shuffle(order)
    packet = {
        'version': '2.0',
        'task': 'Independently annotate the semantic commitments of each Russian source for a faithful English translation. No additional scenario facts are supplied. General competent Russian/English language knowledge is allowed; distinguish defeasible inference from assertion.',
        'translation_policy': translation_policy,
        'instructions': [
            'Pass A only: describe commitments before choosing graph representation. Read only this packet and the empty response template, not the project repository, designer annotations, candidate translations, labels, or other annotators.',
            'For each commitment give an exact supporting source quote, scope/attribution, explicit versus inferred status, and whether preservation is required under the task policy. Distinguish task policy from source assertion.',
            'Record unresolved references, alternative readings, and disagreements. Do not infer that every example has a special phenomenon. Do not resolve missing facts using plausibility.',
            'Use free text; do not force meanings into a fixed ontology. If you cannot decide, explain why. Do not generate a graph in this pass.',
            'Record actual elapsed annotation time and your declared annotator identity/model version and prior exposure; leave unknown measurements null. Do not estimate another annotator’s time or results.',
        ],
        'items': [],
    }
    response = {'version': '2.0', 'annotator': None, 'model_or_background': None,
                'prior_exposure': None, 'items': []}
    key = {'version': '2.0', 'mapping': []}
    for index, case in enumerate(order, 1):
        blind_id = f'P{index:02d}'
        packet['items'].append({'id': blind_id, 'source_language': case['source_language'],
                                'target_language': case['target_language'], 'source': case['source']})
        response['items'].append({'id': blind_id, 'summary': None, 'commitments': [],
                                  'unresolved': [], 'alternatives': [], 'policy_assumptions': [],
                                  'elapsed_seconds': None, 'notes': None})
        key['mapping'].append({'blind_id': blind_id, 'source_id': case['id'],
                               'source_sha256': digest(case['source'])})
    return packet, response, key


def prepare():
    corpus_text = CORPUS.read_text(encoding='utf-8')
    proposal_text = (HERE / 'commitments.toml').read_text(encoding='utf-8')
    proposal = tomllib.loads(proposal_text)
    corpus = tomllib.loads(corpus_text)['case']
    validate_proposal(proposal, corpus)
    packet, response, key = build_packets(corpus, proposal['translation_policy'])
    key.update(corpus_sha256=digest(corpus_text), proposal_sha256=digest(proposal_text),
               packet_sha256=digest(json.dumps(packet, ensure_ascii=False, sort_keys=True)))
    return {'blind/packet.json': packet, 'blind/response-template.json': response,
            'coordinator/manifest.json': key}


if __name__ == '__main__':
    for name, content in prepare().items():
        path = HERE / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(content, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Prepared 10 blind source items and empty responses; no annotations collected.')
