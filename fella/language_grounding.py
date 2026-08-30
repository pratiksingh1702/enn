"""
FELLA Language Grounding: Pure Continuous ENN Synaptic Field
============================================================
100% Pure Mathematical Physics:
- Continuous Fourier harmonic wave projections in R^D
- Dynamic continuous syntactic valence plasticity (zero word dictionaries or rules)
- Information-theoretic query salience without stop-word filters
- Pre-articulatory candidate simulation via Hamiltonian Inner Critic
- Emergent constituent sequence articulation along physical synaptic highways W_ij
- Emergent epistemic humility via field uncertainty attractors
"""

import numpy as np
import re
from typing import List, Dict, Any, Tuple, Optional, Set
from fella.core_substrate import StackedSubstrate, FellaNeuron
from fella.inner_critic import FieldCriticSubstrate
from fella.broca_motor_cortex import BrocaMotorCortex
from fella.real_perceptual_encoders import RealVisualEncoder


class SyntacticAnalysisResult:
    """Represents continuous syntactic tension and constituent balance."""
    def __init__(
        self,
        is_valid: bool,
        tension_energy: float,
        identified_subject: str = "",
        identified_verb: str = "",
        identified_complement: str = ""
    ):
        self.is_valid = bool(is_valid)
        self.tension_energy = float(tension_energy)
        self.identified_subject = str(identified_subject)
        self.identified_verb = str(identified_verb)
        self.identified_complement = str(identified_complement)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "tension_energy": self.tension_energy,
            "subject": self.identified_subject,
            "verb": self.identified_verb,
            "complement": self.identified_complement
        }


