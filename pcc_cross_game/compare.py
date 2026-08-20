from __future__ import annotations

import csv
import io
import json
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


def _axis_recovery_status(construct: dict[str, Any], axis: str) -> tuple[str, dict[str, bool]]:
    family_pass = {}
    for family, data in construct.get("families", {}).items():
        checks = data.get("axis_checks", {}).get(axis, {})
        family_pass[family] = bool(checks) and all(bool(v) for v in checks.values())
    if family_pass and all(family_pass.values()):
        return "confirmed", family_pass
    if any(family_pass.values()):
        return "partial", family_pass
    return "failed", family_pass


def liars_dice_summary(root: str | Path) -> dict[str, Any]:
    root = Path(root)
    balance = _require(root, "validation/balance.json")
    mechanism = _require(root, "validation/control-chaos-mechanism.json")
    construct = _require(root, "validation/construct-recovery.json")

    pathways: dict[str, list[bool]] = {}
    family_summaries: dict[str, Any] = {}
    for family, data in mechanism.get("families", {}).items():
        family_summaries[family] = data.get("summary", {})
        for name, supported in data.get("pathways", {}).items():
            pathways.setdefault(name, []).append(bool(supported))

    replicated = sorted(name for name, vals in pathways.items() if vals and all(vals))
    family_specific = sorted(name for name, vals in pathways.items() if vals and any(vals) and not all(vals))

    axis_evidence: dict[str, Any] = {}
    for axis in AXES:
        state, family_pass = _axis_recovery_status(construct, axis)
        effects = {
            family: data.get("effects", {}).get(axis, {})
            for family, data in construct.get("families", {}).items()
        }
        axis_evidence[axis] = {
            "status": state,
            "selected_components": [construct.get("candidate_observables", {}).get(axis, axis)],
            "basis": (
                "passed the preregistered recovery checks in both independent families"
                if state == "confirmed"
                else "passed the preregistered recovery checks in one of two independent families"
                if state == "partial"
                else "failed the preregistered recovery checks in both independent families"
            ),
            "family_pass": family_pass,
            "effects": effects,
        }

    return {
        "game": "liars-dice",
        "source_version": "0.4.0 construct recovery",
        "source_root": str(root),
        "balance": {
            "status": "confirmed" if balance.get("balance_confirmed") else "failed",
            "criterion": "all pairwise matchups competitive in two independent policy families",
            "cycle_required": False,
            "failure_pattern": "Control over Chaos exceeded the frozen competitiveness bound in both families" if not balance.get("balance_confirmed") else None,
        },
        "axis_evidence": axis_evidence,
        "construct_recovery": {
            "all_axes_confirmed": bool(construct.get("liars_dice_construct_recovery_confirmed")),
            "cross_family_axis_status": construct.get("cross_family_axis_status", {}),
            "thresholds": construct.get("prespecified_thresholds", {}),
            "design": construct.get("design", {}),
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
            "status": "present",
            "note": "The frozen construct-recovery experiment includes shuffled-label 95th-percentile falsification checks.",
        },
    }


def build_comparison(poker_root: str | Path, liars_root: str | Path) -> dict[str, Any]:
    poker = poker_summary(poker_root)
    liars = liars_dice_summary(liars_root)
    return {
        "schema_version": 2,
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
                "finding": "construct recoverability is game-dependent",
                "status": "supported",
                "basis": "Poker's conservative invariant panel supports Pressure but not Control/Chaos, while Liar's Dice cross-family recovery confirms Chaos, only partially recovers Pressure, and fails Control.",
            },
            {
                "finding": "Pressure evidence is currently stronger in poker",
                "status": "supported",
                "basis": "Poker has two cross-family invariant Pressure components; Liar's Dice Pressure passes recovery in only one of two independent families.",
            },
            {
                "finding": "Chaos evidence is currently stronger in Liar's Dice",
                "status": "supported",
                "basis": "Liar's Dice Chaos passes all preregistered recovery checks in both families, while Poker's frozen effective-Chaos construct gate failed.",
            },
            {
                "finding": "Control remains the hardest invariant observational axis",
                "status": "supported",
                "basis": "Poker has mechanism evidence but no family-invariant Control observable; Liar's Dice Control fails preregistered recovery in both families.",
            },
        ],
        "guardrails": [
            "Do not infer human psychological states from synthetic-agent labels.",
            "Do not require a rock-paper-scissors cycle outside the game-specific protocol that defined it.",
            "Mechanism confirmation and observational construct recovery are distinct evidence classes.",
            "A cross-family confirmation in one game does not automatically transfer to another game.",
            "Missing or failed evidence is reported directly, not imputed or repaired from another game.",
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
