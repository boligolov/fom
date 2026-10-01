"""Validate annotation delivery, not semantic correctness or agreement."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def validate_response(response, packet):
    errors = []
    sources = {item['id']: item['source'] for item in packet['items']}
    items = response.get('items', [])
    identifiers = [item.get('id') for item in items]
    if len(identifiers) != len(set(identifiers)) or set(identifiers) != set(sources):
        errors.append('response must cover each packet item exactly once')
    for field in ('annotator', 'model_or_background', 'prior_exposure'):
        if not response.get(field):
            errors.append(f'missing declaration: {field}')
    for item in items:
        label = item.get('id')
        if label not in sources:
            continue
        if not item.get('summary') or not item.get('commitments'):
            errors.append(f'{label}: missing summary or commitments')
        timing = item.get('elapsed_seconds')
        if timing is not None and (type(timing) not in (int, float) or timing < 0):
            errors.append(f'{label}: invalid elapsed_seconds')
        for field in ('unresolved', 'alternatives', 'policy_assumptions'):
            if not isinstance(item.get(field), list):
                errors.append(f'{label}: {field} must be a list')
        seen = set()
        for commitment in item.get('commitments', []):
            cid = commitment.get('id')
            if not cid or cid in seen:
                errors.append(f'{label}: missing or duplicate commitment id')
            seen.add(cid)
            if not commitment.get('claim') or not commitment.get('scope'):
                errors.append(f'{label}/{cid}: missing claim or scope')
            if commitment.get('status') not in ('explicit', 'inferred', 'policy'):
                errors.append(f'{label}/{cid}: unknown status')
            if type(commitment.get('required')) is not bool:
                errors.append(f'{label}/{cid}: required must be boolean')
            evidence = commitment.get('evidence')
            if not isinstance(evidence, list) or not evidence or any(
                not isinstance(quote, str) or not quote or quote not in sources[label] for quote in evidence
            ):
                errors.append(f'{label}/{cid}: evidence must quote the source')
    return errors


def file_hash(path):
    return hashlib.sha256(path.read_text(encoding='utf-8').replace('\r\n', '\n').encode('utf-8')).hexdigest()


def delivery_report():
    packet_path = HERE / 'blind/packet.json'
    packet = json.loads(packet_path.read_text(encoding='utf-8'))
    results = []
    for label in ('annotator-a', 'annotator-b'):
        path = HERE / 'responses' / (label + '.json')
        response = json.loads(path.read_text(encoding='utf-8'))
        results.append({'response': path.name, 'sha256_lf_utf8': file_hash(path),
                        'errors': validate_response(response, packet),
                        'items': len(response['items']),
                        'commitments': sum(len(i['commitments']) for i in response['items']),
                        'measured_items': sum(i['elapsed_seconds'] is not None for i in response['items'])})
    return {'packet_sha256_lf_utf8': file_hash(packet_path), 'responses': results,
            'semantic_agreement_measured_by_this_script': False}


if __name__ == '__main__':
    report = delivery_report()
    (HERE / 'coordinator/delivery-report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    raise SystemExit(1 if any(row['errors'] for row in report['responses']) else 0)
