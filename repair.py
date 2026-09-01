import json
import math
from fella.fella_brain import FellaBrain

print("[1] Waking Fella to repair corruption...")
fella = FellaBrain.load_state("fella_checkpoint.json")

print("[2] Automatically inferring catalysts from network topology...")
# Any node with massive branching factor is a catalyst. 
for nid, n in fella.substrate.neurons.items():
    if len(n.synapses) > 5:
        n.catalyst_potential = 100.0
        print(f"  -> Emergent Catalyst Found: '{n.text}' (Branching Factor: {len(n.synapses)})")

# Ensure hot spectrons are active
hot_words = ["?", "what", "where", "who", "why", "how"]
for word in hot_words:
    node = fella.wave_engine._get_or_create_neuron(word)
    node.phase = math.pi
    node.hot_potential = 100.0

fella.save_brain("fella_checkpoint.json")
print("[3] Brain Repaired.")
