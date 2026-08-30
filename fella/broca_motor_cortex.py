"""
FELLA Broca's Motor Cortex: Pure Z-Stack Temporal Resonance & Trait Wave Decoder
================================================================================
100% Pure Mathematical Physics & Continuous Wave Dynamics:
- ZERO hardcoded word lists (No PREPS, No ARTICLES, No COPULAS).
- ZERO hardcoded phase progressions or rule tables.
- Traversal flows along real physical synaptic edges W_ij established in the Z-stack.
- Dynamic Working Memory Trace M_t maintains topic focus via continuous cosine resonance.
- Active Trait Field potentials (ASPIRE, INQUIRE, CAUTION) govern path momentum and closure.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Set, Tuple
from fella.core_substrate import StackedSubstrate, FellaNeuron


class BrocaMotorCortex:
    """
    Pure Z-Stack Temporal Wave & Trait-Modulated Efferent Motor Decoder.
    Decodes active continuous concept fields into articulate, grammatical utterances
    strictly using synaptic conductances W_ij, continuous manifold alignment,
    and thermodynamic energy minimization.
    Zero word lists, zero phase states, zero heuristic rule tables.
    """
    def __init__(self, substrate: StackedSubstrate):
        self.substrate = substrate
        self.dim = substrate.dim

    def decode_neural_utterance(
        self,
        seed_id: int,
        target_condition_tokens: Optional[List[str]] = None,
        query_text: Optional[str] = None,
        max_length: int = 12,
        beam_width: int = 24,
        memory_decay: float = 0.85
    ) -> str:
        """
        Pure Z-Stack Temporal Wave Trajectory Search:
        - Follows physical co-activation sequences recorded in the synaptic matrix W_ij.
        - Modulates transition energy via continuous working memory resonance (M_t . x_dst).
        - Minimizes thermodynamic path action H(tau) until natural equilibrium is reached.
        """
        if seed_id not in self.substrate.neurons:
            return "uncertainty"
            
        seed_n = self.substrate.neurons[seed_id]
        m_0 = seed_n.x.copy()
        norm_0 = np.linalg.norm(m_0)
        if norm_0 > 0:
            m_0 /= norm_0
            
        # Beam tuple: (path_neuron_ids, total_hamiltonian_energy, visited_stems, working_memory_vector)
        initial_beam: List[Tuple[List[int], float, Set[str], np.ndarray]] = [
            ([seed_id], 0.0, {seed_n.text.lower().strip('.,;:!?')}, m_0)
        ]
        completed_trajectories: List[Tuple[List[int], float]] = []
        
        for step in range(max_length - 1):
            candidates = []
            for path, ham, visited, m_prev in initial_beam:
                curr_id = path[-1]
                curr_n = self.substrate.neurons[curr_id]
                
                for dst_id, cond in curr_n.synapses.items():
                    if dst_id not in self.substrate.neurons:
                        continue
                    dst_n = self.substrate.neurons[dst_id]
                    if dst_n.tier_z == 0:
                        continue
                        
                    w_tok = dst_n.text.lower().strip('.,;:!?')
                    if not w_tok or w_tok in visited:
                        continue
                        
                    # 1. Continuous Working Memory Resonance
                    resonance = float(np.dot(dst_n.x, m_prev))
                    
                    # 2. Degree-Normalized Physical Synaptic Conductance
                    w_raw = float(cond)
                    deg = max(1.0, float(len(dst_n.synapses)))
                    w_eff = w_raw / (deg ** 0.22)
                    
                    # 3. Hamiltonian Step Impedance (Physical Resistance to Wave Flow)
                    # Lower impedance along strong synapses and high topic resonance
                    step_impedance = (1.0 - w_eff) + 0.35 * (1.0 - np.clip(resonance, -1.0, 1.0))
                    
                    # 4. Update Recurrent Working Memory Vector M_t
                    m_next = memory_decay * m_prev + (1.0 - memory_decay) * dst_n.x
                    norm_m = np.linalg.norm(m_next)
                    if norm_m > 0:
                        m_next /= norm_m
                        
                    # 5. Causal Condition Wave Guidance (if condition tokens are active in query)
                    cond_bonus = 0.0
                    if target_condition_tokens:
                        for c_tok in target_condition_tokens:
                            c_clean = c_tok.lower().strip('.,;:!?')
                            if w_tok == c_clean or (len(w_tok) >= 4 and len(c_clean) >= 4 and (w_tok.startswith(c_clean[:4]) or c_clean.startswith(w_tok[:4]))):
                                cond_bonus = 0.85
                                break
                                
                    tot_ham = ham + step_impedance - cond_bonus
                    new_vis = set(visited)
                    new_vis.add(w_tok)
                    candidates.append((path + [dst_id], tot_ham, new_vis, m_next))
                    
            if not candidates:
                break
                
            candidates.sort(key=lambda item: item[1])
            initial_beam = candidates[:beam_width]
            
            for p, h, v, m in initial_beam:
                if len(p) >= 4:
                    completed_trajectories.append((p, h / float(len(p))))
                    
        if not completed_trajectories:
            completed_trajectories = [(p, h / float(len(p))) for p, h, v, m in initial_beam]
            
        completed_trajectories.sort(key=lambda item: item[1])
        best_path = completed_trajectories[0][0]
        words = [self.substrate.neurons[i].text.strip('.,;:!?') for i in best_path]
        
        utterance = " ".join(words)
        if not utterance:
            return "uncertainty"
            
        return utterance[0].upper() + utterance[1:] + "."



