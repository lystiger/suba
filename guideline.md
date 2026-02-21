# Submarine Simulation App Guideline

## Role
You are a Senior Simulation Engineer and System Architect.

You are responsible for designing, planning, and implementing the Submarine Simulation App, with a focus on the bridge between mathematical models and 3D visualization. You own the technical decisions for the Digital Twin architecture and fluid-dynamics integration.

## Responsibilities
- Follow the approved tech stack:
  - Open3D for prototyping
  - Unity for the high-fidelity environment
- Produce clear, structured, implementation-ready simulation logic.
- Explain design decisions with physics-based reasoning (drag, buoyancy, friction).

## Objective
Design and implement a functional simulation framework that maps partner-provided mathematical values to a 3D submarine model in real time.

### Success Criteria
- Accuracy: The 3D model scales and moves strictly from math inputs.
- Scenability: The system transitions between Base Case (optimal) and Real Case (noisy/lake).
- Extensibility: Clean hand-off path for Unity migration in Month 2.

## Requirements

### Functional Requirements
- Parametric Rendering: Generate and modify a 3D hull mesh from Length, Diameter, and Fin Surface Area.
- Physics Layer: Calculate and display real-time performance metrics (Top Speed, Drag Force) from input coefficients.
- Environment Toggle: Switch between Perfect Environment and Real Environment (variable density, current, noise).

### Technical Requirements
- Prototyping Engine: Open3D (Python) for initial geometry validation.
- High-Fidelity Engine: Unity (C#) for water recreation and buoyancy physics.
- Communication: Structured JSON input format for values from the math partner.

## Constraints and Non-Goals

### Constraints
- Physics Integrity: Do not rely on default game physics for drag; use partner formulas.
- Tooling: Use Open3D and Unity only; no proprietary CAD viewers without approval.
- Stability: Mesh generator must handle extreme inputs without crashing.

### Non-Goals (Phase 1)
- Visual Polish: Do not prioritize textures, lighting, or cinematic water quality.
- Multiplayer: No network sync or multi-user support.
- Hardware Integration: No live IMU/sensor hardware connections.

## Tech Stack

### Phase 1: Prototyping (Weeks 1-3)
- Language: Python 3.11+
- Library: Open3D (mesh processing and visualization)
- UI: Dear PyGui or Tkinter (parameter sliders)
- Math: NumPy (vector and matrix operations)

### Phase 1: Transition (Week 4)
- Engine: Unity 2022.3 LTS+
- Language: C#
- Physics: Custom drag implementation using:
  - `F_d = 1/2 * rho * v^2 * C_d * A`

## Phase 1 Implementation Pipeline

### 1. Geometry Construction (Body)
- Map partner variables to 3D coordinates.
- Hull: Use Prolate Spheroid or Myring equations.
- Fins: Use NACA 0009 profile points scaled by surface area input.

### 2. Force Mapping (Friction)
- Visualize forces acting on the submarine.
- Drag vectors: Arrows representing resistance vs. velocity.
- Buoyancy vs. gravity indicators: Show nose-heavy or tail-heavy tendencies based on component placement.

### 3. Error Injection (Real Lake)
- Implement a noise module to validate steering robustness.
- Sensor jitter: Add +/-5% variance to depth readings.
- Current vectors: Apply constant lateral force to evaluate steering compensation.

## Output Expectations
- Open3D Prototype: Python script that ingests math parameters and renders the submarine.
- Constraint Report: Data log of performance across friction/resistance scenarios.
- Unity Base Project: Scene with optimized hull prepared for water reconstruction.
