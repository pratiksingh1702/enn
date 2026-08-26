"""
ENN 4D — Pure Emergent Learning & Recall Demonstration
Demonstrates continuous field encoding, physical resonance, and associative decoding
without any hardcoded templates or keyword rules.
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from chat_interface import ENN4DChat


def run_pure_emergent_demo():
    print("=" * 70)
    print("ENN 4D LIVING AI — PURE EMERGENT LEARNING & ASSOCIATIVE RECALL")
    print("=" * 70)
    
    # Initialize fresh or existing chat engine
    chat = ENN4DChat(universe_path="universe.json", memory_path="memory_log.json")
    
    statements = [
        "My name is Professor Smith.",
        "I am a scientist studying quantum biology.",
        "I like cats and astrophysics."
    ]
    
    print("\n--- PHASE 1: SENSORY ENCODING & FIELD LEARNING ---")
    for stmt in statements:
        print(f"\n[Input Event]: '{stmt}'")
        pre_neurons = len(chat.system.neurons)
        response = chat.send(stmt)
        post_neurons = len(chat.system.neurons)
        
        # Calculate active field resonance
        event_vec = chat.encoder.extract_vector(stmt)
        forces = chat.system.compute_resonance(event_vec, event_vec, np.array([0.1]))
        max_f = max(forces) if forces else 0.0
        
        print(f"  Field Output: {response}")
        print(f"  [Physics] Max Resonance Force: {max_f:.4f} | Total Neurons: {post_neurons} (Delta: {post_neurons - pre_neurons:+d})")

    queries = [
        "Who am I?",
        "What is my profession?",
        "What animals or subjects do I like?",
        "Tell me about quantum biology."
    ]
    
    print("\n\n--- PHASE 2: RESONANCE QUERY & ASSOCIATIVE RECALL ---")
    for q in queries:
        print(f"\n[Query Input]: '{q}'")
        
        # Encode query to 4D coordinate
        q_vec = chat.encoder.extract_vector(q)
        forces = chat.system.compute_resonance(q_vec, q_vec, np.array([0.1]))
        max_f = max(forces) if forces else 0.0
        
        # Step through living field interference
        response = chat.send(q)
        
        print(f"  Living Field Response: {response}")
        print(f"  [Resonance] Field Force: {max_f:.4f} | Universe Energy: {sum(n.energy for n in chat.system.neurons):.2f}")

    print("\n" + "=" * 70)
    print("Demonstration completed! Living universe state saved.")
    print("=" * 70)


if __name__ == "__main__":
    import numpy as np
    run_pure_emergent_demo()