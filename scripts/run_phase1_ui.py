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
    parser = argparse.ArgumentParser(description="Minimal Phase 1 simulation UI runner.")
    parser.add_argument("--case", default="data/base_case.json", help="Path to case JSON.")
    parser.add_argument("--mode", choices=["base", "real"], default="base", help="Environment mode.")
    parser.add_argument("--steps", type=int, default=5, help="Simulation steps.")
    parser.add_argument("--report", default="logs/phase1_report.csv", help="CSV report output path.")
    return parser.parse_args()


def _format_metric(name: str, value: float | bool | str) -> str:
    if isinstance(value, float):
        return f"{name}: {value:.3f}"
    return f"{name}: {value}"


def main() -> int:
    args = parse_args()
    app = SubmarineApp()
    ui = app.ui_controller

    ui.load_case(args.case)
    ui.set_environment_mode(args.mode)
    rows = ui.run_simulation(args.steps)
    ui.save_report(args.report)

    last = rows[-1] if rows else {}
    print("Phase 1 Simulation UI")
    print(f"case={args.case} mode={ui.state.environment_mode} steps={args.steps}")
    if last:
        print(
            " | ".join(
                [
                    _format_metric("drag_force_n", last["drag_force_n"]),
                    _format_metric("buoyancy_force_n", last["buoyancy_force_n"]),
                    _format_metric("torque_margin_nm", last["torque_margin_nm"]),
                    _format_metric("cavitation_risk", last["cavitation_risk"]),
                    _format_metric("stability_warning", last["stability_warning"]),
                ]
            )
        )

    summary = {
        "case": args.case,
        "mode": ui.state.environment_mode,
        "steps": args.steps,
        "rows_logged": len(rows),
        "report": args.report,
        "last_snapshot": last,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
