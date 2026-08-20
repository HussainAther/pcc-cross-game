from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any

STAGES = (
    "information_uptake",
    "context_alignment",
    "value_sensitive_intervention",
)


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _family_status(values: dict[str, bool]) -> str:
    vals = list(values.values())
    if vals and all(vals):
        return "confirmed"
    if vals and any(vals):
        return "partial"
    return "failed" if vals else "unresolved"


def build_control_template_benchmark(poker_root: str | Path, liars_root: str | Path, rps_root: str | Path) -> dict[str, Any]:
    poker_root, liars_root, rps_root = map(Path, (poker_root, liars_root, rps_root))
    p_context = _load(poker_root / "validation/contextual-control-observable.json")
    p_mech = _load(poker_root / "validation/control-pressure-mechanism.json")
    l_mech = _load(liars_root / "validation/control-chaos-mechanism.json")
    rps = _load(rps_root / "validation/negative-control.json")

    p_info = {
        fam: bool(data.get("control_correlation", 0) >= p_context["thresholds"]["minimum_control_correlation"])
        for fam, data in p_context.get("families", {}).items()
    }
    p_context_aligned = bool(
        p_context.get("checks", {}).get("control_positive_in_both_families", False)
        or p_context.get("checks", {}).get("control_discriminant_in_both_families", False)
    )
    p_value = bool(p_mech.get("control_pressure_mechanism_confirmed", False))

    l_info = {
        fam: bool(data.get("pathways", {}).get("history_dependence_supported", False))
        for fam, data in l_mech.get("families", {}).items()
    }
    l_value = {
        fam: bool(data.get("pathways", {}).get("challenge_timing_supported", False))
        for fam, data in l_mech.get("families", {}).items()
    }

    r_info = {
        fam: bool(data.get("checks", {}).get("control_signal_exceeds_neutral", False))
        for fam, data in rps.get("families", {}).items()
    }

    games = {
        "poker": {
            "information_uptake": {
                "status": _family_status(p_info),
                "family_checks": p_info,
                "basis": "public-history signal is positively associated with assigned Control in both synthetic families",
            },
            "context_alignment": {
                "status": "confirmed" if p_context_aligned else "partial",
                "basis": "aligned public history outperforms yoked/context-destroyed history, although effect magnitude is not cross-family invariant",
            },
            "value_sensitive_intervention": {
                "status": "confirmed" if p_value else "failed",
                "basis": "frozen aligned-vs-round-swapped/context-yoked payoff intervention against Pressure",
            },
        },
        "liars-dice": {
            "information_uptake": {
                "status": _family_status(l_info),
                "family_checks": l_info,
                "basis": "muting opponent-history information changes Control advantage in Family B but not Family A",
            },
            "context_alignment": {
                "status": _family_status(l_info),
                "family_checks": l_info,
                "basis": "history dependence is implementation-specific; no separate aligned-vs-yoked context experiment exists",
            },
            "value_sensitive_intervention": {
                "status": _family_status(l_value),
                "family_checks": l_value,
                "basis": "Control challenge timing is more accurate in both independent families and contributes to the Control-over-Chaos advantage",
            },
        },
        "rps": {
            "information_uptake": {
                "status": _family_status(r_info),
                "family_checks": r_info,
                "basis": "Control candidate exceeds iid-neutral only in one independent family",
            },
            "context_alignment": {
                "status": "unresolved",
                "basis": "the frozen RPS protocols do not yet contain an aligned-vs-yoked history intervention",
            },
            "value_sensitive_intervention": {
                "status": "not-applicable",
                "basis": "simultaneous one-step RPS lacks the sequential challenge/intervention timing structure used in Poker and Liar's Dice",
            },
        },
    }

    portable = []
    for stage in STAGES:
        statuses = [games[g][stage]["status"] for g in games]
        if sum(s == "confirmed" for s in statuses) >= 2:
            portable.append(stage)

    full_game_support = {
        game: all(games[game][s]["status"] == "confirmed" for s in STAGES)
        for game in games
    }

    return {
        "schema_version": 1,
        "benchmark": "cross-game-control-structural-template",
        "template": ["information_uptake", "context_alignment", "value_sensitive_intervention"],
        "purpose": "Test a portable structural template for Control without defining or tuning a universal scalar Control score.",
        "games": games,
        "portable_confirmed_stages": portable,
        "full_template_confirmed_by_game": full_game_support,
        "conclusion": {
            "single_scalar_control_supported": False,
            "full_three_stage_template_confirmed_cross_game": False,
            "status": "partial-structural-support",
            "basis": "Value-sensitive intervention replicates across Poker and Liar's Dice, while information uptake/context alignment remain implementation-sensitive and RPS lacks the same intervention structure.",
        },
        "guardrails": [
            "No source policy, threshold, or frozen result is modified by this benchmark.",
            "A confirmed stage requires direct evidence in that game; missing evidence remains unresolved.",
            "Not-applicable denotes a structural mismatch, not a failed Control mechanism.",
            "This benchmark does not alter the frozen PCC Poker v0.8.0 human measurement contract.",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    labels = {"poker": "Poker", "liars-dice": "Liar's Dice", "rps": "Repeated RPS"}
    lines = [
        "# Cross-Game Control Structural Template", "",
        "Proposed portable structure: **information uptake → context alignment → value-sensitive intervention**.", "",
        "| Stage | Poker | Liar's Dice | Repeated RPS |", "|---|---|---|---|",
    ]
    for stage in STAGES:
        vals = [report["games"][g][stage]["status"] for g in ("poker", "liars-dice", "rps")]
        lines.append(f"| {stage.replace('_', ' ').title()} | {vals[0]} | {vals[1]} | {vals[2]} |")
    lines += ["", "## Interpretation", "", f"- **Overall status:** {report['conclusion']['status']}.", f"- {report['conclusion']['basis']}", ""]
    for game, label in labels.items():
        lines += [f"### {label}", ""]
        for stage in STAGES:
            item = report["games"][game][stage]
            lines.append(f"- **{stage.replace('_',' ')}** — {item['status']}: {item['basis']}")
        lines.append("")
    lines += ["## Guardrails", ""] + [f"- {x}" for x in report["guardrails"]]
    return "\n".join(lines) + "\n"


def render_csv(report: dict[str, Any]) -> str:
    out = io.StringIO(); w = csv.writer(out)
    w.writerow(["game", "stage", "status", "basis"])
    for game, stages in report["games"].items():
        for stage, item in stages.items():
            w.writerow([game, stage, item["status"], item["basis"]])
    return out.getvalue()


def write_outputs(report: dict[str, Any], output_dir: str | Path) -> None:
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    (out / "control-structural-template.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (out / "CONTROL_STRUCTURAL_TEMPLATE.md").write_text(render_markdown(report), encoding="utf-8")
    (out / "control-structural-template.csv").write_text(render_csv(report), encoding="utf-8")
