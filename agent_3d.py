"""
Embodied Self-Aware 3D Agent Engine
===================================
Features:
- Multimodal Sensory Cortex (Continuous 360° Vision Rays + Acoustic Helmholtz Diffraction + 3D Proprioception).
- Inward Metacognitive Observer (Self-Identity Vector, Epistemic Friction, Self-Confidence Dynamics).
- Continuous 3D Motor Phase Collapse (Smooth 6-DOF Steering & Thrust).
- Self-Tuning Aspiration & Starvation Gravitation in 3D space.
"""

import numpy as np
from typing import Dict, Any, Tuple, List, Optional
from collections import deque
from enn4d import DualFieldENN
from self_awareness_core import InwardSelfObserver
from world_3d import World3D


class SelfAware3DAgent:
    """
    Continuous 3D Self-Aware Living Organism.
    Embodied in World3D with DualFieldENN brain and Inward Metacognitive Mirror.
    """
    def __init__(self, system: Optional[DualFieldENN] = None):
        self.system = system if system is not None else DualFieldENN(dim=4)
        self.observer = InwardSelfObserver(dim=4)
        
        # 3D Kinematics State
        self.pos = np.array([2.0, 2.0, 1.5], dtype=float)     # (x, y, z)
        self.velocity = np.zeros(3, dtype=float)              # (vx, vy, vz)
        self.yaw = 0.0                                        # Horizontal azimuth in radians [0, 2pi)
        self.pitch = 0.0                                      # Elevation in radians [-pi/4, pi/4]
        self.drag_coeff = 0.15
        self.max_speed = 1.8
        
        # Energy & Experience Telemetry
        self.energy_budget = 300.0
        self.goals_harvested = 0
        self.collisions = 0
        self.flight_path: deque = deque(maxlen=200)
        self.flight_path.append(tuple(self.pos))
        
        # Spatial Memory Trace in 3D
        self.spatial_trace_3d: Dict[Tuple[int, int, int], float] = {}
        
        # Motor Action Vectors in R^4 Basis
        rng = np.random.RandomState(101)
        q, _ = np.linalg.qr(rng.randn(4, 4))
        self.v_forward = q[:, 0]
        self.v_turn_left = q[:, 1]
        self.v_turn_right = -q[:, 1]
        self.v_pitch_up = q[:, 2]
        self.v_pitch_down = -q[:, 2]

    def reset(self, start_pos: Tuple[float, float, float] = (2.0, 2.0, 1.5), energy: float = 300.0):
        """Reset agent bodily state for new continuous simulation."""
        self.pos = np.array(start_pos, dtype=float)
        self.velocity = np.zeros(3, dtype=float)
        self.yaw = 0.0
        self.pitch = 0.0
        self.energy_budget = float(energy)
        self.goals_harvested = 0
        self.collisions = 0
        self.flight_path.clear()
        self.flight_path.append(tuple(self.pos))
        self.spatial_trace_3d.clear()
        self.observer.update_metabolism(self.energy_budget)

    def perceive_and_fuse_wave(self, world: World3D, sim_time: float = 0.0) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Multimodal 3D Sensory Perception:
        1. 360° Visual Depth Raycast (Obstacle Repulsion & Corridor Flow).
        2. Acoustic Wave Diffraction (Sound gradient from acoustic beacons).
        3. 3D Proprioceptive Kinematics (Velocity, Heading, Energy).
        4. Inward Self-Identity & Confidence Wave.
        Fuses all 4 modalities into a single continuous 4D wave packet.
        """
        # 1. Visual Raycast
        vis_data = world.cast_visual_rays(self.pos, self.yaw, self.pitch, num_azimuth=16, num_elevation=3)
        depths = vis_data["depth_matrix"] # shape (3, 16)
        ray_dirs = vis_data["ray_dirs"]   # shape (3, 16, 3)
        
        # Compute visual gradient vector in 3D: weighted sum of open ray directions (inverse obstacle repulsion)
        vis_flux_3d = np.zeros(3)
        for e in range(depths.shape[0]):
            for a in range(depths.shape[1]):
                d = depths[e, a]
                r_dir = ray_dirs[e, a]
                # Open corridors (large d) pull forward; close barriers (small d) push away
                weight = (d / 15.0)**1.5 - (1.5 / (d + 0.5))
                vis_flux_3d += r_dir * weight
                
        vis_norm = np.linalg.norm(vis_flux_3d)
        if vis_norm > 0:
            vis_flux_3d /= vis_norm

        # Project 3D visual flux to 4D Brain Basis
        # Forward alignment dot product
        forward_dir = np.array([np.cos(self.pitch) * np.cos(self.yaw), np.cos(self.pitch) * np.sin(self.yaw), np.sin(self.pitch)])
        lateral_dir = np.array([-np.sin(self.yaw), np.cos(self.yaw), 0.0])
        up_dir = np.array([0.0, 0.0, 1.0])
        
        f_vis_fwd = float(np.dot(vis_flux_3d, forward_dir))
        f_vis_lat = float(np.dot(vis_flux_3d, lateral_dir))
        f_vis_up  = float(np.dot(vis_flux_3d, up_dir))
        
        w_vision = (f_vis_fwd * self.v_forward + 
                    f_vis_lat * (self.v_turn_left if f_vis_lat > 0 else self.v_turn_right) + 
                    f_vis_up * (self.v_pitch_up if f_vis_up > 0 else self.v_pitch_down))

        # 2. Diffractive Acoustic Sound Wave
        p_sound, sound_flux_3d = world.sample_acoustics(self.pos, t=sim_time)
        f_snd_fwd = float(np.dot(sound_flux_3d, forward_dir))
        f_snd_lat = float(np.dot(sound_flux_3d, lateral_dir))
        f_snd_up  = float(np.dot(sound_flux_3d, up_dir))
        
        # Sound amplifies under starvation stress (greedy goal seeking)
        stress_factor = float(1.0 + 1.5 * self.observer.metabolic_stress)
        w_sound = stress_factor * (f_snd_fwd * self.v_forward + 
                                   f_snd_lat * (self.v_turn_left if f_snd_lat > 0 else self.v_turn_right) + 
                                   f_snd_up * (self.v_pitch_up if f_snd_up > 0 else self.v_pitch_down))

        # 3. Proprioception & 3D Spatial Trace
        grid_voxel = (int(self.pos[0]), int(self.pos[1]), int(self.pos[2]))
        trace_val = self.spatial_trace_3d.get(grid_voxel, 0.0)
        speed = float(np.linalg.norm(self.velocity))
        w_proprio = (self.v_forward * max(0.1, 1.0 - trace_val)) * 0.8 + (self.v_pitch_up * (1.5 - self.pos[2]) * 0.4)

        # 4. Inward Self-Identity & Confidence Wave (The Metacognitive Mirror)
        w_self = self.observer.generate_inward_self_wave(aspiration_strength=self.system.meta_field.aspiration_strength)

        # Multimodal Superposition
        net_sensory_wave = 0.35 * w_vision + 0.30 * w_sound + 0.15 * w_proprio + 0.20 * w_self
        norm_sens = np.linalg.norm(net_sensory_wave)
        if norm_sens > 0:
            net_sensory_wave /= norm_sens
        else:
            net_sensory_wave = self.v_forward.copy()

        telemetry = {
            "closest_obstacle": vis_data["closest_dist"],
            "sound_pressure": p_sound,
            "sound_flux_mag": float(np.linalg.norm(sound_flux_3d)),
            "self_confidence": self.observer.self_confidence,
            "epistemic_friction": self.observer.epistemic_friction,
            "metabolic_stress": self.observer.metabolic_stress
        }
        return net_sensory_wave, telemetry

    def step(self, world: World3D, dt: float = 0.1, sim_time: float = 0.0) -> Dict[str, Any]:
        """
        Execute one continuous 3D physical perception-reasoning-action-reflection cycle.
        """
        # 1. Update internal metabolic proprioception
        self.energy_budget -= 0.25
        self.observer.update_metabolism(self.energy_budget)
        self.system.update_metabolic_state(self.energy_budget)
        
        # 2. Multimodal Perception & Wave Fusion
        sensory_wave, tele = self.perceive_and_fuse_wave(world, sim_time=sim_time)
        
        # 3. Formulate Forward Intention Wave (Metacognitive Prediction)
        intended_action_estimate = sensory_wave.copy()
        intent_wave = self.observer.prepare_intention_wave(intended_action_estimate, sensory_wave)
        
        # 4. Reason through Coupled 4D Substrate (World Field -> Trait Field Phase Collapse)
        reason_res = self.system.reason(sensory_wave, query_text="3D continuous spatial navigation", max_steps=3)
        
        # Continuous 3D Motor Phase Collapse:
        # Calculate projection along directional basis vectors
        out_wave = sensory_wave # Phase collapsed output
        turn_pull = float(np.dot(out_wave, self.v_turn_left) - np.dot(out_wave, self.v_turn_right))
        pitch_pull = float(np.dot(out_wave, self.v_pitch_up) - np.dot(out_wave, self.v_pitch_down))
        fwd_pull = float(np.dot(out_wave, self.v_forward))
        
        # Convert pulls to smooth continuous steering and thrust
        d_yaw = float(np.clip(turn_pull * 0.45, -np.pi / 5.0, np.pi / 5.0))
        d_pitch = float(np.clip(pitch_pull * 0.30, -np.pi / 8.0, np.pi / 8.0))
        thrust = float(np.clip(0.3 + 0.7 * max(0.0, fwd_pull), 0.1, 1.0))
        
        # Confidence-based velocity modulation:
        # If organism is confident -> Full speed; If high epistemic friction -> Slow and probe
        thrust *= self.observer.self_confidence
        
        # 5. Continuous 3D Physics Integration
        self.yaw = (self.yaw + d_yaw) % (2.0 * np.pi)
        self.pitch = float(np.clip(self.pitch + d_pitch, -np.pi / 4.0, np.pi / 4.0))
        
        # Thrust force vector in world coords
        heading_3d = np.array([
            np.cos(self.pitch) * np.cos(self.yaw),
            np.cos(self.pitch) * np.sin(self.yaw),
            np.sin(self.pitch)
        ])
        
        thrust_force = heading_3d * (thrust * 1.5)
        # Apply Drag & Acceleration
        self.velocity = self.velocity * (1.0 - self.drag_coeff) + thrust_force * dt
        speed = np.linalg.norm(self.velocity)
        if speed > self.max_speed:
            self.velocity = (self.velocity / speed) * self.max_speed
            
        proposed_pos = self.pos + self.velocity * dt
        
        # 6. Physical Collision & Boundary Reaction
        outcome = "gliding"
        reward = 0.0
        
        colliding, normal = world.check_collision_and_normal(self.pos, proposed_pos, radius=0.35)
        if colliding and normal is not None:
            self.collisions += 1
            self.energy_budget -= 0.5
            outcome = "barrier_collision"
            reward = -0.5
            # Elastic reflection along surface normal
            v_dot_n = float(np.dot(self.velocity, normal))
            if v_dot_n < 0:
                self.velocity = self.velocity - 1.4 * v_dot_n * normal
            self.pos = self.pos + normal * 0.12 # Positional standoff
        else:
            self.pos = proposed_pos
            
            # Check proximity to acoustic goal beacons
            for beacon in world.beacons:
                dist_beacon = float(np.linalg.norm(self.pos - beacon.pos))
                if dist_beacon < 1.4:
                    self.goals_harvested += 1
                    self.energy_budget += 50.0
                    reward = +1.5
                    outcome = "goal_harvested"
                    
        # Update 3D spatial trace
        grid_voxel = (int(self.pos[0]), int(self.pos[1]), int(self.pos[2]))
        for k in list(self.spatial_trace_3d.keys()):
            self.spatial_trace_3d[k] *= 0.95
            if self.spatial_trace_3d[k] < 0.02:
                del self.spatial_trace_3d[k]
        self.spatial_trace_3d[grid_voxel] = 1.0
        self.flight_path.append(tuple(self.pos.copy()))
        
        # 7. Inward Metacognitive Reflection Loop
        # Observe actual outcome wave vs intended prediction wave
        outcome_wave = sensory_wave * (1.0 if outcome != "barrier_collision" else -1.0)
        reflection = self.observer.observe_sensory_outcome(outcome_wave, motor_effort=thrust_force)
        
        # Self-Tuning Aspiration & Retrograde Synaptic Consolidation
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
            "outcome": outcome,
            "reward": reward,
            "energy_budget": self.energy_budget,
            "goals_harvested": self.goals_harvested,
            "collisions": self.collisions,
            "epistemic_friction": reflection["epistemic_friction"],
            "self_confidence": reflection["self_confidence"],
            "body_world_coherence": reflection["body_world_coherence"],
            "metabolic_stress": self.observer.metabolic_stress,
            "closest_obstacle": tele["closest_obstacle"],
            "sound_pressure": tele["sound_pressure"]
        }
