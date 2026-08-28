"""
Continuous 3D Self-Aware Living Simulation & Validation Harness
===============================================================
Runs continuous 3D physical navigation with:
- Multimodal 360° Vision & Diffractive Sound Waves
- Inward Metacognitive Observer (Epistemic Friction & Self-Confidence)
- Continuous 3D Locomotion & Barrier Detours
- Exports 'simulation_3d.json' for Three.js WebGL Interactive 3D Visualization
"""

import os
import json
import numpy as np
from world_3d import World3D
from agent_3d import SelfAware3DAgent


def run_3d_living_simulation(total_steps: int = 500):
    print("=" * 80)
    print("🧠 LAUNCHING 3D CONTINUOUS SELF-AWARE LIVING ORGANISM SIMULATION")
    print("Zero Hardcoding | Continuous Multimodal Waves (Vision + Sound + Self)")
    print("=" * 80)

    world = World3D(size_x=20.0, size_y=20.0, size_z=6.0)
    agent = SelfAware3DAgent()
    agent.reset(start_pos=(2.0, 2.0, 1.5), energy=300.0)

    history = []
    
    print(f"\n[Environment Setup]")
    print(f"  • World Volume: 20m x 20m x 6m")
    print(f"  • Obstacles: {len(world.obstacles)} volumetric partitions & perimeter walls")
    print(f"  • Acoustic Beacons: {len(world.beacons)} sound emitters (Goal at (17, 17, 2))")
    print(f"  • Initial Organism State: Pos: (2.0, 2.0, 1.5), Energy: 300.0, Confidence: {agent.observer.self_confidence:.2f}")

    print(f"\n[Running Continuous 3D Simulation ({total_steps} steps)]...")

    for step in range(1, total_steps + 1):
        sim_time = step * 0.1
        state = agent.step(world, dt=0.1, sim_time=sim_time)
        
        # Log periodic telemetry
        if step <= 10 or step % 25 == 0 or state["outcome"] in ["goal_harvested", "barrier_collision"]:
            icon = "🎯" if state["outcome"] == "goal_harvested" else ("💥" if state["outcome"] == "barrier_collision" else "🛸")
            pos_str = f"({state['pos'][0]:.1f}, {state['pos'][1]:.1f}, {state['pos'][2]:.1f})"
            print(f"  [Step {step:03d}] {icon} Pos: {pos_str} | Speed: {np.linalg.norm(state['velocity']):.2f}m/s | "
                  f"Friction: {state['epistemic_friction']:.3f} | Confidence: {state['self_confidence']:.2f} | "
                  f"Energy: {state['energy_budget']:.1f} | Goals: {state['goals_harvested']}")

        # Record for WebGL visualization
        history.append({
            "step": step,
            "pos": [float(state["pos"][0]), float(state["pos"][1]), float(state["pos"][2])],
            "velocity": [float(state["velocity"][0]), float(state["velocity"][1]), float(state["velocity"][2])],
            "yaw": float(state["yaw"]),
            "pitch": float(state["pitch"]),
            "thrust": float(state["thrust"]),
            "outcome": state["outcome"],
            "energy": float(state["energy_budget"]),
            "confidence": float(state["self_confidence"]),
            "friction": float(state["epistemic_friction"]),
            "coherence": float(state["body_world_coherence"]),
            "stress": float(state["metabolic_stress"]),
            "closest_obs": float(state["closest_obstacle"]),
            "sound_pressure": float(state["sound_pressure"])
        })

    # Summary Statistics
    print("\n" + "=" * 80)
    print("📊 3D CONTINUOUS SIMULATION TELEMETRY SUMMARY")
    print("=" * 80)
    print(f"  • Total Steps Simulated:      {total_steps}")
    print(f"  • Acoustic Goals Harvested:   {agent.goals_harvested}")
    print(f"  • Wall / Barrier Collisions:  {agent.collisions}")
    print(f"  • Final Metabolic Energy:     {agent.energy_budget:.1f}")
    print(f"  • Final Inward Confidence:    {agent.observer.self_confidence:.2f}")
    print(f"  • Average Epistemic Friction: {np.mean([h['friction'] for h in history]):.3f}")
    print(f"  • Body-World Phase Coherence: {agent.observer.body_world_coherence:.2f}")
    print("=" * 80)

    # Export for Three.js WebGL Interactive 3D Viewer
    export_data = {
        "world": {
            "size": [world.size_x, world.size_y, world.size_z],
            "obstacles": [
                {
                    "min": [float(o.min_pt[0]), float(o.min_pt[1]), float(o.min_pt[2])],
                    "max": [float(o.max_pt[0]), float(o.max_pt[1]), float(o.max_pt[2])],
                    "label": o.label
                }
                for o in world.obstacles
            ],
            "beacons": [
                {
                    "pos": [float(b.pos[0]), float(b.pos[1]), float(b.pos[2])],
                    "freq": float(b.frequency),
                    "amp": float(b.amplitude),
                    "label": b.label
                }
                for b in world.beacons
            ]
        },
        "trajectory": history
    }

    with open("simulation_3d.json", "w") as f:
        json.dump(export_data, f, indent=2)
        
    print(f"💾 Exported continuous 3D simulation trajectory to 'simulation_3d.json'")
    return export_data


if __name__ == "__main__":
    run_3d_living_simulation(total_steps=500)
