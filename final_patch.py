import os

def apply_final_patch():
    # 1. Update TruePhysicsEngine
    engine_code = """import numpy as np
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
"""
    with open(r'c:\Users\Dell\Downloads\enn\fella\true_physics_engine.py', 'w', encoding='utf-8') as f:
        f.write(engine_code)
        
    # 2. Update language_grounding.py
    lg_path = r'c:\Users\Dell\Downloads\enn\fella\language_grounding.py'
    with open(lg_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find the injection block from the previous patch
    start_marker = "                # TRUE PHYSICS: Hamiltonian Potential Well"
    end_marker = "            if next_id is None:\n                break"
    
    if start_marker in content and end_marker in content:
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker) + len(end_marker)
        
        new_block = """                # TRUE PHYSICS: Hamiltonian Potential Well
                potential_well = 1.0 / (flow_bonus * cluster_bonus * tier_boost * cond_boost * wave_boost * inhibition * gravity_penalty + 1e-9)
                candidates.append((target_id, float(conductance), target_n.x, potential_well))
                
            next_id = None
            w_trans = 1.0
            
            if candidates:
                # Calculate Tier 3 Causal Anchor for Frustration
                causal_momentum = momentum_wave
                tier_3_vectors = []
                for tgt, w in curr_n.synapses.items():
                    if tgt in self.substrate.neurons and self.substrate.neurons[tgt].tier_z >= 3:
                        tier_3_vectors.append(self.substrate.neurons[tgt].x)
                if tier_3_vectors:
                    causal_momentum = np.mean(tier_3_vectors, axis=0)
                    
                cand_ids = [c[0] for c in candidates]
                conductances = [c[1] for c in candidates]
                vectors = np.array([c[2] for c in candidates])
                wells = np.array([c[3] for c in candidates])
                
                physics = TruePhysicsEngine(temperature=0.5)
                next_id, prob, H, frust = physics.boltzmann_thermodynamic_step(
                    cand_ids, conductances, vectors, causal_momentum, wells
                )
                
                # Retrieve original w_trans
                for c in candidates:
                    if c[0] == next_id:
                        w_trans = c[1]
                        break
            else:
                break # Clean collapse into uncertainty if no paths exist"""
                
        new_content = content[:start_idx] + new_block + content[end_idx:]
        with open(lg_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Patch successfully applied!")
    else:
        print("Could not find patch markers. File might be out of sync.")

if __name__ == '__main__':
    apply_final_patch()
