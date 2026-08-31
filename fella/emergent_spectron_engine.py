import numpy as np
from typing import List, Dict, Any
from fella.core_substrate import FellaNeuron

class EmergentSpectronEngine:
    def __init__(self, substrate, grounding_engine):
        self.substrate = substrate
        self.lang = grounding_engine
        
    def _get_or_create_neuron(self, text: str) -> FellaNeuron:
        """Finds or creates a node for the word, completely neutral."""
        text = text.lower()
        for nid, n in self.substrate.neurons.items():
            if n.text.lower() == text:
                return n
                
        # Completely neutral starting point
        new_id = max(self.substrate.neurons.keys()) + 1 if self.substrate.neurons else 1
        vec = self.lang.encode_continuous_wave(text)
        
        n = FellaNeuron(
            neuron_id=new_id,
            x=vec,
            y=np.zeros(2),
            tier_z=1,
            text=text,
            spectron_charge=0.0 # Neutral
        )
        
        # Add emergent tracking properties dynamically
        n.hot_potential = 0.0
        n.cold_potential = 0.0
        n.catalyst_potential = 0.0
        n.mirror_potential = 0.0
        
        self.substrate.neurons[new_id] = n
        return n

    def determine_spectron_type(self, n: FellaNeuron) -> str:
        """Dynamically infer the Spectron type based on accumulated potentials."""
        potentials = {
            "hot": getattr(n, "hot_potential", 0.0),
            "cold": getattr(n, "cold_potential", 0.0),
            "catalyst": getattr(n, "catalyst_potential", 0.0),
            "mirror": getattr(n, "mirror_potential", 0.0)
        }
        
        # If all are zero or near zero, it's neutral/cold by default (mass)
        max_type = max(potentials, key=potentials.get)
        if potentials[max_type] < 0.5:
            return "cold"
        return max_type

    def get_spectron_charge(self, n: FellaNeuron) -> float:
        """Calculate the dynamic thermodynamic charge."""
        h = getattr(n, "hot_potential", 0.0)
        c = getattr(n, "cold_potential", 0.0)
        # Net charge
        return h - c

    def parse_simultaneous_wave(self, sentence: str, speaker_id: str) -> Dict[str, Any]:
        """
        Parses a sentence by injecting a simultaneous wave, applying dynamic Spectrons,
        and forging or querying based on emergent global temperature.
        """
        # Punctuation acts as basic sensory ground truth for Vacuum (e.g., intonation)
        is_question = "?" in sentence
        words = sentence.strip().lower().replace('?', '').split()
        if not words:
            return {"status": "empty"}
            
        neurons = [self._get_or_create_neuron(w) for w in words]
        speaker_neuron = self._get_or_create_neuron(speaker_id)
        
        # 1. Resolve Mirror Spectrons
        for i, n in enumerate(neurons):
            if self.determine_spectron_type(n) == "mirror":
                # Dynamically reflect the speaker
                neurons[i] = speaker_neuron
                
        # 2. Global Temperature (Wave Interference)
        global_t = sum(self.get_spectron_charge(n) for n in neurons)
        
        # If the sensory intonation is a question, it artificially injects heat
        if is_question:
            global_t += 5.0
            
        print(f"[EMERGENT SPECTRON] Global Temperature: {global_t:.2f} Joules")
        state = "CURIOSITY" if global_t > 0 else "GROUNDED"
        print(f"[EMERGENT SPECTRON] Ambient State: {state}")
        
        operations = []
        
        # 3. Structural Processing
        # Identify words behaving as catalysts
        catalyst_indices = [i for i, n in enumerate(neurons) if self.determine_spectron_type(n) == "catalyst"]
        
        if not catalyst_indices and len(neurons) >= 3:
            # If no catalysts are known yet, the engine tries to guess based on structure (middle word)
            # This is how she learns catalysts initially!
            catalyst_indices = [1]
            
        for idx in catalyst_indices:
            if idx == 0 or idx == len(neurons) - 1:
                continue
                
            operator_n = neurons[idx]
            left_n = neurons[idx - 1]
            right_n = neurons[idx + 1]
            
            if state == "CURIOSITY":
                # Searchlight Mode -> Open a Void
                void_target = right_n if self.get_spectron_charge(left_n) > 0 else left_n
                print(f"[EMERGENT SPECTRON] Searchlight opened Void on: '{void_target.text}'")
                operations.append({"action": "void", "target": void_target.id})
                
                # LEARNING: Reinforce hot potential for words in a Void context
                for n in neurons:
                    if n != operator_n and n != void_target:
                        n.hot_potential = getattr(n, "hot_potential", 0.0) + 1.0
                        
            else:
                # Forge Mode -> Causal Edge
                print(f"[EMERGENT SPECTRON] Forging Tier 3 bond: '{left_n.text}' -> '{right_n.text}'")
                left_n.synapses[right_n.id] = 10.0
                left_n.tier_z = max(left_n.tier_z, 3)
                right_n.tier_z = max(right_n.tier_z, 3)
                operations.append({"action": "forge", "source": left_n.id, "target": right_n.id})
                
                # LEARNING: Reinforce cold potential for masses
                left_n.cold_potential = getattr(left_n, "cold_potential", 0.0) + 1.0
                right_n.cold_potential = getattr(right_n, "cold_potential", 0.0) + 1.0
                
            # LEARNING: Reinforce catalyst potential for the operator
            operator_n.catalyst_potential = getattr(operator_n, "catalyst_potential", 0.0) + 1.0
            
        # 4. Topological Collapse & Mirror Emergence
        self._topological_collapse_check(speaker_neuron.id)
        
        return {"status": "success", "state": state, "temperature": global_t, "operations": operations}

    def _topological_collapse_check(self, current_speaker_id: int):
        signature_map = {}
        for nid, n in self.substrate.neurons.items():
            if not n.synapses:
                continue
            sig = tuple(sorted([(tgt, round(w, 2)) for tgt, w in n.synapses.items() if w >= 5.0]))
            if not sig:
                continue
            if sig not in signature_map:
                signature_map[sig] = []
            signature_map[sig].append(nid)
            
        for sig, nids in signature_map.items():
            if len(nids) > 1:
                self._merge_or_mirror_nodes(nids, current_speaker_id)

    def _merge_or_mirror_nodes(self, nids: List[int], current_speaker_id: int):
        # Determine if a node should become a Mirror instead of merging permanently
        # If a node collapses with the current speaker, we flag it.
        # If it collapses with multiple DIFFERENT speakers over time, it becomes a permanent Mirror.
        
        primary = nids[0]
        
        for secondary in nids[1:]:
            sec_node = self.substrate.neurons[secondary]
            
            # If secondary is collapsing with the speaker...
            if primary == current_speaker_id or secondary == current_speaker_id:
                mirror_candidate = sec_node if primary == current_speaker_id else self.substrate.neurons[primary]
                
                if not hasattr(mirror_candidate, "collapsed_with_speakers"):
                    mirror_candidate.collapsed_with_speakers = set()
                    
                mirror_candidate.collapsed_with_speakers.add(current_speaker_id)
                
                if len(mirror_candidate.collapsed_with_speakers) > 1:
                    # It has collapsed with multiple speakers! It is a Mirror Spectron!
                    mirror_candidate.mirror_potential = getattr(mirror_candidate, "mirror_potential", 0.0) + 5.0
                    print(f"[EMERGENCE] '{mirror_candidate.text}' has emerged as a Mirror Spectron!")
                    # Don't merge permanently; it is now dynamic.
                    continue
            
            # Normal Topological Merge
            primary_node = self.substrate.neurons[primary]
            for nid, n in self.substrate.neurons.items():
                if secondary in n.synapses:
                    w = n.synapses.pop(secondary)
                    n.synapses[primary] = w
            
            del self.substrate.neurons[secondary]
            print(f"[TOPOLOGICAL COLLAPSE] '{sec_node.text}' physically merged into '{primary_node.text}'")
