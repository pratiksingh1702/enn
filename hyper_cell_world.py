"""
Grand Living Universe Ecosystem & Physics Engine
=================================================
Complete Living World with:
- Thread-safe cell collections (preventing 'dict changed size during iteration').
- Dynamic Weather Cycles: Clear Skies, Rain Storms, Aurora Borealis, Thunderstorms.
- Living Hyper-Cell Wildlife: Grazing Ether Fawns, Luminescent Sky Birds.
- Full State Restoration preserving continuous civilization history.
"""

import numpy as np
import os
import json
import threading
import math
from typing import Dict, Any, Tuple, List, Optional


class HyperCell:
    """Universal physical primitive of matter, free energy, and living tissue."""
    def __init__(self, cell_id: int, pos: Tuple[float, float, float], cell_type: str = "matter_stone",
                 energy: float = 10.0, mass: float = 1.0, radius: float = 0.4, frequency: float = 1.0):
        self.id = int(cell_id)
        self.pos = np.array(pos, dtype=float)
        self.cell_type = str(cell_type)
        self.energy = float(energy)
        self.mass = float(mass)
        self.radius = float(radius)
        self.frequency = float(frequency)
        self.phase = np.random.uniform(0, 2.0 * np.pi)
        self.bonded_to_agent: bool = False

    def update_phase(self, dt: float = 0.1):
        self.phase = (self.phase + self.frequency * dt) % (2.0 * np.pi)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "pos": [round(float(self.pos[0]), 2), round(float(self.pos[1]), 2), round(float(self.pos[2]), 2)],
            "type": self.cell_type,
            "energy": round(float(self.energy), 1),
            "radius": round(float(self.radius), 2),
            "bonded": self.bonded_to_agent
        }


class EcosystemFauna:
    """Autonomous living wildlife in the hyper-cell meadow."""
    def __init__(self, fauna_id: int, fauna_type: str, pos: Tuple[float, float, float]):
        self.id = fauna_id
        self.fauna_type = fauna_type
        self.pos = np.array(pos, dtype=float)
        self.velocity = np.zeros(3, dtype=float)
        self.yaw = np.random.uniform(0, 2.0 * np.pi)
        self.energy = 50.0

    def update(self, world: "OrganicWorld3D", dt: float = 0.1):
        if self.fauna_type == "fauna_deer":
            if np.random.uniform(0, 1) < 0.05:
                self.yaw += np.random.uniform(-0.8, 0.8)
            speed = 0.8
            fwd = np.array([np.cos(self.yaw), np.sin(self.yaw), 0.0])
            self.velocity[:2] = self.velocity[:2] * 0.8 + fwd[:2] * speed * dt
            self.pos += self.velocity * dt
            ter_z = world.get_terrain_height(self.pos[0], self.pos[1])
            self.pos[2] = ter_z + 0.4
        elif self.fauna_type == "fauna_bird":
            self.yaw += 0.03
            speed = 2.2
            fwd = np.array([np.cos(self.yaw), np.sin(self.yaw), np.sin(self.yaw * 2.0) * 0.2])
            self.velocity = fwd * speed
            self.pos += self.velocity * dt
            ter_z = world.get_terrain_height(self.pos[0], self.pos[1])
            self.pos[2] = max(ter_z + 3.0, self.pos[2])

        self.pos[0] = float(np.clip(self.pos[0], 2.0, world.size_x - 2.0))
        self.pos[1] = float(np.clip(self.pos[1], 2.0, world.size_y - 2.0))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.fauna_type,
            "pos": [round(float(self.pos[0]), 2), round(float(self.pos[1]), 2), round(float(self.pos[2]), 2)],
            "yaw": round(float(self.yaw), 2)
        }


