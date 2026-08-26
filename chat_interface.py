"""
ENN 4D — Pure Emergent Chat Interface
Connects the mathematical text encoder, continuous 4D physics engine, and associative decoder.
No hardcoded rules, templates, or artificial heuristics.
"""

import os
import sys
import json
import numpy as np
from typing import Optional

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from enn4d import ENN4D
from text_encoder import TextEncoder
from text_decoder import TextDecoder


class ENN4DChat:
    """
    Pure emergent conversational interface for ENN 4D.
    Relies entirely on 4D continuous field dynamics (Resonance, Wave Interference,
    Kinetic Momentum, and Spatial Clustering) to encode, learn, and decode memories.
    """

    def __init__(
        self, 
        universe_path: str = "universe.json", 
        memory_path: str = "memory_log.json",
        dim: int = 4
    ):
        self.universe_path = universe_path
        self.memory_path = memory_path
        self.dim = dim
        
        self.system = ENN4D(dim=dim)
        self.encoder = TextEncoder(dim=dim)
        self.decoder = TextDecoder()
        
        self.load_state()

    def load_state(self):
        """Loads existing universe and associative memory log."""
        if os.path.exists(self.universe_path):
            try:
                self.system.load(self.universe_path)
            except Exception as e:
                print(f"[Warning] Could not load {self.universe_path}: {e}")
                
        if os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, 'r', encoding='utf-8') as f:
                    memories = json.load(f)
                    for m in memories:
                        m['x'] = np.array(m['x'], dtype=float)
                        m['y'] = np.array(m['y'], dtype=float)
                        m['z'] = np.array(m['z'], dtype=float)
                    self.encoder.set_memory_log(memories)
                    self.decoder.set_memory_log(memories)
                    print(f"Memory log loaded ({len(memories)} memories).")
            except Exception as e:
                print(f"[Warning] Could not load {self.memory_path}: {e}")

    def save_state(self):
        """Persists the universe state and memory log."""
        self.system.save(self.universe_path)
        
        serializable_memories = []
        for m in self.encoder.get_memory_log():
            serializable_memories.append({
                'text': m['text'],
                'x': np.round(m['x'], 4).tolist(),
                'y': np.round(m['y'], 4).tolist(),
                'z': np.round(m['z'], 4).tolist(),
                'step': int(m.get('step', 0))
            })
            
        with open(self.memory_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_memories, f, indent=2)

    def send(self, user_input: str) -> str:
        """
        Executes one full sensory-physical-generative cycle:
        1. Encodes raw text into a 4D sensory vector
        2. Steps the 4D physics engine (Resonance -> Interference -> Amplification -> Homeostasis -> Phase Transitions)
        3. Decodes the resulting field interference Y vector via geometric associative recall
        4. Auto-saves universe state
        """
        if not user_input.strip():
            return "Please enter a message."
            
        # 1. Sensory Encoding
        event = self.encoder.encode_text_to_4d(user_input, temporal_step=self.system.event_count + 1)
        self.decoder.set_memory_log(self.encoder.get_memory_log())
        
        # 2. Physics Step
        output_y = self.system.step(event['x'], event['y'], event['z'])
        
        # 3. Associative Field Decoding
        response = self.decoder.decode_4d_to_text(
            y_vector=output_y,
            memory_log=self.encoder.get_memory_log()
        )
        
        # 4. Persist
        self.save_state()
        return response

    def run_interactive_loop(self):
        """Starts the interactive terminal chat loop."""
        print("=" * 65)
        print("ENN 4D LIVING AI CHAT INTERFACE (Pure Emergent Field)")
        print("=" * 65)
        print(f"Universe: {len(self.system.neurons)} neurons | {len(set(n.w for n in self.system.neurons))} families.")
        print("Type your message. Type 'exit' or 'quit' to close.\n")

        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ["exit", "quit", "q"]:
                    print("\nSaving living universe state and shutting down...")
                    self.save_state()
                    print("Goodbye!")
                    break
                    
                response = self.send(user_input)
                print(f"System: {response}\n")
                
            except (KeyboardInterrupt, EOFError):
                print("\n\nSession terminated. State saved.")
                self.save_state()
                break


if __name__ == "__main__":
    chat_app = ENN4DChat()
    chat_app.run_interactive_loop()