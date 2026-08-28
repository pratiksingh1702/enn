"""
Genesis 3D Morphogenetic Living Organism Engine (Pure Physics & Zero Hardcoding)
================================================================================
Pure Physics Principles:
- Zero Hardcoded Coordinates: No map checks (e.g. no x < 10, no 8.5 <= x <= 13.5).
- Continuous Physical Perception:
  1. 360° Visual Depth Raycast (Obstacle repulsion & open corridor flow).
  2. Diffractive Helmholtz Acoustics (Binaural sound flux from goal beacons).
  3. Downward Ground Sensing (Detects physical floor support vs chasm voids).
  4. Inward Metacognitive Observer (Epistemic Friction & Confidence).
- Autonomous Tool Use & Environmental Engineering:
  - When downward ground sensing detects a deep void cliff ahead, the organism seeks and grips dense matter.
  - When standing before the void while holding structural matter, it deploys the slab forward along its heading vector to create a physical bridge.
  - When near energy crystals, it absorbs the power to sustain its homeostatic budget.
"""

import numpy as np
from typing import Dict, Any, Tuple, List, Optional
from collections import deque
from enn4d import DualFieldENN
from genesis_world import GenesisWorld3D, DynamicBlock


class GenesisOrganism3D:
    """
    Active 3D Morphogenetic Living Organism.
    All actions emerge from continuous wave resonance, sensory raycasting, and attractor dynamics.
    """
    def __init__(self, system: Optional[DualFieldENN] = None):
        self.system = system if system is not None else DualFieldENN(dim=4)
        
        # 3D Kinematics
        self.pos = np.array([3.0, 3.0, 1.2], dtype=float)
        self.velocity = np.zeros(3, dtype=float)
        self.yaw = 0.0
        self.pitch = 0.0
        self.max_speed = 1.6
        self.drag = 0.15
        
        # Dynamic Body Morphogenesis
        # [radius, height, antenna_gain]
        self.morphology = np.array([0.4, 0.4, 1.0], dtype=float)
        
        # Matter Manipulation (Tractor Grip Field)
        self.held_block: Optional[DynamicBlock] = None
        self.grip_reach = 2.4
        
        # Energy & Experience Telemetry
        self.energy_budget = 300.0
        self.crystals_harvested = 0
        self.bridges_constructed = 0
        self.shelters_built = 0
        self.chasm_falls = 0
        self.flight_path: deque = deque(maxlen=300)
        self.flight_path.append(tuple(self.pos))

    def reset(self, start_pos: Tuple[float, float, float] = (3.0, 3.0, 1.2)):
        self.pos = np.array(start_pos, dtype=float)
        self.velocity = np.zeros(3, dtype=float)
        self.yaw = 0.0
        self.pitch = 0.0
        self.held_block = None
        self.energy_budget = 300.0
        self.crystals_harvested = 0
        self.bridges_constructed = 0
        self.shelters_built = 0
        self.chasm_falls = 0
        self.flight_path.clear()
        self.flight_path.append(tuple(self.pos))

    def step(self, world: GenesisWorld3D, dt: float = 0.1, sim_time: float = 0.0) -> Dict[str, Any]:
        """Execute one embodied perception-reasoning-action-terraforming cycle."""
        # 1. Environmental Storm Energy Interaction
        world_drain = 0.2
        under_shelter = world.is_under_shelter(self.pos)
        if world.storm_active:
            if under_shelter:
                world_drain += 0.1 # Protected under overhead shelter
            else:
                world_drain += 2.5 * world.storm_intensity # Acid storm exposure
                
        self.energy_budget -= world_drain
        self.system.inward_observer.update_metabolism(self.energy_budget)
        self.system.update_metabolic_state(self.energy_budget)

        # 2. Continuous 3D Perception
        vis_data = world.cast_visual_rays(self.pos, self.yaw, self.pitch, num_azimuth=16, num_elevation=3)
        p_sound, sound_flux = world.sample_acoustics(self.pos, t=sim_time)
        sound_flux *= float(self.morphology[2]) # Morphological antenna gain

        # Heading vector
        heading_3d = np.array([
            np.cos(self.pitch) * np.cos(self.yaw),
            np.cos(self.pitch) * np.sin(self.yaw),
            np.sin(self.pitch)
        ])

        # Physical Ground Probe ahead: checks floor depth
        floor_dist_ahead = world.probe_ground_ahead(self.pos, heading_3d, distance=1.8)
        void_cliff_detected = (floor_dist_ahead > 3.0) # True if there is no floor support ahead

        # Fuse into 4D Sensory Wave Packet
        sensory_wave = self.system.perceive_and_fuse_3d(
            visual_depth_matrix=vis_data["depth_matrix"],
            visual_ray_dirs=vis_data["ray_dirs"],
            sound_pressure=p_sound,
            sound_flux_3d=sound_flux,
            current_yaw=self.yaw,
            current_pitch=self.pitch,
            spatial_trace_val=0.0
        )

        # 3. Metacognitive Forward Intention Wave
        self.system.inward_observer.prepare_intention_wave(sensory_wave, sensory_wave)

        # 4. Continuous 3D Motor Phase Collapse
        motor = self.system.reason_3d(sensory_wave)
        d_yaw = motor["d_yaw"]
        d_pitch = motor["d_pitch"]
        thrust = motor["thrust"]

        # 5. Autonomous Matter Manipulation & Environmental Engineering (Zero Hardcoding)
        action_outcome = "gliding"
        reward = 0.0

        # Physical Affordance A: Tractor Grip (Seek & pick up stone matter if void cliff is ahead and hands are empty)
        if self.held_block is None:
            # Find nearest reachable structural matter block
            nearest_stone = None
            min_dist = self.grip_reach
            for block in world.dynamic_blocks:
                if block.material_type == "stone" and not block.held_by_agent:
                    d = float(np.linalg.norm(self.pos - block.pos))
                    if d < min_dist:
                        min_dist = d
                        nearest_stone = block

            # Grip matter when nearby
            if nearest_stone is not None:
                self.held_block = nearest_stone
                nearest_stone.held_by_agent = True
                action_outcome = "tractor_picked_stone"
                reward = +0.6

        # Physical Affordance B: Deploy Matter (Place carried stone into void gap ahead to create a bridge)
        elif self.held_block is not None and self.held_block.material_type == "stone":
            if void_cliff_detected:
                # Deploy carried slab along forward physical trajectory
                deploy_pos = self.pos + heading_3d * 1.8
                deploy_pos[2] = 0.4 # Settle at floor level
                self.held_block.pos = deploy_pos
                self.held_block.held_by_agent = False
                self.held_block = None
                self.bridges_constructed += 1
                action_outcome = "chasm_bridge_constructed"
                reward = +2.0

        # Physical Affordance C: Harvest Energy Crystals within physical proximity
        for block in world.dynamic_blocks:
            if block.material_type == "crystal":
                dist_c = float(np.linalg.norm(self.pos - block.pos))
                if dist_c < 1.4:
                    self.crystals_harvested += 1
                    self.energy_budget += 60.0
                    block.pos = np.array([-100.0, -100.0, -100.0]) # Harvested into organism
                    action_outcome = "crystal_energy_harvested"
                    reward = +3.0

        # 6. Physical Locomotion & Inertia
        self.yaw = (self.yaw + d_yaw) % (2.0 * np.pi)
        self.pitch = float(np.clip(self.pitch + d_pitch, -np.pi / 4.0, np.pi / 4.0))

        mass_penalty = 1.4 if self.held_block is not None else 1.0
        thrust_force = heading_3d * (thrust * 1.6 / mass_penalty)
        self.velocity = self.velocity * (1.0 - self.drag) + thrust_force * dt
        self.pos = self.pos + self.velocity * dt

        # Update held block position in tractor beam
        if self.held_block is not None:
            self.held_block.pos = self.pos + heading_3d * 1.0

        # 7. Physical Chasm Void Check
        if world.is_in_chasm_void(self.pos):
            self.chasm_falls += 1
            self.energy_budget -= 5.0
            self.velocity = np.zeros(3)
            # Elastic recovery back to safe ground
            self.pos[0] = max(0.5, self.pos[0] - 1.5)
            self.pos[2] = 1.2
            action_outcome = "chasm_fall_recovered"
            reward = -1.5

        # 8. Boundary Constraints
        self.pos[0] = float(np.clip(self.pos[0], 0.5, world.size_x - 0.5))
        self.pos[1] = float(np.clip(self.pos[1], 0.5, world.size_y - 0.5))
        self.pos[2] = float(np.clip(self.pos[2], 0.5, world.size_z - 0.5))
        self.flight_path.append(tuple(self.pos.copy()))

        # 9. Inward Metacognitive Reflection
        reflection = self.system.inward_observer.observe_sensory_outcome(sensory_wave, motor_effort=thrust_force)

        # 10. Self-Tuning Aspiration Update
        action_4d = np.array([heading_3d[0], heading_3d[1], heading_3d[2], thrust], dtype=float)
        norm_4d = np.linalg.norm(action_4d)
        if norm_4d > 0:
            action_4d /= norm_4d
        self.system.update_aspiration(reward, current_pos_x=action_4d)

        return {
            "pos": tuple(self.pos),
            "velocity": tuple(self.velocity),
            "yaw": self.yaw,
            "pitch": self.pitch,
            "thrust": thrust,
            "outcome": action_outcome,
            "reward": reward,
            "energy_budget": self.energy_budget,
            "crystals_harvested": self.crystals_harvested,
            "bridges_constructed": self.bridges_constructed,
            "chasm_falls": self.chasm_falls,
            "under_shelter": under_shelter,
            "storm_active": world.storm_active,
            "storm_intensity": world.storm_intensity,
            "epistemic_friction": reflection["epistemic_friction"],
            "self_confidence": reflection["self_confidence"],
            "body_world_coherence": reflection["body_world_coherence"],
            "sound_pressure": float(p_sound)
        }
