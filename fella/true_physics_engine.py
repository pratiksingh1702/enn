import numpy as np
from typing import List, Tuple

class TruePhysicsEngine:
    def __init__(self, temperature: float = 0.5):
        self.temperature = temperature
        
    def boltzmann_thermodynamic_step(self, 
                                     candidates: List[str], 
                                     conductances: List[float], 
                                     candidate_vectors: np.ndarray, 
                                     causal_momentum: np.ndarray,
                                     potential_wells: np.ndarray) -> Tuple[str, float, float, float]:
        energies = []
        momentum_norm = causal_momentum / (np.linalg.norm(causal_momentum) + 1e-9)
        
        frustrations = []
        for i, c in enumerate(conductances):
            resistance = 1.0 / (c + 1e-9)
            vec = candidate_vectors[i]
            v_norm = vec / (np.linalg.norm(vec) + 1e-9)
            frustration = 1.0 - np.dot(momentum_norm, v_norm)
            
            # H = Resistance + Causal Frustration + Syntax Potential
            H = resistance + (2.5 * frustration) + potential_wells[i]
            energies.append(H)
            frustrations.append(frustration)
            
        energies = np.array(energies)
        # Prevent overflow in exp by subtracting min energy
        # e^(-E/T) / sum(e^(-E/T)) is invariant to shift
        shift_E = energies - np.min(energies)
        boltzmann_factors = np.exp(-shift_E / self.temperature)
        Z = np.sum(boltzmann_factors)
        probs = boltzmann_factors / Z
        
        chosen_idx = np.random.choice(len(candidates), p=probs)
        return candidates[chosen_idx], probs[chosen_idx], energies[chosen_idx], frustrations[chosen_idx]
