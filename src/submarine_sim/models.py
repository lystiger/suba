"""Data models that describe one simulation input payload.

These classes are small "containers" for values loaded from JSON.
Keeping them separate makes the rest of the code easier to read.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HullGeometry:
    """Physical dimensions of the submarine hull and fin."""

    length_m: float
    max_diameter_m: float
    fin_offset_x: float
    naca_profile: str
    fin_surface_area_m2: float


@dataclass
class PhysicsState:
    """Current kinematic state of the submarine."""

    velocity_ms: float
    pitch_deg: float
    yaw_deg: float
    depth_m: float


@dataclass
class SteeringOutput:
    """Commanded steering state from the control system."""

    target_fin_angle_deg: float
    motor_torque_nm: float


@dataclass
class Environment:
    """Water/environment values used by the physics calculations."""

    fluid_density_kgm3: float
    current_vector_ms: list[float]
    sensor_noise_sigma: float


@dataclass
class SimulationInput:
    """Top-level input object grouped by logical sections."""

    hull_geometry: HullGeometry
    physics_state: PhysicsState
    steering_output: SteeringOutput
    environment: Environment
