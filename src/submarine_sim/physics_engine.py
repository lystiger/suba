from __future__ import annotations

import math
import random
from dataclasses import dataclass


@dataclass
class PhysicsSnapshot:
    drag_force_n: float
    buoyancy_force_n: float
    effective_velocity_ms: float
    torque_required_nm: float
    torque_margin_nm: float
    cavitation_risk: bool
    gm_m: float
    stability_warning: bool


class PhysicsEngine:
    def __init__(self, gravity: float = 9.81) -> None:
        self.gravity = gravity
        self.water_density = 1000.0
        self.current_strength = 0.0
        self.noise_factor = 0.0

    def calculate_drag(self, velocity_ms: float, drag_coefficient: float, area_m2: float, density_kgm3: float) -> float:
        return 0.5 * density_kgm3 * velocity_ms * velocity_ms * drag_coefficient * area_m2

    def calculate_buoyancy(self, volume_m3: float, density_kgm3: float) -> float:
        return density_kgm3 * self.gravity * volume_m3

    def apply_environmental_noise(self, value: float, sigma: float) -> float:
        if sigma <= 0.0:
            return value
        return value + random.gauss(0.0, sigma * max(abs(value), 1e-6))

    def evaluate_steering_feasibility(
        self,
        velocity_ms: float,
        drag_force_n: float,
        target_fin_angle_deg: float,
        fin_offset_m: float,
        motor_torque_nm: float,
    ) -> tuple[float, float]:
        angle_ratio = min(abs(target_fin_angle_deg) / 35.0, 1.0)
        torque_required = drag_force_n * abs(fin_offset_m) * angle_ratio
        return torque_required, motor_torque_nm - torque_required

    def cavitation_check(self, depth_m: float, velocity_ms: float) -> bool:
        return depth_m < 2.0 and velocity_ms > 5.0

    def stability_check(self, length_m: float, diameter_m: float) -> float:
        # Simplified placeholder for Phase 1 checks.
        return (diameter_m * 0.2) - (length_m * 0.01)

    def step(
        self,
        *,
        velocity_ms: float,
        current_vector_ms: list[float],
        density_kgm3: float,
        drag_coefficient: float,
        area_m2: float,
        volume_m3: float,
        target_fin_angle_deg: float,
        fin_offset_m: float,
        motor_torque_nm: float,
        depth_m: float,
        length_m: float,
        diameter_m: float,
        sensor_noise_sigma: float,
    ) -> PhysicsSnapshot:
        current_mag = math.sqrt(sum(c * c for c in current_vector_ms))
        effective_velocity = max(0.0, velocity_ms + current_mag)
        noisy_velocity = self.apply_environmental_noise(effective_velocity, sensor_noise_sigma)

        drag = self.calculate_drag(noisy_velocity, drag_coefficient, area_m2, density_kgm3)
        buoyancy = self.calculate_buoyancy(volume_m3, density_kgm3)

        torque_required, torque_margin = self.evaluate_steering_feasibility(
            noisy_velocity, drag, target_fin_angle_deg, fin_offset_m, motor_torque_nm
        )

        gm_m = self.stability_check(length_m, diameter_m)
        return PhysicsSnapshot(
            drag_force_n=drag,
            buoyancy_force_n=buoyancy,
            effective_velocity_ms=noisy_velocity,
            torque_required_nm=torque_required,
            torque_margin_nm=torque_margin,
            cavitation_risk=self.cavitation_check(depth_m, noisy_velocity),
            gm_m=gm_m,
            stability_warning=gm_m < 0.0,
        )
