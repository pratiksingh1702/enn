import sys
import io
import json
import urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def dump_proofs():
    # 1. Fetch raw live state JSON from HTTP server
    raw_state_bytes = urllib.request.urlopen('http://127.0.0.1:8765/api/live_state').read()
    raw_state = json.loads(raw_state_bytes.decode('utf-8'))
    
    # 2. Fetch raw chronicle JSON from HTTP server
    raw_cron_bytes = urllib.request.urlopen('http://127.0.0.1:8765/api/chronicle').read()
    raw_cron = json.loads(raw_cron_bytes.decode('utf-8'))

    print("================================================================================")
    print("RAW UNEDITED TELEMETRY LOG PROOFS FROM LIVE RUNNING SERVER (PORT 8765)")
    print("================================================================================")
    
    # Print instantaneous snapshot
    print("\n--- [PROOF 1: LIVE INSTANTANEOUS WORLD & BRAIN SNAPSHOT] ---")
    summary_snapshot = {
        "step": raw_state["step"],
        "elapsed_seconds": raw_state["elapsed_sec"],
        "daylight_sun_intensity": raw_state["sun_intensity"],
        "organism_kinematics": {
            "position_3d": raw_state["organism"]["pos"],
            "velocity_3d": raw_state["organism"]["velocity"],
            "yaw_rad": raw_state["organism"]["yaw"],
            "pitch_rad": raw_state["organism"]["pitch"],
            "gait_stride_phase": raw_state["organism"]["gait_phase"],
            "is_grounded_on_terrain": raw_state["organism"]["is_grounded"],
            "total_bipedal_steps": raw_state["organism"]["steps_walked"],
            "action_outcome": raw_state["organism"]["outcome"]
        },
        "somatic_anatomy_schema": raw_state["organism"]["anatomy"],
        "inward_metacognitive_gauges": {
            "self_confidence": raw_state["organism"]["confidence"],
            "epistemic_friction": raw_state["organism"]["friction"],
            "body_world_coherence": raw_state["organism"]["coherence"],
            "metabolic_energy": raw_state["organism"]["energy"],
            "ether_harvested": raw_state["organism"]["ether_harvested"],
            "structures_built": raw_state["organism"]["structures_built"],
            "cells_morphed": raw_state["organism"]["cells_morphed"]
        },
        "enn_4d_brain_metrics": raw_state["organism"]["enn_metrics"]
    }
    print(json.dumps(summary_snapshot, indent=2))

    print("\n--- [PROOF 2: VERBATIM MINUTE-BY-MINUTE CHRONICLE LOGS] ---")
    print(f"Total Logged Historical Milestones: {len(raw_cron['chronicle'])}")
    for i, event in enumerate(raw_cron["chronicle"], 1):
        print(f"  Log #{i:02d} | [Min {event['minute']:02d} @ {event['time_str']} | Step {event['step']:05d}] "
              f"Action: {event['action']:<26} | Pos: {str(event['pos']):<20} | Energy: {event['energy']:<7} | "
              f"Ether: {event['ether_harvested']} | Walls: {event['structures_built']} | Somatic Limbs: {event['somatic_cells']}")

    print("\n--- [PROOF 3: LIVE HYPER-CELLS POPULATION IN VIRTUAL MEADOW] ---")
    print(f"Total Active Hyper-Cells in World: {len(raw_state['cells'])}")
    cell_types_count = {}
    for c in raw_state["cells"]:
        cell_types_count[c["type"]] = cell_types_count.get(c["type"], 0) + 1
    print("Cell Census:", cell_types_count)
    print("Sample 5 Hyper-Cells in World Coordinates:")
    for c in raw_state["cells"][:5]:
        print(" ", c)
    print("================================================================================")

if __name__ == "__main__":
    dump_proofs()
