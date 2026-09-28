"""Run with python -m experiments.layered_architecture.run from repository root."""
import hashlib
import json
from pathlib import Path
import tomllib

from fom.canonical import canonicalize_text
from fom.semantic_diff import diff_texts, nonempty_diff
from .adapter import lower
from .fixtures import CASES

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
GOLD = ROOT / 'experiments/translation-retelling/gold/expected.toml'
CORPUS = ROOT / 'experiments/translation-retelling/corpus/cases.toml'
COLLECTIONS = ('nodes', 'relations', 'subgraphs', 'scopes', 'statuses', 'constraints', 'deltas', 'patterns')


def signature(source, candidate):
    result = nonempty_diff(diff_texts(source, candidate))
    return sorted({dimension + '/' + change['status'] for dimension, changes in result.items() for change in changes})


def records(text):
    graph = canonicalize_text(text)
    return sum(len(graph[name]) for name in COLLECTIONS)


def run():
    gold = tomllib.loads(GOLD.read_text(encoding='utf-8'))['case']
    corpus = tomllib.loads(CORPUS.read_text(encoding='utf-8'))['case']
    fixtures = {c['id']: c for c in CASES}
    if len(fixtures) != len(CASES) or set(fixtures) != {g['name'] for g in gold}:
        raise ValueError('layered fixtures must cover exactly the frozen gold pairs')
    inputs = {GOLD, CORPUS, HERE / 'PROTOCOL.md', HERE / 'fixtures.py', HERE / 'adapter.py', HERE / 'run.py'}
    rows = []
    for expected in gold:
        case = fixtures[expected['name']]
        source_path, candidate_path = ROOT / expected['source'], ROOT / expected['candidate']
        inputs.update((source_path, candidate_path))
        source, candidate = source_path.read_text(encoding='utf-8'), candidate_path.read_text(encoding='utf-8')
        layered_source, layered_candidate = lower(case['source']), lower(case['candidate'])
        carrier_source, carrier_candidate = lower(case['source'], True), lower(case['candidate'], True)
        wanted = expected['dimension'] + '/' + expected['status']
        signatures = {name: signature(a, b) for name, a, b in (
            ('standalone', source, candidate), ('layered', layered_source, layered_candidate),
            ('carrier_only', carrier_source, carrier_candidate))}
        controls = {name: signature(text, text) for name, text in (
            ('standalone', source), ('layered', layered_source), ('carrier_only', carrier_source))}
        total, owned = records(layered_source), records(carrier_source)
        rows.append({
            'case': case['id'], 'expected': wanted,
            'hits': {name: wanted in values for name, values in signatures.items()},
            'signatures': signatures, 'self_controls': controls,
            'source_records': {'standalone': records(source), 'layered_total': total,
                               'carrier': owned, 'overlay': total - owned},
            'source_bytes': {'standalone_fom': len(source.encode('utf-8')),
                             'layered_compact_json': len(json.dumps(case['source'], ensure_ascii=False, separators=(',', ':')).encode('utf-8'))},
        })
    return {
        'protocol': 'v1', 'carrier': 'experiment-specific; not UMR',
        'corpus_cases': len(corpus), 'executable_cases': len(rows),
        'missing_gold': [c['id'] for c in corpus if c['id'] not in fixtures],
        'annotation_time': None, 'independent_agreement': None,
        'totals': {mode: sum(r['hits'][mode] for r in rows) for mode in ('standalone', 'layered', 'carrier_only')},
        'rows': rows,
        'input_sha256_lf_utf8': {str(p.relative_to(ROOT)).replace('\\', '/'): hashlib.sha256(p.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
                         for p in sorted(inputs)},
    }


def render(result):
    lines = ['# Layered architecture pilot: measured results', '',
             'Generated with `python -m experiments.layered_architecture.run`.', '',
             'This is a shared-engine feasibility test, not an independent UMR benchmark.', '',
             '| Case | Standalone hit | Layered hit | Carrier-only hit | A records | Carrier + overlay records |',
             '| --- | --- | --- | --- | --- | --- |']
    for row in result['rows']:
        h, n = row['hits'], row['source_records']
        lines.append(f'| {row["case"]} | {h["standalone"]} | {h["layered"]} | {h["carrier_only"]} | {n["standalone"]} | {n["carrier"]} + {n["overlay"]} |')
    n = len(result['rows'])
    lines += ['', f'Target hits: {result["totals"]}; denominator: {n} gold pairs, not all 10 texts.',
              f'Source-self finding counts: {sum(len(v) for r in result["rows"] for v in r["self_controls"].values())}.',
              '', 'Missing gold pairs: ' + ', '.join(result['missing_gold']) + '.', '',
              'Annotation time and independent agreement: not measured. Full signatures, byte counts, and input hashes are in results.json.', '',
              'Interpretation and source-coverage limitations are in AUDIT.md. Architecture selection remains open.', '']
    return '\n'.join(lines)


if __name__ == '__main__':
    result = run()
    (HERE / 'results.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    (HERE / 'RESULTS.md').write_text(render(result), encoding='utf-8')
    print(render(result))
