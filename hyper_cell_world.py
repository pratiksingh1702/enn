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
    def __init__(self, size_x: float = 32.0, size_y: float = 32.0, max_height: float = 14.0, restore_file: Optional[str] = None):
        self.size_x = float(size_x)
        self.size_y = float(size_y)
        self.max_height = float(max_height)
        self.cells: Dict[int, HyperCell] = {}
        self.cells_lock = threading.Lock()
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
        """Continuous multi-scale harmonic terrain heightmap: z = h(x, y)."""
        x_c = np.clip(x, 0.0, self.size_x)
        y_c = np.clip(y, 0.0, self.size_y)
        
        h1 = np.sin(x_c * 0.15) * np.cos(y_c * 0.15) * 1.5
        h2 = np.sin(x_c * 0.30 + 1.2) * np.sin(y_c * 0.30 + 0.8) * 0.8
        h3 = np.cos(np.sqrt((x_c - 16.0)**2 + (y_c - 16.0)**2) * 0.25) * 0.6
        
        base_h = 1.2 + h1 + h2 + h3
        return float(np.clip(base_h, 0.2, self.max_height - 1.0))

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
                    energy=c_data.get("energy", 10.0),
                    radius=c_data.get("radius", 0.4)
                )
                self.cells[cid] = c
                if cid >= self.next_cell_id:
                    self.next_cell_id = cid + 1
            print(f"Restored {len(self.cells)} hyper-cells from {file_path} successfully!")
        except Exception as e:
            print(f"Error restoring world: {e}")
            self._populate_initial_world()

    def _populate_initial_world(self):
        ground_center = self.get_terrain_height(16.0, 16.0)
        for x in range(14, 19):
            for y in range(14, 19):
                is_wall = (x == 14 or x == 18 or y == 14 or y == 18)
                is_door = (x == 16 and y == 18)
                if is_wall and not is_door:
                    for z_lvl in range(1, 4):
                        z_pos = ground_center + z_lvl * 0.9
                        self.spawn_cell((float(x), float(y), z_pos), cell_type="matter_wall", energy=10.0)
                self.spawn_cell((float(x), float(y), ground_center + 3.7), cell_type="matter_wood", energy=10.0)

        for _ in range(25):
            self._spawn_random_ether()

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
            return cell

    def update_physics(self, dt: float = 0.1):
        """Update environmental time, weather transitions, wildlife, daylight, and ether blooming."""
        self.sim_time += dt
        solar_phase = (self.sim_time / 240.0) * 2.0 * np.pi
        self.sun_intensity = float(max(0.12, (np.sin(solar_phase) + 1.0) / 2.0))

        # Weather Transitions
        self.weather_timer += dt
        if self.weather_timer > 90.0:
            self.weather_timer = 0.0
            weathers = ["clear", "rain", "storm", "aurora", "clear"]
            self.weather_type = weathers[np.random.randint(0, len(weathers))]

        # Update Wildlife
        for f in self.fauna:
            f.update(self, dt)

        # Regrowth
        with self.cells_lock:
            cells_list = list(self.cells.values())
            
        active_ether_count = sum(1 for c in cells_list if c.cell_type == "energy_ether")
        if active_ether_count < 28 and (self.sim_time - self.last_ether_spawn > 3.0):
            self.last_ether_spawn = self.sim_time
            self._spawn_random_ether()

        active_stone_count = sum(1 for c in cells_list if c.cell_type == "matter_stone")
        if active_stone_count < 16 and (self.sim_time - self.last_stone_spawn > 5.0):
            self.last_stone_spawn = self.sim_time
            self._spawn_random_stone()

        for cell in cells_list:
            cell.update_phase(dt)
            if cell.cell_type == "energy_ether" and not cell.bonded_to_agent:
                cell.pos[2] += np.sin(cell.phase) * 0.025 * dt
                ground_z = self.get_terrain_height(cell.pos[0], cell.pos[1])
                if cell.pos[2] < ground_z + 0.6:
                    cell.pos[2] = ground_z + 0.6

    def cast_visual_rays(self, origin: np.ndarray, yaw: float, pitch: float, other_agent_pos: Optional[np.ndarray] = None,
                          num_azimuth: int = 16, num_elevation: int = 3, max_range: float = 22.0) -> Dict[str, Any]:
        """Thread-safe continuous visual depth raycast probing terrain, architecture, and other organisms."""
        azimuths = np.linspace(0.0, 2.0 * np.pi, num_azimuth, endpoint=False)
        elevations = np.linspace(-np.pi / 6.0, np.pi / 6.0, num_elevation)

        depths = np.zeros((num_elevation, num_azimuth))
        ray_dirs = np.zeros((num_elevation, num_azimuth, 3))
        closest_dist = max_range
        spotted_other_agent = False

        with self.cells_lock:
            current_cells = list(self.cells.values())

        for e_idx, el in enumerate(elevations):
            for a_idx, az in enumerate(azimuths):
                dx = np.cos(pitch + el) * np.cos(yaw + az)
                dy = np.cos(pitch + el) * np.sin(yaw + az)
                dz = np.sin(pitch + el)
                r_dir = np.array([dx, dy, dz], dtype=float)
                ray_dirs[e_idx, a_idx] = r_dir

                ray_dist = max_range
                for step_d in np.linspace(0.5, max_range, 14):
                    probe_pt = origin + r_dir * step_d
                    
                    if other_agent_pos is not None:
                        dist_to_other = np.linalg.norm(probe_pt - other_agent_pos)
                        if dist_to_other < 0.8:
                            ray_dist = float(step_d)
                            spotted_other_agent = True
                            break

                    if 0.0 <= probe_pt[0] <= self.size_x and 0.0 <= probe_pt[1] <= self.size_y:
                        ter_z = self.get_terrain_height(probe_pt[0], probe_pt[1])
                        if probe_pt[2] <= ter_z:
                            ray_dist = float(step_d)
                            break
                        
                        hit_cell = False
                        for cell in current_cells:
                            if not cell.bonded_to_agent and np.linalg.norm(probe_pt - cell.pos) < cell.radius + 0.25:
                                ray_dist = float(step_d)
                                hit_cell = True
                                break
                        if hit_cell:
                            break
                    else:
                        ray_dist = float(step_d)
                        break

                depths[e_idx, a_idx] = ray_dist
                if ray_dist < closest_dist:
                    closest_dist = ray_dist

        return {
            "depth_matrix": depths,
            "ray_dirs": ray_dirs,
            "closest_obstacle_dist": closest_dist,
            "spotted_other_agent": spotted_other_agent
        }
