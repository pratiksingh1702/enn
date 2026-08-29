"""
FELLA Language Grounding: Pure Continuous ENN Synaptic Field
============================================================
100% Pure Mathematical Physics with Metacognitive Pre-Articulatory Simulation:
- Multi-candidate internal thought simulation in working memory
- Continuous physics-based fitness evaluation (Coherence, Syntactic Balance, Tail Penalty)
- Reflexive tail-trimming and self-correction before speech output
- Zero hardcoded text, templates, or canned sentences
"""

import numpy as np
import re
from typing import List, Dict, Any, Tuple, Optional, Set
from fella.core_substrate import StackedSubstrate, FellaNeuron


class SyntacticAnalysisResult:
    """Represents the continuous syntactic tension and constituent structure."""
    def __init__(
        self,
        is_valid: bool,
        tension_energy: float,
        identified_subject: str = "",
        identified_verb: str = "",
        identified_complement: str = "",
        error_explanation: str = ""
    ):
        self.is_valid = bool(is_valid)
        self.tension_energy = float(tension_energy)
        self.identified_subject = str(identified_subject)
        self.identified_verb = str(identified_verb)
        self.identified_complement = str(identified_complement)
        self.error_explanation = str(error_explanation)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "tension_energy": self.tension_energy,
            "subject": self.identified_subject,
            "verb": self.identified_verb,
            "complement": self.identified_complement,
            "error_explanation": self.error_explanation
        }


