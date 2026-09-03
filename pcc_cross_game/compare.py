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


def rps_summary(root: str | Path) -> dict[str, Any]:
    root = Path(root)
    result = _require(root, "validation/negative-control.json")
    families = result.get("families", {})
    pressure_checks = {
        family: all(bool(checks.get(name)) for name in (
            "pressure_absent_neutral",
            "pressure_absent_control",
            "pressure_absent_chaos",
        ))
        for family, data in families.items()
        for checks in [data.get("checks", {})]
    }
    control_pass = {
        family: bool(data.get("checks", {}).get("control_signal_exceeds_neutral"))
        for family, data in families.items()
    }
    chaos_pass = {
        family: bool(data.get("checks", {}).get("chaos_signal_exceeds_neutral"))
        for family, data in families.items()
    }
    return {
        "game": "rps",
        "source_version": "0.2.0 negative control + effective-Chaos falsification",
        "source_root": str(root),
        "balance": {
            "status": "not-applicable",
            "criterion": "Repeated RPS is used as a two-axis Control/Chaos negative-control laboratory; no Pressure topology is defined.",
            "cycle_required": False,
        },
        "axis_evidence": {
            "pressure": {
                "status": "absent-by-design",
                "selected_components": ["pressure_candidate == 0"],
                "basis": "Pressure is excluded by the environment design and remains exactly zero across neutral, Control-like, and Chaos-like policies in both families.",
                "family_pass": pressure_checks,
            },
            "control": {
                "status": "failed",
                "selected_components": ["control_candidate"],
                "basis": "The provisional Control observable exceeds neutral in only one of two independently coded families.",
                "family_pass": control_pass,
            },
            "chaos": {
                "status": "failed",
                "selected_components": ["chaos_candidate"],
                "basis": "The provisional entropy-style Chaos observable fails because iid-uniform neutral RPS is already maximally unpredictable.",
                "family_pass": chaos_pass,
            },
        },
        "mechanisms": [
            {
                "name": "Pressure absence negative control",
                "status": "confirmed" if pressure_checks and all(pressure_checks.values()) else "failed",
                "scope": "Pressure candidate remains exactly zero in both independently coded families.",
            },
            {
                "name": "Control observable recovery",
                "status": "partial" if any(control_pass.values()) and not all(control_pass.values()) else ("confirmed" if control_pass and all(control_pass.values()) else "failed"),
                "scope": "two-family repeated-RPS recovery test",
            },
            {
                "name": "entropy-style Chaos recovery",
                "status": "failed" if not (chaos_pass and all(chaos_pass.values())) else "confirmed",
                "scope": "negative result: entropy alone does not distinguish strategic unpredictability from iid-uniform randomness",
            },
        ],
        "negative_controls": {
            "status": "confirmed" if pressure_checks and all(pressure_checks.values()) else "failed",
            "note": "The environment deliberately omits strategic Pressure; the measurement layer must not hallucinate it.",
        },
        "frozen_result": {
            "negative_control_confirmed": bool(result.get("negative_control_confirmed")),
            "note": "The aggregate negative_control_confirmed flag is false because C/Chaos recovery also failed; Pressure absence itself passed in both families.",
        },
    }



