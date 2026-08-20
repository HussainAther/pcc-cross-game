# Cross-game Chaos measurement benchmark protocol

## Purpose

Compare frozen Chaos-related evidence from Poker, Liar's Dice, and repeated RPS without forcing a universal scalar score or retuning any source experiment.

## Frozen cross-game requirements

The benchmark separates five questions:

1. Does raw unpredictability/surprisal carry a Chaos-related signal?
2. Is an independent value/performance guardrail present and supported?
3. Is there an explicit exploitability or plausibility guardrail?
4. Does the candidate recover the engineered Chaos manipulation in both independent families?
5. Can the observed behavior uniquely identify latent strategic intent?

These are not interchangeable. A game may confirm a guardrail while failing construct recovery.

## RPS falsification rule

The v0.2 RPS definition is frozen before evaluation. Effective unpredictability is first-order conditional entropy multiplied by a performance-adequacy term derived from fixed-marginal and online first-order exploitability. Iid-neutral RPS is retained as a legitimate counterexample. If it remains at least as effective as engineered Chaos, the result is an identifiability limit rather than a reason to retune the score.

## Cross-game interpretation

The benchmark may support portable **requirements** even when no single portable scalar exists. In particular, high randomness alone is not sufficient evidence for Chaos; value preservation, resistance to exploitation, or another independent adequacy constraint is required before unpredictability can be interpreted strategically.
