import numpy as np
from fella.core_substrate import Spectron

class FrontierManifold:
    def __init__(self, brain):
        self.brain = brain

    def form_spectron(self, z_events: list[int]):
        length = len(self.brain.events[z_events[0]])
        template = [np.zeros(self.brain.dim) for _ in range(length)]
        
        for z in z_events:
            event = self.brain.events[z]
            for i, n in enumerate(event):
                template[i] += n.x_wave
                
        self.brain.w_counter += 1
        w_id = self.brain.w_counter
        
        final_template = []
        for i in range(length):
            vec = template[i] / len(z_events)
            norm = np.linalg.norm(vec)
            if norm < 0.85: 
                final_template.append(np.zeros(self.brain.dim))
            else:
                final_template.append(vec / norm)
                
        spec = Spectron(w_id, final_template)
        spec.source_z_events = set(z_events) 
        self.brain.spectrons.append(spec)
        return spec

    def formulate_thought(self, text: str, recursion_depth=0, simulate=False) -> str:
        words = text.lower().split()
        indent = "  " * recursion_depth
        if not simulate:
            print(f"\\n{indent}[X-INPUT] Received: '{text}'")
        input_waves = [self.brain.get_or_create(w).x_wave for w in words]
        
        best_spec = None
        best_res = 0
        best_alignment = []
        
        for spec in self.brain.spectrons:
            if spec.is_generation: continue
            structural_anchors = [(i, w) for i, w in enumerate(spec.template_waves) if np.linalg.norm(w) > 0]
            if not structural_anchors: continue
            
            resonance = 0
            possible = len(structural_anchors)
            input_idx = 0
            alignment = []
            
            for spec_idx, s_wave in structural_anchors:
                found = False
                while input_idx < len(input_waves):
                    sim = np.dot(input_waves[input_idx], s_wave)
                    if sim > 0.8:
                        resonance += sim
                        alignment.append((spec_idx, input_idx))
                        input_idx += 1
                        found = True
                        break
                    input_idx += 1
            
            if possible > 0 and resonance >= (possible * 0.8) and resonance > best_res:
                best_res = resonance
                best_spec = spec
                best_alignment = alignment
                    
        if best_spec:
            if not simulate:
                print(f"{indent}  -> [RESONANCE] Matched Spectron W={best_spec.w_id}")
            
            isolated = []
            anchor_input_indices = {i_idx for s_idx, i_idx in best_alignment}
            for i in range(len(input_waves)):
                if i not in anchor_input_indices:
                    isolated.append(words[i])
                    
            if not simulate:
                print(f"{indent}  -> [SUBTRACTION] Isolated: {' '.join(isolated)}")
            
            # UPGRADE 2: FRACTAL SPECTRONS (Recursion)
            # We do NOT use hardcoded length checks (like len >= 3).
            # We pass the isolated blob back into the Frontier. If it physically resonates with a Spectron, it is a nested clause!
            if recursion_depth < 1:
                sub_y, sub_target, sub_ret, sub_wid = self.formulate_thought(" ".join(isolated), recursion_depth + 1, simulate=True)
                # If it returned a valid target, it successfully resonated as a mathematical sub-clause
                if sub_target is not None:
                    if not simulate:
                        print(f"{indent}  -> [FRACTAL] Sub-clause geometrically collapsed into: {sub_y}")
                    isolated = sub_y.split()
            
            # MAGNETIC ROUTING
            context_words = [w for w in words if w not in isolated]
            attractor_vectors = []
            for w in context_words:
                n = self.brain.neurons[w]
                if len(n.z_events) <= (self.brain.z_counter * 0.30):
                    attractor_vectors.append(n.x_wave)
                    
            attractor = None
            if attractor_vectors:
                attractor = np.mean(attractor_vectors, axis=0)
                attractor /= (np.linalg.norm(attractor) + 1e-9)
            
            # THERMODYNAMICS
            retrieved_energies = {}
            queue = [(target, 1.0) for target in isolated]
            
            while queue:
                current_word, energy = queue.pop(0)
                if energy < 0.15: continue
                
                n = self.brain.neurons.get(current_word)
                if not n or not n.z_events: continue
                n.last_accessed = self.brain.z_counter # Refresh entropy charge!
                
                split_energy = energy / len(n.z_events)
                for z in n.z_events:
                    if hasattr(best_spec, 'source_z_events') and z in best_spec.source_z_events: continue
                    for en in self.brain.events[z]:
                        if en.text != current_word:
                            if len(en.z_events) > (self.brain.z_counter * 0.30):
                                continue
                            hop_efficiency = 0.9
                            if attractor is not None:
                                alignment = np.dot(en.x_wave, attractor)
                                multiplier = 1.0 + (alignment * 3.0) 
                                hop_efficiency *= multiplier
                            new_energy = min(split_energy * hop_efficiency, energy * 0.95)
                            if new_energy > 0.05:
                                retrieved_energies[en.text] = retrieved_energies.get(en.text, 0) + new_energy
                                queue.append((en.text, new_energy)) 
                                
            retrieved = [w for w, e in sorted(retrieved_energies.items(), key=lambda x: x[1], reverse=True) if w not in isolated][:5]
            
            # PURE GEOMETRIC GENERATION
            y_output = ""
            if retrieved:
                # Find generation spectrons that were specifically taught for THIS question pattern
                gen_specs = [s for s in self.brain.spectrons if getattr(s, 'is_generation', False) and getattr(s, 'triggering_w_id', None) == best_spec.w_id]
                if gen_specs:
                    best_gen = gen_specs[-1] 
                    if not simulate:
                        print(f"{indent}  -> [GENERATION] Applying structural Phase-Locking W={best_gen.w_id}")
                    available_concepts = list(retrieved)
                    out_words = []
                    
                    # UPGRADE 4 LOGIC: Vectorized lookup for generation
                    for expected_wave in best_gen.template_waves:
                        if np.linalg.norm(expected_wave) == 0:
                            out_words.append(" ".join(isolated) if isolated else "")
                        else:
                            best_match_concept = None
                            best_match_sim = -1
                            if available_concepts:
                                sims = [np.dot(self.brain.neurons[c].x_wave, expected_wave) for c in available_concepts]
                                max_idx = np.argmax(sims)
                                best_match_sim = sims[max_idx]
                                if best_match_sim > 0.8:
                                    best_match_concept = available_concepts[max_idx]
                                    
                            if best_match_concept:
                                out_words.append(best_match_concept)
                                available_concepts.remove(best_match_concept)
                            else:
                                sims = self.brain.get_fast_similarity(expected_wave)
                                best_idx = np.argmax(sims)
                                out_words.append(self.brain.matrix_keys[best_idx])
                                
                    y_output = " ".join([w for w in out_words if w])
                else:
                    y_output = f"{' '.join(isolated) if isolated else ''} " + " ".join(retrieved)
            
            # UPGRADE 3: THE HOLOGRAPHIC SIMULATOR
            if not simulate and y_output:
                print(f"{indent}  -> [SIMULATOR] Monologue evaluating: '{y_output}'")
                out_waves = [self.brain.get_or_create(w).x_wave for w in y_output.split()]
                unstable = False
                for i in range(len(out_waves)):
                    for j in range(i+1, len(out_waves)):
                        if np.dot(out_waves[i], out_waves[j]) < -0.15: # Severe geometric contradiction (Repulsion)
                            unstable = True
                
                if unstable:
                    print(f"{indent}  -> [SIMULATOR] ABORT! Logical Contradiction Detected. The thought caused destructive interference.")
                    y_output = "(Aborted Thought due to Paradox)"
                    
            if not simulate:
                print(f"{indent}[Y-OUTPUT] {y_output}")
            return y_output, " ".join(isolated) if isolated else "", retrieved, best_spec.w_id if best_spec else None
        return "", None, None, None

    def process_correction(self, target: str, retrieved: list, correction: str, triggering_w_id: int = None):
        words = correction.lower().split()
        template = []
        for w in words:
            if w == target:
                template.append(np.zeros(self.brain.dim)) 
            elif w in retrieved:
                template.append(self.brain.neurons[w].x_wave.copy())
            else:
                template.append(self.brain.get_or_create(w).x_wave)
                
        self.brain.w_counter += 1
        w_id = self.brain.w_counter
        spec = Spectron(w_id, template, True)
        spec.triggering_w_id = triggering_w_id
        self.brain.spectrons.append(spec)
        return spec
