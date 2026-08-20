# PCC Cross-Game

A neutral comparison layer for frozen synthetic PCC evidence across games.

This repository does **not** define a universal PCC game topology and does not merge the scientific protocols of `pcc-poker`, `pcc-liars-dice`, or `pcc-rps`. It compares evidence classes while preserving game-specific failures, absent dimensions, and asymmetries.

## Current comparison

- **Poker v0.8.0:** engineered balanced cycle confirmed; cross-family invariant Pressure observables supported; Control and Chaos observational axes remain unresolved under the conservative frozen panel.
- **Liar's Dice v0.4.0:** pairwise balance gate failed because Control beats Chaos too strongly in both independent families; frozen construct recovery gives **Pressure = partial, Control = failed, Chaos = confirmed**.
- **Repeated RPS v0.1.0:** Pressure is **absent by design** and its negative control passes in both families; provisional Control recovery is family-specific and naive entropy-style Chaos recovery fails.

The resulting cross-game picture is deliberately non-symmetric:

- the poker cycle is **not** treated as a universal PCC topology;
- Pressure evidence is currently strongest in poker;
- Chaos recovery is currently strongest in Liar's Dice;
- repeated RPS demonstrates that an axis can be absent rather than failed or unresolved;
- naive entropy is not a portable Chaos observable;
- Control remains the hardest observational axis to recover invariantly.

## Run

```bash
python -m pip install -e ".[dev]"
pcc-cross-game \
  --poker-root /path/to/pcc-poker \
  --liars-root /path/to/pcc-liars-dice \
  --rps-root /path/to/pcc-rps \
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
make preflight
```

No human poker data are bundled or accessed.

## Cross-game Control mechanism benchmark

Version 0.4 adds a descriptive benchmark over frozen source results. It separates history/context use, predictive gain, counterfactual value, and timing/intervention sensitivity rather than creating another scalar Control score. See `docs/CONTROL_MECHANISM_BENCHMARK_PROTOCOL.md` and `validation/CONTROL_MECHANISM_BENCHMARK.md`.
