import re

with open('fella/frontier_manifold.py', 'r') as f:
    text = f.read()

# Replace the entire class body with the new physics
new_class_body = '''    def __init__(self, brain: FellaBrain):
        self.brain = brain
        
    def _get_vocabulary_gas(self) -> List[FellaNeuron]:
        return [n for n in self.brain.substrate.neurons.values() if n.tier_z > 0 and len(n.text) > 1]

    def _calculate_spectron_fitness(self, molecule: List[FellaNeuron], candidate: FellaNeuron, gist_wave: np.ndarray, running_trace: np.ndarray) -> Tuple[float, float]:
        # 1. Grammar (Decaying Memory Wave)
        if not molecule:
            left_dent_dist = 0.0
            if candidate.left_context_clusters:
                actual_left_x = np.zeros_like(candidate.x)
                left_dent_dist = min(np.linalg.norm(c['mean'] - actual_left_x) for c in candidate.left_context_clusters)
            right_dent_dist = 0.0
        else:
            actual_left_x = np.zeros_like(candidate.x)
            weight = 1.0
            total_weight = 0.0
            for j in range(1, 4):
                idx = len(molecule) - j
                if idx >= 0:
                    damp = 1.0 / (max(1, len(molecule[idx].synapses)) ** 0.5)
                    actual_left_x += (molecule[idx].x * damp) * weight
                    total_weight += weight
                    weight *= 0.4
            if total_weight > 0:
                actual_left_x /= total_weight
                
            left_dent_dist = 1.0
            if candidate.left_context_clusters:
                left_dent_dist = min(np.linalg.norm(c['mean'] - actual_left_x) for c in candidate.left_context_clusters)
                
            right_dent_dist = 1.0
            left_word = molecule[-1]
            if left_word.right_context_clusters:
                right_dent_dist = min(np.linalg.norm(c['mean'] - candidate.x) for c in left_word.right_context_clusters)
            
        valence_bond = 1.0 / (1.0 + left_dent_dist + right_dent_dist)
        
        # 2. Metacognitive Gist Check (Spectron Prediction)
        max_exp = max((n.exposure_count for n in self.brain.substrate.neurons.values()), default=1)
        is_catalyst = candidate.exposure_count > (max_exp * 0.20)
        
        predicted_trace = running_trace.copy()
        if not is_catalyst:
            predicted_trace += candidate.x
            
        p_norm = np.linalg.norm(predicted_trace)
        if p_norm > 0:
            predicted_trace /= p_norm
            
        gist_alignment = np.dot(predicted_trace, gist_wave)
        
        if is_catalyst:
            fitness = valence_bond * 0.95
        else:
            alignment_penalty = 1.0 if gist_alignment > 0.1 else 0.1
            fitness = ((0.7 * valence_bond) + (0.3 * gist_alignment)) * alignment_penalty
            
        return fitness, gist_alignment

    def crystallize_incremental(self, gist_wave: np.ndarray) -> List[FellaNeuron]:
        molecule: List[FellaNeuron] = []
        gas = self._get_vocabulary_gas()
        if not gas:
            return []
            
        step = 0
        running_trace = np.zeros(self.brain.lang.dim)
        
        while True:
            left_word = molecule[-1] if len(molecule) > 0 else None
            
            best_candidate = None
            best_fitness = -float('inf')
            
            for candidate in gas:
                if left_word and candidate.id == left_word.id:
                    continue
                    
                penalty = 1.0
                for dist_from_end, w in enumerate(reversed(molecule)):
                    if w.id == candidate.id:
                        penalty *= min(1.0, 0.4 + (0.15 * dist_from_end))
                        
                fitness, alignment = self._calculate_spectron_fitness(molecule, candidate, gist_wave, running_trace)
                fitness *= penalty
                
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_candidate = candidate
                    
            if not best_candidate:
                print("[FRONTIER] Grammatical dead end. Halting.")
                break
                
            molecule.append(best_candidate)
            
            max_exp = max((n.exposure_count for n in self.brain.substrate.neurons.values()), default=1)
            is_catalyst = best_candidate.exposure_count > (max_exp * 0.20)
            
            if not is_catalyst:
                running_trace += best_candidate.x
            
            trace_norm = np.linalg.norm(running_trace)
            if trace_norm > 0:
                normalized_trace = running_trace / trace_norm
            else:
                normalized_trace = running_trace
                
            equilibrium = np.dot(normalized_trace, gist_wave)
            print(f"  [SPECTRON] Emitted '{best_candidate.text}' (Fitness: {best_fitness:.3f}, Equilibrium: {equilibrium:.3f})")
            
            if equilibrium > 0.85 and step >= 1:
                print(f"[FRONTIER] Gist satisfied (Equilibrium {equilibrium:.3f} > 0.85). Halting emission naturally.")
                break
                
            step += 1
            if step >= 40:
                print("[FRONTIER] Safety limit reached (40 words). Halting.")
                break
                
        return molecule

    def formulate_thought(self, target_concept: str) -> str:
        print(f"\\n[STIMULUS] Received: '{target_concept}'. Resonating through deep memory...")
        
        words = target_concept.lower().split()
        stimulus_wave = np.zeros(self.brain.lang.dim)
        for w in words:
            stimulus_wave += self.brain.lang.encode_continuous_wave(w)
            
        norm = np.linalg.norm(stimulus_wave)
        if norm > 0:
            stimulus_wave /= norm
            
        memories = []
        for n in self.brain.substrate.neurons.values():
            if n.tier_z > 0 and n.text not in words:
                sim = np.dot(stimulus_wave, n.x)
                if sim > 0.5:
                    memories.append((n, sim))
                    
        gist_wave = np.copy(stimulus_wave)
        if memories:
            memories.sort(key=lambda x: x[1], reverse=True)
            for m, sim in memories[:3]:
                gist_wave += m.x * 0.5
                print(f"  [MEMORY] Pulled associated concept: '{m.text}'")
                
        norm = np.linalg.norm(gist_wave)
        if norm > 0:
            gist_wave /= norm
            
        print("[GIST] Intent Wave fully formed. Initiating Spectron Emission...")
        
        molecule = self.crystallize_incremental(gist_wave)
        
        sentence = " ".join([n.text for n in molecule])
        print(f"[EQUILIBRIUM] Molecule stabilized: '{sentence}'")
        return sentence
'''

# Find everything after class FrontierManifold:
pattern = r'class FrontierManifold:.*'
text = re.sub(pattern, 'class FrontierManifold:\n' + new_class_body, text, flags=re.DOTALL)

with open('fella/frontier_manifold.py', 'w') as f:
    f.write(text)
