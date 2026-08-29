"""
Profile exact bottlenecks in step execution
"""
import time
import json
import numpy as np
from hyper_cell_world import OrganicWorld3D
from hyper_organism import HumanoidENNOrganism

world = OrganicWorld3D(restore_file="c:/Users/Dell/Downloads/enn/universe_master_checkpoint.json")
org_alpha = HumanoidENNOrganism(agent_id="Alpha", initial_pos=(12.0, 12.0, 1.1))
org_beta = HumanoidENNOrganism(agent_id="Beta", initial_pos=(20.0, 20.0, 1.1))

with open("c:/Users/Dell/Downloads/enn/universe_master_checkpoint.json", "r") as f:
    p_data = json.load(f)
    if "full_organisms" in p_data and len(p_data["full_organisms"]) >= 2:
        org_alpha.load_from_full_dict(p_data["full_organisms"][0])
        org_beta.load_from_full_dict(p_data["full_organisms"][1])

print(f"Loaded {len(world.cells)} cells, Alpha {len(org_alpha.system.neurons)}N, Beta {len(org_beta.system.neurons)}N")

# Profile 500 steps
dt = 0.1
t0 = time.perf_counter()

t_world = 0.0
t_alpha = 0.0
t_beta = 0.0

for i in range(500):
    ta = time.perf_counter()
    world.update_physics(dt, is_headless=True)
    tb = time.perf_counter()
    org_alpha.step(world, dt, other_organism=org_beta, is_headless=True)
    tc = time.perf_counter()
    org_beta.step(world, dt, other_organism=org_alpha, is_headless=True)
    td = time.perf_counter()
    
    t_world += (tb - ta)
    t_alpha += (tc - tb)
    t_beta += (td - tc)

total_t = time.perf_counter() - t0
hz = 500 / total_t

print("=" * 60)
print(f"Total time for 500 steps: {total_t*1000:.2f} ms ({hz:.1f} Hz)")
print(f"  • world.update_physics: {t_world*1000/500:.3f} ms / step ({t_world/total_t*100:.1f}%)")
print(f"  • org_alpha.step:       {t_alpha*1000/500:.3f} ms / step ({t_alpha/total_t*100:.1f}%)")
print(f"  • org_beta.step:        {t_beta*1000/500:.3f} ms / step ({t_beta/total_t*100:.1f}%)")
print("=" * 60)