def micro_fighter_summary(root: str | Path) -> dict[str, Any]:
    root = Path(root)
    balance = _require(root, "validation/competitiveness.json")
    pressure = _require(root, "validation/pressure-dominance-decomposition.json")
    threat = _require(root, "validation/threat-conversion-decomposition.json")
    counter = _require(root, "validation/control-counter-intervention-v0.5.0.json")
    recovery = _require(root, "validation/control-recovery-intervention-v0.7.0.json")
    retreat = _require(root, "validation/retreat-backfire-decomposition.json")
    chaos = _require(root, "validation/effective-chaos-validation-v0.9.0.json")
    strong_chaos = _require(root, "validation/strong-exploiter-chaos-validation-v1.0.0.json")

    pressure_rep = pressure.get("replicated_diagnostics", {})
    retreat_checks = retreat.get("prespecified_checks", {})
    return {
        "game": "micro-fighter",
        "source_version": "1.0.0 spatial mechanisms + strong Chaos falsification",
        "source_root": str(root),
        "balance": {
            "status": "failed" if not balance.get("competitiveness_confirmed") else "confirmed",
            "criterion": "all pairwise synthetic mechanism matchups must lie inside the frozen 30%-70% decisive-win-rate window in both independent families",
            "cycle_required": False,
            "failure_pattern": "multiple trivial-dominance matchups remain; construct recovery is intentionally blocked" if not balance.get("competitiveness_confirmed") else None,
        },
        "axis_evidence": {
            axis: {
                "status": "unresolved",
                "selected_components": [],
                "basis": "Micro-Fighter has mechanistic diagnostics but no frozen cross-family observational construct-recovery experiment yet.",
            } for axis in AXES
        },
        "mechanisms": [
            {
                "name": "spatial Pressure threat generation",
                "status": "confirmed" if all(pressure_rep.get(k, {}).get("replicated_expected_direction", False) for k in ("space_capture", "attack_opportunity_generation", "defensive_response_forcing")) else "partial",
                "scope": "space compression, attack-opportunity generation, and defensive-response forcing replicate across frozen Pressure matchups",
            },
            {
                "name": "Control defense-to-counter conversion",
                "status": "partial" if counter.get("target_matchup", {}).get("moved_toward_competitiveness", False) else "failed",
                "scope": "the prospectively justified public counter-window rule improved Family B Pressure-vs-Control but did not clear the frozen competitiveness gate",
            },
            {
                "name": "deterministic spatial retreat as Control",
                "status": "failed" if recovery.get("target_matchup", {}).get("moved_toward_competitiveness") is False else "partial",
                "scope": "the prospective sustained-threat retreat rule worsened Pressure-vs-Control and is retained as a negative intervention result",
            },
            {
                "name": "retreat-backfire decomposition",
                "status": "confirmed" if retreat_checks and all(retreat_checks.values()) else "partial",
                "scope": "retreat commonly forfeits initiative, often fails to create distance, invites immediate re-entry, and rarely preserves separation",
            },
            {
                "name": "damage conversion sufficiency",
                "status": "failed" if not pressure_rep.get("damage_conversion", {}).get("replicated_expected_direction", False) else "confirmed",
                "scope": "Pressure-generated threat volume does not universally convert into damage or victory; Family A Control is the counterexample",
            },
            {
                "name": "effective Chaos resistance to calibrated exploitation",
                "status": "confirmed" if strong_chaos.get("effective_chaos_resistance_supported", False) else "failed",
                "scope": "a stronger adaptive exploiter is calibrated only on predictable play, frozen, then effective Chaos preserves substantially more held-out value than predictable or random baselines",
            },
            {
                "name": "Chaos is not randomness",
                "status": "confirmed" if chaos.get("prespecified_checks") and all(chaos.get("prespecified_checks", {}).values()) else "partial",
                "scope": "the random baseline is more entropic but much less competitively adequate than the effective-Chaos candidate",
            },
        ],
        "negative_controls": {
            "status": "present",
            "note": "Prospective v0.5 and v0.7 Control interventions include one partial improvement and one retained negative result; no post-result tuning is used to relabel them.",
        },
    }


