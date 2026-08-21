# Cross-Game Chaos Measurement Benchmark

This benchmark compares frozen Chaos-measurement evidence without defining a universal scalar Chaos score.

| Measurement requirement | Poker | Liar's Dice | Repeated RPS | Micro-Fighter |
|---|---|---|---|---|
| Raw Unpredictability Signal | partial | confirmed | failed | unresolved |
| Value Or Performance Guardrail | confirmed | confirmed | confirmed | unresolved |
| Exploitability Or Plausibility Guardrail | unresolved | warning-confirmed | confirmed | unresolved |
| Cross Family Construct Recovery | failed | confirmed | failed | unresolved |
| Latent Intent Identifiability | unresolved | unresolved | not-identifiable | unresolved |

## Cross-game conclusion

- Across poker, Liar's Dice, and RPS, the portable structure is effective unpredictability = game-appropriate unpredictability × independent adequacy. Micro-Fighter remains intentionally unresolved for Chaos until its competitiveness and construct-recovery prerequisites mature.

### Poker

- **raw unpredictability signal** — partial: effective surprisal is positively Chaos-related in both families but fails the frozen off-axis discriminant criterion
- **value or performance guardrail** — confirmed: independent value floor is noninferior in both families and improves the discriminant margin in at least one family
- **exploitability or plausibility guardrail** — unresolved: the frozen poker study uses an independent value floor, not an explicit exploitability probe
- **cross family construct recovery** — failed: frozen effective-Chaos construct criterion is not confirmed across both poker policy families
- **latent intent identifiability** — unresolved: the poker protocol validates behavioral constructs and does not claim latent strategic intent is identifiable from actions alone

### Liar's Dice

- **raw unpredictability signal** — confirmed: public-state-conditioned Chaos candidate passes all preregistered recovery checks in both independent families
- **value or performance guardrail** — confirmed: Chaos candidate includes an independent aggregate performance-adequacy floor and recovers cross-family
- **exploitability or plausibility guardrail** — warning-confirmed: engineered Chaos has lower bid truth-plausibility in both families, showing a replicated value/plausibility cost that the measurement must guard against
- **cross family construct recovery** — confirmed: frozen factorial construct-recovery experiment confirms the Chaos axis in both families
- **latent intent identifiability** — unresolved: behavioral recovery does not establish that the same observed pattern uniquely identifies latent strategic intent

### Repeated RPS

- **raw unpredictability signal** — failed: marginal entropy is approximately maximal for both iid-neutral and engineered Chaos and is therefore non-discriminating
- **value or performance guardrail** — confirmed: conditional entropy weighted by resistance to exploitation passes all frozen falsification checks in both families
- **exploitability or plausibility guardrail** — confirmed: fixed-marginal and online first-order exploiters penalize temporally predictable Chaos policies while leaving iid-neutral nearly unexploitable
- **cross family construct recovery** — failed: engineered Chaos does not exceed iid-neutral effective unpredictability in either family
- **latent intent identifiability** — not-identifiable: iid-uniform RPS is already maximally mixed, value-preserving, and minimally exploitable, so action-only data cannot distinguish strategic mixing intent from equivalent randomness

### Micro-Fighter

- **raw unpredictability signal** — unresolved: Micro-Fighter has not yet run a frozen Chaos construct-recovery or effective-unpredictability benchmark; v0.8 evidence is currently Pressure/Control mechanistic only.
- **value or performance guardrail** — unresolved: Micro-Fighter has not yet run a frozen Chaos construct-recovery or effective-unpredictability benchmark; v0.8 evidence is currently Pressure/Control mechanistic only.
- **exploitability or plausibility guardrail** — unresolved: Micro-Fighter has not yet run a frozen Chaos construct-recovery or effective-unpredictability benchmark; v0.8 evidence is currently Pressure/Control mechanistic only.
- **cross family construct recovery** — unresolved: Micro-Fighter has not yet run a frozen Chaos construct-recovery or effective-unpredictability benchmark; v0.8 evidence is currently Pressure/Control mechanistic only.
- **latent intent identifiability** — unresolved: Micro-Fighter has not yet run a frozen Chaos construct-recovery or effective-unpredictability benchmark; v0.8 evidence is currently Pressure/Control mechanistic only.

## Guardrails

- No source experiment is rerun or retuned by this benchmark.
- A confirmed guardrail is not the same as confirmed latent Chaos construct recovery.
- RPS iid-neutral is treated as a legitimate behavioral counterexample, not relabeled after seeing the result.
- The frozen PCC Poker v0.8.0 human-facing measurement contract is unchanged.
