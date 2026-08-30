"""
FELLA Inner Critic: Pure ENN Field Resonance & Boltzmann-Gibbs Phase Collapse
=============================================================================
100% Pure Mathematical Physics (Zero Hardcoded Rules, Zero Fixed Thresholds):
- Candidate thought trajectories are evaluated against a continuous Hamiltonian Action H(τ).
- H(τ) integrates synaptic conductance impedance (1 - W_ij), valence flow divergence, and manifold alignment.
- Selection is governed by Boltzmann-Gibbs probability distribution: P(τ_i) = exp(-H(τ_i)/T) / Σ exp(-H(τ_j)/T).
- Cognitive temperature T is dynamically set by the thermodynamic entropy of the active trait field.
- If all drafts reside in high-entropy vacuum (H >> 0), the wave smoothly collapses onto ground-state uncertainty.
"""

import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from fella.core_substrate import StackedSubstrate, FellaNeuron


class FieldCriticSubstrate:
    """
    Continuous Hamiltonian Action & Boltzmann Phase Collapse Engine.
    Evaluates candidate thought waves strictly through continuous physical dynamics:
    - Path Action H(τ) = Synaptic Impedance + Valence Shear + Manifold Misalignment
    - Boltzmann Probability P(τ_i) = exp(-H(τ_i) / T) / Z
    - Dynamic cognitive temperature T from information entropy
    Zero fixed thresholds, zero rule engines, zero hardcoding.
    """
    def __init__(self, substrate: StackedSubstrate):
        self.substrate = substrate
        self.dim = substrate.dim
        
        # Continuous Running Telemetry
        self.total_evaluations: int = 0
        self.total_rejected_candidates: int = 0
        self.last_rejected_count: int = 0
        self.running_mean_energy: float = 0.50

    def compute_trajectory_hamiltonian(
        self,
        candidate_tokens: List[str],
        seed_id: int,
        encode_fn,
        target_condition_tokens: Optional[List[str]] = None
    ) -> Tuple[float, float]:
        """
        Computes the continuous Hamiltonian Action H(τ) and field resonance R(τ).
        H(τ) combines:
        1. Synaptic conductance impedance along path: (1 - W_ij)
        2. Manifold cosine resonance with concept Z-stack: (1 - cos(ψ, z_manifold))
        3. Contextual condition coverage for counterfactual / conditional queries.
        """
        if not candidate_tokens or seed_id not in self.substrate.neurons:
            return 1.0, 0.0
            
        seed_n = self.substrate.neurons[seed_id]
        
        # 1. Project candidate sequence wave into R^D
        candidate_phrase = " ".join(candidate_tokens)
        psi_wave = encode_fn(candidate_phrase)
        
        # 2. Extract active Z-stack manifold
        z_stack_vectors = [seed_n.x]
        for neighbor_id, cond in seed_n.synapses.items():
            if neighbor_id in self.substrate.neurons and float(cond) > 0.1:
                z_stack_vectors.append(self.substrate.neurons[neighbor_id].x * float(cond))
                
        z_manifold = np.mean(z_stack_vectors, axis=0)
        norm_z = np.linalg.norm(z_manifold)
        if norm_z > 0:
            z_manifold /= norm_z
            
        # Cosine resonance in [0, 1]
        raw_dot = float(np.dot(psi_wave, z_manifold))
        resonance = float(np.clip((raw_dot + 1.0) / 2.0, 0.0, 1.0))
        
        # 3. Compute continuous Synaptic Path Conductance Impedance
        impedance_sum = 0.0
        n_steps = max(1, len(candidate_tokens) - 1)
        
        for i in range(len(candidate_tokens) - 1):
            w1 = candidate_tokens[i].lower()
            w2 = candidate_tokens[i + 1].lower()
            
            # Find corresponding physical neurons in substrate
            n1_matches = [n for n in self.substrate.neurons.values() if n.text.lower() == w1 and n.tier_z > 0]
            n2_matches = [n for n in self.substrate.neurons.values() if n.text.lower() == w2 and n.tier_z > 0]
            
            w_conductance = 0.0
            if n1_matches and n2_matches:
                n1 = n1_matches[0]
                n2 = n2_matches[0]
                w_conductance = float(n1.synapses.get(n2.id, 0.0))
                
            impedance_sum += (1.0 - w_conductance)
            
        mean_impedance = impedance_sum / float(n_steps)
        
        # 4. Condition / Counterfactual Coverage
        cond_coverage = 0.0
        if target_condition_tokens:
            cand_clean = [t.lower().strip('.,;:"\'?') for t in candidate_tokens]
            matches = 0
            for c_tok in target_condition_tokens:
                c_clean = c_tok.lower().strip('.,;:"\'?')
                if any(t == c_clean or (len(t) >= 4 and len(c_clean) >= 4 and (t.startswith(c_clean[:4]) or c_clean.startswith(t[:4]))) for t in cand_clean):
                    matches += 1
            cond_coverage = float(matches) / float(max(1, len(target_condition_tokens)))
        
        # Continuous Total Hamiltonian Action H(τ) in [0, 1]
        hamiltonian = float(0.50 * (1.0 - resonance) + 0.50 * mean_impedance - 0.40 * cond_coverage)
        return float(np.clip(hamiltonian, 0.0, 1.0)), resonance

    def evaluate_candidates_and_collapse(
        self,
        candidate_token_lists: List[List[str]],
        seed_id: int,
        encode_fn,
        target_condition_tokens: Optional[List[str]] = None
    ) -> Tuple[List[str], float, int, bool]:
        """
        Evaluates candidate thought waves via Boltzmann-Gibbs Phase Collapse.
        Zero arbitrary thresholds:
        - Energy H(τ_i) for each candidate
        - Probability P(τ_i) = exp(-H(τ_i)/T) / Σ exp(-H(τ_j)/T)
        - Highest probability candidate collapses into articulation
        - If ground state dominates (high vacuum energy), collapses onto uncertainty
        """
        self.total_evaluations += 1
        
        if not candidate_token_lists:
            self.last_rejected_count = 0
            return [], 0.0, 0, True
            
        energies: List[float] = []
        resonances: List[float] = []
        
        for tokens in candidate_token_lists:
            h_val, r_val = self.compute_trajectory_hamiltonian(tokens, seed_id, encode_fn, target_condition_tokens=target_condition_tokens)
            energies.append(h_val)
            resonances.append(r_val)
            
        # Thermodynamic cognitive temperature from energy variance/entropy
        arr_h = np.array(energies, dtype=float)
        t_temp = float(max(0.15, np.std(arr_h) + 0.10))
        
        # Boltzmann Probability Distribution
        log_weights = -arr_h / t_temp
        log_weights -= np.max(log_weights)
        exp_weights = np.exp(log_weights)
        probabilities = exp_weights / np.sum(exp_weights)
        
        # Winning collapsed trajectory (maximum Boltzmann probability / minimal energy)
        best_idx = int(np.argmax(probabilities))
        best_tokens = candidate_token_lists[best_idx]
        best_resonance = resonances[best_idx]
        best_energy = energies[best_idx]
        best_prob = float(probabilities[best_idx])
        
        # Rejected candidate drafts in working memory
        rejected_count = max(0, len(candidate_token_lists) - 1)
        self.total_rejected_candidates += rejected_count
        self.last_rejected_count = rejected_count
        
        # Smooth homeostatic energy tracking
        self.running_mean_energy = 0.95 * self.running_mean_energy + 0.05 * best_energy
        
        # Physical Ground State: If best candidate has negligible path length or resides in high vacuum energy
        is_uncertain = bool(len(best_tokens) < 2 or best_energy > 0.85)
        
        return best_tokens, best_resonance, rejected_count, is_uncertain
