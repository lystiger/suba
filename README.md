# suba

Phase 1 submarine simulation starter project.

## Overview

This project loads a simulation case from JSON, validates the input contract, runs a lightweight physics step loop, and writes telemetry to CSV.

Who this is for:
- If you are new to programming, treat this as a small pipeline: read input -> compute values -> save output.
- Most code is intentionally simple and split into small files with one responsibility each.

Core flow:
1. Load and validate case data (`data/*.json`) with `MathIngestor`.
2. Build/update hull geometry from the case values.
3. Run physics updates (drag, buoyancy, torque margin, cavitation/stability indicators).
4. Save telemetry output to `logs/*.csv`.

The code is organized in:
- `src/submarine_sim/`: simulation package (app, physics, ingestion, UI controller, Open3D UI).
- `scripts/`: runnable entrypoints for CLI, text UI, and GUI.
- `schemas/`: JSON schema contract for phase 1 input.
- `data/`: example simulation cases.

## Beginner File Guide

- `src/submarine_sim/models.py`: data shapes used across the app (think "input fields grouped into objects").
- `src/submarine_sim/math_ingestor.py`: reads JSON and checks values are safe/valid.
- `src/submarine_sim/hull_generator.py`: creates simple hull geometry and area/volume values.
- `src/submarine_sim/physics_engine.py`: formulas for drag, buoyancy, steering torque, and simple safety checks.
- `src/submarine_sim/app.py`: coordinator that connects all modules and stores telemetry rows.
- `src/submarine_sim/ui_controller.py`: small interface used by CLI/text UI/GUI to call app functions.
- `scripts/run_phase1.py`: one-shot command line run.
- `scripts/run_phase1_ui.py`: text-based UI (one-shot or interactive loop).
- `scripts/run_phase1_gui.py` + `src/submarine_sim/open3d_ui.py`: desktop GUI using Open3D.

## Simple Setup (macOS)

```bash
# optional but recommended on a new Mac
xcode-select --install

# create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# upgrade packaging tools
python -m pip install --upgrade pip setuptools wheel

# install project dependencies
pip install -r requirements.txt
```

If `python3` is not found, install Python 3 first (for example via Homebrew: `brew install python`), then rerun the commands above.

## Simple Setup (Windows)

Use PowerShell:

```powershell
# create and activate virtual environment
py -3 -m venv venv
.\venv\Scripts\Activate.ps1

# upgrade packaging tools
python -m pip install --upgrade pip setuptools wheel

# install project dependencies
pip install -r requirements.txt
```

If script execution is blocked in PowerShell, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Run

Run a basic simulation (writes CSV report):

```bash
python3 scripts/run_phase1.py --case data/base_case.json --steps 5 --mode base --report logs/phase1_report.csv
```

Run text UI once:

```bash
python3 scripts/run_phase1_ui.py --case data/base_case.json --mode base --steps 5
```

Run interactive text UI:

```bash
python3 scripts/run_phase1_ui.py --interactive
```

Run Open3D GUI:

```bash
python3 scripts/run_phase1_gui.py
```

Windows equivalents:

```powershell
py -3 scripts/run_phase1.py --case data/base_case.json --steps 5 --mode base --report logs/phase1_report.csv
py -3 scripts/run_phase1_ui.py --case data/base_case.json --mode base --steps 5
py -3 scripts/run_phase1_ui.py --interactive
py -3 scripts/run_phase1_gui.py
```

macOS note:
- If the GUI does not open on first try, run the CLI/UI commands first to confirm dependencies are installed correctly, then retry the GUI.

## Input Contract

- Schema: `schemas/phase1_contract.schema.json`
- Example cases: `data/base_case.json`, `data/real_case.json`
