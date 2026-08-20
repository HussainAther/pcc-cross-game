# Cross-game comparison contract

`pcc-cross-game` compares **evidence classes**, not raw game scores.

## Rules

1. Each source repository remains authoritative for its own frozen protocol.
2. A poker-specific balanced cycle is not imposed on Liar's Dice or repeated RPS.
3. Mechanism evidence is not promoted into observational construct recovery.
4. Construct status is derived from each source protocol's prespecified checks; thresholds are not harmonized after seeing results.
5. Cross-family confirmation in one game does not imply transfer to another game.
6. Missing evidence is `unresolved`; tested failures remain `failed`; one-family recovery is `partial`.
7. An intentionally unavailable construct is `absent-by-design`, not `failed`, `unresolved`, or `confirmed`.
8. A confirmed negative control means the measurement correctly respects an environmental absence; it is not confirmation of the absent construct.
9. Synthetic policy labels are engineering constructs, not claims about human psychological states.
10. The comparison layer is read-only with respect to source repositories.

## Current source boundary

- PCC Poker: v0.8.0 synthetic-evidence freeze.
- PCC Liar's Dice: v0.4.0 frozen factorial construct-recovery result.
- PCC Repeated RPS: v0.1.0 frozen negative-control result.

The comparison is intentionally asymmetric. Poker currently has the clearest cross-family observational support for Pressure. Liar's Dice has confirmed cross-family recovery for Chaos, partial Pressure recovery, and failed Control recovery. Repeated RPS deliberately removes Pressure and confirms that the Pressure candidate stays absent, while also falsifying naive entropy as a portable Chaos detector. No universal PCC topology or universal measurement panel is inferred from this pattern.
