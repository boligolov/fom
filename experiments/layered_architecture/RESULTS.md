# Layered architecture pilot: measured results

Generated with `python -m experiments.layered_architecture.run`.

This is a shared-engine feasibility test, not an independent UMR benchmark.

| Case | Standalone hit | Layered hit | Carrier-only hit | A records | Carrier + overlay records |
| --- | --- | --- | --- | --- | --- |
| unknown-owner | True | True | False | 5 | 3 + 2 |
| source-attribution | True | True | True | 8 | 8 + 0 |
| inference-route | True | True | False | 11 | 10 + 1 |
| delayed-reveal | True | True | False | 6 | 2 + 4 |
| common-tongue | True | True | False | 5 | 4 + 1 |
| uncertain-train | True | True | True | 5 | 5 + 0 |
| contrastive-focus | True | True | False | 5 | 3 + 2 |

Target hits: {'standalone': 7, 'layered': 7, 'carrier_only': 2}; denominator: 7 gold pairs, not all 10 texts.
Source-self finding counts: 0.

Missing gold pairs: failed-declaration, conflicting-sources, exact-note.

Annotation time and independent agreement: not measured. Full signatures, byte counts, and input hashes are in results.json.

Interpretation and source-coverage limitations are in AUDIT.md. Architecture selection remains open.
