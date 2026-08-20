## 0.4.0

- Add cross-game Control mechanism benchmark over frozen Poker, Liar's Dice, and RPS evidence.
- Keep missing and structurally unavailable evidence explicit as unresolved/not-applicable.
- Add frozen Poker counterfactual-Control source artifact to bundled provenance.

# Changelog

## 0.3.0

- Add PCC Repeated RPS v0.1.0 as a third frozen comparison environment.
- Add `absent-by-design` as an explicit axis status, distinct from confirmed, failed, partial, and unresolved.
- Record the repeated-RPS Pressure negative control as confirmed without promoting Pressure itself into a construct claim.
- Preserve the repeated-RPS failures of provisional Control recovery and entropy-style Chaos recovery.
- Add cross-game findings that Pressure absence can be measured without hallucination and that naive entropy is not a portable Chaos observable.
- Extend JSON/CSV/Markdown outputs and bundled source provenance to all three games.

## 0.2.0

- Update the frozen Liar's Dice source boundary from v0.3.0 to v0.4.0.
- Add the preregistered factorial construct-recovery result to the comparison schema.
- Classify Liar's Dice Pressure as partial, Control as failed, and Chaos as confirmed across families.
- Add cross-game findings for game-dependent construct recoverability, stronger poker Pressure evidence, stronger Liar's Dice Chaos evidence, and persistent Control difficulty.
- Preserve mechanism evidence and balance evidence as separate evidence classes.
- Add bundled source provenance for the v0.4.0 construct-recovery artifact.

## 0.1.0

- Add read-only adapters for PCC Poker v0.8.0 and PCC Liar's Dice v0.3.0 frozen evidence.
- Add common balance, construct, mechanism, and negative-control schema.
- Preserve game-specific balance criteria instead of requiring a universal cycle.
- Generate JSON, CSV, and Markdown cross-game evidence matrices.

## 0.5.0

- Added RPS v0.2 effective-Chaos falsification evidence.
- Added a cross-game Chaos measurement benchmark.
- Separated raw unpredictability, value/performance guards, exploitability/plausibility guards, construct recovery, and latent-intent identifiability.
- Formalized the cross-game result that randomness alone is insufficient and that no single scalar Chaos measure is yet confirmed across all games.
