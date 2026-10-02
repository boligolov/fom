"""Versioned neutral clarification; v2 packet, proposal and responses stay frozen."""
import json
from pathlib import Path
import tomllib

from experiments.annotation_v2.prepare import CORPUS, build_packets, digest

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent / 'annotation_v2'

CLARIFICATION = [
    'Judge source status and preservation obligation separately. A content claim may be explicit, backgrounded, inferred, or unresolved; a task policy is not a source assertion.',
    'Preservation concerns the realization: identify precisely what must survive. Preserving an inference as available does not assert that its conclusion is true. Conversely, a plausible inference is not automatically required to remain recoverable.',
    'For each commitment report source_status, scope, and preservation with decision (required, optional, or unresolved), object (what would be preserved), and rationale (why that obligation follows from the source or shared task policy). Neither source_status nor decision determines the other.',
    'Use unresolved when the source or task does not settle the preservation obligation. Do not force a binary decision or assume the intended answer from an apparent example type.',
    'Do not strengthen unspecified referents, categories, causes, or institutional facts through ordinary plausibility. Retain the coarsest supported description.',
    'No example-specific answers are provided. These instructions do not require you to find a special phenomenon in each text.',
]


def prepare():
    corpus_text = CORPUS.read_text(encoding='utf-8')
    proposal = tomllib.loads((PREVIOUS / 'commitments.toml').read_text(encoding='utf-8'))
    corpus = tomllib.loads(corpus_text)['case']
    packet, response, manifest = build_packets(corpus, proposal['translation_policy'])
    packet['version'] = response['version'] = manifest['version'] = '2.1'
    packet['instructions'] = [
        text for text in packet['instructions'] if not text.startswith('For each commitment')
    ] + CLARIFICATION
    packet['commitment_fields'] = {
        'id': 'Stable local ID, e.g. C01.',
        'claim': 'Free-text semantic commitment.',
        'evidence': 'Nonempty array of exact source substrings.',
        'scope': 'Whose assertion, report, perspective or task obligation this is.',
        'source_status': ['explicit', 'backgrounded', 'inferred', 'policy', 'unresolved'],
        'preservation': {
            'decision': ['required', 'optional', 'unresolved'],
            'object': 'What exactly must/may remain: a fact, attribution, uncertainty, reading availability, form, order, or another justified feature.',
            'rationale': 'Explain from source evidence or shared task policy; do not equate inferred with optional.',
        },
    }
    manifest.update(corpus_sha256=digest(corpus_text),
                    packet_sha256=digest(json.dumps(packet, ensure_ascii=False, sort_keys=True)),
                    previous_version='2.0',
                    distribution='Only blind packet and response template; no coordinator files or repository history.')
    return {'blind/packet.json': packet, 'blind/response-template.json': response,
            'coordinator/manifest.json': manifest}


def validate_response(response, packet):
    errors = []
    sources = {i['id']: i['source'] for i in packet['items']}
    items = response.get('items', [])
    if response.get('version') != '2.1':
        errors.append('response version must be 2.1; do not reinterpret legacy required flags')
    if len(items) != len(sources) or {i.get('id') for i in items} != set(sources):
        errors.append('each item must be covered once')
    for field in ('annotator', 'model_or_background', 'prior_exposure'):
        if not response.get(field):
            errors.append('missing ' + field)
    for item in items:
        item_id = item.get('id')
        if item_id not in sources:
            continue
        if not item.get('summary') or not item.get('commitments'):
            errors.append(f'{item_id}: empty annotation')
        for field in ('unresolved', 'alternatives', 'policy_assumptions'):
            if not isinstance(item.get(field), list):
                errors.append(f'{item_id}: missing list {field}')
        timing = item.get('elapsed_seconds')
        if timing is not None and (type(timing) not in (int, float) or timing < 0):
            errors.append(f'{item_id}: invalid timing')
        seen = set()
        for c in item.get('commitments', []):
            label = f'{item_id}/{c.get("id")}'
            if not c.get('id') or c['id'] in seen:
                errors.append(label + ': invalid or duplicate commitment ID')
            seen.add(c.get('id'))
            if 'required' in c or 'status' in c:
                errors.append(label + ': legacy fields are not v2.1 decisions')
            if not c.get('claim') or not c.get('scope'):
                errors.append(label + ': missing claim or scope')
            if c.get('source_status') not in packet['commitment_fields']['source_status']:
                errors.append(label + ': invalid source_status')
            p = c.get('preservation', {})
            if not isinstance(p, dict) or p.get('decision') not in ('required', 'optional', 'unresolved') or not p.get('object') or not p.get('rationale'):
                errors.append(label + ': incomplete preservation decision')
            quotes = c.get('evidence')
            if not isinstance(quotes, list) or not quotes or any(not isinstance(q, str) or not q or q not in sources[item_id] for q in quotes):
                errors.append(label + ': evidence must quote source')
    return errors


if __name__ == '__main__':
    for name, content in prepare().items():
        path = HERE / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(content, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Prepared version 2.1, without altering version 2.0 or collecting responses.')
