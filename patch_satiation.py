import re

with open('fella/frontier_manifold.py', 'r') as f:
    text = f.read()

# 1. Update _calculate_spectron_fitness to evaluate against ACTIVE gist (Semantic Satiation)
pattern_fitness = r'def _calculate_spectron_fitness.*?return fitness, gist_alignment'
replacement_fitness = '''def _calculate_spectron_fitness(self, molecule: List[FellaNeuron], candidate: FellaNeuron, active_gist: np.ndarray, running_trace: np.ndarray) -> Tuple[float, float]:
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
        
        # 2. Semantic Satiation Check (Matching against the REMAINING unmet gist)
        max_exp = max((n.exposure_count for n in self.brain.substrate.neurons.values()), default=1)
        is_catalyst = candidate.exposure_count > (max_exp * 0.20)
        
        c_norm = np.linalg.norm(candidate.x)
        c_x = candidate.x / c_norm if c_norm > 0 else candidate.x
        
        g_norm = np.linalg.norm(active_gist)
        g_x = active_gist / g_norm if g_norm > 0 else active_gist
        
        # How well does this word fulfill the remaining, unsatisfied cognitive pressure?
        gist_alignment = np.dot(c_x, g_x)
        
        if is_catalyst:
            fitness = valence_bond * 1.15
        else:
            alignment_penalty = 1.0 if gist_alignment > 0.0 else 0.1
            fitness = ((0.7 * valence_bond) + (0.3 * gist_alignment)) * alignment_penalty
            
        return fitness, gist_alignment'''

text = re.sub(pattern_fitness, replacement_fitness, text, flags=re.DOTALL)


# 2. Update crystallize_incremental to exhaust the active gist
pattern_cryst = r'def crystallize_incremental.*?return molecule'
replacement_cryst = '''def crystallize_incremental(self, original_gist: np.ndarray) -> List[FellaNeuron]:
        molecule: List[FellaNeuron] = []
        gas = self._get_vocabulary_gas()
        if not gas:
            return []
            
        step = 0
        running_trace = np.zeros(self.brain.lang.dim)
        active_gist = np.copy(original_gist) # The dynamic cognitive pressure
        
        stall_counter = 0
        prev_equilibrium = -1.0
        
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
                        
                fitness, alignment = self._calculate_spectron_fitness(molecule, candidate, active_gist, running_trace)
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
                # SEMANTIC SATIATION: Subtract the emitted wave from the active gist.
                # She has expressed this concept, so the cognitive pressure to say it is relieved!
                active_gist -= best_candidate.x * 0.8
            
            trace_norm = np.linalg.norm(running_trace)
            normalized_trace = running_trace / trace_norm if trace_norm > 0 else running_trace
                
            gist_norm = np.linalg.norm(original_gist)
            normalized_gist = original_gist / gist_norm if gist_norm > 0 else original_gist
            
            equilibrium = np.dot(normalized_trace, normalized_gist)
            
            print(f"  [SPECTRON] Emitted '{best_candidate.text}' (Fitness: {best_fitness:.3f}, Global Equilibrium: {equilibrium:.3f})")
            
            if abs(equilibrium - prev_equilibrium) < 0.01:
                stall_counter += 1
            else:
                stall_counter = 0
                
            prev_equilibrium = equilibrium
            
            if stall_counter >= 4:
                print("[FRONTIER] Thermodynamic stall (Frustration). Breaking grammar lock to stop.")
                break
            
            # Gist pressure drops as active_gist norm shrinks
            remaining_pressure = np.linalg.norm(active_gist)
            
            can_stop = not is_catalyst and len(molecule) >= 3
            
            # If cognitive pressure is nearly depleted, stop naturally
            if remaining_pressure < (gist_norm * 0.25) and can_stop:
                print(f"[FRONTIER] Cognitive pressure depleted. Halting emission naturally.")
                break
                
            step += 1
            if step >= 30:
                print("[FRONTIER] Safety limit reached (30 words). Halting.")
                break
                
        return molecule'''

text = re.sub(pattern_cryst, replacement_cryst, text, flags=re.DOTALL)


# 3. Update formulate_thought to remove hardcoded [:3] and use continuous physics decay
pattern_formulate = r'def formulate_thought.*?return sentence'
replacement_formulate = '''def formulate_thought(self, target_concept: str, persona_concept: str = None) -> str:
        print(f"\\n[STIMULUS] Received: '{target_concept}'. Resonating through deep memory...")
        
        words = target_concept.lower().split()
        stimulus_wave = np.zeros(self.brain.lang.dim)
        
        for w in words:
            known = False
            for n in self.brain.substrate.neurons.values():
                if n.text == w:
                    known = True
                    break
            
            wave = self.brain.lang.encode_continuous_wave(w)
            if not known:
                print(f"  [NEUROGENESIS] Spontaneously allocating neuron for unknown concept: '{w}'")
                self.brain.substrate.find_or_birth_concept(text=w, x_vec=wave, tier_z=1)
                
            stimulus_wave += wave
            
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
        
        if persona_concept:
            for w in persona_concept.lower().split():
                gist_wave += self.brain.lang.encode_continuous_wave(w) * 0.85
                
        if memories:
            # PHYSICS-BASED MEMORY RETRIEVAL: No hardcoded [:3] limit. 
            # We add ALL resonating memories, scaled exponentially by their resonance (decay factor).
            for m, sim in memories:
                if sim > 0.60: # Base resonance threshold
                    decay_weight = sim ** 3 # Exponential decay: perfectly matching concepts are vastly stronger than weak associations
                    gist_wave += m.x * decay_weight
                    print(f"  [MEMORY] Pulled associated concept: '{m.text}' (Resonance: {sim:.3f}, Weight: {decay_weight:.3f})")
                
        norm = np.linalg.norm(gist_wave)
        if norm > 0:
            gist_wave /= norm
            
        print("[GIST] Intent Wave fully formed. Initiating Spectron Emission...")
        
        molecule = self.crystallize_incremental(gist_wave)
        
        sentence = " ".join([n.text for n in molecule])
        print(f"[EQUILIBRIUM] Molecule stabilized: '{sentence}'")
        return sentence'''

text = re.sub(pattern_formulate, replacement_formulate, text, flags=re.DOTALL)

with open('fella/frontier_manifold.py', 'w') as f:
    f.write(text)
