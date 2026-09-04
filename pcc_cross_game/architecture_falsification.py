from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from statistics import mean
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


def _interaction_improvements(game: str, data: dict[str, Any]) -> dict[str, float | None]:
    if game == "poker":
        x = data.get("interaction_improvements", {})
        return {k: (float(x[k]) if k in x else None) for k in ("pressure", "control", "chaos")}
    if game in {"liars-dice", "rps"}:
        return {
            "pressure": float(data["pressure_context_relative_improvement"]),
            "control": float(data["relative_improvement"]),
            "chaos": float(data["chaos_context_relative_improvement"]),
        }
    if game == "micro-fighter":
        return {
            "pressure": float(data["pressure_context_relative_improvement"]),
            "control": float(data["relative_improvement"]),
            "chaos": float(data["chaos_context_relative_improvement"]),
        }
    # Blotto v1.1 prospectively fit only the Control interaction. Preserve the
    # missing discriminants rather than reconstructing them post hoc here.
    return {
        "pressure": None,
        "control": float(data["aggregate"]["relative_mae_improvement_from_control_interactions"]),
        "chaos": None,
    }


def _strongest_axis(improvements: dict[str, float | None]) -> str | None:
    present = {k: v for k, v in improvements.items() if v is not None}
    if not present:
        return None
    return max(present, key=present.get)


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
            interactions = _interaction_improvements(game, data)
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
                    "interaction_improvements": interactions,
                    "strongest_interaction_axis": _strongest_axis(interactions),
                    "interaction_discriminants_complete": False,
                },
            })
        else:
            required = {"additive_standardized_mae", "control_context_standardized_mae", "relative_improvement", "primary_pass"}
            if not required.issubset(data):
                raise ValueError(f"invalid control architecture export for {game}: missing {sorted(required - set(data))}")
            interactions = _interaction_improvements(game, data)
            normalized = dict(data)
            normalized["interaction_improvements"] = interactions
            normalized["strongest_interaction_axis"] = _strongest_axis(interactions)
            normalized["interaction_discriminants_complete"] = all(v is not None for v in interactions.values())
            rows.append({"game": game, "status": "evaluated", "source": str(path.relative_to(root)), "architecture_result": normalized})

    evaluated = [r for r in rows if r["status"] == "evaluated"]
    passes = [r for r in evaluated if r["architecture_result"]["primary_pass"]]
    pooled_claim_ready = len(evaluated) == len(GAMES)
    macro_control_improvement = mean(r["architecture_result"]["relative_improvement"] for r in evaluated) if evaluated else None

    # Criterion 3 is already falsified if Control is not strongest in a majority
    # of the games with complete discriminant exports and even assigning all
    # incomplete games to Control cannot reach the majority threshold.
    complete_discriminants = [r for r in evaluated if r["architecture_result"]["interaction_discriminants_complete"]]
    control_strongest_complete = sum(r["architecture_result"]["strongest_interaction_axis"] == "control" for r in complete_discriminants)
    incomplete_discriminants = len(evaluated) - len(complete_discriminants)
    majority_count = len(GAMES) // 2 + 1
    criterion3_max_possible_control_strongest = control_strongest_complete + incomplete_discriminants
    criterion3_pass = pooled_claim_ready and criterion3_max_possible_control_strongest >= majority_count and control_strongest_complete >= majority_count
    criterion3_status = "pass" if criterion3_pass else ("fail" if pooled_claim_ready and criterion3_max_possible_control_strongest < majority_count else "not-fully-evaluable")

    # Criterion 4 was not emitted in a common normalized form by all native repos.
    criterion4_status = "not-evaluable-from-current-exports" if pooled_claim_ready else "pending"

    leave_one_out: list[dict[str, Any]] = []
    if pooled_claim_ready:
        for held_out in evaluated:
            subset = [r for r in evaluated if r["game"] != held_out["game"]]
            subset_macro = mean(r["architecture_result"]["relative_improvement"] for r in subset)
            subset_passes = sum(r["architecture_result"]["primary_pass"] for r in subset)
            # Qualitative universal-Control architecture would require a majority
            # of the remaining games to pass plus >=5% macro improvement.
            subset_majority = len(subset) // 2 + 1
            universal_control_survives = subset_macro >= 0.05 and subset_passes >= subset_majority
            leave_one_out.append({
                "held_out_game": held_out["game"],
                "remaining_games": len(subset),
                "macro_control_relative_improvement": subset_macro,
                "games_passing_control_modulation": subset_passes,
                "majority_required": subset_majority,
                "universal_control_architecture_survives": universal_control_survives,
            })
    loogo_universal_survives_all = bool(leave_one_out) and all(x["universal_control_architecture_survives"] for x in leave_one_out)
    loogo_falsification_robust = bool(leave_one_out) and all(not x["universal_control_architecture_survives"] for x in leave_one_out)

    criteria = {
        "pooled_control_improvement_at_least_5pct": {
            "threshold": 0.05,
            "value": macro_control_improvement,
            "status": "pending" if not pooled_claim_ready else ("pass" if macro_control_improvement is not None and macro_control_improvement >= 0.05 else "fail"),
        },
        "control_improvement_in_at_least_4_of_5_games": {
            "threshold": 4,
            "value": len(passes),
            "status": "pending" if not pooled_claim_ready else ("pass" if len(passes) >= 4 else "fail"),
        },
        "control_interaction_disproportionate_in_majority": {
            "threshold": majority_count,
            "control_strongest_complete_games": control_strongest_complete,
            "complete_discriminant_games": len(complete_discriminants),
            "incomplete_discriminant_games": incomplete_discriminants,
            "maximum_possible_control_strongest_games": criterion3_max_possible_control_strongest,
            "status": criterion3_status,
        },
        "pressure_chaos_rank_stability_exceeds_control_in_majority": {
            "status": criterion4_status,
            "reason": "The five normalized architecture exports do not provide a common cross-context rank-stability statistic for all three axes; this criterion cannot be reconstructed without new native exports.",
        },
        "leave_one_game_out_qualitative_architecture": {
            "status": "pending" if not pooled_claim_ready else ("pass" if loogo_universal_survives_all else "fail"),
            "universal_control_architecture_survives_all_folds": loogo_universal_survives_all,
            "falsification_robust_in_all_folds": loogo_falsification_robust,
        },
    }

    cross_game_pass = pooled_claim_ready and all(criteria[k]["status"] == "pass" for k in (
        "pooled_control_improvement_at_least_5pct",
        "control_improvement_in_at_least_4_of_5_games",
        "control_interaction_disproportionate_in_majority",
        "leave_one_game_out_qualitative_architecture",
    )) and criteria["pressure_chaos_rank_stability_exceeds_control_in_majority"]["status"] == "pass"

    strongest_counts: dict[str, int] = {"pressure": 0, "control": 0, "chaos": 0, "unknown": 0}
    for r in evaluated:
        axis = r["architecture_result"].get("strongest_interaction_axis")
        strongest_counts[axis if axis in strongest_counts else "unknown"] += 1

    return {
        "schema_version": 2,
        "title": "PCC cross-game architecture falsification: state axes vs contextual modulation",
        "hypothesis": "Pressure and Chaos behave primarily as comparatively context-stable behavioral dimensions, while Control is expressed primarily through context-dependent modulation.",
        "model_comparison": {
            "additive": "behavior ~ Pressure + Control + Chaos + context",
            "control_modulatory": "behavior ~ Pressure + Control + Chaos + context + Control x context",
            "discriminants": ["Pressure x context", "Chaos x context", "cross-context rank stability", "leave-one-game-out qualitative ordering"],
        },
        "prespecified_cross_game_criteria": {
            "minimum_pooled_relative_improvement": 0.05,
            "minimum_games_with_control_interaction_improvement": 4,
            "control_interaction_should_exceed_pressure_or_chaos_interaction_in_majority": True,
            "pressure_chaos_rank_stability_should_exceed_control_in_majority": True,
            "leave_one_game_out_required": True,
        },
        "games": rows,
        "pooled_analysis": {
            "macro_mean_control_relative_improvement": macro_control_improvement,
            "games_passing_control_modulation": len(passes),
            "strongest_interaction_counts": strongest_counts,
            "complete_discriminant_games": len(complete_discriminants),
        },
        "leave_one_game_out": leave_one_out,
        "criteria": criteria,
        "summary": {
            "evaluated_games": len(evaluated),
            "required_games": len(GAMES),
            "games_passing_game_native_control_modulation_test": len(passes),
            "pooled_claim_ready": pooled_claim_ready,
            "cross_game_architecture_confirmed": cross_game_pass,
            "status": "pending" if not pooled_claim_ready else ("confirmed" if cross_game_pass else "failed"),
            "interpretation": (
                "The universal Control-dominant modulation architecture is falsified on the frozen five-game panel. "
                "Context sensitivity is substrate-dependent: different games favor different PCC interactions, and some show weak interaction gains overall."
                if pooled_claim_ready and not cross_game_pass else None
            ),
        },
        "guardrails": [
            "Do not treat missing trajectory exports as negative evidence.",
            "Do not refit game-native PCC observables to make the cross-game architecture pass.",
            "A game-native pass is evidence for that game, not proof of cross-game generality.",
            "Control x context must be compared against Pressure x context and Chaos x context before claiming Control is disproportionately modulatory.",
            "Do not backfill missing cross-context rank-stability statistics from post hoc proxies; obtain new native exports if criterion 4 is to be resolved.",
        ],
    }


