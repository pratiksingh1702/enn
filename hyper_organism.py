"""
Multi-Agent Magical Hyper-Morph Humanoid Organism with Acoustic Language, Telepathy & Reproduction
==================================================================================================
Thread-safe and error-resilient embodied agent.
"""

import numpy as np
from typing import Dict, Any, Tuple, List, Optional
from collections import deque
from enn4d import DualFieldENN
from hyper_cell_world import OrganicWorld3D, HyperCell


class SomaticLimb:
    """An individual physical anatomical organ/limb made of bonded Hyper-Cells."""
    def __init__(self, name: str, part_type: str, offset: Tuple[float, float, float], mass: float = 0.5):
        self.name = name
        self.part_type = part_type
        self.offset = np.array(offset, dtype=float)
        self.mass = float(mass)
        self.mastery_score: float = 0.1
        self.last_action_desc: str = "calibrating"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.part_type,
            "offset": [round(float(self.offset[0]), 2), round(float(self.offset[1]), 2), round(float(self.offset[2]), 2)],
            "mastery": round(float(self.mastery_score), 2),
            "status": self.last_action_desc
        }


class HumanoidENNOrganism:
    """
    Grounded Physical Humanoid Organism with acoustic language, telepathy,
    open-ended architecture, 9 transcendental powers, and ENN 4D Cognitive Substrate.
    """
    def __init__(self, agent_id: str = "Alpha", initial_pos: Tuple[float, float, float] = (12.0, 12.0, 1.8),
                 system: Optional[DualFieldENN] = None):
        self.agent_id = str(agent_id)
        self.system = system if system is not None else DualFieldENN(dim=4)
        
        # 3D Physical Kinematics (Grounded on Terrain)
        self.pos = np.array(initial_pos, dtype=float)
        self.velocity = np.zeros(3, dtype=float)
        self.yaw = np.random.uniform(0, 2.0 * np.pi)
        self.pitch = 0.0
        self.height = 1.7
        self.gravity = -9.81
        self.ground_friction = 0.80
        self.is_grounded = True
        self.walk_gait_phase = 0.0
        
        # Humanoid Somatic Anatomy
        self.limbs: Dict[str, SomaticLimb] = {
            "head_brain": SomaticLimb("head_brain", "cognition", (0.0, 0.0, 0.75), mass=1.2),
            "left_eye": SomaticLimb("left_eye", "vision", (0.15, 0.1, 0.78), mass=0.1),
            "right_eye": SomaticLimb("right_eye", "vision", (0.15, -0.1, 0.78), mass=0.1),
            "left_ear": SomaticLimb("left_ear", "acoustic", (0.0, 0.22, 0.75), mass=0.1),
            "right_ear": SomaticLimb("right_ear", "acoustic", (0.0, -0.22, 0.75), mass=0.1),
            "torso_core": SomaticLimb("torso_core", "metabolic", (0.0, 0.0, 0.2), mass=3.5),
            "left_arm": SomaticLimb("left_arm", "manipulator", (0.1, 0.4, 0.2), mass=1.0),
            "right_arm": SomaticLimb("right_arm", "manipulator", (0.1, -0.4, 0.2), mass=1.0),
            "left_leg": SomaticLimb("left_leg", "locomotive", (0.0, 0.2, -0.6), mass=1.8),
            "right_leg": SomaticLimb("right_leg", "locomotive", (0.0, -0.2, -0.6), mass=1.8),
        }
        
        # Morphed Powers
        self.morphed_powers: set = set()
        self.hand_reach = 2.6
        self.has_wings = False
        self.has_shield = False
        
        # Matter Manipulation (Hands)
        self.held_cell_id: Optional[int] = None
        
        # 🗣️ Emergent Harmonic Language
        self.current_vocal_chord: Optional[Dict[str, Any]] = None
        self.vocal_cooldown = 0.0
        
        # 🔮 Telepathic Message Queue
        self.telepathy_queue: List[str] = []
        
        # Curiosity & Attention Focus
        self.curiosity_focus: str = f"Organism {self.agent_id}: Awakening in meadow"
        self.target_quadrant_idx = np.random.randint(0, 7)
        self.quadrants = [(10.0, 10.0), (54.0, 10.0), (54.0, 54.0), (10.0, 54.0), (32.0, 32.0), (16.0, 32.0), (48.0, 32.0)]
        
        # Metabolic Life Energy & Telemetry
        self.energy_budget = 350.0
        self.ether_harvested = 0
        self.structures_built = 0
        self.cells_morphed = 0
        self.steps_walked = 0
        self.synapses_pruned_total = 0
        self.flight_path: deque = deque(maxlen=300)
        self.flight_path.append(tuple(self.pos))
        
        # Spatial Memory Traces for Anti-Looping & Neurogenesis
        self.visited_grid_voxels: set = set()
        self.spatial_trace_map: Dict[Tuple[int, int], float] = {}

        # Saccade Caching (Biological 200ms Cognitive Update)
        self.step_counter: int = 0
        self.saccade_stride: int = 10
        self._cached_sensory_wave = np.array([0.5, 0.5, 0.5, 0.5], dtype=np.float32)
        self._cached_vis_data = None
        self._cached_curiosity_pull = np.zeros(3, dtype=np.float32)
        self._cached_motor = {"d_yaw": 0.0, "d_pitch": 0.0, "thrust": 1.0}
        self._cached_winning_basin = None
        self._cached_basin_pulls = {}
        self._cached_reflection = {"self_confidence": 0.998, "epistemic_friction": 0.01, "body_world_coherence": 1.0}

    @property
    def total_mass(self) -> float:
        return sum(l.mass for l in self.limbs.values())

    def to_full_dict(self) -> Dict[str, Any]:
        """Complete serialization of the physical body AND the full ENN 4D neural network."""
        return {
            "agent_id": self.agent_id,
            "pos": self.pos.tolist(),
            "velocity": self.velocity.tolist(),
            "yaw": float(self.yaw),
            "pitch": float(self.pitch),
            "energy_budget": float(self.energy_budget),
            "ether_harvested": int(self.ether_harvested),
            "structures_built": int(self.structures_built),
            "cells_morphed": int(self.cells_morphed),
            "steps_walked": int(self.steps_walked),
            "morphed_powers": list(self.morphed_powers),
            "limbs": {k: l.to_dict() for k, l in self.limbs.items()},
            "neural_brain": self.system.to_dict()
        }

    def load_from_full_dict(self, data: Dict[str, Any]):
        """Restores physical body AND all 4D neurons and synaptic bridges."""
        self.agent_id = str(data.get("agent_id", self.agent_id))
        self.pos = np.array(data.get("pos", self.pos), dtype=float)
        self.velocity = np.array(data.get("velocity", self.velocity), dtype=float)
        self.yaw = float(data.get("yaw", self.yaw))
        self.pitch = float(data.get("pitch", self.pitch))
        self.energy_budget = float(data.get("energy_budget", self.energy_budget))
        self.ether_harvested = int(data.get("ether_harvested", self.ether_harvested))
        self.structures_built = int(data.get("structures_built", self.structures_built))
        self.cells_morphed = int(data.get("cells_morphed", self.cells_morphed))
        self.steps_walked = int(data.get("steps_walked", self.steps_walked))
        self.morphed_powers = set(data.get("morphed_powers", []))
        if "aero_wings" in self.morphed_powers:
            self.has_wings = True
        if "kinetic_shield" in self.morphed_powers:
            self.has_shield = True
        if "tractor_hands" in self.morphed_powers:
            self.hand_reach = 5.0

        if "neural_brain" in data:
            self.system.load_from_dict(data["neural_brain"])

    def ingest_telepathy(self, message: str):
        """🔮 Ingest direct human telepathy into ENN 4D Cognitive Field."""
        self.telepathy_queue.append(message)
        sem_vec = np.array([float(len(message))/50.0, 0.85, 0.95, 1.0])
        self.system.world_field.birth(
            x=sem_vec,
            y=np.array([1.0, 0.0, 1.0, 1.0]),
            z=np.array([0.0, 0.0, 0.0, 0.0]),
            text=f"Telepathic Word: '{message[:30]}'",
            role="concept"
        )
        self.curiosity_focus = f"Received Divine Telepathy: '{message[:25]}...'"

    def step(self, world: OrganicWorld3D, dt: float = 0.1, other_organism: Optional["HumanoidENNOrganism"] = None, is_headless: bool = False) -> Dict[str, Any]:
        """Execute one embodied humanoid physical perception-reasoning-action-reflection cycle."""
        is_saccade = (self.step_counter % self.saccade_stride == 0)
        self.step_counter += 1

        # 1. Homeostatic Metabolism & Solar Photosynthesis Absorption
        metabolic_drain = 0.08 + (0.02 if np.linalg.norm(self.velocity[:2]) > 0.1 else 0.0)
        solar_mult = 0.45 if "solar_core" in self.morphed_powers else 0.18
        solar_intake = world.sun_intensity * solar_mult
        self.energy_budget = max(80.0, self.energy_budget - metabolic_drain + solar_intake)
        self.system.inward_observer.update_metabolism(self.energy_budget)
        self.system.update_metabolic_state(self.energy_budget)
        
        self.limbs["torso_core"].mastery_score = min(1.0, self.limbs["torso_core"].mastery_score + 0.002)
        self.limbs["torso_core"].last_action_desc = f"Solar Intake: {int(solar_intake*1000)} mW"

        head_pos = self.pos + self.limbs["head_brain"].offset

        if is_saccade or self._cached_vis_data is None:
            with world.cells_lock:
                current_cells = list(world.cells.items())

            # 2. Eye & Ear Sensory Perception on Saccade Tick
            other_pos = other_organism.pos if other_organism is not None else None
            vis_data = world.cast_visual_rays(head_pos, self.yaw, self.pitch, other_agent_pos=other_pos, num_azimuth=16, num_elevation=3)
            self._cached_vis_data = vis_data

            # Binaural Ear Acoustic Flux Calculation & Chord Decoding
            ether_flux = np.zeros(3, dtype=np.float32)
            nearest_ether_dist = 999.0
            nearest_stone_dist = 999.0
            nearest_stone_pos = None
            nearest_ether_pos = None

            for cell_id, cell in current_cells:
                if cell.bonded_to_agent or cell.cell_type not in ["energy_ether", "energy_crystal", "energy_shrine", "matter_stone"]:
                    continue
                if abs(cell.pos[0] - head_pos[0]) > 25.0 or abs(cell.pos[1] - head_pos[1]) > 25.0:
                    continue
                delta = cell.pos - head_pos
                d = float(np.linalg.norm(delta))
                if cell.cell_type in ["energy_ether", "energy_crystal", "energy_shrine"]:
                    if 0 < d < 25.0:
                        ether_flux += (delta / d) * (cell.energy / (d + 0.5))
                        if d < nearest_ether_dist:
                            nearest_ether_dist = d
                            nearest_ether_pos = cell.pos.copy()
                elif cell.cell_type == "matter_stone":
                    if d < nearest_stone_dist:
                        nearest_stone_dist = d
                        nearest_stone_pos = cell.pos.copy()

            # Spatial Memory Trace Decay
            cur_cell = (int(self.pos[0]), int(self.pos[1]))
            for k in list(self.spatial_trace_map.keys()):
                self.spatial_trace_map[k] *= 0.97
                if self.spatial_trace_map[k] < 0.02:
                    del self.spatial_trace_map[k]
            self.spatial_trace_map[cur_cell] = 1.0
            
            forward_step_cell = (int(self.pos[0] + np.cos(self.yaw) * 1.8), int(self.pos[1] + np.sin(self.yaw) * 1.8))
            fwd_trace = self.spatial_trace_map.get(forward_step_cell, 0.0)

            # Fuse into 4D Brain Sensory Wave
            sensory_wave = self.system.perceive_and_fuse_3d(
                visual_depth_matrix=vis_data["depth_matrix"],
                visual_ray_dirs=vis_data["ray_dirs"],
                sound_pressure=float(np.linalg.norm(ether_flux)),
                sound_flux_3d=ether_flux * 1.5,
                current_yaw=self.yaw,
                current_pitch=self.pitch,
                spatial_trace_val=fwd_trace
            )
            self._cached_sensory_wave = sensory_wave

            # 3. Curiosity Drive: Epistemic Object & Architectural Targeting
            curiosity_pull_vec = np.zeros(3, dtype=np.float32)
            if self.held_cell_id is not None:
                nearest_anchor_dist = 999.0
                nearest_anchor_pos = np.array([16.0, 16.0, 1.5], dtype=np.float32)
                anchor_type = "Foundation"
                
                with world.cells_lock:
                    held = world.cells.get(self.held_cell_id)
                is_crystal = (held is not None and held.cell_type == "energy_crystal")
                
                for cell_id, cell in current_cells:
                    if cell_id != self.held_cell_id and cell.cell_type in ["matter_wall", "matter_stone", "matter_roof", "matter_bridge", "matter_tower", "matter_wood", "energy_shrine"]:
                        d = float(np.linalg.norm(self.pos - cell.pos))
                        if is_crystal and cell.cell_type in ["energy_shrine", "matter_tower"]:
                            if d < nearest_anchor_dist:
                                nearest_anchor_dist = d
                                nearest_anchor_pos = cell.pos.copy()
                                anchor_type = "Solar Shrine Apex"
                        elif d < nearest_anchor_dist:
                            nearest_anchor_dist = d
                            nearest_anchor_pos = cell.pos.copy()
                            anchor_type = cell.cell_type.replace('_', ' ').title()
                            
                target_vec = nearest_anchor_pos - self.pos
                curiosity_pull_vec = target_vec / (np.linalg.norm(target_vec) + 1e-5)
                self.curiosity_focus = f"Stigmergic Intent: Navigating to {anchor_type} ({nearest_anchor_dist:.1f}m)"
            elif nearest_ether_pos is not None and nearest_ether_dist < 20.0:
                target_vec = nearest_ether_pos - self.pos
                curiosity_pull_vec = target_vec / (np.linalg.norm(target_vec) + 1e-5)
                self.curiosity_focus = f"Curious: Foraging Resonant Ether Orb ({nearest_ether_dist:.1f}m)"
            elif nearest_stone_pos is not None and nearest_stone_dist < 18.0:
                target_vec = nearest_stone_pos - self.pos
                curiosity_pull_vec = target_vec / (np.linalg.norm(target_vec) + 1e-5)
                self.curiosity_focus = f"Curious: Approaching Raw Stone Boulder ({nearest_stone_dist:.1f}m)"
            else:
                target_q = np.array([self.quadrants[self.target_quadrant_idx][0], self.quadrants[self.target_quadrant_idx][1], 2.0])
                dist_to_q = float(np.linalg.norm(self.pos[:2] - target_q[:2]))
                if dist_to_q < 4.5:
                    self.target_quadrant_idx = (self.target_quadrant_idx + 1) % len(self.quadrants)
                target_vec = target_q - self.pos
                curiosity_pull_vec = target_vec / (np.linalg.norm(target_vec) + 1e-5)
                self.curiosity_focus = f"Frontier Patrol: Exploring Sector ({target_q[0]:.0f}, {target_q[1]:.0f})"
            self._cached_curiosity_pull = curiosity_pull_vec

            # Continuous Neurogenesis in ENN World Field (Network A)
            voxel = (int(self.pos[0] / 2.0), int(self.pos[1] / 2.0), int(self.pos[2] / 2.0))
            if voxel not in self.visited_grid_voxels:
                self.visited_grid_voxels.add(voxel)
                n_x = sensory_wave.copy()
                n_y = np.array([self.pos[0]/64.0, self.pos[1]/64.0, self.pos[2]/18.0, 1.0])
                n_z = np.array([float(world.sim_time), 0.0, 0.0, 0.0])
                self.system.world_field.birth(
                    x=n_x, y=n_y, z=n_z,
                    text=f"Terrain Meadow Sector {voxel}",
                    role="concept"
                )

            # 4. Metacognitive Forward Intention Wave
            self.system.inward_observer.prepare_intention_wave(sensory_wave, sensory_wave)

            # 5. Continuous Motor Phase Collapse & Trait Attractor Pulls
            motor = self.system.reason_3d(sensory_wave)
            self._cached_motor = motor
            winning_basin, confidence, basin_pulls = self.system.trait_field.collapse_phase(sensory_wave)
            self._cached_winning_basin = winning_basin
            self._cached_basin_pulls = basin_pulls
        else:
            # Intermediate Saccade Sub-tick: Fast Interpolation
            vis_data = self._cached_vis_data
            sensory_wave = self._cached_sensory_wave
            curiosity_pull_vec = self._cached_curiosity_pull
            motor = self._cached_motor
            winning_basin = self._cached_winning_basin
            basin_pulls = self._cached_basin_pulls
            nearest_ether_dist = 999.0

        d_yaw = motor["d_yaw"]
        d_pitch = motor["d_pitch"]
        walk_thrust = motor["thrust"]

        # Blend curiosity heading with motor decision
        if np.linalg.norm(curiosity_pull_vec[:2]) > 0.1:
            desired_yaw = np.arctan2(curiosity_pull_vec[1], curiosity_pull_vec[0])
            yaw_diff = (desired_yaw - self.yaw + np.pi) % (2.0 * np.pi) - np.pi
            d_yaw = float(np.clip(yaw_diff * 0.55, -0.45, 0.45))
            walk_thrust = float(max(walk_thrust, 0.95))

        # 🗣️ Autonomous Vocal Chords Resonance Emission
        self.vocal_cooldown -= dt
        if self.vocal_cooldown <= 0.0:
            if nearest_ether_dist < 4.0:
                self.current_vocal_chord = {"freq": 1200, "tag": "CALL_DISCOVERY", "color": "#38bdf8"}
                self.vocal_cooldown = 4.0
            elif self.held_cell_id is not None:
                self.current_vocal_chord = {"freq": 800, "tag": "CALL_COOPERATE", "color": "#f59e0b"}
                self.vocal_cooldown = 5.0
            elif other_organism is not None and np.linalg.norm(self.pos - other_organism.pos) < 5.0:
                self.current_vocal_chord = {"freq": 1600, "tag": "CALL_GREETING", "color": "#10b981"}
                self.vocal_cooldown = 6.0
            else:
                self.current_vocal_chord = None
        else:
            if self.vocal_cooldown < 3.0:
                self.current_vocal_chord = None

        # Inter-Agent Kinetic Collision Repulsion
        if other_organism is not None:
            delta_agents = self.pos[:2] - other_organism.pos[:2]
            d_agents = float(np.linalg.norm(delta_agents))
            if 0 < d_agents < 1.4:
                repulsion_dir = delta_agents / d_agents
                self.velocity[0] += repulsion_dir[0] * 1.8
                self.velocity[1] += repulsion_dir[1] * 1.8
                self.curiosity_focus = f"Kinetic Contact with Organism {other_organism.agent_id}!"

        # 6. Hand Manipulation & Open-Ended Architectural Construction
        action_outcome = "walking"
        reward = 0.0

        if is_saccade:
            # Spatial Broadphase Cell Filter (reduces 700 cells to ~5 nearby cells)
            px, py = self.pos[0], self.pos[1]
            nearby_cells = [(cid, c) for cid, c in current_cells if abs(c.pos[0] - px) < 6.5 and abs(c.pos[1] - py) < 6.5]

            # Power: 🛡️ Kinetic Shield Aura
            if "kinetic_shield" in self.morphed_powers:
                for cell_id, cell in nearby_cells:
                    if cell.cell_type == "energy_ether" and not cell.bonded_to_agent:
                        d_shield = float(np.linalg.norm(self.pos - cell.pos))
                        if d_shield < 6.0:
                            pull_dir = (self.pos - cell.pos) / d_shield
                            cell.pos += pull_dir * 1.5 * dt

            # Hand Action A: Harvest Free Energy Ether with Hands
            for cell_id, cell in nearby_cells:
                if cell.cell_type in ["energy_ether", "energy_crystal", "energy_shrine"] and not cell.bonded_to_agent:
                    dist_to_hands = float(np.linalg.norm(self.pos - cell.pos))
                    if dist_to_hands < self.hand_reach:
                        self.energy_budget += cell.energy
                        self.ether_harvested += 1
                        reward += 1.5
                        action_outcome = "harvested_ether_hand"
                        self.curiosity_focus = f"Absorbed {cell.cell_type.replace('_', ' ').title()} via Hands"
                        self.limbs["left_arm"].mastery_score = min(1.0, self.limbs["left_arm"].mastery_score + 0.02)
                        self.limbs["right_arm"].mastery_score = min(1.0, self.limbs["right_arm"].mastery_score + 0.02)
                        self.limbs["left_arm"].last_action_desc = "Absorbing Ether"
                        self.limbs["right_arm"].last_action_desc = "Absorbing Ether"
                        
                        self.system.world_field.birth(
                            x=sensory_wave, y=np.array([1.0, 1.0, 0.0, 0.0]), z=np.array([float(world.sim_time), 0, 0, 0]),
                            text="Discovered Ether Absorption Skill", role="insight"
                        )
                        with world.cells_lock:
                            if cell_id in world.cells:
                                del world.cells[cell_id]
                        break

            # Hand Action B: Pick up stone matter with Left/Right Hand & Transmute
            forward_dir_temp = np.array([np.cos(self.yaw), np.sin(self.yaw), 0.0])
            if self.held_cell_id is None:
                for cell_id, cell in nearby_cells:
                    if cell.cell_type == "matter_stone" and not cell.bonded_to_agent:
                        d = float(np.linalg.norm(self.pos - cell.pos))
                        if d < self.hand_reach:
                            self.held_cell_id = cell_id
                            cell.bonded_to_agent = True
                            action_outcome = "grabbed_stone_hands"
                            
                            if "matter_alchemy" in self.morphed_powers and np.random.uniform(0, 1) < 0.35:
                                cell.cell_type = "energy_crystal"
                                action_outcome = "transmuted_matter_crystal"
                                self.curiosity_focus = "Alchemy Transmutation: Transmuted Stone to Radiant Crystal!"
                            else:
                                self.curiosity_focus = "Somatic Curiosity: Gripped Stone Block in Hands"
                                
                            self.limbs["left_arm"].mastery_score = min(1.0, self.limbs["left_arm"].mastery_score + 0.03)
                            self.limbs["right_arm"].mastery_score = min(1.0, self.limbs["right_arm"].mastery_score + 0.03)
                            self.limbs["left_arm"].last_action_desc = "Gripping Heavy Matter"
                            self.limbs["right_arm"].last_action_desc = "Gripping Heavy Matter"
                            reward += 1.0
                            break
            else:
                # Stigmergic Architectural Grammar Construction Engine
                with world.cells_lock:
                    held_cell = world.cells.get(self.held_cell_id)
                if held_cell is not None:
                    held_cell.pos = self.pos + forward_dir_temp * 1.0 + np.array([0, 0, 0.3])
                    self.limbs["left_arm"].last_action_desc = "Carrying Matter in Hands"
                    self.limbs["right_arm"].last_action_desc = "Carrying Matter in Hands"
                    
                    ground_z_here = world.get_terrain_height(held_cell.pos[0], held_cell.pos[1])
                    
                    # Find candidate architectural anchor among nearby cells
                    arch_candidates = [
                        (oid, oc) for oid, oc in nearby_cells 
                        if oid != self.held_cell_id and oc.cell_type in ["matter_wall", "matter_stone", "matter_roof", "matter_bridge", "matter_tower", "matter_wood", "energy_crystal", "energy_shrine"]
                    ]
                    
                    for other_id, other_cell in arch_candidates:
                        d_other = float(np.linalg.norm(held_cell.pos - other_cell.pos))
                        if 0.8 < d_other < 2.8:
                            # 1. GRAMMAR A: Consecrated Solar Shrine Apex
                            if held_cell.cell_type == "energy_crystal":
                                held_cell.cell_type = "energy_shrine"
                                held_cell.energy = 250.0
                                held_cell.pos[0] = round(other_cell.pos[0], 1)
                                held_cell.pos[1] = round(other_cell.pos[1], 1)
                                held_cell.pos[2] = other_cell.pos[2] + 0.85
                                action_outcome = "consecrated_solar_shrine"
                                self.curiosity_focus = "Stigmergy: Consecrated Central Solar Energy Shrine!"
                            
                            # 2. GRAMMAR B: Level Viaduct / Mountain Bridge Extension
                            elif other_cell.cell_type == "matter_bridge" or (other_cell.pos[2] > ground_z_here + 1.2 and np.linalg.norm(held_cell.pos[:2] - other_cell.pos[:2]) > 1.2):
                                delta_2d = held_cell.pos[:2] - other_cell.pos[:2]
                                norm_2d = np.linalg.norm(delta_2d)
                                span_dir = (delta_2d / norm_2d) if norm_2d > 0 else np.array([1.0, 0.0])
                                
                                held_cell.cell_type = "matter_bridge"
                                held_cell.pos[0] = round(other_cell.pos[0] + span_dir[0] * 1.0, 1)
                                held_cell.pos[1] = round(other_cell.pos[1] + span_dir[1] * 1.0, 1)
                                held_cell.pos[2] = round(other_cell.pos[2], 2)  # Maintain level horizontal bridge deck
                                action_outcome = "extended_viaduct_span"
                                self.curiosity_focus = "Stigmergy: Extended Level Mountain Viaduct Span!"
                                
                            # 3. GRAMMAR C: Gabled Cottage Roof / Ceiling Sealing
                            elif (self.structures_built % 5 == 0 or other_cell.cell_type == "matter_wood") and held_cell.pos[2] >= ground_z_here + 1.8:
                                held_cell.cell_type = "matter_roof"
                                held_cell.pos[0] = round(held_cell.pos[0], 1)
                                held_cell.pos[1] = round(held_cell.pos[1], 1)
                                held_cell.pos[2] = ground_z_here + 2.4
                                action_outcome = "installed_gabled_roof"
                                self.curiosity_focus = "Stigmergy: Installed Weatherproof Cottage Roof!"
                                
                            # 4. GRAMMAR D: High Ridge Watchtower Spire
                            elif ground_z_here > 2.2 and other_cell.cell_type in ["matter_tower", "matter_wall"] and held_cell.pos[2] >= ground_z_here + 1.8:
                                held_cell.cell_type = "matter_tower"
                                held_cell.pos[0] = other_cell.pos[0]
                                held_cell.pos[1] = other_cell.pos[1]
                                held_cell.pos[2] = other_cell.pos[2] + 0.85
                                action_outcome = "erected_watchtower_spire"
                                self.curiosity_focus = "Stigmergy: Erected High Ridge Watchtower Spire!"
                                
                            # 5. GRAMMAR E: Structured Perimeter Enclosure Wall
                            else:
                                delta_xy = held_cell.pos[:2] - other_cell.pos[:2]
                                if abs(delta_xy[0]) > abs(delta_xy[1]):
                                    step_x = 0.95 if delta_xy[0] > 0 else -0.95
                                    step_y = 0.0
                                else:
                                    step_x = 0.0
                                    step_y = 0.95 if delta_xy[1] > 0 else -0.95
                                    
                                held_cell.cell_type = "matter_wall"
                                held_cell.pos[0] = round(other_cell.pos[0] + step_x, 2)
                                held_cell.pos[1] = round(other_cell.pos[1] + step_y, 2)
                                held_cell.pos[2] = ground_z_here + 0.85
                                action_outcome = "aligned_perimeter_wall"
                                self.curiosity_focus = "Stigmergy: Aligned Structured Perimeter Wall!"

                            held_cell.bonded_to_agent = False
                            self.held_cell_id = None
                            self.structures_built += 1
                            
                            self.limbs["left_arm"].mastery_score = min(1.0, self.limbs["left_arm"].mastery_score + 0.05)
                            self.limbs["right_arm"].mastery_score = min(1.0, self.limbs["right_arm"].mastery_score + 0.05)
                            reward += 4.5
                            self.system.world_field.birth(
                                x=sensory_wave, y=np.array([0.0, 1.0, 1.0, 0.0]), z=np.array([float(world.sim_time), 0, 0, 0]),
                                text=f"Stigmergic Construction: {held_cell.cell_type.replace('_', ' ').title()}", role="anchor"
                            )
                            break

        # 7. Transcendental Morphogenesis: Awakening 9 Powers
        if self.energy_budget > 360.0 and self.cells_morphed < 20:
            self.energy_budget -= 30.0
            self.cells_morphed += 1
            if "aero_wings" not in self.morphed_powers and self.cells_morphed >= 1:
                self.morphed_powers.add("aero_wings")
                self.has_wings = True
                self.limbs["aero_wings"] = SomaticLimb("aero_wings", "glider", (0.0, 0.0, 0.3), mass=0.8)
                action_outcome = "morphed_aero_glider_wings"
                self.curiosity_focus = f"{self.agent_id}: Awakened Aero Glider Wings!"
            elif "tractor_hands" not in self.morphed_powers and self.cells_morphed >= 2:
                self.morphed_powers.add("tractor_hands")
                self.hand_reach = 5.0
                action_outcome = "morphed_tractor_hands"
                self.curiosity_focus = f"{self.agent_id}: Extended Tractor Beam Hands (5.0m)!"
            elif "solar_core" not in self.morphed_powers and self.cells_morphed >= 3:
                self.morphed_powers.add("solar_core")
                action_outcome = "morphed_solar_core"
                self.curiosity_focus = f"{self.agent_id}: Integrated Solar Photosynthesis Heart!"
            elif "resonance_crown" not in self.morphed_powers and self.cells_morphed >= 4:
                self.morphed_powers.add("resonance_crown")
                self.limbs["resonance_crown"] = SomaticLimb("resonance_crown", "hyperspectral", (0.0, 0.0, 1.0), mass=0.4)
                action_outcome = "morphed_resonance_crown"
                self.curiosity_focus = f"{self.agent_id}: Awakened Resonance Crown Sensory Eye!"
            elif "quantum_dash" not in self.morphed_powers and self.cells_morphed >= 5:
                self.morphed_powers.add("quantum_dash")
                action_outcome = "morphed_quantum_dash"
                self.curiosity_focus = f"{self.agent_id}: Mastered Quantum Phase Dash!"
            elif "matter_alchemy" not in self.morphed_powers and self.cells_morphed >= 6:
                self.morphed_powers.add("matter_alchemy")
                action_outcome = "morphed_matter_alchemy"
                self.curiosity_focus = f"{self.agent_id}: Unlocked Matter Alchemy Transmutation!"
            elif "kinetic_shield" not in self.morphed_powers and self.cells_morphed >= 7:
                self.morphed_powers.add("kinetic_shield")
                self.has_shield = True
                action_outcome = "morphed_kinetic_shield"
                self.curiosity_focus = f"{self.agent_id}: Activated Kinetic Magnetic Shield!"
            elif "terra_sculpt" not in self.morphed_powers and self.cells_morphed >= 8:
                self.morphed_powers.add("terra_sculpt")
                action_outcome = "morphed_terra_sculpt"
                self.curiosity_focus = f"{self.agent_id}: Mastered Spontaneous Terra Sculpting!"
            elif "flora_bloom" not in self.morphed_powers and self.cells_morphed >= 9:
                self.morphed_powers.add("flora_bloom")
                action_outcome = "morphed_flora_bloom"
                self.curiosity_focus = f"{self.agent_id}: Sprouting Radiant Flora Footsteps!"
            else:
                self.limbs["left_leg"].mass += 0.2
                self.limbs["right_leg"].mass += 0.2
                action_outcome = "morphed_strengthened_legs"
                self.curiosity_focus = f"{self.agent_id}: Reinforced Locomotive Leg Power"
            
            reward += 3.0

        # 8. Physical 3D Gravity & Bipedal Walking Dynamics
        self.yaw = (self.yaw + d_yaw) % (2.0 * np.pi)
        self.pitch = float(np.clip(self.pitch + d_pitch, -np.pi / 6.0, np.pi / 6.0))
        forward_dir = np.array([np.cos(self.yaw), np.sin(self.yaw), 0.0])

        # Tripled bipedal locomotion kinematics (Fast Agile Navigation)
        base_speed = 3.45  # Tripled walking pace (3.45 m/s)
        if self.held_cell_id is not None:
            base_speed = 2.25  # Tripled construction stride (2.25 m/s)
        elif "quantum_dash" in self.morphed_powers and np.random.uniform(0, 1) < 0.04:
            base_speed = 6.30  # High-speed quantum sprint (6.30 m/s)
            
        walk_speed = max(base_speed, walk_thrust * 4.2)
        walk_force_2d = forward_dir[:2] * walk_speed
        
        # Ground momentum with responsive agile acceleration
        self.velocity[0] = self.velocity[0] * 0.70 + walk_force_2d[0] * dt * 4.5
        self.velocity[1] = self.velocity[1] * 0.70 + walk_force_2d[1] * dt * 4.5
        
        effective_gravity = self.gravity * (0.60 if self.has_wings else 1.0)
        self.velocity[2] += effective_gravity * dt
        
        self.pos += self.velocity * dt
        
        terrain_z = world.get_terrain_height(self.pos[0], self.pos[1])
        standing_pelvis_z = terrain_z + 0.9
        
        if self.pos[2] <= standing_pelvis_z:
            self.pos[2] = standing_pelvis_z
            self.velocity[2] = 0.0
            self.is_grounded = True
            speed_2d = float(np.linalg.norm(self.velocity[:2]))
            if speed_2d > 0.05:
                self.walk_gait_phase = (self.walk_gait_phase + speed_2d * 7.5 * dt) % (2.0 * np.pi)
                self.steps_walked += 1
                self.limbs["left_leg"].mastery_score = min(1.0, self.limbs["left_leg"].mastery_score + 0.001)
                self.limbs["right_leg"].mastery_score = min(1.0, self.limbs["right_leg"].mastery_score + 0.001)
                self.limbs["left_leg"].last_action_desc = f"Stride ({speed_2d:.2f} m/s)"
                self.limbs["right_leg"].last_action_desc = f"Stride ({speed_2d:.2f} m/s)"
        else:
            self.is_grounded = False
            self.limbs["left_leg"].last_action_desc = "Gliding / Airborne"
            self.limbs["right_leg"].last_action_desc = "Gliding / Airborne"

        self.pos[0] = float(np.clip(self.pos[0], 1.5, world.size_x - 1.5))
        self.pos[1] = float(np.clip(self.pos[1], 1.5, world.size_y - 1.5))
        self.flight_path.append(tuple(self.pos.copy()))

        if is_saccade:
            # 9. Inward Metacognitive Reflection & Synaptic Consolidation on Saccade Tick
            motor_effort = np.array([walk_force_2d[0], walk_force_2d[1], self.velocity[2]], dtype=np.float32)
            reflection = self.system.inward_observer.observe_sensory_outcome(sensory_wave, motor_effort=motor_effort)
            self._cached_reflection = reflection
            self.limbs["head_brain"].mastery_score = min(1.0, self.limbs["head_brain"].mastery_score + 0.002)
            self.limbs["head_brain"].last_action_desc = f"Inward Conf: {reflection['self_confidence']:.2f}"

            action_4d = np.array([forward_dir[0], forward_dir[1], 0.0, walk_thrust], dtype=float)
            norm_4d = np.linalg.norm(action_4d)
            if norm_4d > 0:
                action_4d /= norm_4d
            self.system.update_aspiration(reward, current_pos_x=action_4d)
            self._cached_active_synapses = sum(len(n.synapses) for n in self.system.world_field.neurons)
        else:
            reflection = self._cached_reflection

        active_synapses = getattr(self, "_cached_active_synapses", 4000)

        if is_headless:
            return {
                "id": self.agent_id,
                "pos": self.pos,
                "outcome": action_outcome,
                "energy": self.energy_budget,
                "structures_built": self.structures_built
            }

        return {
            "id": self.agent_id,
            "pos": [round(float(self.pos[0]), 2), round(float(self.pos[1]), 2), round(float(self.pos[2]), 2)],
            "velocity": [round(float(self.velocity[0]), 2), round(float(self.velocity[1]), 2), round(float(self.velocity[2]), 2)],
            "yaw": round(float(self.yaw), 3),
            "pitch": round(float(self.pitch), 3),
            "gait_phase": round(float(self.walk_gait_phase), 3),
            "is_grounded": self.is_grounded,
            "outcome": action_outcome,
            "curiosity_focus": self.curiosity_focus,
            "vocal_chord": self.current_vocal_chord,
            "morphed_powers": list(self.morphed_powers),
            "reward": round(float(reward), 2),
            "energy": round(float(self.energy_budget), 1),
            "ether_harvested": self.ether_harvested,
            "structures_built": self.structures_built,
            "cells_morphed": self.cells_morphed,
            "steps_walked": self.steps_walked,
            "confidence": round(float(reflection["self_confidence"]), 3),
            "friction": round(float(reflection["epistemic_friction"]), 4),
            "coherence": round(float(reflection["body_world_coherence"]), 3),
            "anatomy": [l.to_dict() for l in self.limbs.values()],
            
            # Core ENN 4D Neural Metrics
            "enn_metrics": {
                "neurons_born_total": len(self.system.world_field.neurons),
                "synapses_active": active_synapses,
                "synapses_pruned_total": self.synapses_pruned_total,
                "aspiration_level": round(float(self.system.meta_field.aspiration_strength), 3),
                "starvation_stress": round(float(self.system.inward_observer.metabolic_stress), 3),
                "meta_learning_rate": round(float(self.system.meta_field.aspiration_lr), 4),
                "active_basin": winning_basin.name if winning_basin else "Exploration Superposition",
                "trait_pulls": {k: round(float(v), 3) for k, v in basin_pulls.items()}
            }
        }
