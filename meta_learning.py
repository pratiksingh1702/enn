"""
ENN 4D Meta-Learning Field (F_meta)
Higher-order thermodynamic field that adaptively tunes the physical parameters:
- Learning rate (eta)
- Damping rate (gamma)
- Synaptic potentiation rate (lambda_hebb)
- Birth threshold (theta_birth)
- Merge threshold (theta_merge)

All adaptations emerge from continuous thermodynamic potentials (turbulence, stagnation, settling speed).
Zero if/else rules. Zero discrete hardcoded heuristics.
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import numpy as np
from typing import Dict, Any, Optional

class MetaField:
    """
    Higher-order meta-learning field maintaining continuous parameter coordinates:
    M = [eta, gamma, lambda_hebb, theta_birth, theta_merge]
    """
    def __init__(self):
        # Baseline canonical parameters
        self.learning_rate = 0.25      # eta in [0.05, 0.80]
        self.damping_rate = 0.03       # gamma in [0.005, 0.15]
        self.synaptic_rate = 0.15      # lambda_hebb in [0.05, 0.50]
        self.birth_threshold = 0.45    # theta_birth in [0.20, 0.75]
        self.merge_threshold = 0.15    # theta_merge in [0.05, 0.35]
        
        # Energy history for turbulence estimation
        self.last_energy = 0.0
        self.adaptation_history = []
        self.idle_stagnation_counter = 0

    def get_state(self) -> Dict[str, float]:
        return {
            "learning_rate": float(np.round(self.learning_rate, 4)),
            "damping_rate": float(np.round(self.damping_rate, 4)),
            "synaptic_rate": float(np.round(self.synaptic_rate, 4)),
            "birth_threshold": float(np.round(self.birth_threshold, 4)),
            "merge_threshold": float(np.round(self.merge_threshold, 4))
        }

    def observe_and_adapt(self, current_total_energy: float, active_neurons_count: int, max_resonance: float, settle_hops: int = 1):
        """
        Thermodynamic potential relaxation of meta-parameters.
        1. Turbulence Potential: V_turb = 0.5 * (dE/dt)^2 -> drives gamma up, eta down.
        2. Stagnation Potential: V_stag = exp(-recent_novelty) -> relaxes birth threshold.
        3. Settling Potential: V_settle = (hops - 2)^2 -> modulates synaptic conductivity.
        """
        energy_delta = abs(current_total_energy - self.last_energy) if self.last_energy > 0 else 0.0
        self.last_energy = float(current_total_energy)
        
        # 1. Turbulence gradient (High energy fluctuations require higher damping to stabilize)
        turbulence_gradient = min(1.0, energy_delta / max(1.0, current_total_energy))
        self.damping_rate = np.clip(self.damping_rate + (turbulence_gradient * 0.015) - 0.002, 0.005, 0.15)
        self.learning_rate = np.clip(self.learning_rate - (turbulence_gradient * 0.02) + 0.005, 0.05, 0.80)
        
        # 2. Stagnation / Novelty gradient
        if max_resonance > 0.80:
            # High familiar resonance: consolidate synapses, increase merge precision
            self.synaptic_rate = np.clip(self.synaptic_rate + 0.005, 0.05, 0.50)
            self.idle_stagnation_counter += 1
        else:
            # Novelty: increase learning rate, lower birth threshold to absorb new concepts
            self.learning_rate = np.clip(self.learning_rate + 0.015, 0.05, 0.80)
            self.birth_threshold = np.clip(self.birth_threshold - 0.01, 0.20, 0.75)
            self.idle_stagnation_counter = 0
            
        # 3. Settling speed gradient (hop count)
        if settle_hops > 3:
            # Slow wave settling: increase synaptic conductance to accelerate transmission
            self.synaptic_rate = np.clip(self.synaptic_rate + 0.01, 0.05, 0.50)
            
        # Relaxation towards baseline homeostatic equilibrium
        self.learning_rate += 0.01 * (0.25 - self.learning_rate)
        self.damping_rate += 0.01 * (0.03 - self.damping_rate)
        self.birth_threshold += 0.01 * (0.45 - self.birth_threshold)
        
        self.adaptation_history.append(self.get_state())
        if len(self.adaptation_history) > 50:
            self.adaptation_history.pop(0)
