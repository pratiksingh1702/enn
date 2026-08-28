"""
3D Continuous Physical World Engine
=====================================
Features:
- Continuous 3D Environment with Volumetric Obstacles & Corridors.
- Continuous 360° Visual Raycaster (Azimuth + Elevation Depth Rays).
- Diffractive Acoustic Helmholtz Field: Acoustic beacons emit sound that wraps around corners.
- Continuous 3D Kinematics (Thrust, Drag, Inertia, 6-DOF Orientation).
"""

import numpy as np
from typing import Dict, Any, Tuple, List, Optional


class BoxObstacle:
    """Volumetric 3D Axis-Aligned Bounding Box Obstacle."""
    def __init__(self, min_pt: Tuple[float, float, float], max_pt: Tuple[float, float, float], label: str = "wall"):
        self.min_pt = np.array(min_pt, dtype=float)
        self.max_pt = np.array(max_pt, dtype=float)
        self.label = label

    def contains(self, pt: np.ndarray, margin: float = 0.2) -> bool:
        return np.all(pt >= (self.min_pt - margin)) and np.all(pt <= (self.max_pt + margin))

    def intersect_ray(self, origin: np.ndarray, direction: np.ndarray, max_dist: float = 20.0) -> float:
        """Ray-AABB intersection returning hit distance (or max_dist if no hit)."""
        dir_norm = direction / (np.linalg.norm(direction) + 1e-9)
        t_min = 0.0
        t_max = max_dist

        for i in range(3):
            if abs(dir_norm[i]) < 1e-8:
                if origin[i] < self.min_pt[i] or origin[i] > self.max_pt[i]:
                    return max_dist
            else:
                t1 = (self.min_pt[i] - origin[i]) / dir_norm[i]
                t2 = (self.max_pt[i] - origin[i]) / dir_norm[i]
                t_enter = min(t1, t2)
                t_exit = max(t1, t2)
                t_min = max(t_min, t_enter)
                t_max = min(t_max, t_exit)
                if t_min > t_max:
                    return max_dist

        return t_min if t_min > 0.0 else (t_max if t_max > 0.0 else max_dist)


class AcousticBeacon:
    """Continuous Harmonic Acoustic Wave Emitter (Sound Source)."""
    def __init__(self, pos: Tuple[float, float, float], frequency: float = 440.0, amplitude: float = 5.0, label: str = "goal_beacon"):
        self.pos = np.array(pos, dtype=float)
        self.frequency = frequency
        self.amplitude = amplitude
        self.label = label
        self.wave_speed = 340.0 # m/s
        self.k = (2.0 * np.pi * self.frequency) / self.wave_speed

    def compute_sound_at(self, receiver_pos: np.ndarray, obstacles: List[BoxObstacle], t: float = 0.0) -> Tuple[float, np.ndarray]:
        """
        Compute acoustic pressure amplitude and acoustic gradient flux vector at receiver position.
        Incorporates diffraction attenuation through open acoustic paths.
        """
        delta = self.pos - receiver_pos
        direct_dist = np.linalg.norm(delta)
        if direct_dist < 1e-4:
            return float(self.amplitude), np.zeros(3)

        direct_dir = delta / direct_dist

        # Check line of sight occlusion
        occluded = False
        for obs in obstacles:
            hit_d = obs.intersect_ray(receiver_pos, direct_dir, max_dist=direct_dist)
            if hit_d < (direct_dist - 0.1):
                occluded = True
                break

        # Diffractive attenuation: sound diffracts around walls but loses high-frequency intensity
        diffraction_factor = 0.45 if occluded else 1.0
        
        # 1/r Spherical wave dispersion with diffractive phase lag
        pressure = (self.amplitude * diffraction_factor / (direct_dist + 1.0)) * np.cos(self.k * direct_dist - 2.0 * np.pi * self.frequency * t)
        
        # Acoustic energy flux gradient pointing along arrival path
        flux_vec = direct_dir * float(self.amplitude * diffraction_factor / ((direct_dist + 1.0)**2))
        return float(pressure), flux_vec


