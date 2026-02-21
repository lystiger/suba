# Submarine Simulation App - Phase 1 Implementation Guide

## 1. Project Overview

### Objective
Build a Digital Twin simulation that bridges theoretical math outputs with real-time 3D visualization for submarine hull optimization and automatic steering validation.

### Focus
- Base Case: optimal environment for baseline validation.
- Real Case: noisy, current-affected lake conditions for robustness testing.

## 2. Data Contract (Math-App Bridge)

All partner-to-app communication must use a structured JSON payload.

```json
{
  "hull_geometry": {
    "length_m": 3.05,
    "max_diameter_m": 0.54,
    "fin_offset_x": -1.2,
    "naca_profile": "0009"
  },
  "physics_state": {
    "velocity_ms": 2.5,
    "pitch_deg": 2.1,
    "yaw_deg": 0.0,
    "depth_m": 4.5
  },
  "steering_output": {
    "target_fin_angle_deg": 12.5,
    "motor_torque_nm": 5.6
  },
  "environment": {
    "fluid_density_kgm3": 1025.0,
    "current_vector_ms": [0.1, 0.05, 0.0],
    "sensor_noise_sigma": 0.02
  }
}
```

## 3. Technical Roadmap (1 Month)

### Week 1 - Parametric Hull Generation (Open3D)
- Deliverable: Python module that generates a submarine mesh from input parameters.
- Inputs: `length_m`, `max_diameter_m`, fin surface configuration.
- Method: Generate hull profile points (Myring/prolate spheroid approach), then reconstruct a triangle mesh.

### Week 2 - Physics and Friction Layer
- Deliverable: Real-time force calculations integrated with scene updates.
- Core equation:
  - `F_drag = 0.5 * rho * v^2 * C_d * A`
- Visualization:
  - Render drag vectors in-scene.
  - Scale vector magnitude with computed drag.

### Week 3 - Sensor Noise and Real Environment Toggle
- Deliverable: Environment mode switch plus controllable error injection.
- Flow:
  1. Compute clean state from physics layer.
  2. Inject Gaussian noise using `sensor_noise_sigma`.
  3. Feed noisy state to steering logic for robustness evaluation.

### Week 4 - Unity Migration and Buoyancy Setup
- Deliverable: Unity base scene with imported optimized hull.
- Focus areas:
  - Center of Gravity (CG) vs Center of Buoyancy (CB) behavior.
  - Validation of stability response under base and real conditions.

## 4. App Architecture (Phase 1 / Python + Open3D)

- `SubmarineApp`
  - Orchestrates update loop, component wiring, and frame lifecycle.
- `MathIngestor`
  - Loads and validates JSON payloads from the math partner.
- `HullGenerator`
  - Builds/updates hull mesh and exposes geometric properties (area, volume).
- `PhysicsEngine`
  - Computes drag, buoyancy, and environment-induced perturbations.
- `UIController`
  - Handles sliders, scenario toggles, and noise-control inputs.

## 5. Constraint Validation Rules

The app must reject or clamp commands that violate physical constraints.

- Torque Limit
  - If hydrodynamic resistance torque exceeds motor capability, cap fin angle command.
- Cavitation Risk Check
  - Raise warning when speed/depth combinations exceed cavitation-safe thresholds.
- Stability Check
  - Raise warning when metacentric height (`GM`) becomes negative.

## 6. Phase 1 Deliverables

- Open3D prototype script with parametric hull updates.
- Physics overlay for drag and buoyancy indicators.
- Environment toggle with configurable sensor noise/current.
- Constraint report logs for torque, cavitation, and stability outcomes.
- Unity starter scene prepared for water reconstruction in Phase 2.
