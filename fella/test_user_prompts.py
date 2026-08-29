import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.fella_brain import FellaBrain

brain = FellaBrain.load_state('fella_checkpoint.json')

test_queries = [
    'where is the moon ?',
    'when do star glow ?',
    'what is a black hole ?',
    'who is a friend ?',
    'what is fire ?',
    'what is volcano ?'
]

print("=== VERIFYING EXACT USER QUERIES ===")
for q in test_queries:
    res = brain.converse(q)
    print(f"User  > {q}")
    print(f"FELLA > {res['last_response']}\n")
