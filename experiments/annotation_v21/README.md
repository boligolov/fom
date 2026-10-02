# Pass A version 2.1: source status and preservation are separate

This neutral clarification follows a real required-flag disagreement in v2.0.
It does not change the sources, translation policy, item order, or old results.
It does not tell annotators which case should be required. Author corrections
and known disputes live only in `coordinator/ERRATA.md`.

Each commitment now has independent fields:

- `source_status`: explicit, backgrounded, inferred, policy, or unresolved;
- `scope`: attribution/perspective in free text;
- `preservation.decision`: required, optional, or unresolved;
- `preservation.object`: the fact, attribution, available reading, form/order,
  or other supported feature to retain;
- `preservation.rationale`: why the source or task policy warrants that choice.

An inferred reading may be required to remain available without its conclusion
being asserted true. It may also be merely optional. The schema accepts both;
evidence and argument, not a hard-coded mapping, decide. Unresolved is a valid
answer. Old binary required flags are never converted automatically.

Send only `blind/packet.json` and `blind/response-template.json` to an annotator
who has not seen prior answers or this repository. The repository is public:
blindness is a delivery/context protocol, not technical secrecy. Keep actual
model identity, prior exposure and null timings when not measured.

Reproduce with `python -m experiments.annotation_v21.prepare`.
The validator checks schema and evidence only; it does not score meaning.
Independent cross-model results and any adjudication belong in a separately
recorded collection run. A new model plus changed instructions confounds the
two effects; do not claim that a changed answer proves the guide improved.

Run 02 collected one response with requested dispatch model GPT-5.6-terra.
See [protocol](coordinator/RUN-02.md) and [qualitative results](coordinator/RESULTS-02.md).
Reproduce delivery checks with `python -m experiments.annotation_v21.review_response`.
The obligation boundary remains open; this is not adjudicated gold.
