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
from text_encoder import TextEncoder

class ENNChatBrain:
    def __init__(self, universe_file: str = "universe.json", dim: int = 4):
        self.universe_file = universe_file
        self.dim = dim
        
        self.system = ENN4D(dim=self.dim)
        self.encoder = TextEncoder(dim=self.dim)
        
        self.step_counter = 0
        self.load_state()

    def load_state(self):
        """Load living universe state from disk."""
        if os.path.exists(self.universe_file):
            try:
                self.system.load(self.universe_file)
            except Exception:
                pass
        self.step_counter = self.system.event_count

    def save_state(self):
        """Persist living universe state to disk."""
        self.system.save(self.universe_file)

    def is_probe_query(self, text: str) -> bool:
        """Check if user input is probing memory (query) vs presenting new knowledge."""
        t = text.strip().lower()
        if t.endswith('?'):
            return True
        first_word = t.split()[0] if t.split() else ""
        return first_word in {"who", "what", "where", "when", "why", "how", "tell", "explain", "recall", "do"}

    def learn(self, text: str) -> Dict[str, Any]:
        """Step the physical universe with new knowledge, birthing or amplifying living particles."""
        self.step_counter += 1
        time_coord = (self.step_counter * 0.05) % 1.0
        
        event = self.encoder.encode(text, time_step=time_coord)
        event_x, event_y, event_z = event["x"], event["y"], event["z"]
        features = event.get("features")
        
        neurons_before = len(self.system.neurons)
        output_y = self.system.step(event_x, event_y, event_z, text=text, features=features)
        neurons_after = len(self.system.neurons)
        new_neurons = neurons_after - neurons_before
        
        forces = self.system.compute_resonance(event_x, event_y, event_z)
        family_id = int(np.argmax(forces)) if forces else 0
        
        self.save_state()
        
        return {
            "mode": "learn",
            "text": text,
            "family_id": family_id,
            "new_neurons": new_neurons,
            "total_neurons": neurons_after,
            "response": f"Learned & integrated into Family {family_id} (Total: {neurons_after} neurons)."
        }

    def query(self, text: str) -> Dict[str, Any]:
        """Send a non-destructive probe wave into the field to find the most physically active resonant neuron."""
        event = self.encoder.encode(text, time_step=0.0)
        query_x = event["x"]
        features = event.get("features")
        
        # Probe physical resonance across living particles
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
    """Run pure physical terminal chat with ENN 4D."""
    brain = ENNChatBrain()
    
    print("=" * 70)
    print("🧠 ENN 4D LIVING SYSTEM: PURE PHYSICS NATURAL LANGUAGE INTERFACE")
    print("=" * 70)
    print(f"Universe Loaded: {len(brain.system.neurons)} neurons across {len(set(n.w for n in brain.system.neurons))} families.")
    print("No hardcoded templates. Everything emerges from 4D wave resonance.")
    print("Type your message below. Type 'exit' or 'quit' to end session.\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("\nSaving living universe state... Goodbye!")
                brain.save_state()
                break
                
            result = brain.process_input(user_input)
            if result.get("mode") == "query":
                print(f"System (Resonant Memory): \"{result['response']}\"")
                print(f"  [Physics: Probed Family {result['family_id']} | Energy: {result['energy']:.2f}]\n")
            else:
                print(f"System: {result['response']}")
                print(f"  [Physics: Family {result['family_id']} | Total Neurons: {result['total_neurons']}]\n")
            
        except (KeyboardInterrupt, EOFError):
            print("\nSession ended. Universe saved.")
            brain.save_state()
            break

if __name__ == "__main__":
    run_interactive_chat()