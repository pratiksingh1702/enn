"""
FELLA Curiosity Engine: Epistemic Friction & Wave Propagation
==============================================================
Pure Continuous Physics:
- Calculates Epistemic Friction H = 1 - cos(x_current, x_known)
- Triggers field tension and unprompted wave propagation when H > 0.70
- Zero hardcoded templates, zero word lists, zero pre-defined questions.
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple, List
from fella.core_substrate import StackedSubstrate


class CuriosityEngine:
    """
    Continuous Epistemic Curiosity Engine.
    Detects knowledge voids and propagates field curiosity waves toward novel substrate regions.
    """
    def __init__(self, substrate: StackedSubstrate, friction_threshold: float = 0.70):
        self.substrate = substrate
        self.friction_threshold = float(friction_threshold)
        self.curiosity_history: List[float] = []

    def compute_epistemic_friction(self, x_current: np.ndarray, x_known: Optional[np.ndarray] = None) -> float:
        """
        Calculates continuous epistemic friction H_epistemic = 1 - cos(x_current, x_known).
        High friction (H > 0.70) signifies an ungrounded or novel concept void.
        """
        norm_curr = np.linalg.norm(x_current)
        if norm_curr == 0.0:
            return 1.0
            
        u_curr = x_current / norm_curr
        
        if x_known is None or len(x_known) == 0:
            # Evaluate against substrate mean state
            if not self.substrate.neurons:
                return 1.0
            all_x = np.array([n.x for n in self.substrate.neurons.values() if n.tier_z > 0])
            if len(all_x) == 0:
                return 1.0
            x_known = np.mean(all_x, axis=0)
            
        norm_known = np.linalg.norm(x_known)
        if norm_known == 0.0:
            return 1.0
            
        u_known = x_known / norm_known
        cos_sim = float(np.dot(u_curr, u_known))
        friction = 1.0 - max(-1.0, min(1.0, cos_sim))
        return float(friction)

    def trigger_curiosity_wave(self, seed_wave: np.ndarray) -> Tuple[bool, float, np.ndarray]:
        """
        Evaluates incoming perturbation. If epistemic friction > threshold,
        generates an orthogonal curiosity wave packet in continuous space.
        """
        friction = self.compute_epistemic_friction(seed_wave)
        self.curiosity_history.append(friction)
        
        if friction > self.friction_threshold:
            # Epistemic Vacuum: Generate orthogonal curiosity wave vector
            orthogonal_push = np.roll(seed_wave, 2) * 0.7071 - np.roll(seed_wave, -2) * 0.7071
            norm_push = np.linalg.norm(orthogonal_push)
            curiosity_wave = orthogonal_push / norm_push if norm_push > 0 else seed_wave
            return True, friction, curiosity_wave
            
        return False, friction, seed_wave
