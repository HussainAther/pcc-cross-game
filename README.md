# PCC Cross-Game

A neutral comparison layer for frozen synthetic PCC evidence across games.

This repository does **not** define a universal PCC game topology and does not merge the scientific protocols of `pcc-poker` and `pcc-liars-dice`. It compares evidence classes while preserving game-specific failures and asymmetries.

## Current comparison

- **Poker v0.8.0:** engineered balanced cycle confirmed; cross-family invariant Pressure observables supported; Control and Chaos observational axes remain unresolved under the conservative frozen panel.
- **Liar's Dice v0.4.0:** pairwise balance gate failed because Control beats Chaos too strongly in both independent families; challenge timing and Chaos bid-plausibility cost replicate across both families; history dependence is family-specific; frozen construct recovery gives **Pressure = partial, Control = failed, Chaos = confirmed**.

The resulting cross-game picture is deliberately non-symmetric:

- the poker cycle is **not** treated as a universal PCC topology;
- Pressure evidence is currently stronger in poker;
- Chaos recovery is currently stronger in Liar's Dice;
- Control remains the hardest observational axis to recover invariantly;
- context/history effects remain implementation-sensitive.

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

The small frozen validation summaries needed for the matrix are included under `sources/`:

```bash
pcc-cross-game \
  --poker-root sources/pcc-poker-v0.8.0 \
  --liars-root sources/pcc-liars-dice-v0.4.0 \
  --output-dir validation
```

No human poker data are bundled or accessed.
