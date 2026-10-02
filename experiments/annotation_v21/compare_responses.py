"""Audit manual object alignment, without computing semantic agreement."""
import json

from experiments.annotation_v21.prepare import HERE
from experiments.annotation_v2.prepare import digest
from experiments.annotation_v21.review_response import review

RESPONSES = {'terra': 'annotator-terra.json', 'fresh': 'annotator-fresh.json'}


def validate_ledger(ledger, responses):
    errors = []
    expected = {i['id'] for i in responses['terra']['items']}
    rows = ledger['items']
    if len(rows) != len(expected) or {r['id'] for r in rows} != expected:
        errors.append('ledger must cover each source once')
    for row in rows:
        if not row.get('finding') or not row.get('disposition'):
            errors.append(row['id'] + ': missing review')
        for name, response in responses.items():
            item = next((i for i in response['items'] if i['id'] == row['id']), None)
            if item is None:
                errors.append(row['id'] + ': unknown item')
                continue
            valid = {c['id'] for c in item['commitments']}
            cited = set()
            for group in row['alignments']:
                refs = group.get(name + '_refs', [])
                cited.update(refs)
                if not set(refs) <= valid:
                    errors.append(row['id'] + ': unknown ' + name + ' reference')
                if not group.get('object') or not group.get('relation'):
                    errors.append(row['id'] + ': incomplete alignment')
            if cited != valid:
                errors.append(row['id'] + ': uncited ' + name + ' commitments')
    return errors


def compare():
    reports = {name: review(path) for name, path in RESPONSES.items()}
    responses = {name: json.loads((HERE / 'responses' / path).read_text(encoding='utf-8'))
                 for name, path in RESPONSES.items()}
    ledger_text = (HERE / 'coordinator/alignment-03.json').read_text(encoding='utf-8')
    ledger = json.loads(ledger_text)
    return dict(run='03', delivery=reports,
                ledger_sha256=digest(ledger_text),
                ledger_errors=validate_ledger(ledger, responses),
                scope='Same frozen packet; manual object alignment; no agreement score or adjudication.')


if __name__ == '__main__':
    result = compare()
    (HERE / 'coordinator/comparison-report-03.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(bool(result['ledger_errors'] or any(
        r['validation_errors'] for r in result['delivery'].values())))
