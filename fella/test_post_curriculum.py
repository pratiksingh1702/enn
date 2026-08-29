import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.fella_brain import FellaBrain

brain = FellaBrain.load_state('fella_checkpoint.json')

test_queries = [
    "What is a supernova?",
    "What is plate tectonics?",
    "What is the water cycle?",
    "What is photosynthesis?",
    "What is kinetic energy?",
    "What is an atom?",
    "What is empathy?",
    "What is curiosity?"
]

print("=== 2ND VERIFICATION PASS (AFTER 200-QUESTION REINFORCEMENT & DEVELOPMENT) ===\n")
for q in test_queries:
    res = brain.converse(q)
    print(f"User  > {q}")
    print(f"FELLA [{res['active_trait']}] > {res['last_response']}\n")
