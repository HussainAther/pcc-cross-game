from __future__ import annotations
import argparse
import json
from .compare import build_comparison, write_outputs


def main() -> int:
    p = argparse.ArgumentParser(description="Compare frozen PCC game-validation evidence")
    p.add_argument("--poker-root", required=True)
    p.add_argument("--liars-root", required=True)
    p.add_argument("--rps-root")
    p.add_argument("--output-dir", default="validation")
    args = p.parse_args()
    report = build_comparison(args.poker_root, args.liars_root, args.rps_root)
    write_outputs(report, args.output_dir)
    print(json.dumps({"games": [g["game"] for g in report["games"]], "findings": len(report["cross_game_findings"]), "output_dir": args.output_dir}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
