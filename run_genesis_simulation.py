"""
Genesis 3D Continuous Sandbox Simulation Harness
================================================
Executes 600 steps of dynamic matter manipulation, chasm bridge building,
crystal harvesting, and environmental storm survival.
Exports 'genesis_simulation.json' for Three.js WebGL visualization.
"""

import json
import numpy as np
from genesis_world import GenesisWorld3D
from genesis_organism import GenesisOrganism3D


def run_genesis_simulation(total_steps: int = 600):
    print("=" * 80)
    print("🌌 LAUNCHING GENESIS 3D SELF-AWARE LIVING ORGANISM SIMULATION")
    print("Dynamic Raw Materials | Tool Use & Bridge Building | Storm Survival")
    print("=" * 80)

    world = GenesisWorld3D(size_x=24.0, size_y=24.0, size_z=8.0)
    organism = GenesisOrganism3D()
    organism.reset(start_pos=(3.0, 3.0, 1.2))

    history = []

    print(f"\n[Genesis World Initial State]")
    print(f"  • World Volume: 24m x 24m x 8m")
    print(f"  • Raw Matter: {len(world.dynamic_blocks)} dynamic blocks (Stone slabs, Metal plates, Crystals)")
    print(f"  • The Great Chasm: Dividers at x in [10.0, 14.0]")
    print(f"  • Organism Position: (3.0, 3.0, 1.2) | Energy: 300.0 | Confidence: {organism.system.inward_observer.self_confidence:.2f}")

    print(f"\n[Running Genesis Physical Simulation ({total_steps} steps)]...")

    for step in range(1, total_steps + 1):
        sim_time = step * 0.1
        world.update_environment(step)
        state = organism.step(world, dt=0.1, sim_time=sim_time)

        # Telemetry logging on key events
        if (step <= 10 or step % 25 == 0 or 
            state["outcome"] in ["tractor_picked_stone", "chasm_bridge_constructed", "crystal_energy_harvested", "chasm_fall_recovered"]):
            
            icon = "🌉" if state["outcome"] == "chasm_bridge_constructed" else (
                   "💎" if state["outcome"] == "crystal_energy_harvested" else (
                   "🧲" if state["outcome"] == "tractor_picked_stone" else (
                   "⚡" if state["storm_active"] else "🛸")))
            
            pos_str = f"({state['pos'][0]:.1f}, {state['pos'][1]:.1f}, {state['pos'][2]:.1f})"
            print(f"  [Step {step:03d}] {icon} Pos: {pos_str} | Energy: {state['energy_budget']:.1f} | "
                  f"Bridges: {state['bridges_constructed']} | Crystals: {state['crystals_harvested']} | "
                  f"Storm: {'ACTIVE' if state['storm_active'] else 'Clear'} | Confidence: {state['self_confidence']:.2f} | Action: {state['outcome']}")

        # Record frame for WebGL
        block_snapshots = [
            {
                "id": b.block_id,
                "pos": [float(b.pos[0]), float(b.pos[1]), float(b.pos[2])],
                "type": b.material_type,
                "held": b.held_by_agent
            }
            for b in world.dynamic_blocks
        ]

        history.append({
            "step": step,
            "pos": [float(state["pos"][0]), float(state["pos"][1]), float(state["pos"][2])],
            "velocity": [float(state["velocity"][0]), float(state["velocity"][1]), float(state["velocity"][2])],
            "yaw": float(state["yaw"]),
            "pitch": float(state["pitch"]),
            "outcome": state["outcome"],
            "energy": float(state["energy_budget"]),
            "confidence": float(state["self_confidence"]),
            "friction": float(state["epistemic_friction"]),
            "coherence": float(state["body_world_coherence"]),
            "bridges": state["bridges_constructed"],
            "crystals": state["crystals_harvested"],
            "storm": world.storm_active,
            "storm_intensity": world.storm_intensity,
            "sheltered": state["under_shelter"],
            "blocks": block_snapshots
        })

    # Summary Statistics
    print("\n" + "=" * 80)
    print("📊 GENESIS 3D LIVING ORGANISM SIMULATION RESULTS")
    print("=" * 80)
    print(f"  • Total Steps Simulated:        {total_steps}")
    print(f"  • Chasm Bridges Constructed:    {organism.bridges_constructed}")
    print(f"  • Energy Crystals Harvested:    {organism.crystals_harvested}")
    print(f"  • Chasm Fall Events:            {organism.chasm_falls}")
    print(f"  • Final Metabolic Energy:       {organism.energy_budget:.1f}")
    print(f"  • Average Epistemic Friction:   {np.mean([h['friction'] for h in history]):.3f}")
    print(f"  • Final Inward Confidence:      {organism.system.inward_observer.self_confidence:.2f}")
    print("=" * 80)

    # Export for Three.js WebGL Interactive Viewer
    export_data = {
        "world": {
            "size": [world.size_x, world.size_y, world.size_z],
            "chasm": [world.chasm_bounds[0], world.chasm_bounds[1]],
            "static_obstacles": world.static_obstacles,
            "beacons": [
                {
                    "pos": [float(b["pos"][0]), float(b["pos"][1]), float(b["pos"][2])],
                    "freq": float(b["frequency"]),
                    "amp": float(b["amplitude"]),
                    "label": b["label"]
                }
                for b in world.beacons
            ]
        },
        "trajectory": history
    }

    with open("genesis_simulation.json", "w") as f:
        json.dump(export_data, f, indent=2)

    print(f"💾 Exported Genesis trajectory to 'genesis_simulation.json'")
    return export_data


if __name__ == "__main__":
    run_genesis_simulation(total_steps=600)
