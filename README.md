# suba

Phase 1 submarine simulation starter project.

## Overview

This project loads a simulation case from JSON, validates the input contract, runs a lightweight physics step loop, and writes telemetry to CSV.

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

## Simple Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
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

## Input Contract

- Schema: `schemas/phase1_contract.schema.json`
- Example cases: `data/base_case.json`, `data/real_case.json`
