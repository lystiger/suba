# UI Design Specification - Submarine Control and Simulation Station

## 1. Design Philosophy

- Functional Minimalism
  - Prioritize readability and operator focus over decorative styling.
- Telemetry First
  - Every visual behavior in the 3D viewport must have a corresponding numeric readout.
- State-Based Color Coding
  - Green: within constraints.
  - Yellow: approaching limits.
  - Red: constraint violation or failure state.

## 2. Layout Structure

- Center (Viewport)
  - 3D Open3D/Unity render of hull, orientation, and force vectors.
- Left Sidebar (Inputs)
  - Real-time parameter controls (geometry and motion inputs).
- Right Sidebar (Telemetry)
  - Live physics and steering metrics.
- Bottom Bar (Environment and Safety)
  - Scenario toggles, noise/current controls, and emergency actions.

## 3. UI Components and Interactions

### A. Force Vector Overlay (Viewport)
- Blue Arrow (Nose): Drag force (`F_drag`), scaled by magnitude.
- Yellow Arrow (Center): Buoyancy force (`F_buoyancy`), upward direction.
- White Arrows (Fins): Lift/steering vectors tied to fin commands and flow conditions.

### B. Input Controls (Left Sidebar)
- Geometry
  - `length_m`
  - `max_diameter_m`
  - `fin_surface_area_m2`
- Motion and Steering
  - `velocity_ms`
  - `target_fin_angle_deg`
- Simulation Rate
  - Update frequency target (30-60 FPS equivalent loop pacing).

### C. Telemetry Dashboard (Right Sidebar)
- Forces
  - `F_drag`
  - `F_buoyancy`
- State
  - Depth, pitch, roll, yaw
- Steering Quality
  - Commanded fin angle vs actual fin angle
  - Error delta trend (small rolling graph)
- Constraint Status
  - Torque margin
  - Cavitation risk flag
  - Stability status (`GM` sign and threshold zone)

### D. Environment Controls (Bottom Bar)
- Fluid Preset
  - Fresh water (`rho = 1000 kg/m^3`)
  - Salt water (`rho = 1025 kg/m^3`)
- Current Vector
  - XY controls for direction and magnitude.
- Noise Injection
  - Gaussian sensor noise slider (`0%` to `10%`).
- Emergency Surface
  - Immediate override action for safety scenario testing.

## 4. UI States and Transitions

### Base Case
- Clean, stable vector behavior.
- Neutral/normal color theme for all telemetry values.

### Real Environment
- Minor telemetry fluctuation from injected noise/current.
- Visible vector jitter consistent with sensor uncertainty.

### Failure Mode
- Red-highlighted constraint panel and persistent alert text.
- Example alerts:
  - `TORQUE LIMIT EXCEEDED`
  - `CAVITATION RISK`
  - `NEGATIVE GM - INSTABILITY`

## 5. Technical Implementation Guidance

### Open3D Phase (Phase 1)
- Use `open3d.visualization.gui` for panels, controls, and status displays.
- Keep UI update cycle synchronized with physics tick to avoid stale readouts.
- Separate view state (UI) from simulation state (domain classes) through a controller boundary.

### Unity Phase (Phase 2 Transition)
- Use UI Toolkit (`UIElements`) for responsive layout and scalable dashboards.
- Keep naming parity between Open3D and Unity UI fields to reduce migration friction.
- Preserve the same state model and alert semantics across engines.
