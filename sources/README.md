# Bundled frozen sources

These files are exact frozen validation summaries copied from named PCC game release snapshots solely to reproduce cross-game comparisons. No human data are included.

Current bundled sources:

- `pcc-poker-v0.8.0`
- `pcc-liars-dice-v0.5.0`
- `pcc-rps-v0.2.0`
- `pcc-micro-fighter-v1.0.0`
- `pcc-colonel-blotto-v1.1.0`

Colonel Blotto includes the frozen v1.1 Control-modulation result plus the v1.0 learned-agent emergence and the mechanistic Pressure/Chaos results needed to interpret that architecture experiment.

The architecture falsification now includes frozen architecture-level exports for all five games. Poker, Liar's Dice, repeated RPS, and Micro-Fighter provide normalized `control-architecture-export.json` artifacts; Colonel Blotto contributes its frozen v1.1 `control-modulation.json`. The cross-game layer preserves each native measurement contract and does not reconstruct missing discriminants post hoc. In particular, Blotto v1.1 did not prospectively export matched Pressure/Chaos interaction controls, and the common cross-context rank-stability criterion remains unresolved across the five normalized exports.
