# Cross-Game Architecture Falsification Protocol

## Question

Does the same structural architecture recur across strategically distinct games: **Pressure and Chaos as comparatively context-stable behavioral dimensions, with Control expressed disproportionately through context-dependent modulation**?

## Games

1. Leduc Poker
2. Liar's Dice
3. Repeated RPS
4. Micro-Fighter
5. Colonel Blotto

No sixth game is added until this five-game architecture test is resolved.

## Measurement rule

Each native game repository owns its PCC observables. The cross-game repository may standardize columns and fit common model forms, but it must not retune the native Pressure, Control, Chaos, context, or outcome definitions after inspecting cross-game results.

Required per-game exports must use disjoint seeds (or an equivalent non-overlapping evaluation split) for signature estimation and outcome measurement.

## Primary model comparison

Additive:

`behavior ~ Pressure + Control + Chaos + context`

Control-modulatory:

`behavior ~ Pressure + Control + Chaos + context + Control x context`

## Discriminant comparisons

The final cross-game test must also fit otherwise matched models adding `Pressure x context` and `Chaos x context`. A generic benefit from interactions is not sufficient evidence that Control is specially modulatory.

## Prespecified cross-game success criteria

1. `Control x context` improves held-out standardized MAE by at least 5% pooled across games.
2. Improvement appears in at least 4 of 5 games.
3. The incremental gain from `Control x context` exceeds the corresponding gain from `Pressure x context` or `Chaos x context` in the majority of games.
4. Pressure and Chaos show higher cross-context rank stability than raw Control expression in the majority of applicable games.
5. The qualitative architecture survives leave-one-game-out analysis.

A missing native trajectory export is **pending**, not failed.

## Final frozen evidence

All five games now provide the required architecture-level export for the primary additive-versus-`Control x context` comparison. The frozen game-native Control-modulation results are:

- Poker: **FAIL**, -4.09% relative improvement.
- Liar's Dice: **FAIL**, +1.56%.
- Repeated RPS: **PASS**, +6.56%.
- Micro-Fighter: **FAIL**, +0.76%.
- Colonel Blotto: **PASS**, +15.04%.

The macro-mean improvement is **3.96%**, below the prespecified 5% threshold, and only **2/5** games pass rather than the required 4/5. The universal Control-dominant modulation architecture is therefore falsified on the frozen panel.

Discriminant interaction exports show substrate dependence: Pressure is strongest in Poker, Chaos is strongest in Liar's Dice and repeated RPS, Micro-Fighter has only weak interaction gains with Pressure slightly largest, and Blotto prospectively exported only the Control interaction. Because the normalized exports do not contain one common cross-context rank-stability statistic for all three axes, criterion 4 remains explicitly unresolved rather than being reconstructed post hoc.

Leave-one-game-out analysis is required in the generated final report and tests whether the universal Control architecture reappears after removing any single substrate.
