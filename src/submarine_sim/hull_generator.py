from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

try:
    import open3d as o3d
except ImportError:  # pragma: no cover - optional for CI/headless
    o3d = None


@dataclass
class HullProperties:
    area_m2: float
    volume_m3: float


class HullGenerator:
    def __init__(self) -> None:
        self.submarine_mesh = None
        self.length_m = 3.0
        self.diameter_m = 0.5
        self.fin_surface_area_m2 = 0.08

    def generate_myring_points(self, length_m: float, diameter_m: float, n_theta: int = 48, n_phi: int = 64) -> np.ndarray:
        a = length_m / 2.0
        b = diameter_m / 2.0

        theta = np.linspace(0.0, np.pi, n_theta)
        phi = np.linspace(0.0, 2.0 * np.pi, n_phi)
        t_grid, p_grid = np.meshgrid(theta, phi, indexing="ij")

        x = a * np.cos(t_grid)
        y = b * np.sin(t_grid) * np.cos(p_grid)
        z = b * np.sin(t_grid) * np.sin(p_grid)
        return np.column_stack((x.ravel(), y.ravel(), z.ravel()))

    def create_mesh(self, points: np.ndarray):
        if o3d is None:
            self.submarine_mesh = {"points": points}
            return self.submarine_mesh

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        hull_mesh, _ = pcd.compute_convex_hull()
        hull_mesh.compute_vertex_normals()
        self.submarine_mesh = hull_mesh
        return hull_mesh

    def update_hull(self, length_m: float, diameter_m: float, fin_surface_area_m2: float):
        self.length_m = length_m
        self.diameter_m = diameter_m
        self.fin_surface_area_m2 = fin_surface_area_m2
        points = self.generate_myring_points(length_m, diameter_m)
        return self.create_mesh(points)

    def get_hydro_area(self) -> float:
        radius = self.diameter_m / 2.0
        return math.pi * radius * radius

    def get_volume(self) -> float:
        a = self.length_m / 2.0
        b = self.diameter_m / 2.0
        return (4.0 / 3.0) * math.pi * a * b * b

    def get_properties(self) -> HullProperties:
        return HullProperties(area_m2=self.get_hydro_area(), volume_m3=self.get_volume())
