# PCC Cross-Game Architecture Falsification

> Prospective architecture-level comparison using frozen game-native exports. Missing measurements remain explicitly unresolved rather than being backfilled post hoc.

## Hypothesis

Pressure and Chaos behave primarily as comparatively context-stable behavioral dimensions, while Control is expressed primarily through context-dependent modulation.

## Frozen model comparison

- Additive: `behavior ~ Pressure + Control + Chaos + context`
- Control-modulatory: `behavior ~ Pressure + Control + Chaos + context + Control x context`
- Discriminants: matched `Pressure x context` and `Chaos x context` interactions, cross-context rank stability, and leave-one-game-out robustness.

## Game-level results

| Game | Status | P x context | C x context | Chaos x context | Strongest available interaction | Native C-modulation test |
|---|---|---:|---:|---:|---|---|
| Poker | evaluated | 7.93% | -4.09% | 3.92% | pressure | FAIL |
| Liar's Dice | evaluated | 7.69% | 1.56% | 29.83% | chaos | FAIL |
| Repeated RPS | evaluated | 0.00% | 6.56% | 11.14% | chaos | PASS |
| Micro-Fighter | evaluated | 1.29% | 0.76% | -0.97% | pressure | FAIL |
| Colonel Blotto | evaluated | — | 15.04% | — | control* | PASS |

* Colonel Blotto v1.1 froze only the Control interaction comparison; Pressure/Chaos interaction discriminants were not prospectively exported and are not reconstructed here.

## Pooled cross-game result

- Macro-mean `Control x context` improvement: **3.96%** (frozen target: >= 5%).
- Games passing their native Control-modulation threshold: **2/5** (frozen target: >= 4/5).
- Strongest available interactions: **Pressure 2**, **Control 1**, **Chaos 2**, **unknown/incomplete 0**.

## Prespecified criteria

| Criterion | Result | Status |
|---|---|---|
| Pooled C x context improvement >= 5% | 3.96% | **FAIL** |
| C modulation in >= 4/5 games | 2/5 | **FAIL** |
| C interaction strongest in majority | 0 observed; maximum possible 1/5 | **FAIL** |
| P/Chaos rank stability > raw C in majority | Common statistic not present in all exports | **NOT-EVALUABLE-FROM-CURRENT-EXPORTS** |
| Leave-one-game-out universal architecture | survives all folds: False | **FAIL** |

## Leave-one-game-out robustness

| Held-out game | Remaining macro C improvement | Remaining C-pass games | Universal C architecture survives? |
|---|---:|---:|---|
| Poker | 5.98% | 2/4 | NO |
| Liar's Dice | 4.56% | 2/4 | NO |
| Repeated RPS | 3.31% | 1/4 | NO |
| Micro-Fighter | 4.76% | 2/4 | NO |
| Colonel Blotto | 1.19% | 1/4 | NO |

## Final conclusion

**FAILED** — all 5/5 games are evaluable for the primary Control-modulation comparison.

The frozen universal hypothesis is **rejected**. `Control x context` does not achieve the prespecified pooled 5% gain, reaches the game-native threshold in only 2/5 games, and the failure is robust to every leave-one-game-out fold.

The stronger descriptive pattern is **substrate-dependent PCC architecture**: Poker is Pressure-modulatory, Liar's Dice is strongly Chaos-modulatory, repeated RPS supports Control modulation but Chaos is stronger, Micro-Fighter shows only weak interaction gains, and Colonel Blotto strongly supports Control modulation. This is a post-falsification interpretation, not a replacement preregistered success claim.

One prespecified criterion remains **unresolved rather than failed**: the normalized exports do not contain a common cross-context rank-stability statistic for Pressure, Control, and Chaos. Resolving that criterion requires new native exports; it is not necessary to rescue the already-falsified universal Control-modulation hypothesis.

## Guardrails

- Do not treat missing trajectory exports as negative evidence.
- Do not refit game-native PCC observables to make the cross-game architecture pass.
- A game-native pass is evidence for that game, not proof of cross-game generality.
- Control x context must be compared against Pressure x context and Chaos x context before claiming Control is disproportionately modulatory.
- Do not backfill missing cross-context rank-stability statistics from post hoc proxies; obtain new native exports if criterion 4 is to be resolved.
