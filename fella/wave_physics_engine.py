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
            getattr(n, "hot_potential", 0.0) = 0.0
            getattr(n, "cold_potential", 0.0) = 0.0
            getattr(n, "catalyst_potential", 0.0) = 0.0
            getattr(n, "mirror_potential", 0.0) = 0.0
            
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
        # We calculate the effective interference intensity I
        # For simplicity in this discrete step: 
        # Hot spectrons (phase near PI) cause destructive interference (I -> 0)
        # Cold spectrons (phase near 0) cause constructive interference (I -> high)
        
        # The sentence is "hot" (vacuum) if there is significant destructive interference
        # i.e., average phase shift is closer to PI than 0.
        avg_phase = sum(n.phase for n in neurons) / len(neurons)
        
        # Artificial sensory injection (environmental ground truth)
        if sensory_target_vacuum:
            avg_phase = math.pi # Force destructive interference environment
            
        is_void_state = avg_phase > (math.pi / 2.0)
        
        print(f"[WAVE ENGINE] Sentence Average Phase: {avg_phase:.2f} rad")
        state = "DESTRUCTIVE (VOID)" if is_void_state else "CONSTRUCTIVE (FORGE)"
        print(f"[WAVE ENGINE] Interference State: {state}")
        
        operations = []
        
        # 3. Structural Processing
        # Identify words behaving as catalysts (Phase-Lockers)
        catalyst_indices = [i for i, n in enumerate(neurons) if self.determine_spectron_type(n) == "catalyst"]
        
        if not catalyst_indices and len(neurons) >= 3:
            # Bootstrap catalyst finding: the structural center of a small sentence
            catalyst_indices = [1]
            
        for idx in catalyst_indices:
            if idx == 0 or idx == len(neurons) - 1:
                continue
                
            operator_n = neurons[idx]
            left_n = neurons[idx - 1]
            right_n = neurons[idx + 1]
            
            if is_void_state:
                # Destructive Interference -> Open a Void
                # The node with phase closer to 0 is the mass; the one closer to PI is the void trigger
                void_target = right_n if left_n.phase > right_n.phase else left_n
                print(f"[WAVE ENGINE] Wave Trough opened Epistemic Vacuum on: '{void_target.text}'")
                operations.append({"action": "void", "target": void_target.id})
                
                # LEARNING: Phase Drift (Gradient Descent on Tension)
                # Environment demands a void (PI). Nodes driving this shift towards PI.
                for n in neurons:
                    if n != operator_n and n != void_target:
                        # Drift phase towards PI
                        n.phase += 0.1 * (math.pi - n.phase)
                        getattr(n, "hot_potential", 0.0) += 1.0
                        
            else:
                # Constructive Interference -> Wave-Hebbian Forge
                print(f"[WAVE ENGINE] Forging Tier 3 Standing Wave: '{left_n.text}' -> '{right_n.text}'")
                # Increase conductance (C_ij)
                left_n.synapses[right_n.id] = left_n.synapses.get(right_n.id, 0.0) + 10.0
                left_n.tier_z = max(left_n.tier_z, 3)
                right_n.tier_z = max(right_n.tier_z, 3)
                operations.append({"action": "forge", "source": left_n.id, "target": right_n.id})
                
                # LEARNING: Reinforce mass (Phase towards 0)
                left_n.phase -= 0.1 * left_n.phase
                right_n.phase -= 0.1 * right_n.phase
                left_getattr(n, "cold_potential", 0.0) += 1.0
                right_getattr(n, "cold_potential", 0.0) += 1.0
                
            # LEARNING: Reinforce catalyst potential for the operator
            operator_getattr(n, "catalyst_potential", 0.0) += 1.0
            
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
            
            # Check if this is an Identity/Pronoun Collapse
            if primary == current_speaker_id or secondary == current_speaker_id:
                mirror_candidate = sec_node if primary == current_speaker_id else self.substrate.neurons[primary]
                
                mirror_candidate.collapsed_with_speakers.add(current_speaker_id)
                
                if len(mirror_candidate.collapsed_with_speakers) > 1:
                    # Collapsed with multiple distinct speakers! Mutate into Mirror Spectron.
                    mirror_candidate.mirror_potential += 5.0
                    print(f"[WAVE ENGINE] '{mirror_candidate.text}' has emerged as a Mirror Spectron!")
                    continue
            
            # Standard Topological Merge
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
