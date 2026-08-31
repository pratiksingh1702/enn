import numpy as np
from typing import List, Dict, Any, Tuple
from fella.core_substrate import FellaNeuron

class SpectronParser:
    def __init__(self, substrate, grounding_engine):
        self.substrate = substrate
        self.lang = grounding_engine
        
        # Define basic Spectron types based on experiential history (Hardcoded for bootstrap, but emergent in practice)
        # Hot = Curiosity/Seeking (T > 0), Cold = Mass/Grounded (T < 0), Catalyst = Operators (is, and), Mirror = Identity (I, me)
        self.bootstrap_spectrons = {
            "what": {"type": "hot", "charge": 3.0},
            "who": {"type": "hot", "charge": 3.0},
            "why": {"type": "hot", "charge": 3.0},
            "is": {"type": "catalyst", "charge": 0.0},
            "are": {"type": "catalyst", "charge": 0.0},
            "i": {"type": "mirror", "charge": 0.0},
            "me": {"type": "mirror", "charge": 0.0},
            "my": {"type": "mirror", "charge": 0.0}
        }

    def _get_neuron_by_text(self, text: str) -> FellaNeuron:
        """Finds or creates a node for the word."""
        text = text.lower()
        for nid, n in self.substrate.neurons.items():
            if n.text.lower() == text:
                return n
                
        # If it doesn't exist, create it as a Tier 1 semantic mass (0 edges)
        new_id = max(self.substrate.neurons.keys()) + 1 if self.substrate.neurons else 1
        vec = self.lang.encode_continuous_wave(text)
        
        # Check bootstrap specs
        stype = self.bootstrap_spectrons.get(text, {"type": "cold", "charge": -1.0})
        
        n = FellaNeuron(
            neuron_id=new_id,
            x=vec,
            y=np.zeros(2),
            tier_z=1,
            text=text,
            spectron_charge=stype["charge"]
        )
        n.spectron_type = stype["type"]
        self.substrate.neurons[new_id] = n
        return n

    def parse_simultaneous_wave(self, sentence: str, speaker_id: str) -> Dict[str, Any]:
        """
        Phase 2 & 3: Simultaneous Wave Interference & Contextual Forge.
        """
        words = sentence.strip().lower().replace('?', '').split()
        if not words:
            return {"status": "empty"}
            
        neurons = [self._get_neuron_by_text(w) for w in words]
        
        # 1. Resolve Mirror Spectrons (Phase 4 Identity Tracking)
        for i, n in enumerate(neurons):
            if getattr(n, "spectron_type", "cold") == "mirror":
                # Instantly map to speaker
                neurons[i] = self._get_neuron_by_text(speaker_id)
                
        # 2. Calculate Global Temperature (Wave Interference)
        # Hot waves vs Cold waves
        global_t = 0.0
        for n in neurons:
            charge = getattr(n, "spectron_charge", -1.0) # default cold
            global_t += charge
            
        print(f"[SPECTRON PARSER] Global Temperature: {global_t:.2f} Joules")
        
        state = "CURIOSITY" if global_t > 0 else "GROUNDED"
        print(f"[SPECTRON PARSER] Ambient State: {state}")
        
        # 3. Contextual Forge vs Void Creation
        # Find catalysts ("is", "are")
        catalyst_indices = [i for i, n in enumerate(neurons) if getattr(n, "spectron_type", "cold") == "catalyst"]
        
        operations = []
        for idx in catalyst_indices:
            if idx == 0 or idx == len(neurons) - 1:
                continue # Bad structure
                
            left_n = neurons[idx - 1]
            right_n = neurons[idx + 1]
            
            if state == "CURIOSITY":
                # High T: Catalyst becomes a Searchlight -> Opens a Void
                # Check which side is the unknown (the one with the hot spectron)
                if getattr(left_n, "spectron_type", "cold") == "hot":
                    void_target = right_n
                else:
                    void_target = left_n
                    
                print(f"[SPECTRON PARSER] Epistemic Vacuum created on: '{void_target.text}'")
                operations.append({"action": "void", "target": void_target.id})
                
            else:
                # Low T: Catalyst acts as a Forge -> Causal Edge
                print(f"[SPECTRON PARSER] Forging Tier 3 bond: '{left_n.text}' -> '{right_n.text}'")
                left_n.synapses[right_n.id] = 10.0  # High initial conductance for verified truth
                left_n.tier_z = max(left_n.tier_z, 3) # Elevate to Tier 3
                right_n.tier_z = max(right_n.tier_z, 3)
                operations.append({"action": "forge", "source": left_n.id, "target": right_n.id})
                
        # Phase 4: Topological Collapse Check
        self._topological_collapse_check()
        
        return {"status": "success", "state": state, "temperature": global_t, "operations": operations}
        
    def _topological_collapse_check(self):
        """Merges nodes sharing exact identical outgoing vectors."""
        # Map signature -> list of node IDs
        signature_map = {}
        for nid, n in self.substrate.neurons.items():
            if not n.synapses:
                continue
            # A signature is a sorted tuple of (target_id, weight)
            # To be robust, we only look at high-strength Tier 3 causal links
            sig = tuple(sorted([(tgt, round(w, 2)) for tgt, w in n.synapses.items() if w >= 5.0]))
            if not sig:
                continue
            if sig not in signature_map:
                signature_map[sig] = []
            signature_map[sig].append(nid)
            
        for sig, nids in signature_map.items():
            if len(nids) > 1:
                print(f"[TOPOLOGICAL COLLAPSE] Merging nodes {nids} due to identical gravitational vectors: {sig}")
                self._merge_nodes(nids)

    def _merge_nodes(self, nids: List[int]):
        primary = nids[0]
        primary_node = self.substrate.neurons[primary]
        
        for secondary in nids[1:]:
            if secondary not in self.substrate.neurons:
                continue
            sec_node = self.substrate.neurons[secondary]
            
            # Snap incoming edges to primary
            for nid, n in self.substrate.neurons.items():
                if secondary in n.synapses:
                    w = n.synapses.pop(secondary)
                    n.synapses[primary] = w
            
            # Delete secondary
            del self.substrate.neurons[secondary]
            print(f"[TOPOLOGICAL COLLAPSE] '{sec_node.text}' merged into '{primary_node.text}'")
