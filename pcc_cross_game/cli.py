from __future__ import annotations
import argparse
import json
from .compare import build_comparison, write_outputs
from .control_benchmark import build_control_benchmark, write_outputs as write_control_outputs
from .chaos_benchmark import build_chaos_benchmark, write_outputs as write_chaos_outputs
from .control_template import build_control_template_benchmark, write_outputs as write_control_template_outputs
from .pressure_template import build_pressure_template_benchmark, write_outputs as write_pressure_template_outputs
from .theory_status import build_theory_status, write_outputs as write_theory_status_outputs
from .architecture_falsification import build_architecture_falsification, write_outputs as write_architecture_outputs


def main() -> int:
    p = argparse.ArgumentParser(description="Compare frozen PCC game-validation evidence")
    p.add_argument("--poker-root", required=True)
    p.add_argument("--liars-root", required=True)
    p.add_argument("--rps-root")
    p.add_argument("--micro-root")
    p.add_argument("--blotto-root")
    p.add_argument("--output-dir", default="validation")
    p.add_argument("--control-benchmark", action="store_true", help="also write the cross-game Control mechanism benchmark")
    p.add_argument("--chaos-benchmark", action="store_true", help="also write the cross-game Chaos measurement benchmark")
    p.add_argument("--control-template", action="store_true", help="also write the cross-game Control structural-template benchmark")
    p.add_argument("--pressure-template", action="store_true", help="also write the cross-game Pressure structural-template benchmark")
    p.add_argument("--theory-status", action="store_true", help="also write the canonical PCC cross-game theory/status report")
    p.add_argument("--architecture-falsification", action="store_true", help="write the state-axes-vs-Control-modulation architecture status report")
    args = p.parse_args()
    report = build_comparison(args.poker_root, args.liars_root, args.rps_root, args.micro_root, args.blotto_root)
    write_outputs(report, args.output_dir)
    if args.control_benchmark:
        control = build_control_benchmark(args.poker_root, args.liars_root, args.rps_root)
        write_control_outputs(control, args.output_dir)
    if args.chaos_benchmark:
        chaos = build_chaos_benchmark(args.poker_root, args.liars_root, args.rps_root, args.micro_root)
        write_chaos_outputs(chaos, args.output_dir)
    if args.control_template:
        template = build_control_template_benchmark(args.poker_root, args.liars_root, args.rps_root, args.micro_root)
        write_control_template_outputs(template, args.output_dir)
    if args.pressure_template:
        pressure = build_pressure_template_benchmark(args.poker_root, args.liars_root, args.rps_root, args.micro_root)
        write_pressure_template_outputs(pressure, args.output_dir)
    if args.theory_status:
        theory = build_theory_status(".")
        write_theory_status_outputs(theory, args.output_dir)
    if args.architecture_falsification:
        architecture = build_architecture_falsification(".")
        write_architecture_outputs(architecture, args.output_dir)
    print(json.dumps({"games": [g["game"] for g in report["games"]], "findings": len(report["cross_game_findings"]), "output_dir": args.output_dir}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
