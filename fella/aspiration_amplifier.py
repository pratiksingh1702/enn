"""
FELLA Aspiration Amplifier: Incompletion Tension & Energy Gradient Drive
========================================================================
Pure Continuous Physics:
- Calculates Incompletion Tension T_incomplete = ||x_current - x_goal||
- Forces continuous trajectory propagation when T_incomplete > 0.30
- Zero hardcoded templates, zero grammar rules, zero dictionary lookups.
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple, List
from fella.core_substrate import StackedSubstrate, FellaNeuron


class AspirationAmplifier:
    """
    Continuous Aspiration Drive Engine.
    Monitors pattern completeness and applies physical potential gradients
    to complete incomplete thought trajectories.
    """
    def __init__(self, substrate: StackedSubstrate, tension_threshold: float = 0.30):
        self.substrate = substrate
        self.tension_threshold = float(tension_threshold)
        self.aspiration_history: List[float] = []

    def compute_incompletion_tension(self, x_current: np.ndarray, x_goal: Optional[np.ndarray] = None) -> float:
        """
        Calculates continuous incompletion tension T = ||x_current - x_goal||.
        T > 0.30 indicates an unresolved or truncated energy trajectory.
        """
        if x_goal is None or len(x_goal) == 0:
            # If no target provided, evaluate against the Tier 3 Causal Law centroid
            causal_neurons = [n for n in self.substrate.neurons.values() if n.tier_z >= 3]
            if causal_neurons:
                x_goal = np.mean([n.x for n in causal_neurons], axis=0)
            else:
                x_goal = np.roll(x_current, 1) * 0.90
                
        norm_c = np.linalg.norm(x_current)
        norm_g = np.linalg.norm(x_goal)
        
        if norm_c == 0.0 or norm_g == 0.0:
            return 1.0
            
        u_c = x_current / norm_c
        u_g = x_goal / norm_g
        
        tension = float(np.linalg.norm(u_c - u_g))
        return tension

    def apply_completion_gradient(self, x_current: np.ndarray, x_goal: Optional[np.ndarray] = None, alpha: float = 0.40) -> Tuple[bool, float, np.ndarray]:
        """
        Evaluates tension. If tension > threshold, applies a continuous energy
        gradient to propel x_current along the physical trajectory toward x_goal.
        """
        tension = self.compute_incompletion_tension(x_current, x_goal)
        self.aspiration_history.append(tension)
        
        if tension > self.tension_threshold:
            if x_goal is None or len(x_goal) == 0:
                causal_neurons = [n for n in self.substrate.neurons.values() if n.tier_z >= 3]
                if causal_neurons:
                    x_goal = np.mean([n.x for n in causal_neurons], axis=0)
                else:
                    x_goal = np.roll(x_current, 1) * 0.90
                    
            u_g = x_goal / np.linalg.norm(x_goal) if np.linalg.norm(x_goal) > 0 else x_goal
            u_c = x_current / np.linalg.norm(x_current) if np.linalg.norm(x_current) > 0 else x_current
            
            direction = u_g - u_c
            propelled_wave = u_c + alpha * direction
            norm_p = np.linalg.norm(propelled_wave)
            if norm_p > 0:
                propelled_wave = propelled_wave / norm_p
                
            return True, tension, propelled_wave
            
        return False, tension, x_current
