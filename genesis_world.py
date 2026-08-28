"""
3D Genesis Virtual World Engine with Dynamic Matter & Environmental Physics
===========================================================================
Pure Physics Principles:
- Zero Hardcoding / Zero Cheats.
- Dynamic Raw Materials: Structural Stone Blocks, Reflective Plates, Energy Crystals.
- Physical Manipulation: Pick, Place, Carry, Fuse Matter in 3D.
- Dynamic Environmental Cycles: Periodic Cosmic Acid Storms requiring shelter construction.
- Acoustic & Visual Ray Physics: Sound and light interact with dynamic blocks in real time.
"""

import numpy as np
from typing import Dict, Any, Tuple, List, Optional


class DynamicBlock:
    """A moveable, interactive physical matter block in the 3D world."""
    def __init__(self, block_id: int, pos: Tuple[float, float, float], size: Tuple[float, float, float] = (1.0, 1.0, 1.0), material_type: str = "stone", mass: float = 2.0):
        self.block_id = block_id
        self.pos = np.array(pos, dtype=float)
        self.size = np.array(size, dtype=float)
        self.material_type = material_type  # "stone" (structural), "metal" (acoustic reflector), "crystal" (energy food)
        self.mass = mass
        self.held_by_agent = False

    @property
    def min_pt(self) -> np.ndarray:
        return self.pos - self.size / 2.0

    @property
    def max_pt(self) -> np.ndarray:
        return self.pos + self.size / 2.0

    def contains(self, pt: np.ndarray, margin: float = 0.1) -> bool:
        return np.all(pt >= (self.min_pt - margin)) and np.all(pt <= (self.max_pt + margin))

    def intersect_ray(self, origin: np.ndarray, direction: np.ndarray, max_dist: float = 20.0) -> float:
        dir_norm = direction / (np.linalg.norm(direction) + 1e-9)
        t_min, t_max = 0.0, max_dist
        min_p, max_p = self.min_pt, self.max_pt

        for i in range(3):
            if abs(dir_norm[i]) < 1e-8:
                if origin[i] < min_p[i] or origin[i] > max_p[i]:
                    return max_dist
            else:
                t1 = (min_p[i] - origin[i]) / dir_norm[i]
                t2 = (max_p[i] - origin[i]) / dir_norm[i]
                t_enter = min(t1, t2)
                t_exit = max(t1, t2)
                t_min = max(t_min, t_enter)
                t_max = min(t_max, t_exit)
                if t_min > t_max:
                    return max_dist

        return t_min if t_min > 0.0 else (t_max if t_max > 0.0 else max_dist)


