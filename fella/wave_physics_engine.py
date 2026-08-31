import numpy as np
import math
from typing import List, Dict, Any
from fella.core_substrate import FellaNeuron

class WavePhysicsEngine:
    def __init__(self, substrate, grounding_engine):
        self.substrate = substrate
        self.lang = grounding_engine
        
    def _get_or_create_neuron(self, text: str) -> FellaNeuron:
        """Finds or creates a node for the word, completely neutral."""
        text = text.lower()
        for nid, n in self.substrate.neurons.items():
            if n.text.lower() == text:
                # Ensure it has wave properties
                self._ensure_wave_properties(n)
                return n
                
        # Completely neutral starting point
        new_id = max(self.substrate.neurons.keys()) + 1 if self.substrate.neurons else 1
        vec = self.lang.encode_continuous_wave(text)
        
        n = FellaNeuron(
            neuron_id=new_id,
            x=vec,
            y=np.zeros(2),
            tier_z=1,
            text=text
        )
        self._ensure_wave_properties(n)
        self.substrate.neurons[new_id] = n
        return n

    def _ensure_wave_properties(self, n: FellaNeuron):
        if not hasattr(n, 'phase'):
            n.phase = 0.0          # Phase angle (phi)
            n.amplitude = 1.0      # Amplitude (A)
            
            # Spectron Emergence Tracking
            n.hot_potential = 0.0
            n.cold_potential = 0.0
            n.catalyst_potential = 0.0
            n.mirror_potential = 0.0
            
            # For tracking topological collapses
            n.collapsed_with_speakers = set()

    def determine_spectron_type(self, n: FellaNeuron) -> str:
        """Dynamically infer the Spectron type based on accumulated potentials."""
        potentials = {
            "hot": getattr(n, "hot_potential", 0.0),
            "cold": getattr(n, "cold_potential", 0.0),
            "catalyst": getattr(n, "catalyst_potential", 0.0),
            "mirror": getattr(n, "mirror_potential", 0.0)
        }
        max_type = max(potentials, key=potentials.get)
        if potentials[max_type] < 0.5:
            return "mass"
        return max_type

    def parse_simultaneous_wave(self, sentence: str, speaker_id: str) -> Dict[str, Any]:
        """
        Parses a sentence by injecting a simultaneous wave, applying Phase operators,
        and forging or querying based on emergent wave interference.
        """
        # Punctuation acts as basic sensory ground truth for Vacuum
        sensory_target_vacuum = "?" in sentence
        
        words = sentence.strip().lower().replace('?', '').split()
        if not words:
            return {"status": "empty"}
            
        neurons = [self._get_or_create_neuron(w) for w in words]
        speaker_neuron = self._get_or_create_neuron(speaker_id)
        
        # 1. Resolve Mirror Spectrons (Identity Tracking)
        for i, n in enumerate(neurons):
            if self.determine_spectron_type(n) == "mirror":
                neurons[i] = speaker_neuron
                
        # 2. Wave Superposition
        avg_phase = sum(n.phase for n in neurons) / len(neurons)
        
        # Artificial sensory injection (environmental ground truth)
        if sensory_target_vacuum:
            avg_phase = math.pi # Force destructive interference environment
            
        is_void_state = avg_phase > (math.pi / 2.0)
        
        print(f"[WAVE ENGINE] Sentence Average Phase: {avg_phase:.2f} rad")
        state = "DESTRUCTIVE (VOID)" if is_void_state else "CONSTRUCTIVE (FORGE)"
        print(f"[WAVE ENGINE] Interference State: {state}")
        
        operations = []
        
        # 3. Catalyst Emergence (Spatial Topology)
        # Any node trapped temporally between two nodes undergoing severe wave deformation 
        # (e.g. between a Vacuum Target and a Phase-Shifter, or between two Forging nodes) 
        # acts as the physical conduit, absorbing Catalyst Potential.
        operator_nodes = set()
        if len(neurons) >= 3:
            for i in range(1, len(neurons) - 1):
                left_n = neurons[i-1]
                right_n = neurons[i+1]
                operator_n = neurons[i]
                
                # If there's a significant phase differential or tension passing through it
                if is_void_state:
                    # In a vacuum, if it's adjacent to the void, it's the conduit
                    # We estimate the void is at the end (temporally forward)
                    operator_n.catalyst_potential += 1.0
                    operator_nodes.add(operator_n)
                else:
                    operator_n.catalyst_potential += 1.0
                    operator_nodes.add(operator_n)

        # 4. Wave Field Operations (Decoupled from Catalysts)
        if is_void_state:
            # 1. First, check if there is a known Hot Spectron (Curiosity node). It naturally absorbs the vacuum.
            void_target = None
            for n in neurons:
                if self.determine_spectron_type(n) == "hot":
                    void_target = n
                    break
                    
            # 2. If no Hot Spectron exists, the vacuum propagates forward in time.
            if not void_target:
                void_target = min(reversed(neurons), key=lambda n: getattr(n, "cold_potential", 0.0))
                
            print(f"[WAVE ENGINE] Wave Trough opened Epistemic Vacuum on: '{void_target.text}'")
            operations.append({"action": "void", "target": void_target.id})
            
            # Phase Drift (Gradient Descent on Tension)
            for n in neurons:
                if n != void_target and n not in operator_nodes:
                    n.phase += 0.1 * (math.pi - n.phase)
                    if hasattr(n, "hot_potential"):
                        n.hot_potential += 1.0
        else:
            # Constructive Interference -> Resonant Triad Forging
            # The entire wave resonates, linking all nodes with gravity decaying by temporal distance.
            for i in range(len(neurons)):
                for j in range(i + 1, len(neurons)):
                    left_n, right_n = neurons[i], neurons[j]
                    distance = j - i
                    weight = 10.0 / distance  # Adjacent = 10.0, Skip-1 = 5.0
                    
                    print(f"[WAVE ENGINE] Forging Resonant Bond (d={distance}): '{left_n.text}' -> '{right_n.text}'")
                    left_n.synapses[right_n.id] = left_n.synapses.get(right_n.id, 0.0) + weight
                    left_n.tier_z = max(left_n.tier_z, 3)
                    right_n.tier_z = max(right_n.tier_z, 3)
                    
                    if distance == 1:
                        operations.append({"action": "forge", "source": left_n.id, "target": right_n.id})
                    
                    if left_n not in operator_nodes:
                        left_n.phase -= 0.1 * left_n.phase
                        left_n.cold_potential += (1.0 / distance)
                    if right_n not in operator_nodes:
                        right_n.phase -= 0.1 * right_n.phase
                        right_n.cold_potential += (1.0 / distance)
            
        # 4. Topological Collapse (Geometric Logic)
        self._topological_collapse_check(speaker_neuron.id)
        
        return {"status": "success", "state": state, "average_phase": avg_phase, "operations": operations}

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
        primary = nids[0]
        
        for secondary in nids[1:]:
            sec_node = self.substrate.neurons[secondary]
            
            if primary == current_speaker_id or secondary == current_speaker_id:
                mirror_candidate = sec_node if primary == current_speaker_id else self.substrate.neurons[primary]
                
                if not hasattr(mirror_candidate, "collapsed_with_speakers"):
                    mirror_candidate.collapsed_with_speakers = set()
                    
                mirror_candidate.collapsed_with_speakers.add(current_speaker_id)
                
                if len(mirror_candidate.collapsed_with_speakers) > 1:
                    if hasattr(mirror_candidate, "mirror_potential"):
                        mirror_candidate.mirror_potential += 5.0
                    print(f"[WAVE ENGINE] '{mirror_candidate.text}' has emerged as a Mirror Spectron!")
                    continue
            
            primary_node = self.substrate.neurons[primary]
            for nid, n in self.substrate.neurons.items():
                if secondary in n.synapses:
                    w = n.synapses.pop(secondary)
                    n.synapses[primary] = w
            
            del self.substrate.neurons[secondary]
            print(f"[WAVE ENGINE] Topological Collapse: '{sec_node.text}' merged into '{primary_node.text}'")

    def run_inner_voice_rumination(self, memories: List[str]):
        """
        The continuous autonomous loop. Replays structural paths.
        Since it injects the exact same waves, it triggers Wave-Hebbian strengthening without a user.
        """
        print("[HEARTBEAT] Inner Voice Rumination started...")
        for memory in memories:
            self.parse_simultaneous_wave(memory, speaker_id="fella")
            
    def get_brain_state(self):
        hot_nodes = sum(1 for n in self.substrate.neurons.values() if self.determine_spectron_type(n) == "hot")
        catalyst_nodes = sum(1 for n in self.substrate.neurons.values() if self.determine_spectron_type(n) == "catalyst")
        mirror_nodes = sum(1 for n in self.substrate.neurons.values() if self.determine_spectron_type(n) == "mirror")
        
        return {
            "total_neurons": len(self.substrate.neurons),
            "hot_spectrons": hot_nodes,
            "catalysts": catalyst_nodes,
            "mirrors": mirror_nodes
        }