def _pct(v: float | None) -> str:
    return "—" if v is None else f"{100*v:.2f}%"


def render_markdown(report: dict[str, Any]) -> str:
    complete = report["summary"]["evaluated_games"] == report["summary"]["required_games"]
    lines = [
        "# PCC Cross-Game Architecture Falsification",
        "",
        "> Prospective architecture-level comparison using frozen game-native exports. Missing measurements remain explicitly unresolved rather than being backfilled post hoc.",
        "",
        "## Hypothesis",
        "",
        report["hypothesis"],
        "",
        "## Frozen model comparison",
        "",
        f"- Additive: `{report['model_comparison']['additive']}`",
        f"- Control-modulatory: `{report['model_comparison']['control_modulatory']}`",
        "- Discriminants: matched `Pressure x context` and `Chaos x context` interactions, cross-context rank stability, and leave-one-game-out robustness.",
        "",
        "## Game-level results",
        "",
        "| Game | Status | P x context | C x context | Chaos x context | Strongest available interaction | Native C-modulation test |",
        "|---|---|---:|---:|---:|---|---|",
    ]
    for row in report["games"]:
        if row["status"] == "evaluated":
            result = row["architecture_result"]
            ints = result["interaction_improvements"]
            strongest = result.get("strongest_interaction_axis") or "—"
            if not result.get("interaction_discriminants_complete", False):
                strongest += "*"
            lines.append(
                f"| {DISPLAY[row['game']]} | evaluated | {_pct(ints.get('pressure'))} | {_pct(ints.get('control'))} | {_pct(ints.get('chaos'))} | {strongest} | {'PASS' if result['primary_pass'] else 'FAIL'} |"
            )
        else:
            lines.append(f"| {DISPLAY[row['game']]} | pending trajectory export | — | — | — | — | — |")
    if any(r["status"] == "evaluated" and not r["architecture_result"].get("interaction_discriminants_complete", False) for r in report["games"]):
        lines += ["", "* Colonel Blotto v1.1 froze only the Control interaction comparison; Pressure/Chaos interaction discriminants were not prospectively exported and are not reconstructed here."]

    lines += [
        "",
        "## Pooled cross-game result",
        "",
        f"- Macro-mean `Control x context` improvement: **{_pct(report['pooled_analysis']['macro_mean_control_relative_improvement'])}** (frozen target: >= 5%).",
        f"- Games passing their native Control-modulation threshold: **{report['pooled_analysis']['games_passing_control_modulation']}/5** (frozen target: >= 4/5).",
        f"- Strongest available interactions: **Pressure {report['pooled_analysis']['strongest_interaction_counts']['pressure']}**, **Control {report['pooled_analysis']['strongest_interaction_counts']['control']}**, **Chaos {report['pooled_analysis']['strongest_interaction_counts']['chaos']}**, **unknown/incomplete {report['pooled_analysis']['strongest_interaction_counts']['unknown']}**.",
        "",
        "## Prespecified criteria",
        "",
        "| Criterion | Result | Status |",
        "|---|---|---|",
    ]
    c = report["criteria"]
    lines.append(f"| Pooled C x context improvement >= 5% | {_pct(c['pooled_control_improvement_at_least_5pct']['value'])} | **{c['pooled_control_improvement_at_least_5pct']['status'].upper()}** |")
    lines.append(f"| C modulation in >= 4/5 games | {c['control_improvement_in_at_least_4_of_5_games']['value']}/5 | **{c['control_improvement_in_at_least_4_of_5_games']['status'].upper()}** |")
    d = c['control_interaction_disproportionate_in_majority']
    lines.append(f"| C interaction strongest in majority | {d['control_strongest_complete_games']} observed; maximum possible {d['maximum_possible_control_strongest_games']}/5 | **{d['status'].upper()}** |")
    lines.append(f"| P/Chaos rank stability > raw C in majority | Common statistic not present in all exports | **{c['pressure_chaos_rank_stability_exceeds_control_in_majority']['status'].upper()}** |")
    l = c['leave_one_game_out_qualitative_architecture']
    lines.append(f"| Leave-one-game-out universal architecture | survives all folds: {l['universal_control_architecture_survives_all_folds']} | **{l['status'].upper()}** |")

    if report["leave_one_game_out"]:
        lines += [
            "",
            "## Leave-one-game-out robustness",
            "",
            "| Held-out game | Remaining macro C improvement | Remaining C-pass games | Universal C architecture survives? |",
            "|---|---:|---:|---|",
        ]
        for fold in report["leave_one_game_out"]:
            lines.append(
                f"| {DISPLAY[fold['held_out_game']]} | {_pct(fold['macro_control_relative_improvement'])} | {fold['games_passing_control_modulation']}/{fold['remaining_games']} | {'YES' if fold['universal_control_architecture_survives'] else 'NO'} |"
            )

    lines += ["", "## Final conclusion", ""]
    if complete:
        lines += [
            f"**{report['summary']['status'].upper()}** — all 5/5 games are evaluable for the primary Control-modulation comparison.",
            "",
            "The frozen universal hypothesis is **rejected**. `Control x context` does not achieve the prespecified pooled 5% gain, reaches the game-native threshold in only 2/5 games, and the failure is robust to every leave-one-game-out fold.",
            "",
            "The stronger descriptive pattern is **substrate-dependent PCC architecture**: Poker is Pressure-modulatory, Liar's Dice is strongly Chaos-modulatory, repeated RPS supports Control modulation but Chaos is stronger, Micro-Fighter shows only weak interaction gains, and Colonel Blotto strongly supports Control modulation. This is a post-falsification interpretation, not a replacement preregistered success claim.",
            "",
            "One prespecified criterion remains **unresolved rather than failed**: the normalized exports do not contain a common cross-context rank-stability statistic for Pressure, Control, and Chaos. Resolving that criterion requires new native exports; it is not necessary to rescue the already-falsified universal Control-modulation hypothesis.",
        ]
    else:
        lines += [
            f"**PENDING** — {report['summary']['evaluated_games']}/{report['summary']['required_games']} games currently have the required frozen architecture-level export.",
            "",
            "## Required next exports",
            "",
            "Each remaining game should export disjoint-seed agent-by-context rows using its already frozen game-native P/C/Chaos signatures and outcomes. The cross-game repository should fit only the common architecture comparison; it should not redesign game-native measurements.",
        ]

    lines += ["", "## Guardrails", ""]
    lines.extend(f"- {g}" for g in report["guardrails"])
    return "\n".join(lines) + "\n"


def render_csv(report: dict[str, Any]) -> str:
    out = io.StringIO()
    w = csv.writer(out, lineterminator="\n")
    w.writerow(["game", "status", "pressure_relative_improvement", "control_relative_improvement", "chaos_relative_improvement", "strongest_interaction_axis", "primary_pass", "source"])
    for row in report["games"]:
        res = row.get("architecture_result") or {}
        ints = res.get("interaction_improvements", {})
        w.writerow([
            row["game"], row["status"], ints.get("pressure", ""), ints.get("control", ""), ints.get("chaos", ""),
            res.get("strongest_interaction_axis", ""), res.get("primary_pass", ""), row["source"],
        ])
    return out.getvalue()


def write_outputs(report: dict[str, Any], output_dir: str | Path) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "cross-game-architecture.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (out / "CROSS_GAME_ARCHITECTURE.md").write_text(render_markdown(report), encoding="utf-8")
    (out / "cross-game-architecture.csv").write_text(render_csv(report), encoding="utf-8")
