from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


AXES = ("pressure", "control", "chaos")


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _require(root: Path, rel: str) -> dict[str, Any]:
    path = root / rel
    if not path.is_file():
        raise FileNotFoundError(f"required frozen source is missing: {path}")
    return _load(path)


def _status_claims(status: dict[str, Any], axis: str) -> list[dict[str, Any]]:
    rows = []
    for claim in status.get("claims", []):
        if axis.lower() in str(claim.get("axis", "")).lower() or axis.lower() in str(claim.get("claim", "")).lower():
            rows.append(claim)
    return rows


def poker_summary(root: str | Path) -> dict[str, Any]:
    root = Path(root)
    cycle = _require(root, "validation/balanced-cycle.json")
    panel = _require(root, "validation/family-invariant-panel.json")
    status = _require(root, "validation/research-status.json")
    mechanism = _require(root, "validation/control-pressure-mechanism.json")
    contextual = _require(root, "validation/contextual-control-observable.json")
    chaos = _require(root, "validation/effective-chaos-validation.json")

    coverage = panel.get("axis_coverage", {})
    axis_evidence: dict[str, Any] = {}
    for axis in AXES:
        selected = list(coverage.get(axis, []))
        if selected:
            state = "confirmed"
            basis = "cross-family invariant observable component(s) selected"
        else:
            state = "unresolved"
            basis = "no component survived the frozen family-invariance gate"
        axis_evidence[axis] = {
            "status": state,
            "selected_components": selected,
            "basis": basis,
            "research_status_claims": _status_claims(status, axis),
        }

    # Preserve the important nuance: mechanism evidence does not promote the
    # observational Control axis to confirmed.
    axis_evidence["control"]["mechanism_evidence"] = {
        "control_pressure_mechanism_confirmed": bool(mechanism.get("control_pressure_mechanism_confirmed")),
        "contextual_control_observable_confirmed": bool(contextual.get("contextual_control_observable_confirmed", False)),
        "note": "Mechanism evidence is kept separate from family-invariant observational measurement.",
    }
    axis_evidence["chaos"]["mechanism_evidence"] = {
        "effective_chaos_construct_confirmed": bool(chaos.get("effective_chaos_construct_confirmed")),
    }

    return {
        "game": "poker",
        "source_version": "0.8.0 synthetic evidence freeze",
        "source_root": str(root),
        "balance": {
            "status": "confirmed" if cycle.get("balanced_cycle_confirmed") else "failed",
            "criterion": "engineered balanced cycle under the poker-specific frozen protocol",
            "cycle_required": True,
            "cross_game_comparability_warning": "A poker cycle is not assumed to be a universal PCC topology.",
        },
        "axis_evidence": axis_evidence,
        "mechanisms": [
            {
                "name": "control-pressure contextual mechanism",
                "status": "confirmed" if mechanism.get("control_pressure_mechanism_confirmed") else "failed",
                "scope": "engineered synthetic poker agents",
            },
            {
                "name": "contextual Control observable",
                "status": "partial" if not contextual.get("contextual_control_observable_confirmed", False) else "confirmed",
                "scope": "positive/discriminant in both families but not family-invariant in strength",
            },
            {
                "name": "effective Chaos construct",
                "status": "failed" if not chaos.get("effective_chaos_construct_confirmed") else "confirmed",
                "scope": "frozen construct-validation gate",
            },
        ],
        "negative_controls": {
            "status": "present",
            "note": "Poker validation includes shuffled/yoked/counterfactual controls in frozen experiments; this comparison does not collapse them into one score.",
        },
    }


def liars_dice_summary(root: str | Path) -> dict[str, Any]:
    root = Path(root)
    balance = _require(root, "validation/balance.json")
    mechanism = _require(root, "validation/control-chaos-mechanism.json")

    pathways: dict[str, list[bool]] = {}
    family_summaries: dict[str, Any] = {}
    for family, data in mechanism.get("families", {}).items():
        family_summaries[family] = data.get("summary", {})
        for name, supported in data.get("pathways", {}).items():
            pathways.setdefault(name, []).append(bool(supported))

    replicated = sorted(name for name, vals in pathways.items() if vals and all(vals))
    family_specific = sorted(name for name, vals in pathways.items() if vals and any(vals) and not all(vals))

    return {
        "game": "liars-dice",
        "source_version": "0.3.0 control-chaos mechanism",
        "source_root": str(root),
        "balance": {
            "status": "confirmed" if balance.get("balance_confirmed") else "failed",
            "criterion": "all pairwise matchups competitive in two independent policy families",
            "cycle_required": False,
            "failure_pattern": "Control over Chaos exceeded the frozen competitiveness bound in both families" if not balance.get("balance_confirmed") else None,
        },
        "axis_evidence": {
            axis: {
                "status": "unresolved",
                "selected_components": [],
                "basis": "construct-recovery has not yet been run; v0.3 is mechanism/balance evidence only",
            }
            for axis in AXES
        },
        "mechanisms": [
            {
                "name": "Control-vs-Chaos challenge timing",
                "status": "confirmed" if "challenge_timing_supported" in replicated else "partial",
                "scope": "replicated across both independent Liar's Dice policy families",
            },
            {
                "name": "Chaos bid-plausibility cost",
                "status": "confirmed" if "chaos_lower_bid_plausibility_supported" in replicated else "partial",
                "scope": "replicated across both independent Liar's Dice policy families",
            },
            {
                "name": "history dependence",
                "status": "partial" if "history_dependence_supported" in family_specific else ("confirmed" if "history_dependence_supported" in replicated else "failed"),
                "scope": "family-specific rather than universal" if "history_dependence_supported" in family_specific else "cross-family",
            },
        ],
        "mechanism_diagnostics": {
            "replicated_pathways": replicated,
            "family_specific_pathways": family_specific,
            "family_summaries": family_summaries,
        },
        "negative_controls": {
            "status": "planned",
            "note": "No construct-recovery negative-control panel has been frozen yet.",
        },
    }


