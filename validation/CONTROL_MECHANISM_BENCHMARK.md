# Cross-Game Control Mechanism Benchmark

This benchmark compares frozen synthetic Control evidence without creating a new scalar Control score.

| Mechanism | Poker | Liar's Dice | Repeated RPS |
|---|---|---|---|
| History Or Context Use | partial | partial | unresolved |
| Predictive Gain | partial | failed | partial |
| Counterfactual Value | failed | unresolved | unresolved |
| Timing Or Intervention Sensitivity | confirmed | confirmed | not-applicable |

## Interpretation

- **Single portable Control observable:** false.
- No candidate observational Control signal is confirmed across all three environments; intervention/timing evidence is strongest but is not structurally available in RPS.

### Poker

- **history or context use** — partial: aligned-vs-yoked contextual observable is positive/discriminant in both families but not invariant in strength
- **predictive gain** — partial: public-history conditional action likelihood signal
- **counterfactual value** — failed: frozen counterfactual-control validation
- **timing or intervention sensitivity** — confirmed: round-swapped and context-yoked interventions against Pressure

### Liar's Dice

- **history or context use** — partial: muted opponent-history intervention
- **predictive gain** — failed: frozen Control construct-recovery observable
- **counterfactual value** — unresolved: no frozen counterfactual-value experiment
- **timing or intervention sensitivity** — confirmed: challenge-timing accuracy pathway

### Repeated RPS

- **history or context use** — unresolved: v0.1 negative-control protocol did not isolate history use
- **predictive gain** — partial: Control candidate exceeds iid-neutral baseline
- **counterfactual value** — unresolved: no frozen counterfactual-value experiment
- **timing or intervention sensitivity** — not-applicable: simultaneous RPS actions provide no challenge-timing analogue in v0.1

## Guardrails

- This benchmark is descriptive over frozen synthetic results; it does not rerun or retune source experiments.
- Unmeasured mechanisms remain unresolved rather than being inferred from another game.
- Not-applicable means the game/protocol lacks the relevant structural analogue; it is not a failed Control result.
- Mechanism evidence does not promote any human-facing Control measure in frozen PCC Poker v0.8.0.
