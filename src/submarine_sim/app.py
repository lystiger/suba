from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import csv

from .hull_generator import HullGenerator
from .math_ingestor import MathIngestor
from .physics_engine import PhysicsEngine
from .ui_controller import UIController


class SubmarineApp:
    def __init__(self) -> None:
        self.ingestor = MathIngestor()
        self.hull_generator = HullGenerator()
        self.physics_engine = PhysicsEngine()
        self.ui_controller = UIController()
        self.telemetry_rows: list[dict] = []

    def load_case(self, json_path: str | Path) -> None:
        payload = self.ingestor.load_json(json_path)
        self.ingestor.validate_constraints()
        self.hull_generator.update_hull(
            payload.hull_geometry.length_m,
            payload.hull_geometry.max_diameter_m,
            payload.hull_geometry.fin_surface_area_m2,
        )

    def update_scene(self) -> dict:
        payload = self.ingestor.current_params
        if payload is None:
            raise ValueError("No case loaded.")

        props = self.hull_generator.get_properties()
        cd = self.ingestor.get_drag_coefficient()
        sigma = payload.environment.sensor_noise_sigma if self.ui_controller.state.noise_enabled else 0.0

        snap = self.physics_engine.step(
            velocity_ms=payload.physics_state.velocity_ms,
            current_vector_ms=payload.environment.current_vector_ms,
            density_kgm3=payload.environment.fluid_density_kgm3,
            drag_coefficient=cd,
            area_m2=props.area_m2,
            volume_m3=props.volume_m3,
            target_fin_angle_deg=payload.steering_output.target_fin_angle_deg,
            fin_offset_m=payload.hull_geometry.fin_offset_x,
            motor_torque_nm=payload.steering_output.motor_torque_nm,
            depth_m=payload.physics_state.depth_m,
            length_m=payload.hull_geometry.length_m,
            diameter_m=payload.hull_geometry.max_diameter_m,
            sensor_noise_sigma=sigma,
        )

        row = asdict(snap)
        row["environment_mode"] = self.ui_controller.state.environment_mode
        self.telemetry_rows.append(row)
        return row

    def run(self, steps: int = 10) -> list[dict]:
        return [self.update_scene() for _ in range(steps)]

    def save_report(self, output_path: str | Path) -> None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not self.telemetry_rows:
            path.write_text("", encoding="utf-8")
            return

        fieldnames = list(self.telemetry_rows[0].keys())
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.telemetry_rows)
