from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HullGeometry:
    length_m: float
    max_diameter_m: float
    fin_offset_x: float
    naca_profile: str
    fin_surface_area_m2: float


@dataclass
class PhysicsState:
    velocity_ms: float
    pitch_deg: float
    yaw_deg: float
    depth_m: float


@dataclass
class SteeringOutput:
    target_fin_angle_deg: float
    motor_torque_nm: float


@dataclass
class Environment:
    fluid_density_kgm3: float
    current_vector_ms: list[float]
    sensor_noise_sigma: float


@dataclass
class SimulationInput:
    hull_geometry: HullGeometry
    physics_state: PhysicsState
    steering_output: SteeringOutput
    environment: Environment
