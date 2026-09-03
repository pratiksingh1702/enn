import re

with open('fella/frontier_manifold.py', 'r') as f:
    text = f.read()

# 1. Update formulate_thought for Native Neurogenesis
pattern_formulate = r'def formulate_thought.*?return sentence'
replacement_formulate = '''def formulate_thought(self, target_concept: str, persona_concept: str = None) -> str:
        print(f"\\n[STIMULUS] Received: '{target_concept}'. Resonating through deep memory...")
        
        words = target_concept.lower().split()
        stimulus_wave = np.zeros(self.brain.lang.dim)
        
        for w in words:
            # NATIVE NEUROGENESIS: If she doesn't know a word, allocate a neuron instantly
            if w not in self.brain.substrate.neurons:
                print(f"  [NEUROGENESIS] Spontaneously allocating neuron for unknown concept: '{w}'")
                new_wave = self.brain.lang.encode_continuous_wave(w)
                from fella.fella_neuron import FellaNeuron
                new_n = FellaNeuron(w, new_wave)
                self.brain.substrate.add_neuron(new_n)
                
            stimulus_wave += self.brain.substrate.neurons[w].x
            
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
                if w in self.brain.substrate.neurons:
                    gist_wave += self.brain.substrate.neurons[w].x * 0.85
                else:
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

# 2. Update crystallize_incremental for Fatigue/Stall
pattern_cryst = r'def crystallize_incremental.*?return molecule'
replacement_cryst = '''def crystallize_incremental(self, gist_wave: np.ndarray) -> List[FellaNeuron]:
        molecule: List[FellaNeuron] = []
        gas = self._get_vocabulary_gas()
        if not gas:
            return []
            
        step = 0
        running_trace = np.zeros(self.brain.lang.dim)
        
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
            
            # FRUSTRATION / STALL MECHANISM
            if abs(equilibrium - prev_equilibrium) < 0.01:
                stall_counter += 1
            else:
                stall_counter = 0
                
            prev_equilibrium = equilibrium
            
            if stall_counter >= 3:
                print("[FRONTIER] Thermodynamic stall (Frustration) detected. Breaking grammar lock to stop.")
                break
            
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

with open('fella/frontier_manifold.py', 'w') as f:
    f.write(text)
