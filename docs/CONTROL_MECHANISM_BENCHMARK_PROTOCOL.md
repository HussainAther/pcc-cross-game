# Cross-Game Control Mechanism Benchmark Protocol

## Question

Why has observational **Control** been the least portable PCC axis across Poker, Liar's Dice, and repeated RPS?

This benchmark does **not** invent another Control score. It decomposes Control into four mechanism classes that can be read from already-frozen synthetic experiments:

1. history/context use;
2. predictive gain;
3. counterfactual value;
4. timing/intervention sensitivity.

## Evidence rule

Each cell is derived only from a frozen source artifact. `confirmed` requires the source experiment's relevant preregistered checks to pass across its independent families where family replication exists. `partial` denotes mixed/non-invariant evidence. `failed` denotes a measured mechanism that failed its frozen recovery criterion. `unresolved` means no qualifying frozen experiment exists. `not-applicable` means the current game/protocol lacks the structural analogue.

No source policy, threshold, observable, or frozen result is changed by this benchmark.

## Interpretation boundary

The benchmark tests whether Control behaves more like a portable scalar observable or a family of game-conditioned mechanisms. It cannot establish psychological Control in human players and does not modify PCC Poker's v0.8.0 human measurement contract.
