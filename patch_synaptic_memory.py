import re

with open('fella/frontier_manifold.py', 'r') as f:
    text = f.read()

pattern_formulate = r'def formulate_thought.*?return sentence'
replacement_formulate = '''def formulate_thought(self, target_concept: str, persona_concept: str = None) -> str:
        print(f"\\n[STIMULUS] Received: '{target_concept}'. Resonating through deep memory...")
        
        words = target_concept.lower().split()
        stimulus_wave = np.zeros(self.brain.lang.dim)
        
        anchor_neurons = []
        
        for w in words:
            known = False
            for n in self.brain.substrate.neurons.values():
                if n.text == w:
                    known = True
                    anchor_neurons.append(n)
                    break
            
            wave = self.brain.lang.encode_continuous_wave(w)
            if not known:
                print(f"  [NEUROGENESIS] Spontaneously allocating neuron for unknown concept: '{w}'")
                new_n, _ = self.brain.substrate.find_or_birth_concept(text=w, x_vec=wave, tier_z=1)
                anchor_neurons.append(new_n)
                
            stimulus_wave += wave
            
        norm = np.linalg.norm(stimulus_wave)
        if norm > 0:
            stimulus_wave /= norm
            
        gist_wave = np.copy(stimulus_wave)
        
        if persona_concept:
            for w in persona_concept.lower().split():
                gist_wave += self.brain.lang.encode_continuous_wave(w) * 0.85
                
        # PHYSICS-BASED HEBBIAN RECALL
        # Instead of comparing semantic CLIP vectors (which caused the cognitive seizure),
        # we flow energy through the actual synaptic connections built during ingestion!
        associated_energy = {}
        for anchor in anchor_neurons:
            if anchor.synapses:
                for target_id, weight in anchor.synapses.items():
                    target_n = self.brain.substrate.neurons.get(target_id)
                    if target_n and target_n.text not in words:
                        # Only add energy to valid concepts, ignore pure catalysts
                        max_exp = max((n.exposure_count for n in self.brain.substrate.neurons.values()), default=1)
                        is_tgt_catalyst = target_n.exposure_count > (max_exp * 0.20)
                        if not is_tgt_catalyst:
                            associated_energy[target_n] = associated_energy.get(target_n, 0.0) + weight
                            
        # Any memory that received significant synaptic energy is added to the Gist!
        # NO hardcoded limits! Just pure energy thresholding.
        for m, energy in associated_energy.items():
            if energy > 0.3: # Minimum synaptic resonance threshold
                decay_weight = min(1.0, energy * 0.5)
                gist_wave += m.x * decay_weight
                print(f"  [SYNAPSE] Pulled experiential memory: '{m.text}' (Hebbian Energy: {energy:.3f}, Weight: {decay_weight:.3f})")
                
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
