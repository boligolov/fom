# Standalone vs carrier + overlay pilot

- [Protocol fixed before implementation](PROTOCOL.md)
- [Measured results](RESULTS.md)
- [Interpretation, all-ten-case audit, and next decision gate](AUDIT.md)
- [Machine-readable results](results.json)

Run from the repository root:

```sh
python -m experiments.layered_architecture.run
python -m unittest discover -s python_tests -p test_layered_architecture.py
```

`fixtures.py` contains hand-authored JSON-compatible carrier/overlay objects,
with small constructors and explicit corruption edits. It does not read or
partition the FoM gold files. The author did see gold; this is not independent
annotation. `adapter.py` accepts the typed object profile without case-specific
logic and rejects unknown fields, dangling references, and duplicate ownership.
Carrier objects must be valid without importing overlay objects.

`run.py` uses the frozen gold manifest as the label oracle, runs standalone,
layered, and carrier-only paths through the same diff engine, and writes the
two results artifacts. Input hashes normalize line endings to LF and UTF-8
for reproducibility across Windows and CI. Tests verify the checked-in result
as well as invalid references and layer ownership.

The code stays under experiments; it is not a production carrier interface,
a UMR importer, or an independent semantic evaluator. The generic status
evaluator remains separate and has narrower operator support.