def colonel_blotto_summary(root: str | Path) -> dict[str, Any]:
    root = Path(root)
    pressure = _require(root, "validation/pressure-leverage-intervention.json")
    chaos = _require(root, "validation/chaos-exploiter-falsification.json")
    emergence = _require(root, "validation/emergent-learned-agents.json")
    modulation = _require(root, "validation/control-modulation.json")
    return {
        "game": "colonel-blotto",
        "source_version": "1.1.0 learned-agent architecture + mechanistic freeze",
        "source_root": str(root),
        "balance": {
            "status": "not-applicable",
            "criterion": "no universal dominance cycle is required; Blotto is used for resource-allocation mechanism and learned-agent architecture tests",
            "cycle_required": False,
        },
        "axis_evidence": {
            "pressure": {"status": "confirmed", "selected_components": ["targeted_leverage", "response_constriction"], "basis": "Matched intervention holds budget, expected value, and raw concentration approximately fixed while high-leverage targeting reduces viable responses by 48.0%."},
            "control": {"status": "partial", "selected_components": ["context_modulation"], "basis": "Control is stable but does not emerge as an independent PC3; Control x context improves held-out prediction by 15.04%, supporting a modulatory rather than orthogonal-axis interpretation."},
            "chaos": {"status": "confirmed", "selected_components": ["guarded_unpredictability", "exploit_resistance"], "basis": "Guarded Chaos retains 93.1% of uniform-random entropy while outperforming random allocation against a held-out learner by 0.294 payoff."},
        },
        "mechanisms": [
            {"name": "targeted-leverage Pressure", "status": "confirmed" if pressure.get("aggregate", {}).get("pairwise_reduction_rate") == 1.0 else "partial", "scope": "matched resource-allocation intervention"},
            {"name": "guarded Chaos under held-out exploitation", "status": "confirmed" if chaos.get("aggregate", {}).get("all_primary_checks_pass") else "failed", "scope": "held-out adaptive exploiter"},
            {"name": "learned-agent low-dimensional PCC-related structure", "status": "partial", "scope": "independently optimized agents; Pressure and Chaos align strongly with PCs, Control does not form an independent PC3"},
            {"name": "Control as context-dependent modulation", "status": "confirmed" if modulation.get("aggregate", {}).get("all_primary_checks_pass") else "failed", "scope": "leave-one-agent-out predictive comparison with disjoint signature/outcome seeds"},
        ],
        "negative_controls": {
            "status": "present",
            "note": "Raw concentration fails as Pressure in v0.5, strong temporal-order claims for Control fail in v0.2-v0.4, and these negative results are retained rather than retuned away.",
        },
        "emergent_architecture": {
            "latent_pcc_weights_in_generator": emergence["design"]["latent_pcc_weights_in_generator"],
            "first_three_pc_cumulative_variance": emergence["aggregate"]["first_three_pc_cumulative_variance"],
            "pressure_pc_correlation": emergence["aggregate"]["assigned_correlations"]["pressure"],
            "control_forced_pc_correlation": emergence["aggregate"]["assigned_correlations"]["control"],
            "chaos_pc_correlation": emergence["aggregate"]["assigned_correlations"]["chaos"],
            "control_context_relative_improvement": modulation["aggregate"]["relative_mae_improvement_from_control_interactions"],
        },
    }

