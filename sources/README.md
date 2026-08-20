# Bundled frozen evidence summaries

This directory contains only the frozen **synthetic validation JSON summaries** needed to reproduce the default cross-game comparison.

- `pcc-poker-v0.8.0/`: copied from the tagged/frozen poker evidence snapshot.
- `pcc-liars-dice-v0.3.0/`: copied from the v0.3 Liar's Dice mechanism snapshot.

No poker hand histories, human records, raw gameplay datasets, or personally identifying data are included.

`PROVENANCE.json` records SHA-256 values for every bundled source summary. These snapshots are inputs; the comparison code must not modify them.
