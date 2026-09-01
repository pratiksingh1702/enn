import numpy as np
from typing import List, Tuple
from fella.fella_brain import FellaBrain
from fella.core_substrate import FellaNeuron

class FrontierManifold:
    """
    The Physics-Based Working Memory (Global Workspace).
    Uses psycholinguistics-backed incremental, left-to-right generation 
    guided by a global "plan vector" to destroy permutation explosion.
    """
    def __init__(self, brain: FellaBrain):
        self.brain = brain
        
    def _get_vocabulary_gas(self) -> List[FellaNeuron]:
        """Returns all viable words in her deep memory to act as candidate gas."""
        return [n for n in self.brain.substrate.neurons.values() if n.tier_z > 0 and len(n.text) > 1]

    def _calculate_bond_fitness(self, left_word: FellaNeuron, candidate: FellaNeuron, plan_vector: np.ndarray) -> float:
        """
        Calculates how well the candidate bonds to the left_word AND how well it 
        resonates with the global plan vector. Uses GMM clusters to support multi-sense words!
        """
        # 1. Valence Bond (Grammar) via GMM Clusters
        if left_word is None:
            left_dent_dist = 0.0
            if candidate.left_context_clusters:
                actual_left_x = np.zeros_like(candidate.x)
                left_dent_dist = min(np.linalg.norm(c['mean'] - actual_left_x) for c in candidate.left_context_clusters)
            right_dent_dist = 0.0
        else:
            actual_left_x = left_word.x
            
            left_dent_dist = 1.0 # default high penalty if no clusters
            if candidate.left_context_clusters:
                left_dent_dist = min(np.linalg.norm(c['mean'] - actual_left_x) for c in candidate.left_context_clusters)
                
            right_dent_dist = 1.0
            if left_word.right_context_clusters:
                right_dent_dist = min(np.linalg.norm(c['mean'] - candidate.x) for c in left_word.right_context_clusters)
            
        valence_bond = 1.0 / (1.0 + left_dent_dist + right_dent_dist)
        
        # 2. Semantic Resonance & Catalyst Weighting
        # Gap 4 Fix: Catalysts are syntactic glue. Defined by high exposure frequency relative to corpus max
        max_exp = max((n.exposure_count for n in self.brain.substrate.get_all_neurons()), default=1)
        is_catalyst = candidate.exposure_count > (max_exp * 0.20)
        
        if is_catalyst:
            # Catalysts have 0 semantic resonance. They exist entirely to bridge valence gaps.
            semantic_resonance = 0.0
            # Boost the fitness artificially so the engine willingly picks them to fulfill grammar gaps
            fitness = valence_bond * 0.95 
        else:
            semantic_dist = np.linalg.norm(candidate.x - plan_vector)
            semantic_resonance = 1.0 / (1.0 + semantic_dist)
            fitness = (0.7 * valence_bond) + (0.3 * semantic_resonance)
        
        return fitness

    def crystallize_incremental(self, plan_vector: np.ndarray, max_length: int = 10, stop_threshold: float = 0.35) -> List[FellaNeuron]:
        """
        Autoregressive, left-to-right generation with bounded backtracking.
        """
        molecule: List[FellaNeuron] = []
        gas = self._get_vocabulary_gas()
        
        if not gas:
            return []
            
        step = 0
        backtracks = 0
        max_backtracks = 3
        
        # History for backtracking: stores (molecule_state, blacklisted_candidates_for_this_step)
        history = []
        
        while step < max_length:
            left_word = molecule[-1] if len(molecule) > 0 else None
            
            # Get blacklist for current step if we backtracked here
            blacklist = []
            if len(history) > step:
                blacklist = history[step][1]
            else:
                history.append((list(molecule), []))
                
            # Score all candidates
            candidates_scored = []
            for candidate in gas:
                if candidate.id in blacklist:
                    continue
                # Prevent pure stuttering (saying the exact same word twice in a row)
                if left_word is not None and candidate.id == left_word.id:
                    continue
                    
                # Distance-Decayed Inhibition of Return
                # Heavily penalize words reused immediately, but let the penalty fade back 
                # toward 1.0 as distance increases to allow natural language repetition (like 'the').
                penalty = 1.0
                for dist_from_end, w in enumerate(reversed(molecule)):
                    if w.id == candidate.id:
                        # dist_from_end = 0 means it was the immediately previous word
                        # Penalty starts at 0.4 and fades by 0.15 per slot
                        penalty_factor = min(1.0, 0.4 + (0.15 * dist_from_end))
                        penalty *= penalty_factor
                        
                fitness = penalty * self._calculate_bond_fitness(left_word, candidate, plan_vector)
                candidates_scored.append((fitness, candidate))
                
            candidates_scored.sort(key=lambda x: x[0], reverse=True)
            
            if not candidates_scored:
                break
                
            best_fitness, best_word = candidates_scored[0]
            plan_mag = np.linalg.norm(plan_vector)
            print(f"  [STEP {step}] Selected '{best_word.text}' (Fitness: {best_fitness:.3f}, Plan_Mag: {plan_mag:.3f})")
            
            # Dynamic Relative Stopping Condition
            # If the first word is a catalyst, we don't want to inflate the stop threshold.
            if step == 0:
                max_exp = max((n.exposure_count for n in self.brain.substrate.get_all_neurons()), default=1)
                is_best_cat = best_word.exposure_count > (max_exp * 0.20)
                anchor_fitness = best_fitness if not is_best_cat else 0.85
                dynamic_stop = max(stop_threshold, anchor_fitness * 0.45)
                initial_plan_mag = plan_mag
            
            # 1. Semantic Exhaustion (Magnitude Gate)
            if plan_mag < (initial_plan_mag * 0.15) and len(molecule) > 0:
                print(f"[FRONTIER] Semantic exhaustion (Plan_Mag {plan_mag:.3f} < Floor). Halting generation.")
                break
                
            # 2. Grammatical Dead End (Fitness Gate)
            if best_fitness < dynamic_stop and len(molecule) > 0:
                print(f"[FRONTIER] Grammatical dead end (Fitness {best_fitness:.3f} < {dynamic_stop:.3f}). Halting generation.")
                break
                
            # Garden-Path Check (Dead End)
            if best_fitness < (dynamic_stop * 0.7) and len(molecule) > 0 and backtracks < max_backtracks:
                print(f"[FRONTIER] Garden-path detected. Backtracking...")
                step -= 1
                backtracks += 1
                bad_word = molecule.pop()
                history[step][1].append(bad_word.id)
                history = history[:step+1]
                
                # Restore the plan vector tension that we falsely relieved
                overlap = np.dot(bad_word.x, plan_vector)
                if overlap > 0:
                    plan_vector = plan_vector + (overlap * bad_word.x)
                continue
                
            # Accept word
            molecule.append(best_word)
            step += 1
            
            # Thought Dissipation: Subtract the projection of the word onto the plan.
            # Catalysts (function words) are syntactic glue, they do not relieve semantic tension.
            max_exp = max((n.exposure_count for n in self.brain.substrate.get_all_neurons()), default=1)
            is_catalyst = best_word.exposure_count > (max_exp * 0.20)
            if not is_catalyst:
                overlap = np.dot(best_word.x, plan_vector)
                if overlap > 0:
                    # Decay Floor: A single word can only relieve up to 70% of the current plan magnitude.
                    current_mag = np.linalg.norm(plan_vector)
                    max_decay_mag = current_mag * 0.70
                    
                    projection_vector = overlap * best_word.x
                    projection_mag = np.linalg.norm(projection_vector)
                    
                    if projection_mag > max_decay_mag:
                        scale = max_decay_mag / projection_mag
                        projection_vector = projection_vector * scale
                        
                    plan_vector = plan_vector - projection_vector
                
        return molecule

    def formulate_thought(self, target_concept: str, max_length: int = 15, stop_threshold: float = 0.35) -> str:
        """
        Physics-driven sentence generation. The target_concept acts as a semantic vacuum 
        that pulls related words out of the void until its tension is satisfied.
        """
        print(f"\n[FRONTIER] Vacuum detected: '{target_concept}'. Establishing Plan Vector...")
        
        # Compositional Plan Vector: sum the individual wave embeddings so it geometrically represents the parts
        words = target_concept.lower().split()
        plan_vector = np.zeros(self.brain.lang.dim)
        for w in words:
            plan_vector += self.brain.lang.encode_continuous_wave(w)
            
        norm = np.linalg.norm(plan_vector)
        if norm > 0:
            plan_vector = plan_vector / norm
        
        molecule = self.crystallize_incremental(plan_vector, max_length=max_length, stop_threshold=stop_threshold)
        
        sentence = " ".join([n.text for n in molecule])
        print(f"[FRONTIER] Molecule stabilized: '{sentence}'")
        return sentence
