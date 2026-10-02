# Run 03: same-packet comparison

Collection date: 2026-10-02. Before collection, the coordinator dispatched a
fresh agent with `fork_turns=none`, no model override, and instructions to read
only the frozen 2.1 blind packet and empty template. It receives no prior
responses, coordinator results, expected phenomena or author proposal.
Output is `responses/annotator-fresh.json`; missing timings stay null.

The comparator is the already collected requested GPT-5.6-terra response from
Run 02. Both receive exactly the same source order, task policy, field schema
and annotation instructions. The new dispatch inherits the parent model
configuration; exact backend identities are not independently attested.
Describe this as a same-instruction comparison of dispatch configurations,
not verified model-family independence or external human validation.

Repository blindness is by instruction and fresh context, not enforced file
isolation. Exposure statements are self-reports. The coordinator knows earlier
results, and its manual alignment is not blind adjudication.

Compare preservation objects before decisions. Allow one-to-many and absent
row alignments. An omitted inference row is not a rejection, and a required
cue is not automatically equivalent to a required inference. Record textual
boundaries and unresolved obligations; do not produce a raw-row agreement
percentage. Keep original files immutable. The delivery report checks evidence,
hashes, coverage and valid references only, not semantic equivalence.
