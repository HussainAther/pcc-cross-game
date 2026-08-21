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

## Chaos measurement benchmark (v0.5.0)

The cross-game Chaos benchmark uses repeated RPS as a strict falsification laboratory. RPS v0.2 shows that iid-neutral play can be maximally mixed, value-preserving, and minimally exploitable, while structured engineered Chaos can be more exploitable despite equally high marginal entropy.

```bash
make chaos-benchmark
```

The cross-game conclusion is deliberately narrower than a universal Chaos score: **unpredictability needs an independent value/performance or exploitability guardrail**, but the exact scalar is not yet portable across Poker, Liar's Dice, and RPS. See `docs/CHAOS_MEASUREMENT_BENCHMARK_PROTOCOL.md`.

## Control structural template

The v0.6.0 benchmark tests a portable Control structure rather than a universal scalar:

`information uptake -> context alignment -> value-sensitive intervention`

Run:

```bash
make control-template
```

See `docs/CONTROL_STRUCTURAL_TEMPLATE_PROTOCOL.md` and `validation/CONTROL_STRUCTURAL_TEMPLATE.md`.

## Pressure structural template (v0.7.0)

The Pressure benchmark tests a portable structure rather than a universal scalar:

`commitment exposure -> response constriction -> strategic consequence`

Run:

```bash
make pressure-template
```

Poker supports all three stages on frozen synthetic evidence. Liar's Dice confirms commitment exposure and strategic consequence but does not yet contain a separate response-constriction test. Repeated RPS is retained as an absent-by-design Pressure negative control. See `docs/PRESSURE_STRUCTURAL_TEMPLATE_PROTOCOL.md` and `validation/PRESSURE_STRUCTURAL_TEMPLATE.md`.

## v0.8 Pressure response-constriction update

The Pressure structural benchmark now incorporates `pcc-liars-dice` v0.5.0. The missing middle link is no longer untested: matched-state replay supports response constriction in Family B but not Family A. The cross-game Pressure template therefore remains **partial / implementation-sensitive**, not universally confirmed.

## v0.9.0: Micro-Fighter integration

The comparison layer now includes `pcc-micro-fighter` v0.8.0 as a fourth, spatial competitive environment. Micro-Fighter contributes frozen mechanistic evidence for spatial Pressure and value-sensitive Control, but **all three observational construct axes remain unresolved** because its frozen competitiveness prerequisite still fails. This distinction is intentional: mechanism evidence is not construct recovery.

The four environments now play different methodological roles: Poker (rich imperfect information), Liar's Dice (bluff/escalation replication), repeated RPS (minimal negative-control/falsification lab), and Micro-Fighter (spatial threat/initiative lab).
