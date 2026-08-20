# PCC Cross-Game Evidence Matrix

This report compares frozen synthetic evidence without assuming that poker-specific topology or measurements transfer to Liar's Dice.

| Dimension | Poker | Liar's Dice |
|---|---|---|
| Balance | confirmed: engineered balanced cycle under the poker-specific frozen protocol | failed: all pairwise matchups competitive in two independent policy families |
| Pressure observational construct | confirmed (pressure_exposure, predicted_fold_probability) | partial (public commitment/escalation score) |
| Control observational construct | unresolved (none) | failed (conditional mutual information between public opponent-profile regime and action, controlling for current-bid truth-probability bin) |
| Chaos observational construct | unresolved (none) | confirmed (public-state-conditioned action entropy multiplied by an independent aggregate performance-adequacy floor) |

## Mechanism evidence

### poker
- **control-pressure contextual mechanism** — confirmed. engineered synthetic poker agents
- **contextual Control observable** — partial. positive/discriminant in both families but not family-invariant in strength
- **effective Chaos construct** — failed. frozen construct-validation gate

### liars-dice
- **Control-vs-Chaos challenge timing** — confirmed. replicated across both independent Liar's Dice policy families
- **Chaos bid-plausibility cost** — confirmed. replicated across both independent Liar's Dice policy families
- **history dependence** — partial. family-specific rather than universal

## Cross-game findings

- **game topology is not invariant** — supported. Poker's frozen engineered cycle passes, whereas Liar's Dice pairwise competitiveness fails because Control exceeds Chaos in both families.
- **context/history effects are implementation-sensitive** — supported. Poker contextual Control strength is not family-invariant; Liar's Dice history dependence appears in one policy family but not the other.
- **construct recoverability is game-dependent** — supported. Poker's conservative invariant panel supports Pressure but not Control/Chaos, while Liar's Dice cross-family recovery confirms Chaos, only partially recovers Pressure, and fails Control.
- **Pressure evidence is currently stronger in poker** — supported. Poker has two cross-family invariant Pressure components; Liar's Dice Pressure passes recovery in only one of two independent families.
- **Chaos evidence is currently stronger in Liar's Dice** — supported. Liar's Dice Chaos passes all preregistered recovery checks in both families, while Poker's frozen effective-Chaos construct gate failed.
- **Control remains the hardest invariant observational axis** — supported. Poker has mechanism evidence but no family-invariant Control observable; Liar's Dice Control fails preregistered recovery in both families.

## Guardrails

- Do not infer human psychological states from synthetic-agent labels.
- Do not require a rock-paper-scissors cycle outside the game-specific protocol that defined it.
- Mechanism confirmation and observational construct recovery are distinct evidence classes.
- A cross-family confirmation in one game does not automatically transfer to another game.
- Missing or failed evidence is reported directly, not imputed or repaired from another game.
