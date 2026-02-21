#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from submarine_sim import SubmarineApp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 1 submarine simulation starter.")
    parser.add_argument("--case", default="data/base_case.json", help="Path to case JSON.")
    parser.add_argument("--steps", type=int, default=5, help="Simulation steps to run.")
    parser.add_argument("--mode", choices=["base", "real"], default="base", help="Environment mode.")
    parser.add_argument("--report", default="logs/phase1_report.csv", help="CSV report output path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    app = SubmarineApp()
    app.load_case(args.case)

    if args.mode == "real":
        app.ui_controller.toggle_environment_mode()

    rows = app.run(steps=args.steps)
    app.save_report(args.report)

    summary = {
        "case": args.case,
        "steps": args.steps,
        "mode": app.ui_controller.state.environment_mode,
        "last_snapshot": rows[-1] if rows else {},
        "report": args.report,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
