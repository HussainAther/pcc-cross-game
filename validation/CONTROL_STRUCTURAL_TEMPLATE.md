# Cross-Game Control Structural Template

Proposed portable structure: **information uptake → context alignment → value-sensitive intervention**.

| Stage | Poker | Liar's Dice | Repeated RPS |
|---|---|---|---|
| Information Uptake | confirmed | partial | partial |
| Context Alignment | confirmed | partial | unresolved |
| Value Sensitive Intervention | confirmed | confirmed | not-applicable |

## Interpretation

- **Overall status:** partial-structural-support.
- Value-sensitive intervention replicates across Poker and Liar's Dice, while information uptake/context alignment remain implementation-sensitive and RPS lacks the same intervention structure.

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

## Guardrails

- No source policy, threshold, or frozen result is modified by this benchmark.
- A confirmed stage requires direct evidence in that game; missing evidence remains unresolved.
- Not-applicable denotes a structural mismatch, not a failed Control mechanism.
- This benchmark does not alter the frozen PCC Poker v0.8.0 human measurement contract.
