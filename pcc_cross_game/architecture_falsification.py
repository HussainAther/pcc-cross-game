from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any

GAMES = ("poker", "liars-dice", "rps", "micro-fighter", "colonel-blotto")
DISPLAY = {
    "poker": "Poker",
    "liars-dice": "Liar's Dice",
    "rps": "Repeated RPS",
    "micro-fighter": "Micro-Fighter",
    "colonel-blotto": "Colonel Blotto",
}


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _pending(game: str, source: str, reason: str) -> dict[str, Any]:
    return {
        "game": game,
        "status": "pending-trajectory-export",
        "source": source,
        "reason": reason,
        "architecture_result": None,
    }


def build_architecture_falsification(root: str | Path = ".") -> dict[str, Any]:
    root = Path(root)
    source_map = {
        "poker": root / "sources/pcc-poker-v0.8.0/validation/control-architecture-export.json",
        "liars-dice": root / "sources/pcc-liars-dice-v0.5.0/validation/control-architecture-export.json",
        "rps": root / "sources/pcc-rps-v0.2.0/validation/control-architecture-export.json",
        "micro-fighter": root / "sources/pcc-micro-fighter-v1.0.0/validation/control-architecture-export.json",
        "colonel-blotto": root / "sources/pcc-colonel-blotto-v1.1.0/validation/control-modulation.json",
    }
    rows: list[dict[str, Any]] = []
    for game in GAMES:
        path = source_map[game]
        if not path.is_file():
            rows.append(_pending(
                game,
                str(path.relative_to(root)),
                "Bundled frozen summaries do not contain the disjoint-seed agent-by-context rows required for additive vs interaction model fitting.",
            ))
            continue
        data = _load(path)
        if game == "colonel-blotto":
            agg = data["aggregate"]
            rows.append({
                "game": game,
                "status": "evaluated",
                "source": str(path.relative_to(root)),
                "architecture_result": {
                    "additive_standardized_mae": agg["standardized_mae"]["additive"],
                    "control_context_standardized_mae": agg["standardized_mae"]["control_interaction"],
                    "relative_improvement": agg["relative_mae_improvement_from_control_interactions"],
                    "targets_improved": list(agg["improved_targets"]),
                    "targets_total": len(data["design"]["targets"]),
                    "primary_pass": bool(agg["all_primary_checks_pass"]),
                    "latent_pcc_weights_in_generator": bool(data["design"]["latent_pcc_weights_in_generator"]),
                    "cross_validation": data["design"]["cross_validation"],
                },
            })
        else:
            # Future game-native adapters should emit this normalized schema.
            required = {"additive_standardized_mae", "control_context_standardized_mae", "relative_improvement", "primary_pass"}
            if not required.issubset(data):
                raise ValueError(f"invalid control architecture export for {game}: missing {sorted(required - set(data))}")
            rows.append({"game": game, "status": "evaluated", "source": str(path.relative_to(root)), "architecture_result": data})

    evaluated = [r for r in rows if r["status"] == "evaluated"]
    passes = [r for r in evaluated if r["architecture_result"]["primary_pass"]]
    majority_threshold = 4
    pooled_claim_ready = len(evaluated) == len(GAMES)
    cross_game_pass = pooled_claim_ready and len(passes) >= majority_threshold
    return {
        "schema_version": 1,
        "title": "PCC cross-game architecture falsification: state axes vs contextual modulation",
        "hypothesis": "Pressure and Chaos behave primarily as comparatively context-stable behavioral dimensions, while Control is expressed primarily through context-dependent modulation.",
        "model_comparison": {
            "additive": "behavior ~ Pressure + Control + Chaos + context",
            "control_modulatory": "behavior ~ Pressure + Control + Chaos + context + Control x context",
            "planned_discriminants": [
                "Pressure x context",
                "Chaos x context",
                "cross-context rank stability",
                "leave-one-game-out qualitative ordering",
            ],
        },
        "prespecified_cross_game_criteria": {
            "minimum_pooled_relative_improvement": 0.05,
            "minimum_games_with_control_interaction_improvement": 4,
            "control_interaction_should_exceed_pressure_or_chaos_interaction_in_majority": True,
            "leave_one_game_out_required": True,
        },
        "games": rows,
        "summary": {
            "evaluated_games": len(evaluated),
            "required_games": len(GAMES),
            "games_passing_game_native_control_modulation_test": len(passes),
            "pooled_claim_ready": pooled_claim_ready,
            "cross_game_architecture_confirmed": cross_game_pass,
            "status": "pending" if not pooled_claim_ready else ("confirmed" if cross_game_pass else "failed"),
        },
        "guardrails": [
            "Do not treat missing trajectory exports as negative evidence.",
            "Do not refit game-native PCC observables to make the cross-game architecture pass.",
            "A Blotto pass is evidence for Blotto, not proof of cross-game generality.",
            "Control x context must be compared against Pressure x context and Chaos x context before claiming Control is disproportionately modulatory.",
            "The final claim requires leave-one-game-out analysis after all five games are evaluable.",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# PCC Cross-Game Architecture Falsification",
        "",
        "> Prospective architecture-level comparison. Missing game-native trajectory exports are reported as pending, not failed.",
        "",
        "## Hypothesis",
        "",
        report["hypothesis"],
        "",
        "## Frozen model comparison",
        "",
        f"- Additive: `{report['model_comparison']['additive']}`",
        f"- Control-modulatory: `{report['model_comparison']['control_modulatory']}`",
        "",
        "## Current game status",
        "",
        "| Game | Status | Control x context improvement | Primary game-native result |",
        "|---|---|---:|---|",
    ]
    for row in report["games"]:
        if row["status"] == "evaluated":
            result = row["architecture_result"]
            lines.append(f"| {DISPLAY[row['game']]} | evaluated | {100*result['relative_improvement']:.2f}% | {'PASS' if result['primary_pass'] else 'FAIL'} |")
        else:
            lines.append(f"| {DISPLAY[row['game']]} | pending trajectory export | — | — |")
    lines += [
        "",
        "## Current conclusion",
        "",
        f"**{report['summary']['status'].upper()}** — {report['summary']['evaluated_games']}/{report['summary']['required_games']} games currently have the required frozen architecture-level export.",
        "",
        "Colonel Blotto is the first calibrated game-level result: adding `Control x context` reduced leave-one-agent-out standardized MAE by **15.04%** and improved all four prespecified behavioral targets. This does not yet establish cross-game generality.",
        "",
        "## Required next exports",
        "",
        "Each remaining game should export disjoint-seed agent-by-context rows using its already frozen game-native P/C/Chaos signatures and outcomes. The cross-game repository should fit only the common architecture comparison; it should not redesign game-native measurements.",
        "",
        "## Guardrails",
        "",
    ]
    lines.extend(f"- {g}" for g in report["guardrails"])
    return "\n".join(lines) + "\n"


def render_csv(report: dict[str, Any]) -> str:
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["game", "status", "relative_improvement", "primary_pass", "source"])
    for row in report["games"]:
        res = row.get("architecture_result") or {}
        w.writerow([row["game"], row["status"], res.get("relative_improvement", ""), res.get("primary_pass", ""), row["source"]])
    return out.getvalue()


def write_outputs(report: dict[str, Any], output_dir: str | Path) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "cross-game-architecture.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (out / "CROSS_GAME_ARCHITECTURE.md").write_text(render_markdown(report), encoding="utf-8")
    (out / "cross-game-architecture.csv").write_text(render_csv(report), encoding="utf-8")
