# PCC Cross-Game Evidence Matrix

This report compares frozen synthetic evidence without assuming that topology or measurements transfer unchanged across games.

| Dimension | Poker | Liar's Dice | Repeated RPS | Micro-Fighter |
|---|---|---|---|---|
| Balance/topology | confirmed: engineered balanced cycle under the poker-specific frozen protocol | failed: all pairwise matchups competitive in two independent policy families | not-applicable: Repeated RPS is used as a two-axis Control/Chaos negative-control laboratory; no Pressure topology is defined. | failed: all pairwise synthetic mechanism matchups must lie inside the frozen 30%-70% decisive-win-rate window in both independent families |
| Pressure observational construct | confirmed (pressure_exposure, predicted_fold_probability) | partial (public commitment/escalation score) | absent-by-design (pressure_candidate == 0) | unresolved (none) |
| Control observational construct | unresolved (none) | failed (conditional mutual information between public opponent-profile regime and action, controlling for current-bid truth-probability bin) | failed (control_candidate) | unresolved (none) |
| Chaos observational construct | unresolved (none) | confirmed (public-state-conditioned action entropy multiplied by an independent aggregate performance-adequacy floor) | failed (chaos_candidate) | unresolved (none) |

## Mechanism evidence

### Poker
- **control-pressure contextual mechanism** — confirmed. engineered synthetic poker agents
- **contextual Control observable** — partial. positive/discriminant in both families but not family-invariant in strength
- **effective Chaos construct** — failed. frozen construct-validation gate

### Liar's Dice
- **Control-vs-Chaos challenge timing** — confirmed. replicated across both independent Liar's Dice policy families
- **Chaos bid-plausibility cost** — confirmed. replicated across both independent Liar's Dice policy families
- **history dependence** — partial. family-specific rather than universal

### Repeated RPS
- **Pressure absence negative control** — confirmed. Pressure candidate remains exactly zero in both independently coded families.
- **Control observable recovery** — partial. two-family repeated-RPS recovery test
- **entropy-style Chaos recovery** — failed. negative result: entropy alone does not distinguish strategic unpredictability from iid-uniform randomness

### Micro-Fighter
- **spatial Pressure threat generation** — confirmed. space compression, attack-opportunity generation, and defensive-response forcing replicate across frozen Pressure matchups
- **Control defense-to-counter conversion** — partial. the prospectively justified public counter-window rule improved Family B Pressure-vs-Control but did not clear the frozen competitiveness gate
- **deterministic spatial retreat as Control** — failed. the prospective sustained-threat retreat rule worsened Pressure-vs-Control and is retained as a negative intervention result
- **retreat-backfire decomposition** — confirmed. retreat commonly forfeits initiative, often fails to create distance, invites immediate re-entry, and rarely preserves separation
- **damage conversion sufficiency** — failed. Pressure-generated threat volume does not universally convert into damage or victory; Family A Control is the counterexample

## Cross-game findings

- **game topology is not invariant** — supported. Poker's frozen engineered cycle passes, whereas Liar's Dice pairwise competitiveness fails because Control exceeds Chaos in both families.
- **context/history effects are implementation-sensitive** — supported. Poker contextual Control strength is not family-invariant; Liar's Dice history dependence appears in one policy family but not the other.
- **construct recoverability is game-dependent** — supported. Poker's conservative invariant panel supports Pressure but not Control/Chaos, while Liar's Dice cross-family recovery confirms Chaos, only partially recovers Pressure, and fails Control.
- **Pressure evidence is currently stronger in poker** — supported. Poker has two cross-family invariant Pressure components; Liar's Dice Pressure passes recovery in only one of two independent families.
- **Chaos evidence is currently stronger in Liar's Dice** — supported. Liar's Dice Chaos passes all preregistered recovery checks in both families, while Poker's frozen effective-Chaos construct gate failed.
- **Control remains the hardest invariant observational axis** — supported. Poker has mechanism evidence but no family-invariant Control observable; Liar's Dice Control fails preregistered recovery in both families.
- **Pressure absence is recoverable as a negative control** — supported. Repeated RPS excludes strategic Pressure by design and the Pressure candidate remains exactly zero for neutral, Control-like, and Chaos-like policies in both independent families.
- **naive entropy is not a portable Chaos observable** — supported. Liar's Dice recovers Chaos under its frozen construct protocol, whereas repeated RPS shows that iid-uniform neutral play can be more entropic than the Chaos-like policies.
- **the cross-game framework can represent an absent axis** — supported. RPS Pressure is recorded as absent-by-design rather than failed, unresolved, or confirmed, separating environmental absence from construct evidence.
- **PCC mechanisms can be probed in a spatial non-card environment** — supported. Micro-Fighter reproduces spatial Pressure threat-generation diagnostics and value-sensitive Control intervention effects without cards, dice, hidden information, or wagering.
- **spatial Control is not equivalent to maximizing distance** — supported. The frozen retreat intervention worsens Control while the v0.8 decomposition shows frequent initiative forfeiture, ineffective displacement, rapid Pressure re-entry, and almost no persistent separation.
- **mechanistic support can precede construct recovery** — supported. Micro-Fighter contributes Pressure and Control mechanism evidence while all three observational axes remain unresolved because the competitiveness prerequisite has not passed.

## Guardrails

- Do not infer human psychological states from synthetic-agent labels.
- Do not require a rock-paper-scissors cycle outside the game-specific protocol that defined it.
- Mechanism confirmation and observational construct recovery are distinct evidence classes.
- A cross-family confirmation in one game does not automatically transfer to another game.
- Missing or failed evidence is reported directly, not imputed or repaired from another game.