class World3D:
    """
    Continuous 3D Volumetric Environment:
    - Dimensions: [0, size_x] x [0, size_y] x [0, size_z]
    - Partition Walls & Maze Obstacles
    - Acoustic Emitters (Goals / Beacons)
    - 360° Visual Depth Raycaster
    """
    def __init__(self, size_x: float = 20.0, size_y: float = 20.0, size_z: float = 6.0):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.obstacles: List[BoxObstacle] = []
        self.beacons: List[AcousticBeacon] = []
        self._build_default_3d_environment()

    def _build_default_3d_environment(self):
        """Construct continuous 3D multi-room environment with doorway detours and partitions."""
        # 1. Outer perimeter bounding walls
        wall_thick = 0.5
        # Floor & Ceiling
        self.obstacles.append(BoxObstacle((-1, -1, -1), (self.size_x + 1, self.size_y + 1, 0.0), label="floor"))
        self.obstacles.append(BoxObstacle((-1, -1, self.size_z), (self.size_x + 1, self.size_y + 1, self.size_z + 1), label="ceiling"))
        # Perimeter Walls
        self.obstacles.append(BoxObstacle((-1, -1, 0), (0.0, self.size_y + 1, self.size_z), label="west_wall"))
        self.obstacles.append(BoxObstacle((self.size_x, -1, 0), (self.size_x + 1, self.size_y + 1, self.size_z), label="east_wall"))
        self.obstacles.append(BoxObstacle((-1, -1, 0), (self.size_x + 1, 0.0, self.size_z), label="south_wall"))
        self.obstacles.append(BoxObstacle((-1, self.size_y, 0), (self.size_x + 1, self.size_y + 1, self.size_z), label="north_wall"))

        # 2. Interior Partitions (Creating 3D multi-room navigation with doorways)
        # Middle vertical barrier with doorway at (10, 3, 0)->(10, 7, 3)
        self.obstacles.append(BoxObstacle((9.5, 0.0, 0.0), (10.5, 8.0, self.size_z), label="partition_south"))
        self.obstacles.append(BoxObstacle((9.5, 12.0, 0.0), (10.5, self.size_y, self.size_z), label="partition_north"))
        # Doorway left open at y in [8.0, 12.0]!

        # Lateral baffle in Room B (requiring 3D detour)
        self.obstacles.append(BoxObstacle((14.0, 6.0, 0.0), (15.0, 16.0, 3.5), label="low_baffle"))
        # Open air passage above z > 3.5!

        # 3. Acoustic Goal Beacon placed in Room B at (17.0, 17.0, 2.0)
        self.beacons.append(AcousticBeacon((17.0, 17.0, 2.0), frequency=350.0, amplitude=8.0, label="primary_food_cache"))

    def cast_visual_rays(self, origin: np.ndarray, yaw: float, pitch: float, num_azimuth: int = 16, num_elevation: int = 3, max_range: float = 15.0) -> Dict[str, Any]:
        """
        Continuous 360° Visual Depth Raycast.
        Returns:
        - depth_matrix: distances array of shape (num_elevation, num_azimuth)
        - ray_vectors: 3D direction vectors for each ray
        - closest_obstacle_dist: float
        """
        azimuths = np.linspace(0.0, 2.0 * np.pi, num_azimuth, endpoint=False)
        elevations = np.linspace(-np.pi / 6.0, np.pi / 6.0, num_elevation)

        depths = np.zeros((num_elevation, num_azimuth))
        ray_dirs = np.zeros((num_elevation, num_azimuth, 3))

        closest_dist = max_range

        for e_idx, el in enumerate(elevations):
            for a_idx, az in enumerate(azimuths):
                total_yaw = yaw + az
                total_pitch = pitch + el

                # Direction vector in 3D spherical coords
                dx = np.cos(total_pitch) * np.cos(total_yaw)
                dy = np.cos(total_pitch) * np.sin(total_yaw)
                dz = np.sin(total_pitch)
                r_dir = np.array([dx, dy, dz], dtype=float)
                r_dir /= np.linalg.norm(r_dir)
                ray_dirs[e_idx, a_idx] = r_dir

                # Raycast against all obstacles
                min_hit = max_range
                for obs in self.obstacles:
                    hit_d = obs.intersect_ray(origin, r_dir, max_dist=max_range)
                    if hit_d < min_hit:
                        min_hit = hit_d

                depths[e_idx, a_idx] = min_hit
                if min_hit < closest_dist:
                    closest_dist = min_hit

        return {
            "depth_matrix": depths,
            "ray_dirs": ray_dirs,
            "closest_dist": float(closest_dist),
            "azimuths": azimuths,
            "elevations": elevations
        }

    def sample_acoustics(self, pos: np.ndarray, t: float = 0.0) -> Tuple[float, np.ndarray]:
        """Sample superposed acoustic sound field pressure and directional energy flux at position."""
        total_p = 0.0
        total_flux = np.zeros(3)
        for beacon in self.beacons:
            p, flux = beacon.compute_sound_at(pos, self.obstacles, t=t)
            total_p += p
            total_flux += flux
        return float(total_p), total_flux

    def check_collision(self, pos: np.ndarray, radius: float = 0.35) -> bool:
        """Check if sphere of radius at pos penetrates any obstacle."""
        for obs in self.obstacles:
            if obs.contains(pos, margin=radius):
                return True
        return False

    def check_collision_and_normal(self, current_pos: np.ndarray, proposed_pos: np.ndarray, radius: float = 0.35) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Continuous physical collision detection with outward surface normal reflection.
        """
        for obs in self.obstacles:
            if obs.contains(proposed_pos, margin=radius):
                center = (obs.min_pt + obs.max_pt) / 2.0
                half_ext = (obs.max_pt - obs.min_pt) / 2.0 + radius
                delta = proposed_pos - center
                overlap = half_ext - np.abs(delta)
                min_axis = int(np.argmin(overlap))
                normal = np.zeros(3)
                normal[min_axis] = float(np.sign(delta[min_axis])) if delta[min_axis] != 0 else 1.0
                return True, normal
        return False, None
