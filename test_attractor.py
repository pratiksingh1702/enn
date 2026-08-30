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
    
    print("\n[TEACHING VOCABULARY]")
    facts = [
        "Pratik is a human.",
        "An apple is an object.",
        "Water is a liquid."
    ]
    for f in facts:
        print(f"Teaching: {f}")
        brain.converse(f)
        
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
