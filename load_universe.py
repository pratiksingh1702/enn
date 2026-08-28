"""
ENN Universe State Loader & Inspector
====================================
Loads any saved universe checkpoint file, inspects all neurons, synapses,
and architectural hyper-cells, and reports the exact status.
"""

import json
import os
import sys

DEFAULT_CHECKPOINT = "c:/Users/Dell/Downloads/enn/universe_master_checkpoint.json"

def inspect_and_load_universe(checkpoint_path: str = DEFAULT_CHECKPOINT):
    sys.stdout.reconfigure(encoding='utf-8')
    if not os.path.exists(checkpoint_path):
        print(f"Checkpoint file not found: {checkpoint_path}")
        return

    print("=" * 80)
    print(f"📂 LOADING UNIVERSE CHECKPOINT: {checkpoint_path}")
    print("=" * 80)
    
    with open(checkpoint_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sim_time = data.get("sim_time", 0.0)
    hours = sim_time / 3600.0
    cells = data.get("cells", [])
    weather = data.get("weather", "clear")
    
    print(f"• Civilization Lifespan:  {sim_time:.1f} seconds ({hours:.2f} continuous hours)")
    print(f"• Total Hyper-Cells:      {len(cells)} active physical matter & energy cells")
    print(f"• Environmental Weather:  {weather.upper()}")
    
    # Census
    census = {}
    for c in cells:
        census[c["type"]] = census.get(c["type"], 0) + 1
    print("\n🏛️ ARCHITECTURAL STRUCTURES IN SAVED STATE:")
    for t, count in census.items():
        print(f"  • {t.upper():<20}: {count:>4} cells")

    # Neural networks
    full_orgs = data.get("full_organisms", [])
    if full_orgs:
        print("\n🧠 PRESERVED ENN 4D NEURAL NETWORKS:")
        for org in full_orgs:
            brain = org.get("neural_brain", {})
            wf = brain.get("world_field", {})
            neurons = wf.get("neurons", [])
            synapses_cnt = sum(len(n.get("synapses", {})) for n in neurons)
            print(f"  🚶‍♂️ Organism {org.get('agent_id', 'Unknown').upper()}:")
            print(f"    - Position:       {org.get('pos')}")
            print(f"    - Energy Budget:  {org.get('energy_budget', 0):.1f}")
            print(f"    - Morphed Powers: {org.get('morphed_powers', [])}")
            print(f"    - 4D Neurons:     {len(neurons)} active Concept & Insight Neurons (Serialized with 4D coordinates x, y, z, t)")
            print(f"    - Active Synapses:{synapses_cnt} physical conductance bridges W_ij")
    else:
        print("\n(Legacy organism format saved - full body kinematics and stats preserved)")

    print("=" * 80)
    print("✅ TO RUN THIS WORLD: Run 'python live_universe_daemon.py' and open http://127.0.0.1:8765")
    print("=" * 80)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CHECKPOINT
    inspect_and_load_universe(path)
