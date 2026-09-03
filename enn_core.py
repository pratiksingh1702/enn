import numpy as np

class ENNNeuron:
    def __init__(self, text: str, x_wave: np.ndarray):
        self.text = text
        self.x_wave = x_wave
        self.z_events = set() # Events where this neuron fired
        self.w_families = set() # Spectrons this belongs to

class Spectron:
    def __init__(self, w_id: int, template_waves: list[np.ndarray], structure_text: str):
        self.w_id = w_id
        self.template_waves = template_waves
        self.structure_text = structure_text

class ENNSubstrate:
    def __init__(self, dim: int = 128):
        self.dim = dim
        self.neurons = {}
        self.z_counter = 0
        self.events = {}
        self.w_counter = 0

    def encode_wave(self, text: str) -> np.ndarray:
        # Simulate physical wave embedding by hashing text to stable orthogonal vector
        np.random.seed(abs(hash(text)) % (2**32))
        w = np.random.randn(self.dim)
        return w / np.linalg.norm(w)

    def get_or_create(self, text: str) -> ENNNeuron:
        if text not in self.neurons:
            self.neurons[text] = ENNNeuron(text, self.encode_wave(text))
        return self.neurons[text]

    def record_event(self, words: list[str]) -> int:
        self.z_counter += 1
        z = self.z_counter
        event_neurons = [self.get_or_create(w) for w in words]
        self.events[z] = event_neurons
        for n in event_neurons:
            n.z_events.add(z)
        return z

class ENNFrontier:
    def __init__(self, substrate: ENNSubstrate):
        self.substrate = substrate
        self.spectrons = []

    def form_spectron(self, z_events: list[int]):
        """OVERLAYS Z-EVENTS TO FIND DESTRUCTIVE INTERFERENCE -> [VOID]"""
        length = len(self.substrate.events[z_events[0]])
        template = [np.zeros(self.substrate.dim) for _ in range(length)]
        structure_text_parts = []
        
        for z in z_events:
            event = self.substrate.events[z]
            for i, n in enumerate(event):
                template[i] += n.x_wave
                
        self.substrate.w_counter += 1
        w_id = self.substrate.w_counter
        
        final_template = []
        for i in range(length):
            vec = template[i] / len(z_events)
            norm = np.linalg.norm(vec)
            # In 128D space, the average of 3 different unit vectors has norm ~0.57.
            # So anything < 0.85 indicates destructive interference (a variable slot).
            if norm < 0.85: 
                final_template.append(np.zeros(self.substrate.dim))
                structure_text_parts.append("[VOID]")
            else:
                final_template.append(vec / norm)
                # Reverse-lookup the word that constructively interfered
                for text, n in self.substrate.neurons.items():
                    if np.dot(n.x_wave, vec / norm) > 0.99:
                        structure_text_parts.append(text)
                        break
                
        structure_text = " ".join(structure_text_parts)
        spec = Spectron(w_id, final_template, structure_text)
        self.spectrons.append(spec)
        print(f"[W-AXIS] Formed Spectron {w_id}: '{structure_text}' via destructive interference.")
        return spec

    def process_input(self, text: str) -> str:
        words = text.lower().split()
        print(f"\\n[X-INPUT] Received: '{text}'")
        
        input_waves = [self.substrate.get_or_create(w).x_wave for w in words]
        
        best_spec = None
        best_res = 0
        
        for spec in self.spectrons:
            if len(spec.template_waves) == len(input_waves):
                resonance = 0
                for i in range(len(input_waves)):
                    if np.linalg.norm(spec.template_waves[i]) > 0:
                        resonance += np.dot(input_waves[i], spec.template_waves[i])
                if resonance > best_res:
                    best_res = resonance
                    best_spec = spec
                    
        if best_spec and best_res > 1.5:
            print(f"  -> [RESONANCE] Matched Spectron W={best_spec.w_id} ('{best_spec.structure_text}')")
            
            # WAVE SUBTRACTION to isolate VOID
            isolated = []
            for i in range(len(input_waves)):
                if np.linalg.norm(best_spec.template_waves[i]) == 0:
                    isolated.append(words[i])
            
            print(f"  -> [SUBTRACTION] Isolated target via Physics: {isolated}")
            
            # Z-AXIS SLICING
            retrieved = set()
            for target in isolated:
                n = self.substrate.neurons[target]
                print(f"  -> [Z-AXIS] Slicing events for '{target}'...")
                for z in n.z_events:
                    event_words = [en.text for en in self.substrate.events[z]]
                    # Ignore the events where we learned the 'what is' Spectron
                    if event_words[0] == "what" and event_words[1] == "is":
                        continue
                        
                    print(f"     Found Event Z={z}: {' '.join(event_words)}")
                    for en in self.substrate.events[z]:
                        if en.text != target and en.text != "is": # Filter out structure
                            retrieved.add(en.text)
                            
            print(f"  -> [GIST] Retrieved episodic concepts: {retrieved}")
            
            if retrieved:
                # Build Output
                y_output = f"{isolated[0]} is " + " ".join(retrieved)
                print(f"[Y-OUTPUT] {y_output}")
                return y_output
            else:
                print("[Y-OUTPUT] (Babble) I don't know.")
                return ""
        else:
            print("[FRONTIER] No resonating Spectron. (Babbling...)")
            return ""

def run_test():
    print("=========================================")
    print("ENN DUAL-PROCESS ENGINE (X, Y, Z, W)")
    print("=========================================")
    substrate = ENNSubstrate(dim=128)
    frontier = ENNFrontier(substrate)
    
    print("\\n--- PHASE 1: INGESTING EPISODIC Z-EVENTS ---")
    z1 = substrate.record_event(["apple", "is", "fruit"])
    z2 = substrate.record_event(["apple", "is", "red"])
    z3 = substrate.record_event(["apple", "is", "tasty"])
    print(f"Recorded Events Z={z1}, Z={z2}, Z={z3}")
    
    print("\\n--- PHASE 2: TRAINING W-SPECTRONS ---")
    qz1 = substrate.record_event(["what", "is", "apple"])
    qz2 = substrate.record_event(["what", "is", "tub"])
    qz3 = substrate.record_event(["what", "is", "car"])
    # Engine organically forms Spectron from these events
    frontier.form_spectron([qz1, qz2, qz3])
    
    print("\\n--- PHASE 3 & 4: THE FRONTIER TEST ---")
    frontier.process_input("what is apple")
    
if __name__ == '__main__':
    run_test()