def build_comparison(poker_root: str | Path, liars_root: str | Path) -> dict[str, Any]:
    poker = poker_summary(poker_root)
    liars = liars_dice_summary(liars_root)
    return {
        "schema_version": 1,
        "purpose": "Cross-game comparison of frozen synthetic evidence without assuming identical PCC topology or measurement validity across games.",
        "games": [poker, liars],
        "cross_game_findings": [
            {
                "finding": "game topology is not invariant",
                "status": "supported",
                "basis": "Poker's frozen engineered cycle passes, whereas Liar's Dice pairwise competitiveness fails because Control exceeds Chaos in both families.",
            },
            {
                "finding": "context/history effects are implementation-sensitive",
                "status": "supported",
                "basis": "Poker contextual Control strength is not family-invariant; Liar's Dice history dependence appears in one policy family but not the other.",
            },
            {
                "finding": "Pressure has cross-family observational support only in poker so far",
                "status": "supported",
                "basis": "Poker selected two invariant Pressure components; Liar's Dice has not yet run construct recovery.",
            },
            {
                "finding": "Chaos measurement is not yet cross-game validated",
                "status": "supported",
                "basis": "Poker effective-Chaos construct gate failed and Liar's Dice has only mechanism diagnostics, not construct recovery.",
            },
        ],
        "guardrails": [
            "Do not infer human psychological states from synthetic-agent labels.",
            "Do not require a rock-paper-scissors cycle outside the game-specific protocol that defined it.",
            "Mechanism confirmation and observational construct recovery are distinct evidence classes.",
            "Missing evidence is reported as unresolved, not imputed from another game.",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# PCC Cross-Game Evidence Matrix",
        "",
        "This report compares frozen synthetic evidence without assuming that poker-specific topology or measurements transfer to Liar's Dice.",
        "",
        "| Dimension | Poker | Liar's Dice |",
        "|---|---|---|",
    ]
    games = {g["game"]: g for g in report["games"]}
    p, l = games["poker"], games["liars-dice"]
    lines.append(f"| Balance | {p['balance']['status']}: {p['balance']['criterion']} | {l['balance']['status']}: {l['balance']['criterion']} |")
    for axis in AXES:
        pa = p["axis_evidence"][axis]
        la = l["axis_evidence"][axis]
        pcomp = ", ".join(pa.get("selected_components", [])) or "none"
        lcomp = ", ".join(la.get("selected_components", [])) or "none"
        lines.append(f"| {axis.title()} observational construct | {pa['status']} ({pcomp}) | {la['status']} ({lcomp}) |")
    lines += ["", "## Mechanism evidence", ""]
    for game in (p, l):
        lines.append(f"### {game['game']}")
        for item in game["mechanisms"]:
            lines.append(f"- **{item['name']}** — {item['status']}. {item['scope']}")
        lines.append("")
    lines += ["## Cross-game findings", ""]
    for item in report["cross_game_findings"]:
        lines.append(f"- **{item['finding']}** — {item['status']}. {item['basis']}")
    lines += ["", "## Guardrails", ""]
    lines.extend(f"- {x}" for x in report["guardrails"])
    return "\n".join(lines) + "\n"


def render_csv(report: dict[str, Any]) -> str:
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(["game", "dimension", "status", "details"])
    for game in report["games"]:
        writer.writerow([game["game"], "balance", game["balance"]["status"], game["balance"]["criterion"]])
        for axis in AXES:
            ev = game["axis_evidence"][axis]
            writer.writerow([game["game"], axis, ev["status"], ev["basis"]])
        for mech in game["mechanisms"]:
            writer.writerow([game["game"], f"mechanism:{mech['name']}", mech["status"], mech["scope"]])
    return out.getvalue()


def write_outputs(report: dict[str, Any], output_dir: str | Path) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "cross-game-comparison.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (output_dir / "CROSS_GAME_COMPARISON.md").write_text(render_markdown(report), encoding="utf-8")
    (output_dir / "cross-game-comparison.csv").write_text(render_csv(report), encoding="utf-8")
