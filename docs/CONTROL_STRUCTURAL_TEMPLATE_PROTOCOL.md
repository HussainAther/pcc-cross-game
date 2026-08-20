# Control Structural Template Protocol

This benchmark tests a portable structural template for Control across frozen synthetic game environments:

1. **Information uptake** — behavior changes in response to opponent/public-history information.
2. **Context alignment** — information must be attached to the correct public decision context rather than merely present somewhere in history.
3. **Value-sensitive intervention** — the information is used at a strategically consequential decision point and improves a prespecified performance/timing criterion.

The benchmark does **not** define a universal scalar Control score. Source experiments are read-only and are not retuned. Missing evidence remains `unresolved`; a stage that lacks a structural analogue is `not-applicable` rather than failed.

The frozen PCC Poker v0.8.0 human measurement contract is not changed by this comparison.
