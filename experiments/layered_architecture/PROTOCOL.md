# Layered architecture pilot: protocol v1

Frozen before authoring layered fixtures or running the comparison.
Baseline: d21b3ff5e92b1746d2c9d9c6b2b24612a0f95854.

Question: can ordinary content and static speaker commitments live in a
separate carrier while FoM retains preservation and reader-state controls?
This tests ownership separation, not superiority or UMR conformance.

## Inputs and controls

- Audit all 10 original post-freeze corpus cases without changing their text.
- Run the 7 existing gold source/corruption pairs with frozen expected labels.
- Author a small typed JSON content carrier and overlay by hand, using those
  existing annotations as visible references. This is not blind annotation.
- Give each layer sole ownership of its records; overlays reference carrier
  objects rather than copying their predicate/argument structures.
- Carrier owns entities, predicate/argument content, reports, and ordinary
  static epistemic commitments. Overlay owns attention, evidence-route links,
  disclosure checkpoints, fixed-unknown requirements, and coactivation.
- No per-case conditionals or expected labels in the adapter. The adapter must
  know only the supported schema, not case IDs or corruption outcomes.
- Lower carrier + overlay to existing FoM input and use the unchanged diff
  engine. Label parity tests adapter expressiveness, not independent detection.
- Also run carrier-only ablation. Absence of a finding means the selected
  carrier projection lacks that signal, not that UMR necessarily lacks it.
- Include source-self negative controls and invalid cross-layer reference
  controls. Source-self is not a valid-paraphrase false-positive study.

## Measurements fixed in advance

For each pair report the expected dimension/status hit in standalone,
layered, and carrier-only modes; full dimension/status signatures; source-self
findings; source representation record counts by owner; and serialized bytes.
Count carrier entities, propositions, predicates, relations, and commitments;
count corresponding overlay records separately. Report total layer size,
not only a smaller overlay. Serialized byte comparison is format-dependent.

Audit uncovered source details, cross-layer dependencies, and carrier/overlay
boundary tensions for all 10 cases. Do not calculate precision/recall for
unlabeled extra findings, unimplemented dimensions, or missing gold pairs.

## Decision rule

A feasibility pass requires all 7 frozen target findings to survive lowering,
no source-self findings, and no duplicated semantic records across layers.
A failed target is an explicit counterexample to this prototype boundary.
Feasibility alone does not select an architecture: automatic lowering and a
shared diff engine make detection parity an engineering property.

Prefer layering only after it also reduces annotation burden without worse
independent agreement. Annotation time and independent agreement are **not
measured** in this single-author pilot. A smaller overlay alone is insufficient.
UMR conformance, independent extraction, translated-text false positives,
LLM/embedding baselines, and the 3 missing gold pairs remain separate gates.

## Prior-art boundary

The UMR document schema already models cognizer/modal commitment and attributed
speech, so those must not be assigned to FoM merely to improve the ablation.
Receiver disclosure order is kept distinct from event time.

Sources checked 2026-09-28:
- https://umr4nlp.github.io/web/UMRSchemaPages/Document-Level-Graph.html
- https://aclanthology.org/2024.lrec-main.229/

This carrier is an experiment-specific semantic graph, not a UMR annotation.
No UMR role, word-sense, modality, or syntax conformance is claimed.