def build_comparison(poker_root: str | Path, liars_root: str | Path, rps_root: str | Path | None = None, micro_root: str | Path | None = None, blotto_root: str | Path | None = None) -> dict[str, Any]:
    poker = poker_summary(poker_root)
    liars = liars_dice_summary(liars_root)
    games = [poker, liars]
    rps = rps_summary(rps_root) if rps_root is not None else None
    if rps is not None:
        games.append(rps)
    micro = micro_fighter_summary(micro_root) if micro_root is not None else None
    if micro is not None:
        games.append(micro)
    blotto = colonel_blotto_summary(blotto_root) if blotto_root is not None else None
    if blotto is not None:
        games.append(blotto)
    findings = [
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
    ]
    if rps is not None:
        findings.extend([
            {
                "finding": "Pressure absence is recoverable as a negative control",
                "status": "supported",
                "basis": "Repeated RPS excludes strategic Pressure by design and the Pressure candidate remains exactly zero for neutral, Control-like, and Chaos-like policies in both independent families.",
            },
            {
                "finding": "naive entropy is not a portable Chaos observable",
                "status": "supported",
                "basis": "Liar's Dice recovers Chaos under its frozen construct protocol, whereas repeated RPS shows that iid-uniform neutral play can be more entropic than the Chaos-like policies.",
            },
            {
                "finding": "the cross-game framework can represent an absent axis",
                "status": "supported",
                "basis": "RPS Pressure is recorded as absent-by-design rather than failed, unresolved, or confirmed, separating environmental absence from construct evidence.",
            },
        ])
    if micro is not None:
        findings.extend([
            {
                "finding": "PCC mechanisms can be probed in a spatial non-card environment",
                "status": "supported",
                "basis": "Micro-Fighter reproduces spatial Pressure threat-generation diagnostics and value-sensitive Control intervention effects without cards, dice, hidden information, or wagering.",
            },
            {
                "finding": "spatial Control is not equivalent to maximizing distance",
                "status": "supported",
                "basis": "The frozen retreat intervention worsens Control while the v0.8 decomposition shows frequent initiative forfeiture, ineffective displacement, rapid Pressure re-entry, and almost no persistent separation.",
            },
            {
                "finding": "Chaos is not randomness in spatial combat",
                "status": "supported",
                "basis": "Micro-Fighter's more-entropic random baseline is strategically much worse than the effective-Chaos candidate, and a calibrated held-out exploiter suppresses predictable play while effective Chaos preserves positive value.",
            },
            {
                "finding": "mechanistic support can precede construct recovery",
                "status": "supported",
                "basis": "Micro-Fighter contributes Pressure, Control, and strong effective-Chaos mechanism evidence while all three observational axes remain unresolved because no frozen cross-family construct-recovery gate has passed.",
            },
        ])
    if blotto is not None:
        findings.extend([
            {"finding": "resource-allocation Pressure depends on targeted leverage rather than concentration alone", "status": "supported", "basis": "Blotto v0.5 falsifies raw concentration while v0.6 shows a 48.0% viable-response reduction when concentration is redirected toward leverage-bearing fronts under matched value and concentration."},
            {"finding": "independently optimized agents can exhibit PCC-related structure without latent PCC generator weights", "status": "supported", "basis": "Blotto v1.0 learns agents under generic objectives/opponents; Pressure and Chaos align strongly with separate behavioral PCs while Control is stable but not an independent PC3."},
            {"finding": "Control may be better represented as contextual modulation than as an orthogonal axis", "status": "supported-in-blotto", "basis": "Blotto v1.1 Control x context interactions reduce leave-one-agent-out standardized MAE by 15.04%; cross-game generalization remains pending."},
        ])
    return {
        "schema_version": 6,
        "purpose": "Cross-game comparison of frozen synthetic evidence without assuming identical PCC topology or measurement validity across games.",
        "games": games,
        "cross_game_findings": findings,
        "guardrails": [
            "Do not infer human psychological states from synthetic-agent labels.",
            "Do not require a rock-paper-scissors cycle outside the game-specific protocol that defined it.",
            "Mechanism confirmation and observational construct recovery are distinct evidence classes.",
            "A cross-family confirmation in one game does not automatically transfer to another game.",
            "Missing or failed evidence is reported directly, not imputed or repaired from another game.",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    games = {g["game"]: g for g in report["games"]}
    ordered = [name for name in ("poker", "liars-dice", "rps", "micro-fighter", "colonel-blotto") if name in games]
    display = {"poker": "Poker", "liars-dice": "Liar's Dice", "rps": "Repeated RPS", "micro-fighter": "Micro-Fighter", "colonel-blotto": "Colonel Blotto"}
    lines = [
        "# PCC Cross-Game Evidence Matrix",
        "",
        "This report compares frozen synthetic evidence without assuming that topology or measurements transfer unchanged across games.",
        "",
        "| Dimension | " + " | ".join(display[name] for name in ordered) + " |",
        "|---|" + "---|" * len(ordered),
    ]
    lines.append("| Balance/topology | " + " | ".join(f"{games[name]['balance']['status']}: {games[name]['balance']['criterion']}" for name in ordered) + " |")
    for axis in AXES:
        cells=[]
        for name in ordered:
            ev=games[name]["axis_evidence"][axis]
            comp=", ".join(ev.get("selected_components", [])) or "none"
            cells.append(f"{ev['status']} ({comp})")
        lines.append(f"| {axis.title()} observational construct | " + " | ".join(cells) + " |")
    lines += ["", "## Mechanism evidence", ""]
    for name in ordered:
        game=games[name]
        lines.append(f"### {display[name]}")
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
