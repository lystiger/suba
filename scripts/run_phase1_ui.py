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
    parser.add_argument("--interactive", action="store_true", help="Run interactive simulation prompt loop.")
    return parser.parse_args()


def _format_metric(name: str, value: float | bool | str) -> str:
    if isinstance(value, float):
        return f"{name}: {value:.3f}"
    return f"{name}: {value}"


def main() -> int:
    args = parse_args()
    if args.interactive:
        return run_interactive()
    return run_once(args.case, args.mode, args.steps, args.report)


def run_once(case: str, mode: str, steps: int, report: str) -> int:
    app = SubmarineApp()
    ui = app.ui_controller

    ui.load_case(case)
    ui.set_environment_mode(mode)
    rows = ui.run_simulation(steps)
    ui.save_report(report)

    last = rows[-1] if rows else {}
    print("Phase 1 Simulation UI")
    print(f"case={case} mode={ui.state.environment_mode} steps={steps}")
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
        "case": case,
        "mode": ui.state.environment_mode,
        "steps": steps,
        "rows_logged": len(rows),
        "report": report,
        "last_snapshot": last,
    }
    print(json.dumps(summary, indent=2))
    return 0


def _prompt(message: str, default: str) -> str:
    value = input(f"{message} [{default}]: ").strip()
    return value or default


def _prompt_steps(default: int) -> int:
    while True:
        value = _prompt("steps", str(default))
        try:
            steps = int(value)
        except ValueError:
            print("Invalid steps value. Enter an integer.")
            continue
        if steps <= 0:
            print("Steps must be > 0.")
            continue
        return steps


def _prompt_mode(default: str) -> str:
    while True:
        mode = _prompt("mode (base/real)", default).lower()
        if mode in {"base", "real"}:
            return mode
        print("Mode must be 'base' or 'real'.")


def run_interactive() -> int:
    print("Phase 1 Interactive Simulation UI")
    case = "data/base_case.json"
    mode = "base"
    steps = 5
    report = "logs/phase1_report.csv"

    while True:
        case = _prompt("case", case)
        mode = _prompt_mode(mode)
        steps = _prompt_steps(steps)
        report = _prompt("report", report)

        try:
            run_once(case, mode, steps, report)
        except Exception as exc:  # noqa: BLE001
            print(f"Simulation failed: {exc}")

        again = _prompt("run again? (y/n)", "n").lower()
        if again not in {"y", "yes"}:
            break

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