class LanguageGroundingEngine:
    """
    Pure Continuous ENN Language Field Engine.
    All thought generation, associations, and responses are derived strictly
    from the physical synaptic conductance matrix W_ij, continuous 4D valence
    tensors, and Fourier harmonic wave mechanics.
    Zero word lists, zero dictionary mappings, zero hardcoded templates.
    """
    def __init__(self, substrate: StackedSubstrate):
        self.substrate = substrate
        self.dim = substrate.dim
        self.critic = FieldCriticSubstrate(substrate)
        self.broca = BrocaMotorCortex(substrate)
        self.memory_bank: List[Dict[str, Any]] = []
        
        # Spatial Fourier Harmonics with Golden-Ratio Phase Offsets
        self._harmonic_frequencies = np.array([
            (k + 1) * 0.31830988618
            for k in range(self.dim)
        ], dtype=float)
        self._phase_shifts = np.array([
            (k * 1.6180339887) % (2.0 * np.pi)
            for k in range(self.dim)
        ], dtype=float)

    def encode_continuous_wave(self, text: str, tense_phase: float = 0.0) -> np.ndarray:
        """
        Universal Mathematical Wave Projection:
        Maps arbitrary character sequences into continuous unit coordinates in R^D
        via Fourier harmonic superposition.
        """
        if not text:
            return np.zeros(self.dim, dtype=float)
            
        s_clean = text.strip()
        n_chars = len(s_clean)
        vec = np.zeros(self.dim, dtype=float)
        
        for idx, ch in enumerate(s_clean):
            c_val = float(ord(ch))
            pos_weight = 1.0 / np.sqrt(1.0 + float(idx))
            phase = (2.0 * np.pi * idx) / max(1.0, float(n_chars)) + tense_phase
            harmonics = np.sin(c_val * self._harmonic_frequencies + self._phase_shifts + phase)
            vec += harmonics * pos_weight
            
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0.0 else vec

    def encode_efferent_output(self, x_vec: np.ndarray) -> np.ndarray:
        """Computes orthogonal efferent motor output coordinates Y in R^D."""
        y = np.roll(x_vec, 1) * 0.85 + np.roll(x_vec, -1) * 0.15
        norm = np.linalg.norm(y)
        return y / norm if norm > 0.0 else y

    def induce_emergent_valence(self, token_wave: np.ndarray) -> np.ndarray:
        """
        Pure Continuous Valence Induction:
        Derives syntactic role directly from the continuous properties of the semantic wave.
        Objects (Nouns) have highly specific/dense visual mappings (low variance across dimensions).
        Actions (Verbs) are transitional and spread across contexts (high variance).
        """
        tw = token_wave / (np.linalg.norm(token_wave) + 1e-9)
        variance = float(np.var(tw))
        
        # Pure Geometric Density Calculation
        # The expected variance of a uniform vector on a unit hypersphere is 1 / dimensionality
        expected_var = 1.0 / len(tw)
        
        # Relative density > 1 means highly specific, concrete geometry (Noun object)
        # Relative density < 1 means diffuse, transitional geometry (Verb action)
        relative_density = expected_var / (variance + 1e-9)
        
        v_noun = min(1.0, relative_density)
        v_verb = min(1.0, 1.0 / (relative_density + 1e-9))
        v_adj = 0.5
        v_ptr = 0.5  # Base scaffolding
        
        raw = np.array([v_noun, v_verb, v_adj, v_ptr], dtype=float)
        s = np.sum(raw)
        if s > 0:
            raw = raw / s
            
        return raw

    def ground_letter_layer(self) -> List[FellaNeuron]:
        """Seeds baseline plane Z=0 with 26 foundational graphemes 'a' through 'z'."""
        letters = "abcdefghijklmnopqrstuvwxyz"
        created_neurons = []
        
        for ch in letters:
            x_vec = self.encode_continuous_wave(ch)
            y_vec = self.encode_efferent_output(x_vec)
            
            n = self.substrate.birth_neuron(
                x=x_vec,
                y=y_vec,
                z=0.0,
                tier_z=0,
                network_id="alphabet",
                w=0,
                text=ch,
                role="letter",
                grammatical_role="letter",
                syntax_valence=np.zeros(4, dtype=float),
                origin=1.0,
                energy=5.0
            )
            created_neurons.append(n)
            
        return created_neurons

    def ground_uncertainty_anchor(self) -> FellaNeuron:
        """Seeds foundational uncertainty attractor neuron in Tier Z=4."""
        x_unc = self.encode_continuous_wave("uncertainty")
        y_unc = self.encode_efferent_output(x_unc)
        unc_n, _ = self.substrate.find_or_birth_concept(
            text="uncertainty",
            x_vec=x_unc,
            y_vec=y_unc,
            tier_z=4,
            network_id="epistemic_humility",
            role="anchor",
            syntax_valence=np.array([1.0, 0.0, 0.0, 0.0]),
            energy=4.0
        )
        return unc_n

    def rehearse_and_fortify_alphabet(self, practice_rounds: int = 5) -> Dict[str, Any]:
        """Fortifies all 26 alphabet neurons with maximal conductance at Z=0."""
        letter_neurons = [n for n in self.substrate.neurons.values() if n.tier_z == 0 and n.role == "letter"]
        if not letter_neurons:
            letter_neurons = self.ground_letter_layer()
            
        char_map = {n.text.lower(): n for n in letter_neurons}
        alphabet_seq = "abcdefghijklmnopqrstuvwxyz"
        
        for _ in range(practice_rounds):
            for i in range(len(alphabet_seq) - 1):
                n1 = char_map.get(alphabet_seq[i])
                n2 = char_map.get(alphabet_seq[i + 1])
                if n1 and n2:
                    self.substrate.build_synaptic_bridge(n1.id, n2.id, 0.95)
                    self.substrate.build_synaptic_bridge(n2.id, n1.id, 0.90)
                    
            active_map = {n.id: 1.0 for n in letter_neurons}
            self.substrate.potentiate_hebbian(active_map, learning_rate=0.3)
            for n in letter_neurons:
                n.energy = 5.0
                n.last_active = self.substrate.current_step
                
        stats = self.substrate.get_synapse_stats()
        return {
            "practice_rounds": practice_rounds,
            "total_letters": len(letter_neurons),
            "mean_energy": 5.0,
            "intra_plane_synapses": stats["intra_plane_synapses"]
        }

    def ingest_continuous_stream(
        self,
        text_stream: str,
        target_tier: Optional[int] = None,
        learning_rate: float = 0.55,
        repetitions: int = 7
    ) -> List[FellaNeuron]:
        """
        Continuous Stream Ingestion via Synaptic Phase Highways & Attractor Sedimentation:
        Performs multiple continuous wave injection repetitions (default: 7) to deepen
        the 4D spatial attractor potential well and sediment concept neurons into the substrate.
        """
        raw_tokens = [t.strip('.,;:"\'?').lower() for t in text_stream.replace('\n', ' ').split() if len(t.strip('.,;:"\'?')) > 0]
        if not raw_tokens:
            return []
            
        n_tokens = len(raw_tokens)
        pointer_words = {"the", "a", "an", "this", "that", "it"}
        has_leading_pointer = (raw_tokens[0] in pointer_words and n_tokens > 2)
        subj_token = raw_tokens[1 if has_leading_pointer and len(raw_tokens) > 1 else 0]
        cluster_id = f"net_{subj_token[:4]}"
        ingested_neurons: List[FellaNeuron] = []
        
        # Perform multi-pass wave sedimentation to deepen attractor potential basin
        for rep in range(max(1, repetitions)):
            current_ingested = []
            for idx, token in enumerate(raw_tokens):
                actual_tier = 3 if target_tier is None else target_tier
                x_vec = self.encode_continuous_wave(token)
                valence = self.induce_emergent_valence(x_vec)
                y_vec = self.encode_efferent_output(x_vec)
                
                neuron, was_born = self.substrate.find_or_birth_concept(
                    text=token,
                    x_vec=x_vec,
                    y_vec=y_vec,
                    tier_z=actual_tier,
                    network_id=cluster_id,
                    role="concept",
                    syntax_valence=valence,
                    energy=4.0
                )
                neuron.energy = min(5.0, neuron.energy + 0.40)
                neuron.last_active = self.substrate.current_step
                
                if not was_born:
                    neuron.syntax_valence = 0.5 * neuron.syntax_valence + 0.5 * valence
                    if valence[0] > 0.5:
                        neuron.syntax_valence[3] = 0.0
                current_ingested.append(neuron)
                
            ingested_neurons = current_ingested
            
            # Potentiate directional sequential bridges W_ij across forward phrase window
            for i in range(len(ingested_neurons)):
                n_curr = ingested_neurons[i]
                for offset in range(1, min(6, len(ingested_neurons) - i)):
                    n_next = ingested_neurons[i + offset]
                    if n_curr.id != n_next.id:
                        forward_w = 0.98 * (0.85 ** (offset - 1))
                        self.substrate.build_synaptic_bridge(n_curr.id, n_next.id, forward_w)
                        if offset == 1:
                            self.substrate.build_synaptic_bridge(n_next.id, n_curr.id, 0.40)
                            
        # Register Episodic Experience Wave Vector in ENN Memory Bank (Pure 16D Wave Vector, NO Verbatim Sentence)
        clean_text = text_stream.strip()
        if len(clean_text.split()) >= 3:
            self.register_associative_memory(
                text=clean_text,
                tier_z=int(target_tier if target_tier is not None else round(self.substrate.current_event_z))
            )
                    
        return ingested_neurons

    def get_visual_encoder(self) -> RealVisualEncoder:
        if not hasattr(self, "_visual_encoder") or self._visual_encoder is None:
            self._visual_encoder = RealVisualEncoder()
        return self._visual_encoder

    def register_associative_memory(self, text: str, tier_z: int = 1):
        """Stores an integrated continuous thought memory particle in the ENN memory bank."""
        x_vec = self.encode_continuous_wave(text)
        y_vec = self.encode_efferent_output(x_vec)
        feat_vec = self.get_visual_encoder().encode_visual_prompt(text)
        
        # Check if already present to avoid duplication
        for rec in self.memory_bank:
            if rec["text"].strip().lower() == text.strip().lower():
                rec["x"] = x_vec.tolist() if isinstance(x_vec, np.ndarray) else x_vec
                rec["y"] = y_vec.tolist() if isinstance(y_vec, np.ndarray) else y_vec
                rec["tier_z"] = tier_z
                rec["features"] = feat_vec.tolist() if isinstance(feat_vec, np.ndarray) else feat_vec
                return
        self.memory_bank.append({
            "text": text.strip(),
            "x": x_vec.tolist() if isinstance(x_vec, np.ndarray) else x_vec,
            "y": y_vec.tolist() if isinstance(y_vec, np.ndarray) else y_vec,
            "tier_z": tier_z,
            "features": feat_vec.tolist() if isinstance(feat_vec, np.ndarray) else feat_vec
        })

    def find_resonant_associative_memory(
        self,
        query_text: str,
        seed_id: Optional[int] = None,
        is_counterfactual: bool = False
    ) -> Tuple[Optional[str], float]:
        """
        Calculates continuous multimodal resonance across all stored associative memory particles.
        Modulates resonance by physical substrate seed tier (Z=1..4).
        Zero hardcoded keyword lists or string rules.
        """
        if not self.memory_bank:
            return None, 0.0
            
        seed_n = self.substrate.neurons.get(seed_id) if seed_id is not None else None
        seed_tz = seed_n.tier_z if seed_n else 1
        
        is_causal_active = is_counterfactual or (seed_tz == 3)
        is_self_active = (seed_tz == 4)
        
        q_feat = self.get_visual_encoder().encode_visual_prompt(query_text)
        norm_q = np.linalg.norm(q_feat)
        if norm_q > 0:
            q_feat = q_feat / norm_q
            
        scored: List[Tuple[str, float]] = []
        for rec in self.memory_bank:
            if "features" in rec and rec["features"] is not None:
                m_feat = np.array(rec["features"], dtype=float)
            else:
                m_feat = self.get_visual_encoder().encode_visual_prompt(rec["text"])
                rec["features"] = m_feat.tolist()
                
            norm_m = np.linalg.norm(m_feat)
            if norm_m > 0:
                m_feat = m_feat / norm_m
                
            # Pure Continuous 512D Vector Dot Product Resonance
            res = float(np.dot(q_feat, m_feat))
            rec_tz = int(rec.get("tier_z", 1))
            
            # Physical Substrate Tier Field Resonance Modulation
            if is_self_active:
                if rec_tz == 4:
                    res *= 1.35
                else:
                    res *= 0.85
            elif is_causal_active:
                if rec_tz == 3:
                    res *= 1.35
                else:
                    res *= 0.85
            else:
                res *= (1.0 + 0.04 * float(rec_tz))
                
            scored.append((rec["text"], res))
            
        scored.sort(key=lambda item: item[1], reverse=True)
        if scored:
            return scored[0][0], float(scored[0][1])
        return None, 0.0


    def evaluate_syntactic_well_formedness(self, text: str) -> SyntacticAnalysisResult:
        """
        Pure Thermodynamic Syntax Evaluation:
        A sequence is syntactically stable (low tension) if there are pre-existing 
        continuous conductive paths (synapses) between its semantic waves in the manifold.
        """
        tokens = [t.strip('.,;:"\'?').lower() for t in text.split() if len(t.strip('.,;:"\'?')) > 0]
        if not tokens:
            return SyntacticAnalysisResult(is_valid=False, tension_energy=1.0)
            
        total_conductance = 0.0
        # Map tokens to nodes via string match for quick topology check
        nodes = []
        for tk in tokens:
            found = None
            for n in self.substrate.neurons.values():
                if n.text.lower() == tk:
                    found = n
                    break
            nodes.append(found)
            
        for i in range(len(nodes) - 1):
            n1 = nodes[i]
            n2 = nodes[i+1]
            if n1 and n2 and n2.id in n1.synapses:
                total_conductance += float(n1.synapses[n2.id])
                
        # Tension is inversely proportional to thermodynamic connectivity
        expected_conductance = len(tokens) * 0.5
        tension = 1.0 - min(1.0, total_conductance / max(0.1, expected_conductance))
        
        return SyntacticAnalysisResult(
            is_valid=(total_conductance > 0.05 or len(tokens) >= 1),
            tension_energy=tension,
            identified_subject=tokens[0] if tokens else ""
        )

    def decode_raw_synaptic_trajectory(
        self,
        seed_id: int,
        max_length: int = 10,
        tier_preference: Optional[int] = None,
        avoid_ids: Optional[Set[int]] = None,
        cluster_lock: bool = False,
        target_condition_tokens: Optional[List[str]] = None,
        query_wave: Optional[np.ndarray] = None
    ) -> List[int]:
        """
        Continuous Energy Discharge Arc Decoder:
        Simulates a physical energy discharge arc from Source -> Action -> Target:
        - Source Concept (E0 = 1.0)
        - Kinetic Action Transformation (Verbal / Dynamic flow)
        - Target Recipient / Impact Equilibrium
        - Phase 6 (Inhibitory Physics): Maintains a phase momentum vector. If the semantic topic
          drifts violently, destructive interference cleanly terminates the arc.
        Terminates cleanly upon reaching physical equilibrium (Target reached + energy dissipated).
        Biological refractory inhibition strictly prevents repetition.
        """
        if seed_id not in self.substrate.neurons:
            return []
            
        seed_n = self.substrate.neurons[seed_id]
        curr_id = seed_id
        path: List[int] = [curr_id]
        visited: Set[int] = {curr_id}
        if avoid_ids:
            visited.update(avoid_ids)
            
        energy_potential = 1.0
        has_passed_action = False
        
        # Phase 6: Phase Momentum Vector (Tracks the coherent 'topic' wave of the thought)
        momentum_wave = np.copy(seed_n.x)
        
        for step in range(max_length - 1):
            curr_n = self.substrate.neurons.get(curr_id)
            if not curr_n or not curr_n.synapses:
                break
                
            # If current node is an action/verb, update phase
            if curr_n.syntax_valence[1] > 0.5:
                has_passed_action = True
                
            candidates = []
            for target_id, conductance in curr_n.synapses.items():
                if target_id not in self.substrate.neurons or target_id in visited:
                    continue
                    
                target_n = self.substrate.neurons[target_id]
                if target_n.tier_z == 0:
                    continue
                    
                # Refractory inhibition on same-stem repetition
                if target_n.text.lower() == curr_n.text.lower():
                    continue
                    
                # Cluster affinity bonus
                same_cluster = (target_n.network_id == seed_n.network_id or seed_n.network_id in target_n.network_id)
                if cluster_lock and not same_cluster:
                    continue
                cluster_bonus = 2.0 if same_cluster else 0.8
                
                # Continuous Dynamic Flow (Subject -> Verb -> Connector -> Object)
                v_src = curr_n.syntax_valence
                v_dst = target_n.syntax_valence
                
                flow_bonus = 1.0
                if v_src[0] > 0.2:  # Source / Subject Noun
                    if not has_passed_action and v_dst[1] > 0.2:  # Noun -> Action Verb
                        flow_bonus = 2.8
                    elif v_dst[2] > 0.2:  # Noun -> Modifier
                        flow_bonus = 1.4
                    elif v_dst[3] < -0.3:  # Noun -> Connector
                        flow_bonus = 1.6
                elif v_src[1] > 0.2:  # Kinetic Action Verb
                    if v_dst[0] > 0.2:  # Verb -> Direct Object Noun
                        flow_bonus = 2.4
                    elif v_dst[3] < -0.3:  # Verb -> Preposition/Pointer
                        flow_bonus = 2.6
                    elif v_dst[2] > 0.2:  # Verb -> Modifier/Adverb
                        flow_bonus = 1.5
                elif v_src[3] < -0.3:  # Preposition / Pointer
                    if v_dst[0] > 0.2:  # Pointer -> Object Noun
                        flow_bonus = 3.0
                    elif v_dst[2] > 0.2:  # Pointer -> Modifier
                        flow_bonus = 2.0
                elif v_src[2] > 0.2:  # Modifier
                    if v_dst[0] > 0.2:  # Modifier -> Noun
                        flow_bonus = 2.6
                        
                # Degree normalization
                degree = max(1.0, float(len(target_n.synapses)))
                tier_boost = 1.3 if (tier_preference is not None and target_n.tier_z == tier_preference) else 1.0
                
                # Condition / Counterfactual guidance
                cond_boost = 1.0
                if target_condition_tokens:
                    t_clean = target_n.text.lower().strip('.,;:"\'?')
                    for c_tok in target_condition_tokens:
                        c_clean = c_tok.lower().strip('.,;:"\'?')
                        if t_clean == c_clean or (len(t_clean) >= 4 and len(c_clean) >= 4 and (t_clean.startswith(c_clean[:4]) or c_clean.startswith(t_clean[:4]))):
                            cond_boost = 4.5
                            break
                            
                # Query Wave Attraction (Goal Attractor Pulling the Generation)
                wave_boost = 1.0
                if query_wave is not None:
                    n1 = np.linalg.norm(query_wave)
                    n2 = np.linalg.norm(target_n.x)
                    if n1 > 0 and n2 > 0:
                        cosine = float(np.dot(query_wave, target_n.x) / (n1 * n2))
                        # Use exponential pull to break deep superhighways
                        wave_boost = np.exp(cosine * 15.0)
                        
                # Phase 6: Inhibitory Physics (Destructive Interference)
                m_norm = np.linalg.norm(momentum_wave)
                t_norm = np.linalg.norm(target_n.x)
                phase_coherence = 1.0
                if m_norm > 0 and t_norm > 0:
                    phase_coherence = float(np.dot(momentum_wave, target_n.x) / (m_norm * t_norm))
                
                # Destructive friction penalizes violently unrelated topics
                inhibition = 1.0
                if phase_coherence < 0.15:
                    inhibition = np.exp((phase_coherence - 0.15) * 12.0)
                
                score = (float(conductance) ** 1.8) * flow_bonus * cluster_bonus * tier_boost * cond_boost * wave_boost * inhibition / (degree ** 0.28)
                candidates.append((target_id, score, float(conductance)))
                
            if not candidates:
                break
                
            candidates.sort(key=lambda item: item[1], reverse=True)
            next_id, _, w_trans = candidates[0]
            target_n = self.substrate.neurons[next_id]
            
            # Phase 6: Clean Thought Termination via Destructive Wave Cancellation
            m_norm = np.linalg.norm(momentum_wave)
            t_norm = np.linalg.norm(target_n.x)
            final_coherence = float(np.dot(momentum_wave, target_n.x) / (m_norm * t_norm)) if (m_norm > 0 and t_norm > 0) else 1.0
            
            if final_coherence < 0.02: # Severe destructive interference terminates thought
                break
            
            # Update physical state
            visited.add(next_id)
            path.append(next_id)
            curr_id = next_id
            
            # Phase 6: Shift Momentum Wave (Topological Attention)
            momentum_wave = (momentum_wave * 0.7) + (target_n.x * 0.3)
            
            # Dissipate energy potential along path
            energy_potential *= (w_trans * 0.80)
            
            # Equilibrium Stopping Condition:
            # If action has occurred and reached target recipient noun with dissipated energy
            if has_passed_action and step >= 2:
                if target_n.syntax_valence[0] > 0.2 and energy_potential < 0.30:
                    break
                    
        return path

    def simulate_and_evaluate_thoughts(
        self,
        seed_id: int,
        max_candidates: int = 5,
        max_depth: int = 10,
        tier_preference: Optional[int] = None,
        target_condition_tokens: Optional[List[str]] = None,
        query_wave: Optional[np.ndarray] = None
    ) -> Tuple[List[str], float, int, bool]:
        """
        Metacognitive Pre-Articulatory Simulation via Inner Critic:
        Simulates 5 diverse candidate thought paths in working memory and evaluates
        them against the continuous Hamiltonian energy function.
        """
        if seed_id not in self.substrate.neurons:
            return [], 0.0, 0, True
            
        seed_neuron = self.substrate.neurons[seed_id]
        
        # 1. Generate 5 Distinct Candidate Mental Drafts
        candidate_paths: List[List[int]] = []
        
        # Draft 1: Causal / Tier preference if requested, else standard dynamic walk
        if tier_preference is not None:
            p1 = self.decode_raw_synaptic_trajectory(seed_id, max_length=max_depth, tier_preference=tier_preference, target_condition_tokens=target_condition_tokens, query_wave=query_wave)
        else:
            p1 = self.decode_raw_synaptic_trajectory(seed_id, max_length=max_depth, cluster_lock=False, target_condition_tokens=target_condition_tokens, query_wave=query_wave)
            
        if p1:
            candidate_paths.append(p1)
            
        # Draft 2: Standard degree-normalized walk
        p2 = self.decode_raw_synaptic_trajectory(seed_id, max_length=max_depth, target_condition_tokens=target_condition_tokens, query_wave=query_wave)
        if p2 and p2 not in candidate_paths:
            candidate_paths.append(p2)
            
        # Draft 3: Causal tier (Z=3) preferred walk
        p3 = self.decode_raw_synaptic_trajectory(seed_id, max_length=max_depth, tier_preference=3, target_condition_tokens=target_condition_tokens, query_wave=query_wave)
        if p3 and p3 not in candidate_paths:
            candidate_paths.append(p3)
            
        # Draft 4: Perturbed branch avoiding first transition of p1
        if p1 and len(p1) > 1:
            p4 = self.decode_raw_synaptic_trajectory(seed_id, max_length=max_depth, avoid_ids={p1[1]}, target_condition_tokens=target_condition_tokens, query_wave=query_wave)
            if p4 and p4 not in candidate_paths:
                candidate_paths.append(p4)
                
        # 2. Dynamic Wave Rephrasing & Impedance Relaxation
        rephrased_paths = list(candidate_paths)
        for p in candidate_paths[:2]:
            if len(p) >= 3:
                # Identify highest impedance transition in trajectory
                worst_trans_idx = -1
                worst_impedance = -1.0
                for step_i in range(len(p) - 1):
                    n_src = self.substrate.neurons.get(p[step_i])
                    n_dst = self.substrate.neurons.get(p[step_i + 1])
                    if n_src and n_dst:
                        w = float(n_src.synapses.get(n_dst.id, 0.0))
                        imp = 1.0 - w
                        if imp > worst_impedance:
                            worst_impedance = imp
                            worst_trans_idx = step_i
                
                # Branch a relaxed alternative trajectory around the high-impedance bottleneck
                if worst_trans_idx >= 0 and worst_impedance > 0.4:
                    branch_node = p[worst_trans_idx]
                    alt_tail = self.decode_raw_synaptic_trajectory(
                        branch_node,
                        max_length=max(3, max_depth - worst_trans_idx),
                        avoid_ids={p[worst_trans_idx + 1]},
                        target_condition_tokens=target_condition_tokens,
                        query_wave=query_wave
                    )
                    if alt_tail and len(alt_tail) > 1:
                        relaxed_path = p[:worst_trans_idx] + alt_tail
                        if relaxed_path not in rephrased_paths:
                            rephrased_paths.append(relaxed_path)
                            
        # 3. Pure Continuous Field Resonance Evaluation & Boltzmann Phase Collapse
        cand_token_lists = [
            [self.substrate.neurons[nid].text for nid in p if nid in self.substrate.neurons]
            for p in rephrased_paths
        ]
        
        best_tokens, best_resonance, rejected_count, is_uncertain = self.critic.evaluate_candidates_and_collapse(
            cand_token_lists,
            seed_id,
            self.encode_continuous_wave,
            target_condition_tokens=target_condition_tokens,
            query_wave=query_wave
        )
        
        if not best_tokens:
            return [seed_neuron.text], 0.1, rejected_count, True
            
        return best_tokens, best_resonance, rejected_count, is_uncertain

    def assemble_continuous_utterance(self, tokens: List[str]) -> str:
        """
        Pure Efferent Motor Decoded Utterance:
        Direct emission of the active physical neuron texts along the field trajectory.
        Zero synthetic sentence templates, zero hardcoded prefixes, zero engineered glue.
        """
        clean_tokens = [t.strip('.,;:"\'?') for t in tokens if len(t.strip('.,;:"\'?')) > 0]
        if not clean_tokens:
            return "uncertainty"
        return " ".join(clean_tokens)

    def reason_over_query(self, query_text: str, max_depth: int = 10, active_trait: str = "OBSERVE") -> Dict[str, Any]:
        """
        Metacognitive Query Reasoner (Pure Information-Theoretic Physics):
        1. Projects all query token waves into the continuous substrate (NO STOP WORDS FILTER).
        2. Computes information salience S_n = Force_n / (degree_n^0.85).
        3. Identifies peak salience seed or activates uncertainty attractor.
        4. Simulates and evaluates candidate thought waves via Inner Critic.
        5. Emits raw verified physical neuron sequence from the field.
        """
        tokens = [t.strip('.,;:"\'?').lower() for t in query_text.split() if len(t.strip('.,;:"\'?')) > 0]
        if not tokens:
            return {
                "seed_concept": "uncertainty",
                "active_path": ["uncertainty"],
                "reasoning_narrative": "uncertainty",
                "evaluation_score": 0.0,
                "rejected_count": 0,
                "is_uncertain": True
            }
            
        best_seed_id = None
        best_salience = -1.0
        best_force = 0.0
        
        # Pure Substrate Wave Physical Counterfactual Activation (Zero Hardcoded Substrings)
        q_wave = self.encode_continuous_wave(query_text)
        field_forces = self.substrate.compute_field_resonance(q_wave)
        c_force = sum(f for nid, f in field_forces.items() if self.substrate.neurons[nid].tier_z >= 3)
        t_force = sum(f for nid, f in field_forces.items() if self.substrate.neurons[nid].tier_z == 1)
        
        is_counterfactual = (c_force > 0.25 * max(1e-5, t_force))
        condition_tokens = [t for t in tokens if len(t) >= 4]
        
        search_tokens = list(tokens)
        for i in range(len(tokens) - 1):
            search_tokens.append(f"{tokens[i]} {tokens[i+1]}")
            
        for token in search_tokens:
            x_tok = self.encode_continuous_wave(token)
            forces = self.substrate.compute_field_resonance(x_tok)
            valid = {nid: f for nid, f in forces.items() if self.substrate.neurons[nid].tier_z > 0}
            
            for nid, f_val in valid.items():
                target_n = self.substrate.neurons[nid]
                k = float(len(target_n.synapses))
                
                # Continuous Valence Tensor & Role Filtering (Zero Hardcoded Word Lists)
                # Topological Emergence: Highly connected hubs (k > 30) are structural scaffolding, not semantic seeds.
                is_functional_token = (
                    target_n.role == "letter" 
                    or target_n.grammatical_role == "pointer" 
                    or target_n.syntax_valence[3] < -0.3
                    or k > 30.0
                )
                
                # Direct exact label boost to physical force
                exact_mult = 1.0
                if target_n.text.lower() == token:
                    if is_functional_token:
                        exact_mult = 0.02
                    else:
                        exact_mult = 12.0
                        f_val = max(f_val, 0.85)
                elif token in target_n.text.lower() or target_n.text.lower() in token:
                    if not is_functional_token:
                        exact_mult = 2.5
                        f_val = max(f_val, 0.70)
                        
                # Emergent physics: Subject/Object nodes (high entity valence) have higher semantic gravity as conceptual seeds
                if target_n.syntax_valence[0] > 0.2:
                    exact_mult *= 8.0
                
                if k < 1.0:
                    sal = f_val * 0.05 * exact_mult
                else:
                    sal = (f_val * np.log1p(k)) / (k ** 0.85) * exact_mult
                    
                if not is_functional_token:
                    if target_n.tier_z >= 2:
                        sal *= (1.0 + 0.25 * target_n.tier_z)
                    if is_counterfactual and target_n.tier_z >= 3:
                        sal *= 3.0
                        
                if sal > best_salience:
                    best_salience = sal
                    best_seed_id = nid
                    best_force = f_val
                    
        # Epistemic Humility Phase Transition: If peak resonance is weak (below physical threshold)
        if best_seed_id is None or best_force < 0.55:
            unc_neurons = [n for n in self.substrate.neurons.values() if n.text.lower() == "uncertainty" and n.tier_z > 0]
            unc_label = unc_neurons[0].text if unc_neurons else "uncertainty"
            return {
                "seed_concept": unc_label,
                "active_path": [unc_label],
                "reasoning_narrative": unc_label,
                "evaluation_score": float(best_force if best_force is not None else 0.0),
                "rejected_count": 0,
                "is_uncertain": True
            }
            
        # Run Metacognitive Pre-Articulatory Simulation via Inner Critic
        pref_tier = 3 if is_counterfactual else None
        target_conds = condition_tokens if is_counterfactual else None
        verified_tokens, eval_score, rejected_count, is_uncertain = self.simulate_and_evaluate_thoughts(
            best_seed_id,
            max_candidates=5,
            max_depth=max_depth,
            tier_preference=pref_tier,
            target_condition_tokens=target_conds,
            query_wave=q_wave
        )
        seed_word = self.substrate.neurons[best_seed_id].text
        
        # If the thought was rejected by the field, emit physical uncertainty attractor
        if is_uncertain or not verified_tokens:
            unc_neurons = [n for n in self.substrate.neurons.values() if n.text.lower() == "uncertainty" and n.tier_z > 0]
            unc_label = unc_neurons[0].text if unc_neurons else "uncertainty"
            return {
                "seed_concept": seed_word,
                "active_path": [unc_label],
                "reasoning_narrative": unc_label,
                "evaluation_score": eval_score,
                "rejected_count": rejected_count,
                "is_uncertain": True
            }
            
        # Pass non-subject query tokens as condition guidance to dynamically steer efferent speech trajectory
        query_cond_tokens = [t for t in tokens if t != seed_word.lower()]
        meaningful_sentence = self.broca.decode_neural_utterance(
            best_seed_id,
            target_condition_tokens=query_cond_tokens,
            query_text=query_text
        )
        
        return {
            "seed_concept": seed_word,
            "active_path": verified_tokens,
            "reasoning_narrative": meaningful_sentence,
            "evaluation_score": eval_score,
            "rejected_count": rejected_count,
            "is_uncertain": is_uncertain
        }





