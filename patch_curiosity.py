import re

with open('fella/frontier_manifold.py', 'r') as f:
    text = f.read()

# Replace _calculate_spectron_fitness
pattern_fitness = r'def _calculate_spectron_fitness.*?return fitness, gist_alignment'
replacement_fitness = '''def _calculate_spectron_fitness(self, molecule: List[FellaNeuron], candidate: FellaNeuron, gist_wave: np.ndarray, running_trace: np.ndarray) -> Tuple[float, float]:
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
            # BOOSTED VALENCY: Overclock Catalysts so she uses them to build beautiful grammar
            fitness = valence_bond * 1.15
        else:
            alignment_penalty = 1.0 if gist_alignment > 0.1 else 0.1
            fitness = ((0.7 * valence_bond) + (0.3 * gist_alignment)) * alignment_penalty
            
        return fitness, gist_alignment'''
text = re.sub(pattern_fitness, replacement_fitness, text, flags=re.DOTALL)


# Replace crystallize_incremental
pattern_cryst = r'def crystallize_incremental.*?return molecule'
replacement_cryst = '''def crystallize_incremental(self, gist_wave: np.ndarray) -> List[FellaNeuron]:
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
            
            # GRAMMAR RESOLUTION LOCK (Pure Graph Theory)
            # If the last word is a Catalyst, its wave expects a noun/adjective to its right. We CANNOT stop.
            # We also ensure she speaks at least 3 words to prevent instant-stops on high initial resonance.
            can_stop = not is_catalyst and len(molecule) >= 3
            
            if equilibrium > 0.85 and can_stop:
                print(f"[FRONTIER] Gist satisfied & Grammar Resolved. Halting emission naturally.")
                break
                
            step += 1
            if step >= 40:
                print("[FRONTIER] Safety limit reached (40 words). Halting.")
                break
                
        return molecule'''
text = re.sub(pattern_cryst, replacement_cryst, text, flags=re.DOTALL)


# Replace formulate_thought
pattern_formulate = r'def formulate_thought.*?return sentence'
replacement_formulate = '''def formulate_thought(self, target_concept: str, persona_concept: str = None) -> str:
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
        
        # PERSONA WAVE: Injecting conversational drive without hardcoding generative rules
        if persona_concept:
            for w in persona_concept.lower().split():
                gist_wave += self.brain.lang.encode_continuous_wave(w) * 0.85
                
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
        return sentence'''
text = re.sub(pattern_formulate, replacement_formulate, text, flags=re.DOTALL)

with open('fella/frontier_manifold.py', 'w') as f:
    f.write(text)
