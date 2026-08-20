# PCC Cross-Game

A neutral comparison layer for frozen synthetic PCC evidence across games.

This repository does **not** define a universal PCC game topology and does not merge the scientific protocols of `pcc-poker` and `pcc-liars-dice`. It makes the current asymmetry explicit: poker has frozen construct-validation evidence, while Liar's Dice is still at the balance/mechanism stage.

## Current comparison

- **Poker:** engineered balanced cycle confirmed; cross-family invariant Pressure observables supported; Control and Chaos observational axes unresolved under the conservative panel.
- **Liar's Dice:** pairwise balance gate failed because Control beats Chaos too strongly in both independent families; challenge timing and Chaos bid-plausibility cost replicate across both families; history dependence is family-specific; construct recovery has not yet been run.

This already supports a useful negative result: **the poker cycle is not treated as a universal PCC topology.**

## Run

```bash
python -m pip install -e ".[dev]"
pcc-cross-game \
  --poker-root /path/to/pcc-poker \
  --liars-root /path/to/pcc-liars-dice \
  --output-dir validation
```

Outputs:

- `validation/cross-game-comparison.json`
- `validation/cross-game-comparison.csv`
- `validation/CROSS_GAME_COMPARISON.md`

See `docs/COMPARISON_CONTRACT.md` for evidence rules.

## Reproduce the bundled comparison

The small frozen validation summaries needed for the published matrix are included under `sources/`:

```bash
pcc-cross-game \
  --poker-root sources/pcc-poker-v0.8.0 \
  --liars-root sources/pcc-liars-dice-v0.3.0 \
  --output-dir validation
```

No human poker data are bundled or accessed.
