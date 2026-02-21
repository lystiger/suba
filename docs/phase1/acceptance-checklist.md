# Phase 1 Acceptance Checklist

## Build Readiness
- [ ] `python3 scripts/run_phase1.py --case data/base_case.json` runs without exceptions.
- [ ] `python3 scripts/run_phase1.py --case data/real_case.json --mode real` runs without exceptions.
- [ ] `logs/phase1_report.csv` is generated.

## Contract Validation
- [ ] Invalid JSON payloads are rejected by `MathIngestor`.
- [ ] Depth > 500m is rejected.
- [ ] Fin angle magnitude > 35deg is rejected.

## Physics Outputs
- [ ] Drag force (`drag_force_n`) is non-negative.
- [ ] Buoyancy force (`buoyancy_force_n`) is non-negative.
- [ ] Torque margin decreases when velocity/current increases.

## Scenario Behavior
- [ ] Base mode uses zero noise.
- [ ] Real mode enables noise and affects effective velocity/force values.
- [ ] Cavitation risk flag can trigger under shallow + high speed.

## Logging
- [ ] Output CSV contains fields defined in `docs/phase1/output-spec.md`.
- [ ] At least one row per simulation step is recorded.
