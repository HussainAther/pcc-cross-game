from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any

MECHANISMS = (
    "raw_unpredictability_signal",
    "value_or_performance_guardrail",
    "exploitability_or_plausibility_guardrail",
    "cross_family_construct_recovery",
    "latent_intent_identifiability",
)


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_chaos_benchmark(poker_root: str | Path, liars_root: str | Path, rps_root: str | Path, micro_root: str | Path | None = None) -> dict[str, Any]:
    poker_root, liars_root, rps_root = map(Path, (poker_root, liars_root, rps_root))
    poker = _load(poker_root / "validation/effective-chaos-validation.json")
    liars_construct = _load(liars_root / "validation/construct-recovery.json")
    liars_mech = _load(liars_root / "validation/control-chaos-mechanism.json")
    rps = _load(rps_root / "validation/effective-chaos-falsification.json")

    poker_positive = all(
        data.get("effective_surprisal_weight_correlations", {}).get("chaos", 0) >= 0.20
        for data in poker.get("families", {}).values()
    )
    poker_discriminant = bool(poker.get("prespecified_checks", {}).get("all_families_discriminant", False))
    poker_floor = bool(poker.get("prespecified_checks", {}).get("value_floor_noninferior_in_all_families", False))

    liars_chaos = {
        fam: bool(data.get("axis_checks", {}).get("chaos"))
        and all(bool(v) for v in data.get("axis_checks", {}).get("chaos", {}).values())
        for fam, data in liars_construct.get("families", {}).items()
    }
    liars_plausibility = {
        fam: bool(data.get("pathways", {}).get("chaos_lower_bid_plausibility_supported", False))
        for fam, data in liars_mech.get("families", {}).items()
    }
    liars_floor_present = "performance-adequacy" in str(liars_construct.get("candidate_observables", {}).get("chaos", ""))

    rps_falsification = {
        fam: bool(data.get("falsification_checks_passed", False))
        for fam, data in rps.get("families", {}).items()
    }
    rps_recovery = {
        fam: bool(data.get("engineered_chaos_exceeds_neutral", False))
        for fam, data in rps.get("families", {}).items()
    }

    games = {
        "poker": {
            "raw_unpredictability_signal": {
                "status": "partial" if poker_positive and not poker_discriminant else ("confirmed" if poker_discriminant else "failed"),
                "basis": "effective surprisal is positively Chaos-related in both families but fails the frozen off-axis discriminant criterion",
            },
            "value_or_performance_guardrail": {
                "status": "confirmed" if poker_floor else "failed",
                "basis": "independent value floor is noninferior in both families and improves the discriminant margin in at least one family",
            },
            "exploitability_or_plausibility_guardrail": {
                "status": "unresolved",
                "basis": "the frozen poker study uses an independent value floor, not an explicit exploitability probe",
            },
            "cross_family_construct_recovery": {
                "status": "failed" if not poker.get("effective_chaos_construct_confirmed", False) else "confirmed",
                "basis": "frozen effective-Chaos construct criterion is not confirmed across both poker policy families",
            },
            "latent_intent_identifiability": {
                "status": "unresolved",
                "basis": "the poker protocol validates behavioral constructs and does not claim latent strategic intent is identifiable from actions alone",
            },
        },
        "liars-dice": {
            "raw_unpredictability_signal": {
                "status": "confirmed" if liars_chaos and all(liars_chaos.values()) else "failed",
                "basis": "public-state-conditioned Chaos candidate passes all preregistered recovery checks in both independent families",
            },
            "value_or_performance_guardrail": {
                "status": "confirmed" if liars_floor_present and liars_chaos and all(liars_chaos.values()) else "partial",
                "basis": "Chaos candidate includes an independent aggregate performance-adequacy floor and recovers cross-family",
            },
            "exploitability_or_plausibility_guardrail": {
                "status": "warning-confirmed" if liars_plausibility and all(liars_plausibility.values()) else "partial",
                "basis": "engineered Chaos has lower bid truth-plausibility in both families, showing a replicated value/plausibility cost that the measurement must guard against",
            },
            "cross_family_construct_recovery": {
                "status": "confirmed" if liars_chaos and all(liars_chaos.values()) else "failed",
                "basis": "frozen factorial construct-recovery experiment confirms the Chaos axis in both families",
            },
            "latent_intent_identifiability": {
                "status": "unresolved",
                "basis": "behavioral recovery does not establish that the same observed pattern uniquely identifies latent strategic intent",
            },
        },
        "rps": {
            "raw_unpredictability_signal": {
                "status": "failed",
                "basis": "marginal entropy is approximately maximal for both iid-neutral and engineered Chaos and is therefore non-discriminating",
            },
            "value_or_performance_guardrail": {
                "status": "confirmed" if rps.get("effective_unpredictability_falsification_passed", False) else "failed",
                "basis": "conditional entropy weighted by resistance to exploitation passes all frozen falsification checks in both families",
            },
            "exploitability_or_plausibility_guardrail": {
                "status": "confirmed" if rps_falsification and all(rps_falsification.values()) else "failed",
                "basis": "fixed-marginal and online first-order exploiters penalize temporally predictable Chaos policies while leaving iid-neutral nearly unexploitable",
            },
            "cross_family_construct_recovery": {
                "status": "failed" if not (rps_recovery and all(rps_recovery.values())) else "confirmed",
                "basis": "engineered Chaos does not exceed iid-neutral effective unpredictability in either family",
            },
            "latent_intent_identifiability": {
                "status": "not-identifiable",
                "basis": "iid-uniform RPS is already maximally mixed, value-preserving, and minimally exploitable, so action-only data cannot distinguish strategic mixing intent from equivalent randomness",
            },
        },
    }

    if micro_root is not None:
        games["micro-fighter"] = {
            name: {
                "status": "unresolved",
                "basis": "Micro-Fighter has not yet run a frozen Chaos construct-recovery or effective-unpredictability benchmark; v0.8 evidence is currently Pressure/Control mechanistic only.",
            } for name in MECHANISMS
        }

    return {
        "schema_version": 1,
        "benchmark": "cross-game-chaos-measurement",
        "purpose": "Test which Chaos-measurement requirements survive across frozen games without retuning a game-specific scalar score.",
        "games": games,
        "portable_requirements": {
            "high_randomness_alone_is_sufficient": False,
            "effective_unpredictability_times_adequacy_template_supported": True,
            "value_or_performance_guardrail_required": True,
            "single_scalar_chaos_measure_confirmed_across_all_games": False,
            "latent_strategic_intent_identifiable_from_actions_alone": False,
        },
        "conclusion": {
            "status": "partial-generalization",
            "basis": "Across poker, Liar's Dice, and RPS, the portable structure is effective unpredictability = game-appropriate unpredictability × independent adequacy. Micro-Fighter remains intentionally unresolved for Chaos until its competitiveness and construct-recovery prerequisites mature.",
        },
        "guardrails": [
            "No source experiment is rerun or retuned by this benchmark.",
            "A confirmed guardrail is not the same as confirmed latent Chaos construct recovery.",
            "RPS iid-neutral is treated as a legitimate behavioral counterexample, not relabeled after seeing the result.",
            "The frozen PCC Poker v0.8.0 human-facing measurement contract is unchanged.",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    labels = {"poker": "Poker", "liars-dice": "Liar's Dice", "rps": "Repeated RPS", "micro-fighter": "Micro-Fighter"}
    lines = [
        "# Cross-Game Chaos Measurement Benchmark", "",
        "This benchmark compares frozen Chaos-measurement evidence without defining a universal scalar Chaos score.", "",
        "| Measurement requirement | Poker | Liar's Dice | Repeated RPS | Micro-Fighter |", "|---|---|---|---|---|",
    ]
    for mechanism in MECHANISMS:
        pretty = mechanism.replace("_", " ").title()
        vals = [report["games"][g][mechanism]["status"] for g in ("poker", "liars-dice", "rps", "micro-fighter") if g in report["games"]]
        lines.append(f"| {pretty} | " + " | ".join(vals) + " |")
    lines += ["", "## Cross-game conclusion", "", f"- {report['conclusion']['basis']}", ""]
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
    w.writerow(["game", "measurement_requirement", "status", "basis"])
    for game, mechanisms in report["games"].items():
        for name in MECHANISMS:
            item = mechanisms[name]
            w.writerow([game, name, item["status"], item["basis"]])
    return out.getvalue()


def write_outputs(report: dict[str, Any], output_dir: str | Path) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "chaos-measurement-benchmark.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (out / "CHAOS_MEASUREMENT_BENCHMARK.md").write_text(render_markdown(report), encoding="utf-8")
    (out / "chaos-measurement-benchmark.csv").write_text(render_csv(report), encoding="utf-8")