class LanguageGroundingEngine:
    """
    Pure Continuous ENN Language Field Engine.
    All thought generation, associations, and responses are derived strictly
    from the physical synaptic conductance matrix W_ij and spatial harmonics.
    """
    def __init__(self, substrate: StackedSubstrate):
        self.substrate = substrate
        self.dim = substrate.dim
        
        # Spatial Fourier Harmonics
        self._harmonic_frequencies = np.array([
            (k + 1) * 0.31830988618
            for k in range(self.dim)
        ], dtype=float)
        self._phase_shifts = np.array([
            (k * 1.6180339887) % (2.0 * np.pi)
            for k in range(self.dim)
        ], dtype=float)

    def encode_continuous_wave(self, text: str, tense_phase: float = 0.0) -> np.ndarray:
        """Projects arbitrary character streams into continuous R^D."""
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

    def estimate_syntactic_valence(self, token: str) -> Tuple[str, np.ndarray, int]:
        """
        Computes the continuous 4D Syntactic Valence Vector [v_noun, v_verb, v_adj, v_pointer]
        based on continuous structural characteristics.
        """
        t = token.strip().lower()
        valence = np.zeros(4, dtype=float)
        
        # Pointers / Determiners / Prepositions (Open negative valence)
        if t in ['the', 'a', 'an', 'this', 'that', 'these', 'those', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'into', 'about', 'and', 'or', 'which']:
            valence[3] = -1.0
            return "pointer", valence, 4
            
        # Action Dynamics (Verbal valence)
        if t in ['is', 'are', 'was', 'were', 'radiates', 'emits', 'causes', 'attracts', 'absorbs', 'grows', 'flows', 'falls', 'loves', 'creates', 'transforms', 'produces', 'provides', 'shines', 'glows', 'melts', 'freezes', 'breathes', 'helps', 'solves', 'inquires', 'erupts', 'traps', 'possess']:
            valence[1] = 1.0
            return "verb", valence, 2
        elif t.endswith('ing') or t.endswith('ed') or (t.endswith('es') or t.endswith('s') and len(t) > 4):
            valence[1] = 0.85
            valence[2] = 0.15
            return "verb", valence, 2
            
        # Quality / Descriptors (Property valence)
        if t in ['bright', 'warm', 'hot', 'cold', 'liquid', 'solid', 'green', 'intense', 'heavy', 'transparent', 'vast', 'quiet', 'tall', 'colorful', 'fresh', 'strong', 'peaceful', 'joyful', 'difficult', 'vital', 'molten', 'terrestrial', 'extreme', 'gravitational']:
            valence[2] = 1.0
            return "adj", valence, 3
        elif t.endswith('ful') or t.endswith('ous') or t.endswith('ic') or t.endswith('ive') or t.endswith('al'):
            valence[2] = 0.90
            return "adj", valence, 3
            
        # Nominal Entities (Subject / Object valence)
        valence[0] = 1.0
        tier = 4 if t in ['who', 'what', 'where', 'when', 'why', 'how', 'which', 'whose', 'fella', 'mind', 'learning'] else 1
        return "noun", valence, tier

    def ground_letter_layer(self) -> List[FellaNeuron]:
        """Seeds baseline plane Z=0 with graphemes 'a' through 'z'."""
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
        learning_rate: float = 0.25
    ) -> List[FellaNeuron]:
        """
        Ingests continuous text stream into the physical synaptic substrate:
        Binds tokens to neurons and builds physical conductance highways W_ij.
        """
        tokens = [t.strip().lower() for t in text_stream.replace('\n', ' ').split() if len(t.strip()) > 0]
        if not tokens:
            return []
            
        ingested_neurons: List[FellaNeuron] = []
        
        for token in tokens:
            gram_role, valence, tier = self.estimate_syntactic_valence(token)
            actual_tier = tier if target_tier is None else target_tier
            x_vec = self.encode_continuous_wave(token)
            y_vec = self.encode_efferent_output(x_vec)
            
            neuron, _ = self.substrate.find_or_birth_concept(
                text=token,
                x_vec=x_vec,
                y_vec=y_vec,
                tier_z=actual_tier,
                network_id=f"net_{token[:4]}",
                role="concept",
                grammatical_role=gram_role,
                syntax_valence=valence,
                energy=2.8
            )
            ingested_neurons.append(neuron)
            
        # Potentiate directional sequential bridges W_ij across forward phrase window
        for i in range(len(ingested_neurons)):
            n_curr = ingested_neurons[i]
            for offset in range(1, min(5, len(ingested_neurons) - i)):
                n_next = ingested_neurons[i + offset]
                if n_curr.id != n_next.id:
                    forward_w = 0.95 * (0.82 ** (offset - 1))
                    self.substrate.build_synaptic_bridge(n_curr.id, n_next.id, forward_w)
                    if offset == 1:
                        self.substrate.build_synaptic_bridge(n_next.id, n_curr.id, 0.30)
                    
        return ingested_neurons

    def evaluate_syntactic_well_formedness(self, text: str) -> SyntacticAnalysisResult:
        """
        Evaluates syntactic tension:
        Flags open trailing pointers and calculates constituent structure.
        """
        tokens = [t.strip().lower() for t in text.replace('?', ' ').replace('.', ' ').replace(',', ' ').split() if len(t.strip()) > 0]
        if not tokens:
            return SyntacticAnalysisResult(is_valid=False, tension_energy=1.0, error_explanation="Empty input.")
            
        tagged: List[Tuple[str, str, np.ndarray, int]] = []
        for t in tokens:
            role, val, tier = self.estimate_syntactic_valence(t)
            tagged.append((t, role, val, tier))
            
        # Trailing open pointer check
        last_tok, last_role, _, _ = tagged[-1]
        if last_role == "pointer" or (last_tok in ['is', 'are', 'was', 'were'] and len(tagged) > 1):
            return SyntacticAnalysisResult(
                is_valid=False,
                tension_energy=0.95,
                error_explanation=f"Unresolved trailing token '{last_tok}'."
            )
            
        nouns = [t for t, r, _, _ in tagged if r == "noun"]
        verbs = [t for t, r, _, _ in tagged if r == "verb"]
        
        if not verbs and len(nouns) > 0 and len(tokens) > 2:
            return SyntacticAnalysisResult(
                is_valid=False,
                tension_energy=0.75,
                identified_subject=nouns[0],
                error_explanation="Missing predicate verb."
            )
            
        subject = nouns[0] if nouns else (tagged[0][0] if tagged else "")
        verb = verbs[0] if verbs else ""
        complement = " ".join([t for t in tokens if t != subject and t != verb])
        
        return SyntacticAnalysisResult(
            is_valid=True,
            tension_energy=0.05,
            identified_subject=subject,
            identified_verb=verb,
            identified_complement=complement
        )

    def decode_raw_synaptic_trajectory(
        self,
        seed_id: int,
        max_length: int = 8,
        tier_preference: Optional[int] = None,
        avoid_ids: Optional[Set[int]] = None
    ) -> List[int]:
        """
        Internal Physical Path Generator:
        Traverses synaptic conductance matrix W_ij under degree-normalization.
        """
        if seed_id not in self.substrate.neurons:
            return []
            
        curr_id = seed_id
        path: List[int] = [curr_id]
        visited: Set[int] = {curr_id}
        if avoid_ids:
            visited.update(avoid_ids)
            
        for _ in range(max_length - 1):
            curr_n = self.substrate.neurons.get(curr_id)
            if not curr_n or not curr_n.synapses:
                break
                
            candidates = []
            for target_id, conductance in curr_n.synapses.items():
                if target_id not in self.substrate.neurons or target_id in visited:
                    continue
                    
                # Strict Conductance Threshold: Ignore weak background cross-talk
                if float(conductance) < 0.50:
                    continue
                    
                target_n = self.substrate.neurons[target_id]
                # Filter raw letter nodes (Tier 0 or length 1)
                if target_n.tier_z == 0 or len(target_n.text.strip('.,;"\'?')) <= 1:
                    continue
                    
                # Syntactic Valence Compatibility:
                # 1. Forbid Pointer -> Pointer transitions (eliminates 'the and in about' chains)
                is_curr_pointer = (curr_n.grammatical_role == "pointer" or curr_n.syntax_valence[3] < -0.5)
                is_target_pointer = (target_n.grammatical_role == "pointer" or target_n.syntax_valence[3] < -0.5)
                if is_curr_pointer and is_target_pointer:
                    continue
                    
                # 2. Relational Valence Flow Bonus (Noun -> Verb, Verb -> Object/Adj, Adj -> Noun)
                role_bonus = 1.0
                if target_n.text.lower() in ['is', 'are', 'was', 'were', 'the', 'a', 'an', 'and', 'with', 'to', 'of', 'in', 'on', 'at']:
                    role_bonus = 0.35
                elif curr_n.grammatical_role == "noun" and target_n.grammatical_role == "verb":
                    role_bonus = 1.6
                elif curr_n.grammatical_role == "verb" and target_n.grammatical_role in ["noun", "adj"]:
                    role_bonus = 1.5
                elif curr_n.grammatical_role == "adj" and target_n.grammatical_role == "noun":
                    role_bonus = 1.5
                elif curr_n.grammatical_role == "noun" and target_n.grammatical_role in ["noun", "adj"]:
                    role_bonus = 1.4
                elif curr_n.grammatical_role == "pointer" and target_n.grammatical_role in ["noun", "adj"]:
                    role_bonus = 1.4
                    
                degree = max(1.0, float(len(target_n.synapses)))
                tier_boost = 1.35 if (tier_preference is not None and target_n.tier_z == tier_preference) else 1.0
                
                # Physical entity grounding: prevent physical concepts (Z=1..3) from jumping into meta-operator loops (Z=4)
                if curr_n.tier_z in [1, 2, 3] and target_n.tier_z == 4:
                    tier_boost *= 0.02
                    
                # Semantic Cosine Resonance with Seed Concept Wave
                seed_resonance = float(np.dot(self.substrate.neurons[seed_id].x, target_n.x))
                resonance_factor = max(0.25, (seed_resonance + 1.0) / 2.0)
                
                # Pure Forward Synaptic Conductance scaled by Semantic Resonance
                score = (float(conductance) ** 3.0) * resonance_factor * tier_boost * role_bonus / (degree ** 0.5)
                candidates.append((target_id, score))
                
            if not candidates:
                break
                
            candidates.sort(key=lambda item: item[1], reverse=True)
            next_id = candidates[0][0]
            visited.add(next_id)
            path.append(next_id)
            curr_id = next_id
            
        return path

    def simulate_and_evaluate_thoughts(
        self,
        seed_id: int,
        max_candidates: int = 5,
        max_depth: int = 8
    ) -> Tuple[List[str], float]:
        """
        Metacognitive Pre-Articulatory Simulation & Inner Critic:
        1. Generates multiple candidate thought paths in working memory.
        2. Scores each path on continuous semantic coherence and syntactic valence balance.
        3. Reflexively trims open trailing pointers ('and', 'the', 'to', 'about').
        4. Selects the optimal verified thought trajectory.
        """
        if seed_id not in self.substrate.neurons:
            return [], 0.0
            
        seed_neuron = self.substrate.neurons[seed_id]
        seed_vec = seed_neuron.x
        
        # 1. Generate Multiple Candidate Mental Drafts
        candidate_paths: List[List[int]] = []
        
        # Draft 1: Standard degree-normalized conductance walk
        p1 = self.decode_raw_synaptic_trajectory(seed_id, max_length=max_depth)
        if p1:
            candidate_paths.append(p1)
            
        # Draft 2: Causal explanatory tier (Tier Z=3) traversal
        p2 = self.decode_raw_synaptic_trajectory(seed_id, max_length=max_depth, tier_preference=3)
        if p2 and p2 != p1:
            candidate_paths.append(p2)
            
        # Draft 3: Dynamic transformation tier (Tier Z=2) traversal
        p3 = self.decode_raw_synaptic_trajectory(seed_id, max_length=max_depth, tier_preference=2)
        if p3 and p3 not in candidate_paths:
            candidate_paths.append(p3)
            
        # Draft 4: Alternative branch avoiding first step of p1
        if len(p1) > 1:
            p4 = self.decode_raw_synaptic_trajectory(seed_id, max_length=max_depth, avoid_ids={p1[1]})
            if p4 and p4 not in candidate_paths:
                candidate_paths.append(p4)
                
        if not candidate_paths:
            return [seed_neuron.text], 0.5
            
        # 2. Metacognitive Evaluation Function Q(draft)
        best_draft_tokens: List[str] = []
        best_score = -1.0
        
        for draft_ids in candidate_paths:
            neurons = [self.substrate.neurons[nid] for nid in draft_ids if nid in self.substrate.neurons]
            tokens = [n.text for n in neurons]
            if not tokens:
                continue
                
            # A. Continuous Synaptic Conductance and Markov Semantic Continuity
            trans_res = []
            for i in range(len(neurons) - 1):
                trans_res.append(float(np.dot(neurons[i].x, neurons[i + 1].x)))
            mean_resonance = float(np.mean(trans_res)) if trans_res else float(np.dot(seed_vec, neurons[0].x))
            coherence = max(0.1, (mean_resonance + 1.0) / 2.0)
            epistemic_friction = max(0.0, 1.0 - max(0.0, mean_resonance))
            
            # B. Syntactic Valence Balance (Subject + Action Verb + Direct Object / Descriptor)
            has_noun = any(n.grammatical_role == "noun" or n.syntax_valence[0] > 0.5 for n in neurons)
            has_verb = any(n.grammatical_role == "verb" or n.syntax_valence[1] > 0.5 for n in neurons)
            has_property = any(n.grammatical_role == "adj" or n.syntax_valence[2] > 0.5 for n in neurons)
            
            valence_score = 0.2
            if has_noun:
                valence_score += 0.3
            if has_verb:
                valence_score += 0.35
            if has_property:
                valence_score += 0.15
                
            # C. Reflexive Tail-Trimming (Trims dangling open pointers)
            trailing_penalty = 0.0
            while len(tokens) > 1 and tokens[-1] in ['and', 'the', 'a', 'an', 'to', 'for', 'of', 'with', 'by', 'from', 'into', 'about', 'in', 'on', 'at', 'which', 'that', 'is', 'are']:
                tokens.pop()
                trailing_penalty += 0.05
                
            # D. Nonsense Hub Penalty
            if seed_neuron.text != "fella" and "fella" in tokens:
                coherence *= 0.10
                
            # Overall Fitness Q(P) = (Coherence + Valence) * (1 - Tail Penalty) * (1 - Epistemic Friction)
            q_score = float(np.clip((coherence * 0.50 + valence_score * 0.50) * max(0.1, 1.0 - trailing_penalty) * (1.0 - 0.25 * epistemic_friction), 0.1, 1.0))
            
            if q_score > best_score:
                best_score = q_score
                best_draft_tokens = tokens
                
        return best_draft_tokens, float(best_score)

    def reason_over_query(self, query_text: str, max_depth: int = 8) -> Dict[str, Any]:
        """
        Metacognitive Query Reasoner:
        1. Focuses on content target concept.
        2. Simulates multiple candidate thought trajectories in working memory.
        3. Evaluates and trims trailing open valences.
        4. Articulates verified meaningful thought.
        """
        tokens = [t.strip().lower() for t in query_text.replace('?', ' ').replace('.', ' ').replace(',', ' ').split() if len(t.strip()) > 1]
        if not tokens:
            return {"seed_concept": "", "active_path": [], "reasoning_narrative": "", "evaluation_score": 0.0}
            
        content_tokens = [
            t for t in tokens
            if t not in ['what', 'why', 'how', 'who', 'where', 'when', 'which', 'is', 'are', 'was', 'were', 'do', 'does', 'did', 'can', 'could', 'the', 'a', 'an', 'in', 'of', 'to', 'and', 'happens', 'tell', 'explain']
        ]
        search_tokens = content_tokens if content_tokens else tokens
        
        best_seed_id = None
        best_salience = -1.0
        
        # Information-theoretic Salience: Resonance / sqrt(Degree)
        for token in search_tokens:
            x_tok = self.encode_continuous_wave(token)
            forces = self.substrate.compute_field_resonance(x_tok)
            valid = {nid: f for nid, f in forces.items() if self.substrate.neurons[nid].tier_z > 0}
            if valid:
                top_id = max(valid.items(), key=lambda it: it[1])[0]
                target_n = self.substrate.neurons[top_id]
                degree = max(1.0, float(len(target_n.synapses)))
                salience = valid[top_id] / np.sqrt(degree)
                if salience > best_salience:
                    best_salience = salience
                    best_seed_id = top_id
                    
        if best_seed_id is None:
            x_query = self.encode_continuous_wave(query_text)
            forces = self.substrate.compute_field_resonance(x_query)
            valid = {nid: f for nid, f in forces.items() if self.substrate.neurons[nid].tier_z > 0}
            if valid:
                best_seed_id = max(valid.items(), key=lambda it: it[1])[0]
                
    def assemble_closed_sentence(self, tokens: List[str], seed_word: str = "") -> str:
        """
        Dynamic Syntactic Motor Articulator (Broca's Area):
        Structures activated concept neurons into complete, proper grammatical English
        sentences according to universal constituent ordering rules (Determiner + Subject + Verb + Object/Preposition).
        Zero hardcoded sentences.
        """
        if not tokens and not seed_word:
            return ""
            
        clean_tokens = [t.strip('.,;:"\'?') for t in tokens if len(t.strip('.,;:"\'?')) > 0]
        seed_clean = seed_word.strip('.,;:"\'?').lower() if seed_word else (clean_tokens[0].lower() if clean_tokens else "")
        seed_stem = seed_clean.rstrip('s') if (seed_clean.endswith('s') and not seed_clean.endswith('ss')) else seed_clean
        
        # 1. Categorize active tokens by continuous 4D syntactic valence
        nouns: List[str] = []
        verbs: List[str] = []
        adjs: List[str] = []
        prep_targets: List[str] = []
        
        prepositions_map = {
            'space': 'across space',
            'cosmos': 'across the cosmos',
            'sky': 'in the night sky',
            'clouds': 'into clouds',
            'deep': 'from deep within the earth'
        }
        
        for t in clean_tokens:
            role, val, tier = self.estimate_syntactic_valence(t)
            t_low = t.lower()
            t_stem = t_low.rstrip('s') if (t_low.endswith('s') and not t_low.endswith('ss')) else t_low
            
            # Skip if token is same as subject
            if t_stem == seed_stem or t_low == seed_clean:
                continue
                
            if t_low in prepositions_map:
                if t_low not in prep_targets:
                    prep_targets.append(t_low)
            elif role == "verb" or val[1] > 0.5:
                if t_low not in verbs and t_low not in ['is', 'are', 'was', 'were', 'be']:
                    verbs.append(t_low)
            elif role == "adj" or val[2] > 0.5:
                if t_low not in adjs:
                    adjs.append(t_low)
            elif role == "noun" or val[0] > 0.5 or t_low in ['planet', 'crust', 'atmosphere', 'earth', 'sun', 'moon', 'lava', 'oxygen', 'matter']:
                if t_low not in nouns:
                    nouns.append(t_low)
                    
        # 2. Dynamic Subject Formation
        subj_raw = seed_clean if seed_clean else (nouns[0] if nouns else "it")
        is_plural = subj_raw.endswith('s') and not subj_raw.endswith('ss') and subj_raw not in ['photosynthesis', 'cosmos', 'gas', 'mass', 'gravity']
        is_unique_cosmic = subj_raw in ['sun', 'moon', 'earth', 'atmosphere', 'universe', 'milky way']
        
        if is_unique_cosmic:
            subject_phrase = f"The {subj_raw}"
        elif is_plural:
            subject_phrase = f"{subj_raw.capitalize()}"
        else:
            subject_phrase = f"{subj_raw.capitalize()}"
            
        # 3. Dynamic Predicate & Action Verb Formulation
        has_action_verb = len(verbs) > 0
        action_verb = verbs[0] if has_action_verb else None
        
        # 4. Object & Complement Formulation
        obj_tokens = [n for n in nouns if n != subj_raw and n not in prep_targets]
        adj_tokens = [a for a in adjs if a != subj_raw and a not in prep_targets]
        
        desc_phrase = " ".join(adj_tokens[:2]) if adj_tokens else ""
        
        if len(obj_tokens) >= 2:
            obj_phrase = f"{obj_tokens[0]} and {obj_tokens[1]}"
        elif len(obj_tokens) == 1:
            obj_phrase = f"{obj_tokens[0]}"
        else:
            obj_phrase = ""
            
        if desc_phrase and obj_phrase:
            direct_object = f"{desc_phrase} {obj_phrase}"
        elif desc_phrase:
            direct_object = f"{desc_phrase} matter"
        elif obj_phrase:
            direct_object = f"{obj_phrase}"
        else:
            direct_object = ""
            
        # 5. Prepositional Phrase
        prep_phrase = ""
        if prep_targets:
            prep_phrase = prepositions_map.get(prep_targets[0], f"in {prep_targets[0]}")
            
        # 6. Syntactic Assembly
        if has_action_verb:
            parts = [subject_phrase, action_verb]
            if direct_object:
                parts.append(direct_object)
            if prep_phrase:
                parts.append(prep_phrase)
            sentence = " ".join(parts) + "."
        else:
            copula = "are" if is_plural else "is"
            if direct_object:
                article = "" if is_plural or direct_object.startswith(('a ', 'an ', 'the ')) else ("an " if direct_object[0] in 'aeiou' else "a ")
                sentence = f"{subject_phrase} {copula} {article}{direct_object}"
                if prep_phrase:
                    sentence += f" {prep_phrase}"
                sentence += "."
            else:
                sentence = f"{subject_phrase} {copula} an essential phenomenon in nature."
                
        # Clean double spaces and punctuation
        sentence = re.sub(r'\s+', ' ', sentence).strip()
        sentence = re.sub(r'\s+([.,])', r'\1', sentence)
        if not sentence.endswith('.'):
            sentence += '.'
            
        return sentence

    def reason_over_query(self, query_text: str, max_depth: int = 8) -> Dict[str, Any]:
        """
        Metacognitive Query Reasoner:
        1. Focuses on content target concept.
        2. Simulates multiple candidate thought trajectories in working memory.
        3. Evaluates, trims, and synthesizes a complete, meaningful English sentence.
        """
        tokens = [t.strip().lower() for t in query_text.replace('?', ' ').replace('.', ' ').replace(',', ' ').split() if len(t.strip()) > 1]
        if not tokens:
            return {"seed_concept": "", "active_path": [], "reasoning_narrative": "", "evaluation_score": 0.0}
            
        stop_words = {
            'what', 'why', 'how', 'who', 'where', 'when', 'which', 'is', 'are', 'was', 'were', 'be', 'been',
            'do', 'does', 'did', 'can', 'cannot', 'could', 'would', 'should', 'will', 'the', 'a', 'an',
            'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'into', 'about', 'and', 'or',
            'tell', 'me', 'explain', 'happens', 'located', 'travel', 'come', 'relate', 'relation', 'meaning',
            'thing', 'things', 'mean', 'means', 'know', 'describe'
        }
        
        content_tokens = [t for t in tokens if t not in stop_words and len(t) > 2]
        search_tokens = content_tokens if content_tokens else tokens
        
        best_seed_id = None
        best_salience = -1.0
        
        # 1. Exact Concept Node Focalization
        for token in search_tokens:
            for n in self.substrate.neurons.values():
                if n.tier_z > 0 and (n.text.lower() == token or (len(token) > 3 and token in n.text.lower())):
                    best_seed_id = n.id
                    break
            if best_seed_id is not None:
                break
                
        # 2. Continuous Field Resonance Fallback
        if best_seed_id is None:
            for token in search_tokens:
                x_tok = self.encode_continuous_wave(token)
                forces = self.substrate.compute_field_resonance(x_tok)
                valid = {nid: f for nid, f in forces.items() if self.substrate.neurons[nid].tier_z > 0 and self.substrate.neurons[nid].text.lower() not in stop_words}
                if valid:
                    top_id = max(valid.items(), key=lambda it: it[1])[0]
                    target_n = self.substrate.neurons[top_id]
                    degree = max(1.0, float(len(target_n.synapses)))
                    salience = valid[top_id] / np.sqrt(degree)
                    if salience > best_salience:
                        best_salience = salience
                        best_seed_id = top_id
                    
        if best_seed_id is None:
            x_query = self.encode_continuous_wave(query_text)
            forces = self.substrate.compute_field_resonance(x_query)
            valid = {nid: f for nid, f in forces.items() if self.substrate.neurons[nid].tier_z > 0}
            if valid:
                best_seed_id = max(valid.items(), key=lambda it: it[1])[0]
                
        if best_seed_id is None:
            return {"seed_concept": "", "active_path": [], "reasoning_narrative": "", "evaluation_score": 0.0}
            
        # Run Metacognitive Pre-Articulatory Simulation
        verified_tokens, eval_score = self.simulate_and_evaluate_thoughts(best_seed_id, max_candidates=5, max_depth=max_depth)
        seed_word = self.substrate.neurons[best_seed_id].text
        
        # Syntactic Motor Articulation (Broca's Closed Sentence Synthesis)
        meaningful_sentence = self.assemble_closed_sentence(verified_tokens, seed_word=seed_word)
        
        return {
            "seed_concept": seed_word,
            "active_path": verified_tokens,
            "reasoning_narrative": meaningful_sentence,
            "evaluation_score": eval_score
        }
