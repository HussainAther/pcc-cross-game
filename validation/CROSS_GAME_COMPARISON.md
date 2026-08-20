# PCC Cross-Game Evidence Matrix

This report compares frozen synthetic evidence without assuming that poker-specific topology or measurements transfer to Liar's Dice.

| Dimension | Poker | Liar's Dice |
|---|---|---|
| Balance | confirmed: engineered balanced cycle under the poker-specific frozen protocol | failed: all pairwise matchups competitive in two independent policy families |
| Pressure observational construct | confirmed (pressure_exposure, predicted_fold_probability) | unresolved (none) |
| Control observational construct | unresolved (none) | unresolved (none) |
| Chaos observational construct | unresolved (none) | unresolved (none) |

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
- **Pressure has cross-family observational support only in poker so far** — supported. Poker selected two invariant Pressure components; Liar's Dice has not yet run construct recovery.
- **Chaos measurement is not yet cross-game validated** — supported. Poker effective-Chaos construct gate failed and Liar's Dice has only mechanism diagnostics, not construct recovery.

## Guardrails

- Do not infer human psychological states from synthetic-agent labels.
- Do not require a rock-paper-scissors cycle outside the game-specific protocol that defined it.
- Mechanism confirmation and observational construct recovery are distinct evidence classes.
- Missing evidence is reported as unresolved, not imputed from another game.
