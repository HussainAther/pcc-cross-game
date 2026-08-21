# Cross-Game Control Structural Template

Proposed portable structure: **information uptake → context alignment → value-sensitive intervention**.

| Stage | Poker | Liar's Dice | Repeated RPS | Micro-Fighter |
|---|---|---|---|---|
| Information Uptake | confirmed | partial | partial | partial |
| Context Alignment | confirmed | partial | unresolved | partial |
| Value Sensitive Intervention | confirmed | confirmed | not-applicable | confirmed |

## Interpretation

- **Overall status:** partial-structural-support.
- Value-sensitive intervention is supported in Poker, Liar's Dice, and Micro-Fighter, while information uptake/context alignment remain implementation-sensitive. Micro-Fighter additionally shows that spatial withdrawal can be value-destroying even when it creates nominal distance.

### Poker

- **information uptake** — confirmed: public-history signal is positively associated with assigned Control in both synthetic families
- **context alignment** — confirmed: aligned public history outperforms yoked/context-destroyed history, although effect magnitude is not cross-family invariant
- **value sensitive intervention** — confirmed: frozen aligned-vs-round-swapped/context-yoked payoff intervention against Pressure

### Liar's Dice

- **information uptake** — partial: muting opponent-history information changes Control advantage in Family B but not Family A
- **context alignment** — partial: history dependence is implementation-specific; no separate aligned-vs-yoked context experiment exists
- **value sensitive intervention** — confirmed: Control challenge timing is more accurate in both independent families and contributes to the Control-over-Chaos advantage

### Repeated RPS

- **information uptake** — partial: Control candidate exceeds iid-neutral only in one independent family
- **context alignment** — unresolved: the frozen RPS protocols do not yet contain an aligned-vs-yoked history intervention
- **value sensitive intervention** — not-applicable: simultaneous one-step RPS lacks the sequential challenge/intervention timing structure used in Poker and Liar's Dice

### Micro-Fighter

- **information uptake** — partial: Family B Control uses public action history to recognize a specific successful-defense/cooldown punish window; no independent cross-family information-ablation test exists yet.
- **context alignment** — partial: The v0.5 counter-window rule is context-specific and improves the targeted matchup, while the broader v0.7 sustained-threat rule backfires; context quality therefore matters but is not cross-family validated.
- **value sensitive intervention** — confirmed: A prospectively justified counter-window intervention moves Pressure-vs-Control toward parity, whereas a prospectively justified retreat intervention moves it sharply away; the frozen comparison demonstrates that intervention value depends on what is done with the information.

## Guardrails

- No source policy, threshold, or frozen result is modified by this benchmark.
- A confirmed stage requires direct evidence in that game; missing evidence remains unresolved.
- Not-applicable denotes a structural mismatch, not a failed Control mechanism.
- This benchmark does not alter the frozen PCC Poker v0.8.0 human measurement contract.
