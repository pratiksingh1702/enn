"""
Inspect physical neurons created during the 2D Grid World test.
"""
import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import numpy as np
from test_2d_simulation import PureGridWorldSimulationSuite

suite = PureGridWorldSimulationSuite()
suite.run_simulation(max_steps=120)

print("\n" + "=" * 80)
print("🧬 PHYSICAL NEURONS CREATED IN THE LIVING UNIVERSE DURING 2D TEST")
print("=" * 80)
print(f"Total Neurons in Substrate: {len(suite.dual_system.neurons)}")
print(f"Total Semantic Families: {len(set(n.w for n in suite.dual_system.neurons))}")
print("-" * 80)

for i, n in enumerate(suite.dual_system.neurons):
    origin_label = "Internal Thought (Self)" if n.origin < 0.5 else "Environmental Perception"
    syn_summary = ", ".join([f"#{target}:{w:.2f}" for target, w in list(n.synapses.items())[:4]])
    if len(n.synapses) > 4:
        syn_summary += f", ... (+{len(n.synapses)-4} more)"
        
    print(f"Neuron #{i:02d} | Family: {n.w:02d} | Energy: {n.energy:.3f} | Role: {n.role:7s} | {origin_label}")
    print(f"  📝 Concept: \"{n.text}\"")
    print(f"  📍 4D Position (X): {np.round(n.x, 3).tolist()}")
    print(f"  ⚡ Synaptic Bridges: [{syn_summary if syn_summary else 'No active synapses'}]")
    print("-" * 80)
