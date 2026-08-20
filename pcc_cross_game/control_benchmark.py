from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any

MECHANISMS = (
    "history_or_context_use",
    "predictive_gain",
    "counterfactual_value",
    "timing_or_intervention_sensitivity",
)


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _status_from_family_checks(checks: dict[str, bool]) -> str:
    vals = list(checks.values())
    if vals and all(vals):
        return "confirmed"
    if vals and any(vals):
        return "partial"
    return "failed" if vals else "unresolved"


def build_control_benchmark(poker_root: str | Path, liars_root: str | Path, rps_root: str | Path) -> dict[str, Any]:
    poker_root, liars_root, rps_root = map(Path, (poker_root, liars_root, rps_root))
    p_context = _load(poker_root / "validation/contextual-control-observable.json")
    p_mech = _load(poker_root / "validation/control-pressure-mechanism.json")
    p_cf = _load(poker_root / "validation/counterfactual-control.json")
    l_mech = _load(liars_root / "validation/control-chaos-mechanism.json")
    l_recovery = _load(liars_root / "validation/construct-recovery.json")
    rps = _load(rps_root / "validation/negative-control.json")

    p_context_checks = {
        name: bool(data.get("control_correlation", 0) >= p_context["thresholds"]["minimum_control_correlation"])
        for name, data in p_context["families"].items()
    }
    p_predictive = _status_from_family_checks(p_context_checks)
    # It is positive/discriminant in both families, but its magnitude is not invariant.
    if p_predictive == "confirmed" and not p_context["checks"].get("cross_family_control_gap_at_most_0_20", False):
        p_predictive = "partial"

    l_history = {
        fam: bool(data.get("pathways", {}).get("history_dependence_supported", False))
        for fam, data in l_mech.get("families", {}).items()
    }
    l_timing = {
        fam: bool(data.get("pathways", {}).get("challenge_timing_supported", False))
        for fam, data in l_mech.get("families", {}).items()
    }
    l_control_recovery = {
        fam: bool(data.get("axis_checks", {}).get("control", {}).get("axis_recovered", False))
        for fam, data in l_recovery.get("families", {}).items()
    }
    rps_control = {
        fam: bool(data.get("checks", {}).get("control_signal_exceeds_neutral", False))
        for fam, data in rps.get("families", {}).items()
    }

    # Counterfactual poker result names have changed over development; retain the frozen top-level
    # confirmation when present and otherwise expose unresolved rather than guessing.
    p_cf_confirmed = None
    for key in ("counterfactual_control_confirmed", "counterfactual_control_validation_confirmed", "counterfactual_control_mechanism_confirmed"):
        if key in p_cf:
            p_cf_confirmed = bool(p_cf[key])
            break

    games = {
        "poker": {
            "history_or_context_use": {"status": "partial", "basis": "aligned-vs-yoked contextual observable is positive/discriminant in both families but not invariant in strength"},
            "predictive_gain": {"status": p_predictive, "family_checks": p_context_checks, "basis": "public-history conditional action likelihood signal"},
            "counterfactual_value": {"status": "confirmed" if p_cf_confirmed else ("failed" if p_cf_confirmed is False else "unresolved"), "basis": "frozen counterfactual-control validation"},
            "timing_or_intervention_sensitivity": {"status": "confirmed" if p_mech.get("control_pressure_mechanism_confirmed") else "failed", "basis": "round-swapped and context-yoked interventions against Pressure"},
        },
        "liars-dice": {
            "history_or_context_use": {"status": _status_from_family_checks(l_history), "family_checks": l_history, "basis": "muted opponent-history intervention"},
            "predictive_gain": {"status": _status_from_family_checks(l_control_recovery), "family_checks": l_control_recovery, "basis": "frozen Control construct-recovery observable"},
            "counterfactual_value": {"status": "unresolved", "basis": "no frozen counterfactual-value experiment"},
            "timing_or_intervention_sensitivity": {"status": _status_from_family_checks(l_timing), "family_checks": l_timing, "basis": "challenge-timing accuracy pathway"},
        },
        "rps": {
            "history_or_context_use": {"status": "unresolved", "basis": "v0.1 negative-control protocol did not isolate history use"},
            "predictive_gain": {"status": _status_from_family_checks(rps_control), "family_checks": rps_control, "basis": "Control candidate exceeds iid-neutral baseline"},
            "counterfactual_value": {"status": "unresolved", "basis": "no frozen counterfactual-value experiment"},
            "timing_or_intervention_sensitivity": {"status": "not-applicable", "basis": "simultaneous RPS actions provide no challenge-timing analogue in v0.1"},
        },
    }

    portable = []
    for mechanism in MECHANISMS:
        statuses = {game: games[game][mechanism]["status"] for game in games}
        if sum(s == "confirmed" for s in statuses.values()) >= 2:
            portable.append(mechanism)

    return {
        "schema_version": 1,
        "benchmark": "cross-game-control-mechanisms",
        "purpose": "Compare frozen Control mechanism evidence without defining a new scalar Control score or retuning source experiments.",
        "games": games,
        "portable_confirmed_mechanisms": portable,
        "conclusion": {
            "control_is_single_portable_observable": False,
            "status": "not-supported",
            "basis": "No candidate observational Control signal is confirmed across all three environments; intervention/timing evidence is strongest but is not structurally available in RPS.",
        },
        "guardrails": [
            "This benchmark is descriptive over frozen synthetic results; it does not rerun or retune source experiments.",
            "Unmeasured mechanisms remain unresolved rather than being inferred from another game.",
            "Not-applicable means the game/protocol lacks the relevant structural analogue; it is not a failed Control result.",
            "Mechanism evidence does not promote any human-facing Control measure in frozen PCC Poker v0.8.0.",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    labels = {"poker": "Poker", "liars-dice": "Liar's Dice", "rps": "Repeated RPS"}
    lines = [
        "# Cross-Game Control Mechanism Benchmark", "",
        "This benchmark compares frozen synthetic Control evidence without creating a new scalar Control score.", "",
        "| Mechanism | Poker | Liar's Dice | Repeated RPS |", "|---|---|---|---|",
    ]
    for mechanism in MECHANISMS:
        pretty = mechanism.replace("_", " ").title()
        vals = [report["games"][g][mechanism]["status"] for g in ("poker", "liars-dice", "rps")]
        lines.append(f"| {pretty} | {vals[0]} | {vals[1]} | {vals[2]} |")
    lines += ["", "## Interpretation", "", f"- **Single portable Control observable:** {str(report['conclusion']['control_is_single_portable_observable']).lower()}.", f"- {report['conclusion']['basis']}", ""]
    for game, label in labels.items():
        lines += [f"### {label}", ""]
        for mechanism in MECHANISMS:
            item = report["games"][game][mechanism]
            lines.append(f"- **{mechanism.replace('_', ' ')}** — {item['status']}: {item['basis']}")
        lines.append("")
    lines += ["## Guardrails", ""] + [f"- {x}" for x in report["guardrails"]]
    return "\n".join(lines) + "\n"


def render_csv(report: dict[str, Any]) -> str:
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["game", "mechanism", "status", "basis"])
    for game, mechanisms in report["games"].items():
        for name, item in mechanisms.items():
            w.writerow([game, name, item["status"], item["basis"]])
    return out.getvalue()


def write_outputs(report: dict[str, Any], output_dir: str | Path) -> None:
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    (out / "control-mechanism-benchmark.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (out / "CONTROL_MECHANISM_BENCHMARK.md").write_text(render_markdown(report), encoding="utf-8")
    (out / "control-mechanism-benchmark.csv").write_text(render_csv(report), encoding="utf-8")
