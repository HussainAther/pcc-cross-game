from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


STATUS_ORDER = {"confirmed": 0, "partial": 1, "failed": 2, "unresolved": 3, "absent-by-design": 4, "not-applicable": 5, "not-identifiable": 6}


def _load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _axis_map(cross: dict[str, Any]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for game in cross["games"]:
        out[game["game"]] = {axis: game["axis_evidence"][axis]["status"] for axis in ("pressure", "control", "chaos")}
    return out


def build_theory_status(root: str | Path = ".") -> dict[str, Any]:
    root = Path(root)
    validation = root / "validation"
    cross = _load(validation / "cross-game-comparison.json")
    pressure = _load(validation / "pressure-structural-template.json")
    control = _load(validation / "control-structural-template.json")
    chaos = _load(validation / "chaos-measurement-benchmark.json")

    axes = _axis_map(cross)
    game_order = [g["game"] for g in cross["games"]]

    report: dict[str, Any] = {
        "schema_version": 1,
        "title": "PCC cross-game theory and evidence status",
        "scope": "Synthetic comparative program only; no human-data inference is made here.",
        "games": game_order,
        "axis_status": axes,
        "structural_hypotheses": {
            "pressure": {
                "template": ["commitment_or_threat_exposure", "response_or_space_constriction", "strategic_consequence"],
                "summary": "Pressure is provisionally modeled as credible commitment/threat that narrows the opponent's viable response space and has downstream strategic consequence.",
                "cross_game_status": pressure["conclusion"]["status"],
                "limits": [
                    "The poker-specific dominance cycle is not treated as universal.",
                    "Liar's Dice response constriction is implementation-sensitive rather than universal.",
                    "Micro-Fighter shows that threat generation can be strong even when conversion to value is not universal.",
                    "Pressure is absent-by-design in repeated RPS.",
                ],
            },
            "control": {
                "template": ["information_uptake", "context_alignment", "value_sensitive_intervention"],
                "summary": "Control is provisionally modeled as using opponent-relevant information in the right context to choose an intervention whose value depends on timing and situation.",
                "cross_game_status": control["conclusion"]["status"],
                "limits": [
                    "No single cross-game Control scalar is supported.",
                    "Information uptake and context alignment remain family-sensitive outside poker.",
                    "Micro-Fighter falsifies simple spatial withdrawal as a sufficient Control mechanism.",
                    "Sequential intervention timing is structurally not applicable to one-step RPS in the same form.",
                ],
            },
            "chaos": {
                "template": ["game_appropriate_unpredictability", "independent_adequacy_guardrail"],
                "operator": "multiply_or_jointly_require",
                "summary": "Chaos is provisionally modeled as effective unpredictability: behavioral unpredictability that remains strategically adequate rather than randomness for its own sake.",
                "cross_game_status": chaos["conclusion"]["status"],
                "limits": [
                    "Raw entropy is not a portable Chaos measure.",
                    "Repeated RPS demonstrates that iid-uniform behavior can be maximally unpredictable and value-preserving without identifying latent Chaos intent.",
                    "Poker lacks a conservative family-invariant Chaos observable.",
                    "Micro-Fighter Chaos remains intentionally unresolved pending a dedicated frozen experiment.",
                ],
            },
        },
        "portable_findings": [
            {
                "claim": "PCC axes are better represented by portable structural motifs than by universal scalar observables.",
                "status": "partial",
                "basis": "Pressure, Control, and Chaos each retain a cross-game structural pattern, while exact observables and full construct recovery differ by game and policy family.",
            },
            {
                "claim": "Mechanism evidence must remain separate from observational construct recovery.",
                "status": "confirmed",
                "basis": "Poker and Micro-Fighter contain mechanism-level support even where conservative cross-family observational axes remain unresolved.",
            },
            {
                "claim": "A PCC axis may be absent or structurally non-identifiable in a valid comparison environment.",
                "status": "confirmed",
                "basis": "Pressure is absent-by-design in RPS, and latent Chaos intent is not identifiable from action-only iid-uniform RPS behavior.",
            },
            {
                "claim": "The poker-specific Pressure-Chaos-Control dominance cycle is universal across competitive games.",
                "status": "failed",
                "basis": "Liar's Dice and Micro-Fighter do not reproduce the poker topology under their frozen competitiveness protocols, and RPS lacks Pressure by design.",
            },
            {
                "claim": "Randomness alone is sufficient evidence of Chaos.",
                "status": "failed",
                "basis": "RPS falsification shows high entropy can be strategically equivalent to neutral iid play or highly exploitable temporal structure.",
            },
            {
                "claim": "Creating distance is sufficient evidence of spatial Control.",
                "status": "failed",
                "basis": "Micro-Fighter's deterministic retreat intervention worsens Control by forfeiting initiative and allowing rapid Pressure re-entry.",
            },
        ],
        "game_roles": {
            "poker": "Flagship imperfect-information environment and only current pre-human frozen study; strongest observational Pressure evidence.",
            "liars-dice": "Independent bluff/escalation replication; strongest current cross-family Chaos recovery and useful Pressure/Control mechanism contrasts.",
            "rps": "Minimal falsification/negative-control lab; Pressure absent by design and Chaos intent non-identifiable from action-only iid-uniform behavior.",
            "micro-fighter": "Spatial competitive-control lab; mechanism evidence for threat, constriction, initiative, timing, and value-sensitive intervention without current construct-recovery authorization.",
        },
        "current_boundaries": [
            "Do not infer a universal PCC cycle from the poker result.",
            "Do not promote mechanism evidence into an observational construct label without the relevant frozen recovery test.",
            "Do not interpret entropy or stochasticity alone as Chaos.",
            "Do not interpret prediction/history use alone as Control.",
            "Do not force an absent or structurally mismatched axis into every game.",
            "PCC Poker v0.8.0 remains scientifically frozen; this report does not alter its human-facing measurement contract or ORIA gate.",
        ],
        "next_questions": [
            "Can Micro-Fighter support a dedicated effective-Chaos falsification/recovery experiment without first forcing competitiveness?",
            "Can Control information/context stages be isolated with matched interventions in Liar's Dice and Micro-Fighter?",
            "Which Pressure constriction measures remain stable when policy implementation changes?",
            "Can a future fifth environment add a genuinely new strategic substrate rather than duplicate bluffing, simultaneous choice, or spatial combat?",
        ],
    }
    return report


def _markdown(report: dict[str, Any]) -> str:
    lines = [
        "# PCC Cross-Game Theory & Evidence Status",
        "",
        "> Canonical synthetic-program status summary. This document distinguishes structural hypotheses, mechanism evidence, observational recovery, falsification, absence-by-design, and unresolved questions. It does not make human-data claims.",
        "",
        "## Current structural hypotheses",
        "",
        "### Pressure",
        "",
        "**Commitment/threat exposure → response/space constriction → strategic consequence.**",
        "",
        report["structural_hypotheses"]["pressure"]["summary"],
        "",
        "### Control",
        "",
        "**Information uptake → context alignment → value-sensitive intervention.**",
        "",
        report["structural_hypotheses"]["control"]["summary"],
        "",
        "### Chaos",
        "",
        "**Game-appropriate unpredictability × independent strategic adequacy.**",
        "",
        report["structural_hypotheses"]["chaos"]["summary"],
        "",
        "These are provisional comparative structures, not universal scalar definitions.",
        "",
        "## Observational construct status by game",
        "",
        "| Game | Pressure | Control | Chaos |",
        "|---|---|---|---|",
    ]
    labels = {"poker":"Poker", "liars-dice":"Liar's Dice", "rps":"Repeated RPS", "micro-fighter":"Micro-Fighter"}
    for game in report["games"]:
        s = report["axis_status"][game]
        lines.append(f"| {labels.get(game, game)} | {s['pressure']} | {s['control']} | {s['chaos']} |")

    lines += ["", "## What each environment contributes", ""]
    for game in report["games"]:
        lines += [f"### {labels.get(game, game)}", "", report["game_roles"][game], ""]

    lines += ["## Portable findings", ""]
    for item in report["portable_findings"]:
        lines += [f"- **{item['status']} — {item['claim']}** {item['basis']}"]

    lines += ["", "## Important falsifications and limits", ""]
    for axis in ("pressure", "control", "chaos"):
        lines += [f"### {axis.title()}", ""]
        for limit in report["structural_hypotheses"][axis]["limits"]:
            lines.append(f"- {limit}")
        lines.append("")

    lines += [
        "## Interpretation",
        "",
        "The current comparative evidence does **not** support one universal PCC score, one universal dominance cycle, or one universal observable per axis. The stronger working hypothesis is that Pressure, Control, and Chaos are families of strategic mechanisms whose observable realization depends on the game's information structure, action timing, and value landscape.",
        "",
        "The program therefore treats transfer as a falsifiable question: a game may confirm a stage, partially support it, fail it, leave it unresolved, make it structurally not applicable, or omit an axis by design.",
        "",
        "## Scientific boundaries",
        "",
    ]
    for item in report["current_boundaries"]:
        lines.append(f"- {item}")
    lines += ["", "## Next questions", ""]
    for item in report["next_questions"]:
        lines.append(f"- {item}")
    lines += ["", "---", "", "Generated from the frozen cross-game validation summaries in this repository. Source experiments are not rerun or retuned by this report.", ""]
    return "\n".join(lines)


def write_outputs(report: dict[str, Any], output_dir: str | Path) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "THEORY_STATUS.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (out / "THEORY_STATUS.md").write_text(_markdown(report), encoding="utf-8")
    with (out / "theory-status.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["game", "pressure", "control", "chaos", "role"])
        for game in report["games"]:
            s = report["axis_status"][game]
            w.writerow([game, s["pressure"], s["control"], s["chaos"], report["game_roles"][game]])
