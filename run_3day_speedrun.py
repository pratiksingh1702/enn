"""
3-Day Civilization Speedrunner & Evolutionary Epoch Accelerator
===============================================================
Simulates 3 Full Days (72.0 Simulation Hours = 259,200 seconds)
in headless batch mode with continuous neurogenesis, structural morphogenesis,
and multi-agent architectural expansion.
"""

import time
import json
import sys
import numpy as np
import os
from typing import Dict, Any

from hyper_cell_world import OrganicWorld3D
from hyper_organism import HumanoidENNOrganism

CHECKPOINT_PATH = "c:/Users/Dell/Downloads/enn/universe_master_checkpoint.json"


def run_3day_evolution():
    print("=" * 80, flush=True)
    print("🚀 3-DAY (72.0 SIMULATION HOURS) CIVILIZATION SPEEDRUNNER", flush=True)
    print("=" * 80, flush=True)

    # 1. Initialize World & Organisms from master checkpoint
    world = OrganicWorld3D(restore_file=CHECKPOINT_PATH if os.path.exists(CHECKPOINT_PATH) else None)
    org_alpha = HumanoidENNOrganism(agent_id="Alpha", initial_pos=(12.0, 12.0, 1.1))
    org_beta = HumanoidENNOrganism(agent_id="Beta", initial_pos=(20.0, 20.0, 1.1))

    if os.path.exists(CHECKPOINT_PATH):
        try:
            with open(CHECKPOINT_PATH, "r", encoding="utf-8") as f:
                p_data = json.load(f)
                if "full_organisms" in p_data and len(p_data["full_organisms"]) >= 2:
                    org_alpha.load_from_full_dict(p_data["full_organisms"][0])
                    org_beta.load_from_full_dict(p_data["full_organisms"][1])
                    print(f"✅ Loaded starting brains: Alpha ({len(org_alpha.system.neurons)}N), Beta ({len(org_beta.system.neurons)}N)", flush=True)
        except Exception as e:
            print("Warning loading organisms:", e, flush=True)

    dt = 0.25  # 250ms high-speed physics integration
    org_alpha.saccade_stride = 4
    org_beta.saccade_stride = 4
    
    days = 3
    hours_per_day = 24.0
    steps_per_day = int((hours_per_day * 3600.0) / dt) # 345,600 steps per day

    global_start_time = time.perf_counter()
    initial_cell_count = len(world.cells)

    for day in range(1, days + 1):
        print(f"\n" + "-" * 80, flush=True)
        print(f"🌅 COMMENCING EPOCH: DAY {day}/3 ({hours_per_day} Simulated Hours | {steps_per_day:,} Steps)", flush=True)
        print("-" * 80, flush=True)
        
        day_start_time = time.perf_counter()
        
        for step in range(1, steps_per_day + 1):
            world.update_physics(dt, is_headless=True)
            org_alpha.step(world, dt, other_organism=org_beta, is_headless=True)
            org_beta.step(world, dt, other_organism=org_alpha, is_headless=True)

            # Report every 1,000 steps (~250 seconds of simulation)
            if step % 1000 == 0 or step == steps_per_day:
                now = time.perf_counter()
                elapsed = max(0.001, now - day_start_time)
                raw_hz = step / elapsed
                effective_hz = (step * (dt / 0.05)) / elapsed  # Equivalent 50ms physical clock
                pct = (step / steps_per_day) * 100.0
                sim_hours = (step * dt) / 3600.0
                remaining_steps = steps_per_day - step
                eta_sec = int(remaining_steps / max(1.0, raw_hz))
                
                print(
                    f"  [Day {day}/3 | {pct:5.1f}%] Sim: {sim_hours:4.1f}h / 24h | "
                    f"Speed: {effective_hz:6.0f} Hz ({effective_hz/20.0:4.0f}x Speedup) | "
                    f"ETA: {eta_sec:4d}s | Cells: {len(world.cells)} | "
                    f"Alpha E: {int(org_alpha.energy_budget):5d} | Beta E: {int(org_beta.energy_budget):5d}",
                    flush=True
                )

        day_real_time = time.perf_counter() - day_start_time
        print(f"✅ DAY {day} EPOCH COMPLETE in {day_real_time:.1f} real seconds! Saving checkpoint...", flush=True)
        
        # Save master checkpoint after each day
        payload = {
            "step": world.step_count,
            "running_time": world.sim_time,
            "sim_time": world.sim_time,
            "sun_intensity": world.sun_intensity,
            "weather": world.weather_type,
            "cells": [c.to_dict() for c in world.cells.values()],
            "full_organisms": [org_alpha.to_full_dict(), org_beta.to_full_dict()]
        }
        with open(CHECKPOINT_PATH, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print(f"💾 Checkpoint safely persisted: {len(world.cells)} cells, Alpha {len(org_alpha.system.neurons)}N, Beta {len(org_beta.system.neurons)}N", flush=True)

    total_real_time = time.perf_counter() - global_start_time
    total_sim_hours = days * hours_per_day
    new_cells = len(world.cells) - initial_cell_count

    print("\n" + "=" * 80, flush=True)
    print("🏆 3-DAY EVOLUTIONARY SPEEDRUN FULLY COMPLETE!", flush=True)
    print("=" * 80, flush=True)
    print(f"• Total Simulated Time:    {total_sim_hours:.1f} Hours (3 Full Days)", flush=True)
    print(f"• Total Wall-Clock Time:   {total_real_time:.2f} Real Seconds ({total_real_time/60:.2f} minutes)", flush=True)
    print(f"• Total Physical Steps:    {days * steps_per_day:,} Ticks", flush=True)
    print(f"• Macro Speedup Factor:    {(total_sim_hours * 3600) / total_real_time:.1f}x Faster Than Reality", flush=True)
    print(f"• New Structures Built:    {new_cells} Hyper-Cells", flush=True)
    print(f"• Alpha Brain Size:        {len(org_alpha.system.neurons)} Neurons | {sum(len(n.synapses) for n in org_alpha.system.neurons)} Synapses", flush=True)
    print(f"• Beta Brain Size:         {len(org_beta.system.neurons)} Neurons | {sum(len(n.synapses) for n in org_beta.system.neurons)} Synapses", flush=True)
    print("=" * 80, flush=True)


if __name__ == "__main__":
    run_3day_evolution()
