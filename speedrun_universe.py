"""
Headless Universe Speedrunning Engine (Engine 1)
================================================
Runs pure continuous physical simulation and ENN 4D neurogenesis in headless
batch mode at 1,000Hz to 5,000Hz on laptop CPU without WebGL rendering overhead.
Compresses hours of multi-agent evolution into minutes!
"""

import time
import json
import sys
import numpy as np
import os
from typing import Dict, Any, Optional

from hyper_cell_world import OrganicWorld3D
from hyper_organism import HumanoidENNOrganism

DEFAULT_CHECKPOINT = "c:/Users/Dell/Downloads/enn/universe_master_checkpoint.json"


def run_speedrun_simulation(target_sim_hours: float = 1.0, 
                            checkpoint_path: str = DEFAULT_CHECKPOINT, 
                            save_output: bool = True) -> Dict[str, Any]:
    print("=" * 80, flush=True)
    print(f"⚡ HEADLESS UNIVERSE SPEEDRUNNER (ENGINE 1)", flush=True)
    print(f"• Target Simulation Time: {target_sim_hours:.2f} Hours ({target_sim_hours * 3600:.0f} Simulation Seconds)", flush=True)
    print("=" * 80, flush=True)

    # 1. Initialize World & Organisms
    world = OrganicWorld3D(restore_file=checkpoint_path if os.path.exists(checkpoint_path) else None)
    org_alpha = HumanoidENNOrganism(agent_id="Alpha", initial_pos=(12.0, 12.0, 1.1))
    org_beta = HumanoidENNOrganism(agent_id="Beta", initial_pos=(20.0, 20.0, 1.1))

    # Restore organisms from checkpoint
    if os.path.exists(checkpoint_path):
        try:
            with open(checkpoint_path, "r", encoding="utf-8") as f:
                p_data = json.load(f)
                if "full_organisms" in p_data and len(p_data["full_organisms"]) >= 2:
                    org_alpha.load_from_full_dict(p_data["full_organisms"][0])
                    org_beta.load_from_full_dict(p_data["full_organisms"][1])
                    print(f"✅ Loaded starting brains: Alpha ({len(org_alpha.system.neurons)}N), Beta ({len(org_beta.system.neurons)}N)")
        except Exception as e:
            print("Warning loading organisms:", e)

    dt = 0.05  # 50ms per step
    total_steps = int((target_sim_hours * 3600.0) / dt)
    print(f"• Total Steps to Execute: {total_steps:,} ticks at max compute speed...")

    initial_cells_count = len(world.cells)
    initial_alpha_built = org_alpha.structures_built
    initial_beta_built = org_beta.structures_built

    t_start = time.perf_counter()
    last_report_time = t_start

    # Headless 1000Hz+ compute loop
    for step in range(1, total_steps + 1):
        world.update_physics(dt)
        org_alpha.step(world, dt, other_organism=org_beta)
        org_beta.step(world, dt, other_organism=org_alpha)

        # Progress reporting every 2,000 steps
        if step % 2000 == 0 or step == total_steps:
            now = time.perf_counter()
            elapsed_real = max(0.001, now - t_start)
            sim_time_sec = step * dt
            hz = step / elapsed_real
            speedup_factor = (sim_time_sec) / elapsed_real
            
            print(f"  [Step {step:>7,}/{total_steps:,}] "
                  f"Sim: {sim_time_sec/3600:.2f}h | "
                  f"Real: {elapsed_real:.1f}s | "
                  f"Speed: {hz:>6.0f} Hz ({speedup_factor:.1f}x Real-Time) | "
                  f"Cells: {len(world.cells)} | "
                  f"Alpha Energy: {org_alpha.energy_budget:.0f}", flush=True)

    total_real_time = time.perf_counter() - t_start
    final_cells_count = len(world.cells)
    new_cells_built = final_cells_count - initial_cells_count

    print("\n" + "=" * 80)
    print("🏁 SPEEDRUN SIMULATION EPOCH COMPLETE!")
    print("=" * 80)
    print(f"• Simulated Time:       {target_sim_hours:.2f} Hours")
    print(f"• Real Wall-Clock Time: {total_real_time:.2f} Seconds ({total_steps/total_real_time:.0f} Hz Avg)")
    print(f"• Speedup Multiplier:   {(target_sim_hours * 3600) / total_real_time:.1f}x Faster Than Real-Time!")
    print(f"• New Structures Built: {new_cells_built} Hyper-Cells")
    print(f"• Alpha Brain Size:     {len(org_alpha.system.neurons)} Neurons | {sum(len(n.synapses) for n in org_alpha.system.neurons)} Synapses")
    print(f"• Beta Brain Size:      {len(org_beta.system.neurons)} Neurons | {sum(len(n.synapses) for n in org_beta.system.neurons)} Synapses")

    if save_output:
        # Save back to master checkpoint so live universe daemon picks up the evolved state!
        payload = {
            "step": total_steps,
            "running_time": world.sim_time,
            "sim_time": world.sim_time,
            "sun_intensity": world.sun_intensity,
            "weather": world.weather_type,
            "cells": [c.to_dict() for c in world.cells.values()],
            "full_organisms": [org_alpha.to_full_dict(), org_beta.to_full_dict()]
        }
        with open(checkpoint_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print(f"💾 Checkpoint updated at: {checkpoint_path}")

    return {
        "sim_hours": target_sim_hours,
        "real_seconds": total_real_time,
        "hz": total_steps / total_real_time,
        "new_cells": new_cells_built
    }

if __name__ == "__main__":
    hours = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    run_speedrun_simulation(target_sim_hours=hours)
