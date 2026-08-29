import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.fella_brain import FellaBrain

brain = FellaBrain.load_state('fella_checkpoint.json')

test_inputs = [
    'speed is the rate of change of direction',
    'what is the sun ?',
    'gravity attracts physical matter toward the earth',
    'what is gravity ?',
    'plants grow by absorbing sunlight through photosynthesis',
    'how do plants grow ?',
    'the radiating sun is the'
]

print("=== FELLA 100% RAW SYNAPTIC RESPONSES (ZERO HARCODED STRINGS) ===\n")
for inp in test_inputs:
    res = brain.converse(inp)
    trait = res.get("active_trait", "INQUIRE")
    friction = res.get("epistemic_friction", 0.0)
    print(f"User  > {inp}")
    print(f"FELLA [{trait} | Tension={friction:.2f}] > {res['last_response']}\n")
