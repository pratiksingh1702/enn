"""
ENN 4D Interactive Chat Interface (Brain-Body Integration)
Combines the TextEncoder, TextDecoder, and ENN4D Physics Engine into a conversational agent.
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
    High-level conversational interface for ENN 4D.
    Handles encoding sensory input, running field physics, decoding generative recall,
    and persisting memory logs and universe state.
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
        
        # Core components
        self.system = ENN4D(dim=dim)
        self.encoder = TextEncoder(dim=dim)
        self.decoder = TextDecoder()
        
        # Load existing universe & memory if available
        self.load_state()

    def load_state(self):
        """Loads existing universe and memory log."""
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
                        m['x'] = np.array(m['x'])
                        m['y'] = np.array(m['y'])
                        m['z'] = np.array(m['z'])
                    self.encoder.set_memory_log(memories)
                    self.decoder.set_memory_log(memories)
                    print(f"Memory log loaded ({len(memories)} memories).")
            except Exception as e:
                print(f"[Warning] Could not load {self.memory_path}: {e}")

    def save_state(self):
        """Persists the universe state and memory log."""
        self.system.save(self.universe_path)
        
        # Serialize memories
        serializable_memories = []
        for m in self.encoder.get_memory_log():
            serializable_memories.append({
                'text': m['text'],
                'x': np.round(m['x'], 4).tolist(),
                'y': np.round(m['y'], 4).tolist(),
                'z': np.round(m['z'], 4).tolist(),
                'w': int(m['w']),
                'is_query': bool(m.get('is_query', False)),
                'step': int(m.get('step', 0))
            })
            
        with open(self.memory_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_memories, f, indent=2)

    def send(self, user_input: str) -> str:
        """
        Processes a single conversational turn:
        1. Encodes text into 4D sensory event
        2. Steps the 4D physics engine (Resonance -> Interference -> Amplification -> Homeostasis -> Phase Transitions)
        3. Decodes output Y into response
        4. Auto-saves state
        """
        if not user_input.strip():
            return "Please enter a message."
            
        # 1. Sensory Encoding
        event = self.encoder.encode_text_to_4d(user_input, temporal_step=self.system.event_count + 1)
        self.decoder.set_memory_log(self.encoder.get_memory_log())
        
        # 2. Physics Step
        output_y = self.system.step(event['x'], event['y'], event['z'])
        
        # 3. Compute Resonance diagnostics
        forces = self.system.compute_resonance(event['x'], event['y'], event['z'])
        max_force = max(forces) if forces else 0.0
        
        # 4. Generative Decoding
        response = self.decoder.decode_4d_to_text(
            y_vector=output_y,
            query_text=user_input,
            memory_log=self.encoder.get_memory_log(),
            resonance_force=max_force
        )
        
        # 5. Persist
        self.save_state()
        return response

    def run_interactive_loop(self):
        """Starts interactive terminal chat loop."""
        print("=" * 65)
        print("ENN 4D LIVING AI CHAT INTERFACE (Phase 2)")
        print("=" * 65)
        print(f"Loaded Universe with {len(self.system.neurons)} neurons across {len(set(n.w for n in self.system.neurons))} families.")
        print("Type your message below. Type 'exit' or 'quit' to close.\n")

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