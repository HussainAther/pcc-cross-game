# PCC Cross-Game Architecture Falsification

> Prospective architecture-level comparison. Missing game-native trajectory exports are reported as pending, not failed.

## Hypothesis

Pressure and Chaos behave primarily as comparatively context-stable behavioral dimensions, while Control is expressed primarily through context-dependent modulation.

## Frozen model comparison

- Additive: `behavior ~ Pressure + Control + Chaos + context`
- Control-modulatory: `behavior ~ Pressure + Control + Chaos + context + Control x context`

## Current game status

| Game | Status | Control x context improvement | Primary game-native result |
|---|---|---:|---|
| Poker | pending trajectory export | — | — |
| Liar's Dice | pending trajectory export | — | — |
| Repeated RPS | pending trajectory export | — | — |
| Micro-Fighter | pending trajectory export | — | — |
| Colonel Blotto | evaluated | 15.04% | PASS |

## Current conclusion

**PENDING** — 1/5 games currently have the required frozen architecture-level export.

Colonel Blotto is the first calibrated game-level result: adding `Control x context` reduced leave-one-agent-out standardized MAE by **15.04%** and improved all four prespecified behavioral targets. This does not yet establish cross-game generality.

## Required next exports

Each remaining game should export disjoint-seed agent-by-context rows using its already frozen game-native P/C/Chaos signatures and outcomes. The cross-game repository should fit only the common architecture comparison; it should not redesign game-native measurements.

## Guardrails

- Do not treat missing trajectory exports as negative evidence.
- Do not refit game-native PCC observables to make the cross-game architecture pass.
- A Blotto pass is evidence for Blotto, not proof of cross-game generality.
- Control x context must be compared against Pressure x context and Chaos x context before claiming Control is disproportionately modulatory.
- The final claim requires leave-one-game-out analysis after all five games are evaluable.
