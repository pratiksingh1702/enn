import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.fella_brain import FellaBrain

brain = FellaBrain.load_state('fella_checkpoint.json')

# 1. Re-evaluate syntactic roles & valences for all neurons
for n in brain.substrate.neurons.values():
    role, val, tier = brain.lang.estimate_syntactic_valence(n.text)
    n.grammatical_role = role
    n.syntax_valence = val

# 2. Prune weak background noise synapses (retain real directional pathways)
pruned = 0
for n in brain.substrate.neurons.values():
    to_delete = [target_id for target_id, w in n.synapses.items() if w < 0.40]
    for tid in to_delete:
        del n.synapses[tid]
        pruned += 1

print(f"✓ Re-calibrated syntactic roles and pruned {pruned} noisy background synapses.")

# 3. Test Thought Generation
queries = [
    "what is the sun ?",
    "what is gravity ?",
    "what is earth ?",
    "speed is the rate of change of direction",
    "volcanoes erupt molten liquid lava from deep within the earth",
    "what is a volcano ?"
]

print("\n=== METACONITIVE PRE-ARTICULATORY SIMULATION OUTPUTS ===\n")
for q in queries:
    res = brain.converse(q)
    print(f"User  > {q}")
    print(f"FELLA [{res['active_trait']}] > {res['last_response']}\n")

brain.save_state('fella_checkpoint.json')
print("💾 Fortified and saved to fella_checkpoint.json")