class GenesisWorld3D:
    """
    Continuous 3D Genesis Sandbox World:
    - Volumetric terrain with chasms, building zones, and shelter areas.
    - Moveable dynamic raw material blocks (stone, metal, energy crystals).
    - Environmental Storm Cycle (Storm drains energy if not sheltered under a roof).
    - Diffractive Acoustic Emitters & 360° Visual Depth Raycast.
    """
    def __init__(self, size_x: float = 24.0, size_y: float = 24.0, size_z: float = 8.0):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        
        self.dynamic_blocks: List[DynamicBlock] = []
        self.static_obstacles: List[Dict[str, Any]] = []
        self.beacons: List[Dict[str, Any]] = []
        
        # Environmental Weather System (Periodic Cosmic Storms)
        self.storm_active = False
        self.storm_timer = 0
        self.storm_intensity = 0.0
        
        self._build_genesis_environment()

    def _build_genesis_environment(self):
        """Construct the 3D Genesis world with an impassable gorge and raw materials."""
        # 1. Outer perimeter boundaries
        self.static_obstacles.append({"min": [-1, -1, -1], "max": [self.size_x + 1, self.size_y + 1, 0.0], "label": "bedrock_floor"})
        self.static_obstacles.append({"min": [-1, -1, self.size_z], "max": [self.size_x + 1, self.size_y + 1, self.size_z + 1], "label": "sky_ceiling"})
        self.static_obstacles.append({"min": [-1, -1, 0], "max": [0.0, self.size_y + 1, self.size_z], "label": "west_perimeter"})
        self.static_obstacles.append({"min": [self.size_x, -1, 0], "max": [self.size_x + 1, self.size_y + 1, self.size_z], "label": "east_perimeter"})
        self.static_obstacles.append({"min": [-1, -1, 0], "max": [self.size_x + 1, 0.0, self.size_z], "label": "south_perimeter"})
        self.static_obstacles.append({"min": [-1, self.size_y, 0], "max": [self.size_x + 1, self.size_y + 1, self.size_z], "label": "north_perimeter"})

        # 2. The Great Chasm (Deep void dividing Region A [x <= 10] from Region B [x >= 14])
        # Chasm spans x in [10.0, 14.0], y in [0.0, 24.0]
        # Any entity entering Chasm without a bridge falls into the void!
        self.chasm_bounds = (10.0, 14.0, 0.0, self.size_y)

        # 3. Dispersed Raw Materials in Region A (Spawn area)
        # 6 Heavy Stone Slabs (Ideal for building a bridge across the chasm)
        slab_positions = [
            (4.0, 4.0, 0.6),
            (5.5, 4.0, 0.6),
            (7.0, 4.0, 0.6),
            (4.0, 8.0, 0.6),
            (5.5, 8.0, 0.6),
            (7.0, 8.0, 0.6),
        ]
        for i, pos in enumerate(slab_positions):
            self.dynamic_blocks.append(DynamicBlock(
                block_id=i + 1,
                pos=pos,
                size=(1.8, 1.4, 0.4), # Wide slab
                material_type="stone",
                mass=3.0
            ))

        # 3 Acoustic Reflector Plates (Metal)
        reflector_positions = [(3.0, 14.0, 1.0), (5.0, 16.0, 1.0), (7.0, 18.0, 1.0)]
        for i, pos in enumerate(reflector_positions):
            self.dynamic_blocks.append(DynamicBlock(
                block_id=10 + i + 1,
                pos=pos,
                size=(0.3, 2.0, 2.0), # Flat reflector plate
                material_type="metal",
                mass=1.5
            ))

        # 4 Energy Crystal Nodes across Region B (The Reward Realm)
        crystal_positions = [(18.0, 6.0, 1.0), (20.0, 12.0, 1.0), (18.0, 18.0, 1.0), (22.0, 20.0, 1.0)]
        for i, pos in enumerate(crystal_positions):
            self.dynamic_blocks.append(DynamicBlock(
                block_id=20 + i + 1,
                pos=pos,
                size=(0.8, 0.8, 1.2),
                material_type="crystal",
                mass=0.8
            ))

        # 4. Acoustic Goal Beacon deep in Region B at (20.0, 20.0, 2.0)
        self.beacons.append({
            "pos": np.array([20.0, 20.0, 2.0]),
            "frequency": 380.0,
            "amplitude": 10.0,
            "label": "sanctuary_beacon"
        })

    def update_environment(self, step: int):
        """Update dynamic cosmic storm cycle."""
        # Storm occurs every 120 steps, lasting 35 steps
        cycle = step % 150
        if 80 <= cycle <= 120:
            self.storm_active = True
            self.storm_intensity = float(np.sin((cycle - 80) / 40.0 * np.pi))
        else:
            self.storm_active = False
            self.storm_intensity = 0.0

    def is_under_shelter(self, pos: np.ndarray) -> bool:
        """Check if position is covered by a stone slab or ceiling above it (z > pos.z)."""
        up_dir = np.array([0.0, 0.0, 1.0])
        for block in self.dynamic_blocks:
            if block.material_type == "stone" and block.pos[2] > (pos[2] + 0.3):
                hit = block.intersect_ray(pos, up_dir, max_dist=4.0)
                if hit < 4.0:
                    return True
        return False

    def is_in_chasm_void(self, pos: np.ndarray) -> bool:
        """Check if position is over the chasm without a supporting bridge block beneath."""
        x, y, z = pos[0], pos[1], pos[2]
        if self.chasm_bounds[0] <= x <= self.chasm_bounds[1] and z < 1.0:
            # Check if any stone slab is bridging directly under pos
            down_dir = np.array([0.0, 0.0, -1.0])
            for block in self.dynamic_blocks:
                if block.material_type == "stone" and abs(block.pos[2] - 0.5) < 0.5:
                    hit = block.intersect_ray(pos, down_dir, max_dist=2.0)
                    if hit < 2.0:
                        return False # Bridge exists!
            return True # Void fall!
        return False

    def sample_acoustics(self, receiver_pos: np.ndarray, t: float = 0.0) -> Tuple[float, np.ndarray]:
        """Acoustic pressure & flux gradient calculation with metal reflection bonuses."""
        total_p = 0.0
        total_flux = np.zeros(3)

        for beacon in self.beacons:
            b_pos = beacon["pos"]
            delta = b_pos - receiver_pos
            dist = float(np.linalg.norm(delta))
            if dist < 1e-4:
                continue
            dir_vec = delta / dist
            
            # Sound reflection off metal plates
            reflection_boost = 1.0
            for block in self.dynamic_blocks:
                if block.material_type == "metal":
                    dist_to_plate = float(np.linalg.norm(block.pos - receiver_pos))
                    if dist_to_plate < 4.0:
                        reflection_boost += 0.45

            p = (beacon["amplitude"] * reflection_boost / (dist + 1.0)) * np.cos(0.05 * dist - 2.0 * np.pi * beacon["frequency"] * t)
            flux = dir_vec * float(beacon["amplitude"] * reflection_boost / ((dist + 1.0)**2))
            total_p += p
            total_flux += flux

        return float(total_p), total_flux

    def cast_visual_rays(self, origin: np.ndarray, yaw: float, pitch: float, num_azimuth: int = 16, num_elevation: int = 3, max_range: float = 18.0) -> Dict[str, Any]:
        """360° Visual depth raycast intersecting static barriers and dynamic matter blocks."""
        azimuths = np.linspace(0.0, 2.0 * np.pi, num_azimuth, endpoint=False)
        elevations = np.linspace(-np.pi / 6.0, np.pi / 6.0, num_elevation)

        depths = np.zeros((num_elevation, num_azimuth))
        ray_dirs = np.zeros((num_elevation, num_azimuth, 3))
        closest_dist = max_range

        for e_idx, el in enumerate(elevations):
            for a_idx, az in enumerate(azimuths):
                dx = np.cos(pitch + el) * np.cos(yaw + az)
                dy = np.cos(pitch + el) * np.sin(yaw + az)
                dz = np.sin(pitch + el)
                r_dir = np.array([dx, dy, dz], dtype=float)
                r_dir /= np.linalg.norm(r_dir)
                ray_dirs[e_idx, a_idx] = r_dir

                min_hit = max_range
                # Intersect static walls
                for obs in self.static_obstacles:
                    min_p, max_p = np.array(obs["min"]), np.array(obs["max"])
                    # AABB intersection
                    t_min, t_max = 0.0, max_range
                    for i in range(3):
                        if abs(r_dir[i]) > 1e-8:
                            t1 = (min_p[i] - origin[i]) / r_dir[i]
                            t2 = (max_p[i] - origin[i]) / r_dir[i]
                            t_min = max(t_min, min(t1, t2))
                            t_max = min(t_max, max(t1, t2))
                    if t_min <= t_max and t_min > 0.0:
                        min_hit = min(min_hit, t_min)

                # Intersect dynamic blocks
                for block in self.dynamic_blocks:
                    if not block.held_by_agent:
                        hit_b = block.intersect_ray(origin, r_dir, max_dist=max_range)
                        min_hit = min(min_hit, hit_b)

                depths[e_idx, a_idx] = min_hit
                closest_dist = min(closest_dist, min_hit)

        return {
            "depth_matrix": depths,
            "ray_dirs": ray_dirs,
            "closest_dist": float(closest_dist)
        }

    def probe_ground_ahead(self, origin: np.ndarray, heading_3d: np.ndarray, distance: float = 1.8) -> float:
        """
        Physical floor probe: casts a ray downward from a point ahead of the agent.
        Returns the distance to the solid floor (or large number if over a void/chasm).
        """
        probe_origin = origin + heading_3d * distance
        down_dir = np.array([0.0, 0.0, -1.0])
        
        # Check static floor
        min_hit = 20.0
        # If in chasm void region
        if self.chasm_bounds[0] <= probe_origin[0] <= self.chasm_bounds[1]:
            # Only bridge blocks can provide floor support
            for block in self.dynamic_blocks:
                if block.material_type == "stone" and not block.held_by_agent:
                    hit = block.intersect_ray(probe_origin, down_dir, max_dist=10.0)
                    if hit < min_hit:
                        min_hit = hit
            return min_hit # If no bridge, min_hit is 20.0 (deep void!)
        else:
            # Solid bedrock floor at z=0
            if probe_origin[2] >= 0.0:
                return probe_origin[2]
            return 0.0
