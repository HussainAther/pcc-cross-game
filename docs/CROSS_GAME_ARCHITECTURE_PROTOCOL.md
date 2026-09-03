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

## Current frozen evidence

Colonel Blotto v1.1.0 is currently the only game with a direct architecture-level frozen result. Its `Control x context` model improves leave-one-agent-out standardized MAE by 15.04% and improves all four behavioral targets. The other four bundled repositories currently provide mechanism/construct summaries but not the disjoint-seed agent-by-context rows required for this model comparison.

Therefore the cross-game claim is **not yet evaluable**.