class OrganicWorld3D:
    """3D continuous physics world supporting wildlife, weather, multi-agents, and thread safety."""
    def __init__(self, size_x: float = 64.0, size_y: float = 64.0, max_height: float = 18.0, restore_file: Optional[str] = None):
        self.size_x = float(size_x)
        self.size_y = float(size_y)
        self.max_height = float(max_height)
        self.cells: Dict[int, HyperCell] = {}
        self.cells_lock = threading.Lock()
        self._cached_cell_positions = np.empty((0, 3), dtype=np.float32)
        self._cached_cell_radii = np.empty((0,), dtype=np.float32)
        self._cells_dirty = True
        self.fauna: List[EcosystemFauna] = []
        self.next_cell_id = 1
        self.sim_time = 0.0
        self.sun_intensity = 0.5
        self.last_ether_spawn = 0.0
        self.last_stone_spawn = 0.0
        
        # Dynamic Weather
        self.weather_type = "clear"
        self.weather_timer = 0.0

        if restore_file and os.path.exists(restore_file):
            self._restore_from_file(restore_file)
        else:
            self._populate_initial_world()

        self._spawn_wildlife()

    def get_terrain_height(self, x: float, y: float) -> float:
        """Continuous multi-scale harmonic terrain heightmap: z = h(x, y). Fast scalar math."""
        x_c = max(0.0, min(self.size_x, float(x)))
        y_c = max(0.0, min(self.size_y, float(y)))
        
        h1 = math.sin(x_c * 0.08) * math.cos(y_c * 0.08) * 2.2
        h2 = math.sin(x_c * 0.16 + 1.2) * math.sin(y_c * 0.16 + 0.8) * 1.2
        h3 = math.cos(math.sqrt((x_c - 32.0)**2 + (y_c - 32.0)**2) * 0.12) * 0.8
        
        base_h = 1.6 + h1 + h2 + h3
        return max(0.2, min(self.max_height - 1.0, base_h))

    def _spawn_wildlife(self):
        self.fauna = [
            EcosystemFauna(1, "fauna_deer", (10.0, 14.0, 2.0)),
            EcosystemFauna(2, "fauna_deer", (22.0, 20.0, 2.0)),
            EcosystemFauna(3, "fauna_bird", (16.0, 16.0, 7.0)),
            EcosystemFauna(4, "fauna_bird", (8.0, 8.0, 6.5))
        ]

    def _restore_from_file(self, file_path: str):
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            self.sim_time = float(data.get("sim_time", 20800.0))
            for c_data in data.get("cells", []):
                cid = int(c_data["id"])
                c = HyperCell(
                    cell_id=cid,
                    pos=tuple(c_data["pos"]),
                    cell_type=c_data["type"],
                    energy=float(c_data["energy"]),
                    radius=float(c_data["radius"])
                )
                self.cells[cid] = c
                if cid >= self.next_cell_id:
                    self.next_cell_id = cid + 1
            print(f"Restored {len(self.cells)} hyper-cells from {file_path} successfully!")
        except Exception as e:
            print(f"Error restoring world state: {e}")
            self._populate_initial_world()

    def _populate_initial_world(self):
        for _ in range(25):
            self._spawn_random_ether()
        for _ in range(16):
            self._spawn_random_stone()

    def _spawn_random_ether(self):
        ex = np.random.uniform(3.0, self.size_x - 3.0)
        ey = np.random.uniform(3.0, self.size_y - 3.0)
        ez = self.get_terrain_height(ex, ey) + np.random.uniform(0.8, 2.5)
        self.spawn_cell((ex, ey, ez), cell_type="energy_ether", energy=30.0, radius=0.35, frequency=np.random.uniform(1.5, 3.0))

    def _spawn_random_stone(self):
        sx = np.random.uniform(3.0, self.size_x - 3.0)
        sy = np.random.uniform(3.0, self.size_y - 3.0)
        sz = self.get_terrain_height(sx, sy) + 0.4
        self.spawn_cell((sx, sy, sz), cell_type="matter_stone", energy=15.0, radius=0.4)

    def spawn_celestial_meteor(self, x: float, y: float) -> HyperCell:
        """God Hand: Spawns a glowing celestial crystal at coordinates safely."""
        z = self.get_terrain_height(x, y) + 1.0
        return self.spawn_cell((x, y, z), cell_type="energy_crystal", energy=200.0, radius=0.7)

    def spawn_cell(self, pos: Tuple[float, float, float], cell_type: str = "matter_stone",
                   energy: float = 10.0, mass: float = 1.0, radius: float = 0.4, frequency: float = 1.0) -> HyperCell:
        with self.cells_lock:
            cell = HyperCell(cell_id=self.next_cell_id, pos=pos, cell_type=cell_type, energy=energy, mass=mass, radius=radius, frequency=frequency)
            self.cells[self.next_cell_id] = cell
            self.next_cell_id += 1
            self._cells_dirty = True
            return cell

    def _sync_cell_buffers(self):
        """Synchronizes contiguous NumPy array buffers of cell positions and radii."""
        if not self._cells_dirty and self._cached_cell_positions is not None:
            return
        if not self.cells:
            self._cached_cell_positions = np.empty((0, 3), dtype=np.float32)
            self._cached_cell_radii = np.empty((0,), dtype=np.float32)
        else:
            unbonded = [c for c in self.cells.values() if not c.bonded_to_agent]
            if unbonded:
                self._cached_cell_positions = np.array([c.pos for c in unbonded], dtype=np.float32)
                self._cached_cell_radii = np.array([c.radius + 0.25 for c in unbonded], dtype=np.float32)
            else:
                self._cached_cell_positions = np.empty((0, 3), dtype=np.float32)
                self._cached_cell_radii = np.empty((0,), dtype=np.float32)
        self._cells_dirty = False

    def update_physics(self, dt: float = 0.1, is_headless: bool = False):
        """Update environmental time, weather transitions, wildlife, daylight, and ether blooming."""
        self.sim_time += dt
        solar_phase = (self.sim_time / 240.0) * 2.0 * math.pi
        self.sun_intensity = max(0.12, (math.sin(solar_phase) + 1.0) / 2.0)

        # Weather Transitions
        self.weather_timer += dt
        if self.weather_timer > 90.0:
            self.weather_timer = 0.0
            weathers = ["clear", "rain", "storm", "aurora", "clear"]
            self.weather_type = weathers[int(np.random.randint(0, len(weathers)))]

        # Update Wildlife (Skipped in headless or every 10 steps)
        if not is_headless:
            for f in self.fauna:
                f.update(self, dt)

        # Regrowth
        with self.cells_lock:
            cells_list = list(self.cells.values())
            
        if self.sim_time - self.last_ether_spawn > 3.0:
            active_ether_count = sum(1 for c in cells_list if c.cell_type == "energy_ether")
            if active_ether_count < 28:
                self.last_ether_spawn = self.sim_time
                self._spawn_random_ether()

        if self.sim_time - self.last_stone_spawn > 5.0:
            active_stone_count = sum(1 for c in cells_list if c.cell_type == "matter_stone")
            if active_stone_count < 16:
                self.last_stone_spawn = self.sim_time
                self._spawn_random_stone()

        if not is_headless:
            for cell in cells_list:
                cell.update_phase(dt)
                if cell.cell_type == "energy_ether" and not cell.bonded_to_agent:
                    cell.pos[2] += math.sin(cell.phase) * 0.025 * dt
                    ground_z = self.get_terrain_height(cell.pos[0], cell.pos[1])
                    if cell.pos[2] < ground_z + 0.6:
                        cell.pos[2] = ground_z + 0.6

    def cast_visual_rays(self, origin: np.ndarray, yaw: float, pitch: float, other_agent_pos: Optional[np.ndarray] = None,
                          num_azimuth: int = 16, num_elevation: int = 3, max_range: float = 22.0) -> Dict[str, Any]:
        """Vectorized high-speed continuous visual depth raycast probing terrain, architecture, and other organisms."""
        azimuths = np.linspace(0.0, 2.0 * np.pi, num_azimuth, endpoint=False)
        elevations = np.linspace(-np.pi / 6.0, np.pi / 6.0, num_elevation)
        
        # Grid of ray directions shape: (num_elevation, num_azimuth, 3)
        el_grid, az_grid = np.meshgrid(elevations, azimuths, indexing='ij')
        
        dx = np.cos(pitch + el_grid) * np.cos(yaw + az_grid)
        dy = np.cos(pitch + el_grid) * np.sin(yaw + az_grid)
        dz = np.sin(pitch + el_grid)
        ray_dirs = np.stack([dx, dy, dz], axis=-1)  # shape: (E, A, 3)
        flat_dirs = ray_dirs.reshape(-1, 3)         # shape: (48, 3)
        
        # Default all depths to max_range
        depths_flat = np.full(len(flat_dirs), max_range, dtype=np.float32)
        spotted_other_agent = False

        # 1. Vectorized Other-Agent Sphere Intersection
        if other_agent_pos is not None:
            v_other = other_agent_pos - origin
            proj = np.dot(flat_dirs, v_other)
            perp_sq = np.sum(v_other**2) - proj**2
            mask = (proj > 0.3) & (perp_sq < 0.64) & (proj < max_range)
            if np.any(mask):
                depths_flat[mask] = np.minimum(depths_flat[mask], proj[mask])
                spotted_other_agent = True

        # 2. Vectorized Contiguous Matrix Cell Intersection with BLAS Filter
        ox, oy = origin[0], origin[1]
        with self.cells_lock:
            self._sync_cell_buffers()
            all_pos = self._cached_cell_positions
            all_radii = self._cached_cell_radii

        if len(all_pos) > 0:
            dx_c = all_pos[:, 0] - ox
            dy_c = all_pos[:, 1] - oy
            mask_near = (np.abs(dx_c) <= max_range) & (np.abs(dy_c) <= max_range)
            
            cand_pos = all_pos[mask_near]
            cand_radii = all_radii[mask_near]
            
            if len(cand_pos) > 48:
                dist_sq = dx_c[mask_near]**2 + dy_c[mask_near]**2
                top_idx = np.argpartition(dist_sq, 48)[:48]
                cand_pos = cand_pos[top_idx]
                cand_radii = cand_radii[top_idx]

            if len(cand_pos) > 0:
                v_cells = cand_pos - origin  # (N, 3)
                projs = np.dot(flat_dirs, v_cells.T) # (48, N)
                v_cells_sq = np.sum(v_cells**2, axis=1) # (N,)
                perp_sq = v_cells_sq - projs**2 # (48, N)
                
                valid_hits = (projs > 0.4) & (projs < max_range) & (perp_sq < (cand_radii**2))
                dist_matrix = np.where(valid_hits, projs, max_range)
                min_cell_dists = np.min(dist_matrix, axis=1)
                depths_flat = np.minimum(depths_flat, min_cell_dists)

        # 3. Vectorized Terrain Ground Horizon Probe
        # Test 5 sample points along each ray for ground collision
        sample_dists = np.array([1.5, 3.5, 7.0, 12.0, 18.0], dtype=np.float32) # (5,)
        # probe points: (48, 5, 3)
        probes = origin[None, None, :] + flat_dirs[:, None, :] * sample_dists[None, :, None]
        
        px = probes[:, :, 0]
        py = probes[:, :, 1]
        pz = probes[:, :, 2]
        
        # Vectorized terrain calculation: h = 1.2 + sin(x*0.15)*cos(y*0.15)*1.5 + sin(x*0.3+1.2)*sin(y*0.3+0.8)*0.8
        h1 = np.sin(px * 0.15) * np.cos(py * 0.15) * 1.5
        h2 = np.sin(px * 0.3 + 1.2) * np.sin(py * 0.3 + 0.8) * 0.8
        ter_z = np.maximum(0.2, 1.2 + h1 + h2)
        
        below_ground = (pz <= ter_z) | (px < 0) | (px > self.size_x) | (py < 0) | (py > self.size_y)
        # Find first distance below ground
        has_ground_hit = np.any(below_ground, axis=1)
        first_ground_idx = np.argmax(below_ground, axis=1)
        ground_hit_dists = np.where(has_ground_hit, sample_dists[first_ground_idx], max_range)
        depths_flat = np.minimum(depths_flat, ground_hit_dists)

        depths = depths_flat.reshape(num_elevation, num_azimuth)
        closest_dist = float(np.min(depths))

        return {
            "depth_matrix": depths,
            "ray_dirs": ray_dirs,
            "closest_obstacle_dist": closest_dist,
            "spotted_other_agent": spotted_other_agent
        }

