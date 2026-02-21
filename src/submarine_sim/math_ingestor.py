from __future__ import annotations

import json
from pathlib import Path

from .models import Environment, HullGeometry, PhysicsState, SimulationInput, SteeringOutput


class MathIngestor:
    def __init__(self) -> None:
        self.current_params: SimulationInput | None = None

    def load_json(self, file_path: str | Path) -> SimulationInput:
        path = Path(file_path)
        data = json.loads(path.read_text(encoding="utf-8"))
        self.current_params = self._parse_and_validate(data)
        return self.current_params

    def validate_constraints(self) -> None:
        if self.current_params is None:
            raise ValueError("No parameters loaded.")

        p = self.current_params
        if p.physics_state.depth_m > 500.0:
            raise ValueError("Depth exceeds Phase 1 limit (500m).")
        if abs(p.steering_output.target_fin_angle_deg) > 35.0:
            raise ValueError("Target fin angle exceeds limit (+/-35deg).")

    def get_drag_coefficient(self) -> float:
        if self.current_params is None:
            raise ValueError("No parameters loaded.")

        base_cd = 0.2
        profile_adjustment = 0.0 if self.current_params.hull_geometry.naca_profile == "0009" else 0.03
        return base_cd + profile_adjustment

    def _parse_and_validate(self, data: dict) -> SimulationInput:
        hg = HullGeometry(**data["hull_geometry"])
        ps = PhysicsState(**data["physics_state"])
        so = SteeringOutput(**data["steering_output"])
        env = Environment(**data["environment"])

        if hg.length_m <= 0.0:
            raise ValueError("length_m must be > 0.")
        if hg.max_diameter_m <= 0.0:
            raise ValueError("max_diameter_m must be > 0.")
        if hg.fin_surface_area_m2 <= 0.0:
            raise ValueError("fin_surface_area_m2 must be > 0.")
        if ps.velocity_ms < 0.0:
            raise ValueError("velocity_ms must be >= 0.")
        if ps.depth_m < 0.0:
            raise ValueError("depth_m must be >= 0.")
        if so.motor_torque_nm <= 0.0:
            raise ValueError("motor_torque_nm must be > 0.")
        if len(env.current_vector_ms) != 3:
            raise ValueError("current_vector_ms must have 3 values.")
        if not 900.0 <= env.fluid_density_kgm3 <= 1300.0:
            raise ValueError("fluid_density_kgm3 out of range.")
        if not 0.0 <= env.sensor_noise_sigma <= 0.1:
            raise ValueError("sensor_noise_sigma out of range.")

        return SimulationInput(
            hull_geometry=hg,
            physics_state=ps,
            steering_output=so,
            environment=env,
        )
