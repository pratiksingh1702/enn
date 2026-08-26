"""
ENN 4D Phase 2 Automated Demonstration Script
Demonstrates Text Encoding, 4D Field Resonance, Memory Formation, and Decoding.
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from chat_interface import ENN4DChat


def run_phase2_demo():
    print("=" * 65)
    print("ENN 4D LIVING AI - SENSORY & GENERATIVE DEMONSTRATION")
    print("=" * 65)
    
    # Initialize chat engine
    chat = ENN4DChat(universe_path="universe.json", memory_path="memory_log.json")
    
    dialogue = [
        "My name is Professor Smith.",
        "Who am I?",
        "I am a scientist.",
        "What do you know about me?",
        "I like cats.",
        "What animals do I like?"
    ]
    
    for turn in dialogue:
        print(f"\nYou: {turn}")
        
        # Calculate diagnostics before/after step
        event = chat.encoder.extract_semantic_embedding(turn)
        fam = chat.encoder.assign_family(turn, event)
        pre_neurons = len(chat.system.neurons)
        
        response = chat.send(turn)
        post_neurons = len(chat.system.neurons)
        
        # Output system answer
        print(f"System: {response}")
        print(f"  [Diagnostics] Family: {fam} | Neurons: {post_neurons} (Delta: {post_neurons - pre_neurons:+d}) | Total Energy: {sum(n.energy for n in chat.system.neurons):.2f}")

    print("\n" + "=" * 65)
    print("Demonstration completed successfully! Universe and memory saved.")
    print("=" * 65)


if __name__ == "__main__":
    run_phase2_demo()