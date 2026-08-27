"""
ENN 4D: Living Physical Chat Interface
Zero hardcoded response templates. Zero regexes.
Natural Language operates purely on the 5 Physical Principles of ENN 4D:
- Declarative statements birth & amplify living neuron particles.
- Queries send probe waves across the field to find the most physically resonant neuron.
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import os
import numpy as np
from typing import Dict, Any, List
from enn4d import ENN4D
from text_encoder import TextEncoder, encode_constellation
from text_decoder import TextDecoder
from mind_loop import MindLoop

class ENNChatBrain:
    def __init__(self, universe_file: str = "universe.json", dim: int = 4, auto_start_mind: bool = True, tick_interval: float = 2.0):
        self.universe_file = universe_file
        self.dim = dim
        
        self.system = ENN4D(dim=self.dim)
        self.encoder = TextEncoder(dim=self.dim)
        self.decoder = TextDecoder()
        
        self.spontaneous_thoughts: List[Dict[str, Any]] = []
        self.question_queue: List[Dict[str, Any]] = []
        self.step_counter = 0
        self.load_state()
        
        # Autonomous Living Mind Loop
        self.mind_loop = MindLoop(self.system, self.decoder, tick_interval=tick_interval)
        self.mind_loop.on_thought_callback = self._handle_mind_thought
        if auto_start_mind:
            self.mind_loop.start()

    def _handle_mind_thought(self, thought: Dict[str, Any]):
        self.spontaneous_thoughts.append(thought)
        if thought.get("type") == "epistemic_resolution" or "void" in thought.get("type", ""):
            self.question_queue.append(thought)

    def reset(self):
        """Reset the ENN brain and physical universe to an empty state."""
        with self.mind_loop.get_lock():
            self.system.reset()
            self.decoder.memory_log = []
            self.spontaneous_thoughts = []
            self.question_queue = []
            self.step_counter = 0
            if os.path.exists(self.universe_file):
                try:
                    os.remove(self.universe_file)
                except Exception:
                    pass

    def load_state(self):
        """Load living universe state from disk."""
        if os.path.exists(self.universe_file):
            try:
                self.system.load(self.universe_file)
                # Seed decoder memory bank from loaded neurons
                for n in self.system.neurons:
                    if n.text:
                        self.decoder.record_memory(n.text, n.x, n.y, n.z, n.w, n.age, n.features)
            except Exception:
                pass
        self.step_counter = self.system.event_count

    def save_state(self):
        """Persist living universe state to disk."""
        with self.mind_loop.get_lock():
            self.system.save(self.universe_file)

    def is_probe_query(self, text: str) -> bool:
        """Check if user input is probing memory (query) vs presenting new knowledge."""
        t = text.strip().lower()
        if t.endswith('?'):
            return True
        first_word = t.split()[0] if t.split() else ""
        return first_word in {"who", "what", "where", "when", "why", "how", "tell", "explain", "recall", "do"}

    def learn(self, text: str) -> Dict[str, Any]:
        """Step the physical universe with new knowledge, birthing geometric constellations and checking curiosity vacuums."""
        self.mind_loop.mark_user_activity()
        with self.mind_loop.get_lock():
            self.step_counter += 1
            time_coord = (self.step_counter * 0.05) % 1.0
            
            # Decompose into relational micro-circuit constellation
            nodes = self.encoder.encode_constellation(text, time_step=time_coord, origin=1.0)
            
            neurons_before = len(self.system.neurons)
            output_y, void_event = self.system.step_constellation(nodes, text=text)
            neurons_after = len(self.system.neurons)
            new_neurons = neurons_after - neurons_before
            
            # Record in memory bank
            anchor = nodes[0]
            self.decoder.record_memory(text, anchor["x"], anchor.get("y", anchor["x"]), anchor.get("z", np.array([0.0])), anchor.get("w", 0), self.step_counter, anchor.get("features"))
            
            forces = self.system.compute_resonance(anchor["x"], anchor.get("y", anchor["x"]), anchor.get("z", np.array([0.0])))
            family_id = int(np.argmax(forces)) if forces else 0
            
            curiosity_prompt = None
            if void_event:
                curiosity_prompt = self.decoder.decode_curiosity_void(void_event)
                self.question_queue.append({
                    "type": "curiosity_void",
                    "text": text,
                    "prompt": curiosity_prompt,
                    "tension": void_event["tension"]
                })
            
            self.save_state()
            
            return {
                "mode": "learn",
                "text": text,
                "family_id": family_id,
                "new_neurons": new_neurons,
                "total_neurons": neurons_after,
                "curiosity": curiosity_prompt,
                "response": f"Integrated constellation ({new_neurons} nodes) into Family {family_id}."
            }

    def query(self, text: str) -> Dict[str, Any]:
        """Send a non-destructive probe wave into the field to find the most physically active resonant neuron."""
        self.mind_loop.mark_user_activity()
        with self.mind_loop.get_lock():
            event = self.encoder.encode(text, time_step=0.0, origin=1.0)
            query_x = event["x"]
            features = event.get("features")
            
            matches = self.system.probe_resonance(query_x, query_features=features, top_k=3)
            
            if matches:
                top_neuron, activation = matches[0]
                response_text = top_neuron.text
                family_id = top_neuron.w
                energy = top_neuron.energy
            else:
                response_text = "No active neuron is resonating in memory."
                family_id = 0
                energy = 0.0
                
            return {
                "mode": "query",
                "text": text,
                "response": response_text,
                "family_id": family_id,
                "energy": energy,
                "total_neurons": len(self.system.neurons)
            }

    def process_input(self, user_text: str) -> Dict[str, Any]:
        """Process user input through living 4D physics."""
        if self.is_probe_query(user_text):
            return self.query(user_text)
        else:
            return self.learn(user_text)


def run_interactive_chat():
    """Run pure physical terminal chat with ENN 4D living traits & autonomous mind loop."""
    brain = ENNChatBrain()
    
    # Callback to display autonomous reflections in the background
    def on_thought(thought: Dict[str, Any]):
        msg = thought.get("decoded_text", thought.get("message", ""))
        print(f"\n✨ [ENN Mind Rumination]: {msg}")
        print("You: ", end="", flush=True)
        
    brain.mind_loop.on_thought_callback = on_thought
    brain.mind_loop.start()
    
    print("=" * 75)
    print("🧠 ENN 4D LIVING SYSTEM: AUTONOMOUS PHYSICAL CONSCIOUSNESS & CURIOSITY")
    print("=" * 75)
    print(f"Universe Loaded: {len(brain.system.neurons)} neurons across {len(set(n.w for n in brain.system.neurons))} families.")
    print("Traits Active: Epistemic Curiosity Vacuum | Relational Constellations | Autonomous Reflection")
    print("Type your message below. Pause to let the system ruminate autonomously. Type 'exit' to quit.\n")
    
    try:
        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("\nSaving living universe state... Goodbye!")
                brain.mind_loop.stop()
                brain.save_state()
                break
                
            result = brain.process_input(user_input)
            if result.get("mode") == "query":
                print(f"System (Resonant Memory): \"{result['response']}\"")
                print(f"  [Physics: Probed Family {result['family_id']} | Energy: {result['energy']:.2f}]\n")
            else:
                print(f"System: {result['response']}")
                if result.get("curiosity"):
                    print(f"  🔍 [Curiosity Vacuum Triggered]: \"{result['curiosity']}\"")
                print(f"  [Physics: Family {result['family_id']} | Total Universe: {result['total_neurons']} neurons]\n")
                
    except (KeyboardInterrupt, EOFError):
        print("\nSession ended. Universe saved.")
        brain.mind_loop.stop()
        brain.save_state()

if __name__ == "__main__":
    run_interactive_chat()