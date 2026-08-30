"""
FELLA Coherence Stabilizer: Hamiltonian Friction & Wave Revision Loop
=====================================================================
Pure Continuous Physics:
- Monitors continuous Hamiltonian friction F_Ham = 0.5 * m * ||v||^2 + V(x)
- Triggers physical wave relaxation and deformation when friction exceeds 0.65
- Zero hardcoded templates, zero grammar rules, zero pre-defined dictionaries.
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple, List
from fella.core_substrate import StackedSubstrate


class CoherenceStabilizer:
    """
    Continuous Coherence Stabilizer.
    Evaluates physical Hamiltonian energy friction and performs wave relaxation.
    """
    def __init__(self, substrate: StackedSubstrate, friction_threshold: float = 0.65):
        self.substrate = substrate
        self.friction_threshold = float(friction_threshold)
        self.stabilization_history: List[float] = []

    def compute_hamiltonian_friction(self, x_wave: np.ndarray, v_velocity: Optional[np.ndarray] = None) -> float:
        """
        Calculates continuous Hamiltonian energy friction:
        F_Ham = Kinetic Energy + Potential Field Friction.
        """
        if v_velocity is None:
            v_velocity = np.zeros_like(x_wave)
            
        kinetic = 0.5 * float(np.sum(v_velocity ** 2))
        
        # Potential field friction V(x) from substrate
        forces = self.substrate.compute_field_resonance(x_wave)
        if forces:
            max_force = max(forces.values())
            potential_friction = 1.0 - min(1.0, max_force)
        else:
            potential_friction = 1.0
            
        total_friction = kinetic + potential_friction
        return float(total_friction)

    def relax_and_stabilize_wave(self, x_wave: np.ndarray, max_iterations: int = 5) -> Tuple[bool, float, np.ndarray]:
        """
        If Hamiltonian friction > threshold, applies thermodynamic relaxation
        and deforms the candidate wave into a minimal-friction attractor basin.
        """
        curr_wave = np.array(x_wave, dtype=float).copy()
        initial_friction = self.compute_hamiltonian_friction(curr_wave)
        self.stabilization_history.append(initial_friction)
        
        if initial_friction <= self.friction_threshold:
            return False, initial_friction, curr_wave
            
        # Apply continuous relaxation loop
        for step in range(max_iterations):
            forces = self.substrate.compute_field_resonance(curr_wave)
            if not forces:
                break
                
            best_nid = max(forces.items(), key=lambda item: item[1])[0]
            best_n = self.substrate.neurons[best_nid]
            
            # Gradient pull toward nearest physical attractor
            diff = best_n.x - curr_wave
            curr_wave += 0.25 * diff
            norm_w = np.linalg.norm(curr_wave)
            if norm_w > 0:
                curr_wave = curr_wave / norm_w
                
            friction = self.compute_hamiltonian_friction(curr_wave)
            if friction <= self.friction_threshold:
                return True, friction, curr_wave
                
        final_friction = self.compute_hamiltonian_friction(curr_wave)
        return True, final_friction, curr_wave
