# Run 01: same-model fresh-context Pass A pilot

Date: 2026-10-01. Collection initiated before reading either response.

Two agents received fresh contexts (`fork_turns=none`) and identical task
instructions except label and output filename. They were instructed to read
only `blind/packet.json` and `blind/response-template.json`, not the repository,
author proposal, corpus labels, candidates, or each other's output. No model
override was set; both inherit the parent model configuration. Exact serving
model versions are not independently verified. Shared files are technically
accessible: isolation is by supplied context and instruction, not a security
sandbox. No claim of independent training, model diversity, or human judgment.

Task names: `/root/annotator_a`, `/root/annotator_b`. The additional collection
instruction standardizes commitment fields: local ID, claim, exact evidence
substrings, scope, explicit/inferred/policy status, required boolean. It adds
no case-specific interpretation. Item timings remain null unless actually
measured. No root-agent commentary or author judgments are sent to annotators.

Both raw responses will be retained. File hashes and quote/schema validation
will be recorded by `review_responses.py`. That check measures delivery
integrity, not semantic accuracy. Any correction requires a visible revision
record; the coordinator must not silently rewrite raw answers.

## Review rule set before receiving outputs

The coordinator compares source evidence and both annotations after both are
delivered. The coordinator has seen the author proposal and is not blind;
adjudication is provisional and is not a third independent annotation.

Do not align by commitment count or wording alone. Keep stable references to
both annotators' item/commitment IDs for each reviewed issue. Missing mention
is not rejection. Split commitments can express the same meaning.

Use these qualitative outcomes:
- aligned: compatible commitments on the reviewed issue;
- granularity: same meaning split or elaborated differently;
- coverage: one response explicitly addresses a distinction the other omits;
- boundary: disagreement about assertion/inference/policy or required status;
- contradiction: incompatible commitments about the same source issue;
- unresolved: source/task leaves more than one defensible interpretation.

Review content/reference, attribution, uncertainty, inference, trajectory,
social state, and focus/function/form. A review ledger is diagnostic, not an
exhaustive fixed-unit annotation metric. Do not compute kappa, F1, precision,
or an overall agreement percentage from this selectively matched ledger.
Do not count two same-model responses as satisfying the planned independent
human/different-model study. Do not begin graph encoding before material
source-commitment disputes have an explicit disposition.
