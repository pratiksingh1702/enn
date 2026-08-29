"""
Profile inside org_alpha.step to find the exact sub-millisecond line
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

# Let's inspect sub-times inside org_alpha.step
dt = 0.1

t_perception = 0.0
t_brain_step = 0.0
t_spatial_trace = 0.0
t_curiosity = 0.0
t_kinematics = 0.0
t_dict_return = 0.0

for step in range(500):
    with world.cells_lock:
        current_cells = list(world.cells.items())

    is_saccade = (org_alpha.step_counter % org_alpha.saccade_stride == 0)
    org_alpha.step_counter += 1

    head_pos = org_alpha.pos + org_alpha.limbs["head_brain"].offset

    t1 = time.perf_counter()
    if is_saccade or org_alpha._cached_vis_data is None:
        vis_data = world.cast_visual_rays(head_pos, org_alpha.yaw, org_alpha.pitch, other_agent_pos=org_beta.pos, num_azimuth=16, num_elevation=3)
        org_alpha._cached_vis_data = vis_data
    else:
        vis_data = org_alpha._cached_vis_data
    t2 = time.perf_counter()

    # Spatial Trace
    cur_cell = (int(org_alpha.pos[0]), int(org_alpha.pos[1]))
    forward_step_cell = (int(org_alpha.pos[0] + np.cos(org_alpha.yaw) * 1.8), int(org_alpha.pos[1] + np.sin(org_alpha.yaw) * 1.8))
    fwd_trace = org_alpha.spatial_trace_map.get(forward_step_cell, 0.0)
    t3 = time.perf_counter()

    if is_saccade or org_alpha._cached_sensory_wave is None:
        sensory_wave = org_alpha.system.perceive_and_fuse_3d(
            visual_depth_matrix=vis_data["depth_matrix"],
            visual_ray_dirs=vis_data["ray_dirs"],
            sound_pressure=0.0,
            sound_flux_3d=np.zeros(3),
            current_yaw=org_alpha.yaw,
            current_pitch=org_alpha.pitch,
            spatial_trace_val=fwd_trace
        )
        org_alpha._cached_sensory_wave = sensory_wave
        motor = org_alpha.system.reason_3d(sensory_wave)
        org_alpha._cached_motor = motor
    else:
        sensory_wave = org_alpha._cached_sensory_wave
        motor = org_alpha._cached_motor
    t4 = time.perf_counter()

    # Kinematics
    d_yaw = motor["d_yaw"]
    org_alpha.yaw = (org_alpha.yaw + d_yaw) % (2.0 * np.pi)
    forward_dir = np.array([np.cos(org_alpha.yaw), np.sin(org_alpha.yaw), 0.0])
    org_alpha.pos += forward_dir * 1.5 * dt
    t5 = time.perf_counter()

    t_perception += (t2 - t1)
    t_spatial_trace += (t3 - t2)
    t_brain_step += (t4 - t3)
    t_kinematics += (t5 - t4)

print("=" * 60)
print(f"Perception (Visual Rays): {t_perception*1000/500:.3f} ms / step")
print(f"Spatial Trace Map:        {t_spatial_trace*1000/500:.3f} ms / step")
print(f"4D Brain Step & Reason:   {t_brain_step*1000/500:.3f} ms / step")
print(f"Kinematics / Movement:    {t_kinematics*1000/500:.3f} ms / step")
print("=" * 60)
