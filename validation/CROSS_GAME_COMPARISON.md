# PCC Cross-Game Evidence Matrix

This report compares frozen synthetic evidence without assuming that topology or measurements transfer unchanged across games.

| Dimension | Poker | Liar's Dice | Repeated RPS | Micro-Fighter | Colonel Blotto |
|---|---|---|---|---|---|
| Balance/topology | confirmed: engineered balanced cycle under the poker-specific frozen protocol | failed: all pairwise matchups competitive in two independent policy families | not-applicable: Repeated RPS is used as a two-axis Control/Chaos negative-control laboratory; no Pressure topology is defined. | failed: all pairwise synthetic mechanism matchups must lie inside the frozen 30%-70% decisive-win-rate window in both independent families | not-applicable: no universal dominance cycle is required; Blotto is used for resource-allocation mechanism and learned-agent architecture tests |
| Pressure observational construct | confirmed (pressure_exposure, predicted_fold_probability) | partial (public commitment/escalation score) | absent-by-design (pressure_candidate == 0) | unresolved (none) | confirmed (targeted_leverage, response_constriction) |
| Control observational construct | unresolved (none) | failed (conditional mutual information between public opponent-profile regime and action, controlling for current-bid truth-probability bin) | failed (control_candidate) | unresolved (none) | partial (context_modulation) |
| Chaos observational construct | unresolved (none) | confirmed (public-state-conditioned action entropy multiplied by an independent aggregate performance-adequacy floor) | failed (chaos_candidate) | unresolved (none) | confirmed (guarded_unpredictability, exploit_resistance) |

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
- **effective Chaos resistance to calibrated exploitation** — confirmed. a stronger adaptive exploiter is calibrated only on predictable play, frozen, then effective Chaos preserves substantially more held-out value than predictable or random baselines
- **Chaos is not randomness** — confirmed. the random baseline is more entropic but much less competitively adequate than the effective-Chaos candidate

### Colonel Blotto
- **targeted-leverage Pressure** — confirmed. matched resource-allocation intervention
- **guarded Chaos under held-out exploitation** — confirmed. held-out adaptive exploiter
- **learned-agent low-dimensional PCC-related structure** — partial. independently optimized agents; Pressure and Chaos align strongly with PCs, Control does not form an independent PC3
- **Control as context-dependent modulation** — confirmed. leave-one-agent-out predictive comparison with disjoint signature/outcome seeds

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
- **Chaos is not randomness in spatial combat** — supported. Micro-Fighter's more-entropic random baseline is strategically much worse than the effective-Chaos candidate, and a calibrated held-out exploiter suppresses predictable play while effective Chaos preserves positive value.
- **mechanistic support can precede construct recovery** — supported. Micro-Fighter contributes Pressure, Control, and strong effective-Chaos mechanism evidence while all three observational axes remain unresolved because no frozen cross-family construct-recovery gate has passed.
- **resource-allocation Pressure depends on targeted leverage rather than concentration alone** — supported. Blotto v0.5 falsifies raw concentration while v0.6 shows a 48.0% viable-response reduction when concentration is redirected toward leverage-bearing fronts under matched value and concentration.
- **independently optimized agents can exhibit PCC-related structure without latent PCC generator weights** — supported. Blotto v1.0 learns agents under generic objectives/opponents; Pressure and Chaos align strongly with separate behavioral PCs while Control is stable but not an independent PC3.
- **Control may be better represented as contextual modulation than as an orthogonal axis** — supported-in-blotto. Blotto v1.1 Control x context interactions reduce leave-one-agent-out standardized MAE by 15.04%; cross-game generalization remains pending.

## Guardrails

- Do not infer human psychological states from synthetic-agent labels.
- Do not require a rock-paper-scissors cycle outside the game-specific protocol that defined it.
- Mechanism confirmation and observational construct recovery are distinct evidence classes.
- A cross-family confirmation in one game does not automatically transfer to another game.
- Missing or failed evidence is reported directly, not imputed or repaired from another game.
