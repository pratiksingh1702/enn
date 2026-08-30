import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from fella.fella_brain import FellaBrain

def test_attractor():
    print("=" * 80)
    print("🧪 TESTING 'THINK BEFORE SPEAK' GOAL ATTRACTOR")
    print("=" * 80)
    
    if not os.path.exists("fella_checkpoint.json"):
        print("Error: fella_checkpoint.json not found.")
        return

    brain = FellaBrain.load_state("fella_checkpoint.json")
    print(f"✓ Brain Loaded. Living Neurons: {len(brain.substrate.neurons)}")
    
    print("[TEACHING VOCABULARY]")
    print("Teaching: Oh nice is a reaction.")
    brain.converse("Oh nice is a reaction.")
    print("Teaching: What is a question.")
    brain.converse("What is a question.")
    print("Teaching: More is about curiosity.")
    brain.converse("More is about curiosity.")

    print("Teaching: An apple is an object.")
    brain.converse("An apple is an object.")
    print("Teaching: Water is a liquid.")
    brain.converse("Water is a liquid.")
    
    print("\n[TESTING NOVELTY & EMERGENT CURIOSITY]")
    print("User: 'Pratik is a human.'")
    res = brain.converse("Pratik is a human.")
    print(f"FELLA: '{res['last_response']}'")
    print(f"   -> Inner Critic Logs: {res['last_thought']}")

    print("\n[TESTING ATTRACTOR FIELD PULL]")
    questions = [
        "Who is a human?",
        "What is an object?",
        "What is liquid?"
    ]
    
    for q in questions:
        print(f"\nUser: '{q}'")
        telemetry = brain.converse(q)
        print(f"FELLA: '{telemetry['last_response']}'")
        print(f"   -> Inner Critic Logs: {telemetry['last_thought']}")

if __name__ == "__main__":
    test_attractor()
