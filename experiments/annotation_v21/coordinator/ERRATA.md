# Author errata and unresolved issues

This is coordinator-only material. Do not distribute it with the blind packet.
The version 2.0 proposal, packet, corpus and raw responses are retained unchanged.

## E01: source category narrowing

Affected proposal: `annotation_v2/commitments.toml`, case `unknown-owner`,
requirement `location-wetness`. Its claim currently says bus stop. The source
`На остановке лежал мокрый зонт.` does not specify bus rather than tram or
another stop. Both first-run annotators identified the narrowing independently.

Corrected proposed claim for future gold: **A wet umbrella lay at a stop.**
No new fact about transport type is supplied. The old English candidate and
the gold location label also contain this narrowing; they remain historical
fixtures, not automatically approved full-text translations. Do not silently
substitute the corrected claim into already reported pilot metrics.

## E02: preservation obligation boundary remains open

The first run disagreed on the required flag for inferred language/tongue
interaction. Both recognized it. Version 2.1 clarifies the general meaning
of preservation obligations without providing a verdict on this or any case.
No annotated answer is changed from optional to required by schema migration.
External review must judge the feature afresh and explain the object and basis
of any preservation obligation. A different answer after clarification is not
by itself evidence of improvement; both model and instructions may differ.

## E03: corridor attachment

The relation of the passer-by to the corridor can be described without forcing
speech location versus origin. Retain the alternative if material. This is a
source attachment boundary, not license to invent an institutional setting.
