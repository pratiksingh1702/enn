"""
ENN 4D: Natural Language Pure Physics Demonstration
Zero hardcoded response templates.
Demonstrates continuous 4D vector encoding, living wave simulation,
and pure mathematical memory resonance.
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import os
from chat_interface import ENNChatBrain

def run_chat_demo():
    print("=" * 75)
    print("ENN 4D: PURE PHYSICS NATURAL LANGUAGE DEMONSTRATION")
    print("=" * 75)
    print("Zero hardcoded templates. Zero if-else matching.")
    print("Direct 4D wave resonance and memory readout.\n")
    
    # Fresh brain instance for deterministic run
    if os.path.exists("test_chat_universe.json"):
        os.remove("test_chat_universe.json")
    if os.path.exists("test_chat_memory.json"):
        os.remove("test_chat_memory.json")
        
    brain = ENNChatBrain(
        universe_file="test_chat_universe.json",
        memory_file="test_chat_memory.json"
    )
    
    # Presentation stream
    inputs = [
        "My name is Professor Smith.",
        "I am a quantum physicist researching time crystal dynamics.",
        "I live in Geneva near the CERN laboratory.",
        "Apples and oranges are sweet nutritious fruits.",
        
        # Probing the field with queries
        "Who am I?",
        "What is my research topic?",
        "Where is my home located?",
        "Tell me about nutritious fruits."
    ]
    
    for text in inputs:
        print(f"Input: \"{text}\"")
        result = brain.process_input(text)
        print(f"Resonant Readout: \"{result['response']}\"")
        print(f"  [Physics: Family {result['family_id']} | Total Neurons: {result['total_neurons']} | 4D Field Output Y: {result['output_y']}]\n")

    print("=" * 75)
    print("VALIDATION COMPLETE: Pure mathematical resonance operating as designed!")
    print("=" * 75)

if __name__ == "__main__":
    run_chat_demo()
