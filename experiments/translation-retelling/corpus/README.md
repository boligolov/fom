# Pilot mini-corpus

This directory contains original microtexts created **after** the first annotation guide and validation rules were frozen.

They are not evidence for FoM by themselves.

Their purpose is to provide a fixed target for:

1. independent source annotation;
2. annotation-agreement measurement;
3. good vs deliberately corrupted translation/retelling comparison;
4. baseline comparison.

The corpus is stored in `cases.toml`.

## Important

The supplied `expected_dimensions` are hypotheses for the benchmark designers.

Annotators in a blind agreement study should receive only:

- `source`;
- necessary audience/context information.

They should not receive:

- `valid`;
- `corrupted`;
- `expected_dimensions`;
- `note`.

A later script should materialize blind annotation packets from this file.
