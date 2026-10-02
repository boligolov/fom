"""Reproduce delivery checks; no automated semantic adjudication."""
import json
from collections import Counter

from experiments.annotation_v2.prepare import digest
from experiments.annotation_v21.prepare import HERE, validate_response


def review(response_name='annotator-terra.json'):
    packet_text = (HERE / 'blind/packet.json').read_text(encoding='utf-8')
    packet = json.loads(packet_text)
    response_text = (HERE / 'responses' / response_name).read_text(encoding='utf-8')
    response = json.loads(response_text)
    commitments = [c for item in response['items'] for c in item['commitments']]
    return dict(
        version='2.1',
        response_sha256=digest(response_text),
        packet_sha256=digest(json.dumps(packet, ensure_ascii=False, sort_keys=True)),
        items=len(response['items']), commitments=len(commitments),
        source_status_counts=dict(Counter(c['source_status'] for c in commitments)),
        preservation_counts=dict(Counter(c['preservation']['decision'] for c in commitments)),
        measured_timings=sum(i['elapsed_seconds'] is not None for i in response['items']),
        validation_errors=validate_response(response, packet),
        scope='Schema, exact evidence and delivery checks only; no semantic score.')


if __name__ == '__main__':
    result = review()
    (HERE / 'coordinator/delivery-report.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(bool(result['validation_errors']))
