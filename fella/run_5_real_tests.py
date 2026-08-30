"""
FELLA 5 Real Tests Execution Suite
=================================
Runs the 5 exact user queries on the updated Syntactically Coherent Wave Reconstruction Engine:
1. Direct Recall: 'what is a sun ?'
2. Discrimination: 'what is air ?'
3. Categorical Contrast: 'is sun a gas ?'
4. Curiosity Inquiry: 'what do you want to know ?'
5. Self-Awareness: 'tell me about you'
"""

import os
import sys

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from fella.fella_brain import FellaBrain
from fella.reset_fella import reset_fella_memory


def run_5_real_tests():
    print("=" * 80)
    print("🔬 FELLA 5 REAL TESTS EXECUTION SUITE")
    print("=" * 80)
    
    # Reset state to clean slate
    reset_fella_memory()
    checkpoint_path = "fella_checkpoint.json"
    brain = FellaBrain.load_state(checkpoint_path)
    
    print("\n[TEACHING PHASE: Single-Exposure Teaching (1 pass, no repetition)]")
    
    print("  • Concept 1: 'Sun is not a gas.'")
    brain.converse("Sun is not a gas.")
    
    print("  • Concept 2: 'Sun is a bright star that gives warmth to Earth.'")
    brain.converse("Sun is a bright star that gives warmth to Earth.")
    
    print("  • Concept 3: 'Air is a gas that surrounds Earth.'")
    brain.converse("Air is a gas that surrounds Earth.")

    print("  • Concept 4: 'I want to know about the universe.'")
    brain.converse("I want to know about the universe.")
    
    print("  • Concept 5: 'I am fella. You are fella.'")
    brain.converse("I am fella.")
    brain.converse("You are fella.")
    
    print("\n" + "-" * 80)
    print("EXECUTING 5 REAL TESTS")
    print("-" * 80)
    
    tests = [
        ("Test 1: Direct Recall", "what is a sun ?"),
        ("Test 2: Discrimination", "what is air ?"),
        ("Test 3: Categorical Question", "is sun a gas ?"),
        ("Test 4: Curiosity Inquiry", "what do you want to know ?"),
        ("Test 5: Self-Awareness", "tell me about you")
    ]
    
    for label, query in tests:
        brain.converse(query)
        tel = brain.get_telemetry()
        response = tel["last_response"]
        trait = tel["active_trait"]
        conf = tel["self_confidence"]
        
        print(f"\n{label}")
        print(f"  User > {query}")
        print(f"  FELLA [{trait} | Conf={conf:.2f}] > {response}")

    print("\n" + "=" * 80)
    print("5 REAL TESTS EXECUTION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    run_5_real_tests()
