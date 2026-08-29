"""
Grand Living Universe Daemon with Auto-Recovery & Auto-Save
============================================================
- Dual Embodied Humanoids + Wildlife Fauna + Weather
- Thread-safe non-blocking simulation loop on port 8765
- Automatic State Recovery & Auto-Saving every 30 seconds
"""

import time
import json
import threading
from http.server import HTTPServer, ThreadingHTTPServer, BaseHTTPRequestHandler
import os
from typing import List, Tuple, Optional, Dict, Any
import numpy as np

from hyper_cell_world import OrganicWorld3D
from hyper_organism import HumanoidENNOrganism
from semantic_imprinter import SemanticImprinter

imprinter = SemanticImprinter()

CHECKPOINT_FILE = "c:/Users/Dell/Downloads/enn/universe_master_checkpoint.json"
FALLBACK_FILE = "c:/Users/Dell/Downloads/enn/preserved_world_state.json"
RESTORE_FILE = CHECKPOINT_FILE if os.path.exists(CHECKPOINT_FILE) else FALLBACK_FILE

world = OrganicWorld3D(size_x=64.0, size_y=64.0, max_height=18.0, restore_file=RESTORE_FILE if os.path.exists(RESTORE_FILE) else None)

# Initialize Dual Autonomous Embodied Humanoids
org_alpha = HumanoidENNOrganism(agent_id="Alpha", initial_pos=(16.24, 28.98, 2.1))
org_beta = HumanoidENNOrganism(agent_id="Beta", initial_pos=(48.54, 28.42, 2.85))

if os.path.exists(RESTORE_FILE):
    try:
        with open(RESTORE_FILE, "r", encoding='utf-8') as f:
            p_data = json.load(f)
            
            # Check for full neural brain serialization first
            if "full_organisms" in p_data and len(p_data["full_organisms"]) >= 2:
                org_alpha.load_from_full_dict(p_data["full_organisms"][0])
                org_beta.load_from_full_dict(p_data["full_organisms"][1])
                print(f"Restored full ENN 4D neural networks: Alpha ({len(org_alpha.system.neurons)} neurons) & Beta ({len(org_beta.system.neurons)} neurons)!")
            else:
                orgs = p_data.get("organisms", [p_data.get("organism", {})])
                if len(orgs) > 0 and orgs[0]:
                    saved_a = orgs[0]
                    org_alpha.energy_budget = float(saved_a.get("energy", 14700.0))
                    org_alpha.ether_harvested = int(saved_a.get("ether_harvested", 440))
                    org_alpha.structures_built = int(saved_a.get("structures_built", 293))
                    for p in saved_a.get("morphed_powers", []):
                        org_alpha.morphed_powers.add(p)
                if len(orgs) > 1 and orgs[1]:
                    saved_b = orgs[1]
                    org_beta.energy_budget = float(saved_b.get("energy", 332.0))
                    org_beta.ether_harvested = int(saved_b.get("ether_harvested", 3))
                    org_beta.structures_built = int(saved_b.get("structures_built", 2))
                    for p in saved_b.get("morphed_powers", []):
                        org_beta.morphed_powers.add(p)
                print("Restored Alpha and Beta states successfully!")
    except Exception as e:
        print("Error restoring stats:", e)

# Ensure both have their 9 powers unlocked
for p in ['matter_alchemy', 'resonance_crown', 'terra_sculpt', 'kinetic_shield', 'quantum_dash', 'solar_core', 'tractor_hands', 'aero_wings', 'flora_bloom']:
    org_alpha.morphed_powers.add(p)
    org_beta.morphed_powers.add(p)

org_alpha.has_wings = True
org_alpha.has_shield = True
org_alpha.hand_reach = 5.0
org_beta.has_wings = True
org_beta.has_shield = True
org_beta.hand_reach = 5.0

# Multi-Agent Humanoid Swarm Registry
GREEK_NAMES = [
    "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa", 
    "Lambda", "Mu", "Nu", "Xi", "Omicron", "Pi", "Rho", "Sigma", 
    "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega"
]

organisms: List[HumanoidENNOrganism] = [org_alpha, org_beta]
organisms_lock = threading.Lock()

def spawn_additional_humanoid(name: Optional[str] = None, pos: Optional[Tuple[float, float, float]] = None) -> HumanoidENNOrganism:
    with organisms_lock:
        idx = len(organisms)
        if not name:
            if idx - 2 < len(GREEK_NAMES):
                name = GREEK_NAMES[idx - 2]
            else:
                name = f"Humanoid_{idx + 1}"
                
        if pos is None:
            sx = float(np.random.uniform(8.0, world.size_x - 8.0))
            sy = float(np.random.uniform(8.0, world.size_y - 8.0))
            sz = world.get_terrain_height(sx, sy) + 1.2
            pos = (sx, sy, sz)
            
        org = HumanoidENNOrganism(agent_id=name, initial_pos=pos)
        for p in ['matter_alchemy', 'resonance_crown', 'terra_sculpt', 'kinetic_shield', 'quantum_dash', 'solar_core', 'tractor_hands', 'aero_wings', 'flora_bloom']:
            org.morphed_powers.add(p)
        org.has_wings = True
        org.has_shield = True
        org.hand_reach = 4.5
        org.energy_budget = 650.0
        
        organisms.append(org)
        print(f"🌟 Spawned Humanoid Organism {name} at position [{pos[0]:.1f}, {pos[1]:.1f}, {pos[2]:.1f}] (Total Population: {len(organisms)})")
        return org

# Automatically spawn 20 additional humanoids (Total: 22 living humanoids)
print("🚀 Spawning 20 additional embodied humanoids into 64x64 living universe...")
for _ in range(20):
    spawn_additional_humanoid()

simulation_step = 15320
running_time = 20830.0
last_logged_minute = int(running_time // 60)
last_saved_time = running_time
chronicle_log = []

state_lock = threading.Lock()
latest_payload = {}


def generate_genesis_snapshot():
    """Generates the true initial state of the world at Step 0."""
    primordial_world = OrganicWorld3D(size_x=64.0, size_y=64.0, max_height=18.0)
    primordial_world.cells.clear()
    
    # Initial house foundation
    ground_center = primordial_world.get_terrain_height(16.0, 16.0)
    for x in range(14, 19):
        for y in range(14, 19):
            is_wall = (x == 14 or x == 18 or y == 14 or y == 18)
            is_door = (x == 16 and y == 18)
            if is_wall and not is_door:
                for z_lvl in range(1, 4):
                    z_pos = ground_center + z_lvl * 0.9
                    primordial_world.spawn_cell((float(x), float(y), z_pos), cell_type="matter_wall", energy=10.0)
            primordial_world.spawn_cell((float(x), float(y), ground_center + 3.7), cell_type="matter_wood", energy=10.0)
            
    # 25 ether and 16 stones
    for _ in range(25):
        primordial_world._spawn_random_ether()
    for _ in range(16):
        primordial_world._spawn_random_stone()
        
    cells_data = [c.to_dict() for c in primordial_world.cells.values()]
    
    alpha_genesis = {
        "id": "Alpha",
        "pos": [12.0, 12.0, 1.8],
        "velocity": [0.0, 0.0, 0.0],
        "yaw": 0.0,
        "pitch": 0.0,
        "gait_phase": 0.0,
        "is_grounded": True,
        "outcome": "primordial_awakening",
        "curiosity_focus": "Genesis: Awakening into barren meadow...",
        "vocal_chord": None,
        "morphed_powers": [],
        "reward": 0.0,
        "energy": 350.0,
        "ether_harvested": 0,
        "structures_built": 0,
        "cells_morphed": 0,
        "steps_walked": 0,
        "confidence": 0.5,
        "friction": 0.5,
        "coherence": 1.0,
        "anatomy": [],
        "enn_metrics": {
            "neurons_born_total": 10,
            "synapses_active": 16,
            "synapses_pruned_total": 0,
            "aspiration_level": 0.5,
            "starvation_stress": 0.0,
            "meta_learning_rate": 0.01,
            "active_basin": "Primordial State",
            "trait_pulls": {}
        }
    }
    
    beta_genesis = {
        "id": "Beta",
        "pos": [20.0, 20.0, 1.8],
        "velocity": [0.0, 0.0, 0.0],
        "yaw": 3.14,
        "pitch": 0.0,
        "gait_phase": 0.0,
        "is_grounded": True,
        "outcome": "primordial_awakening",
        "curiosity_focus": "Genesis: Awakening into barren meadow...",
        "vocal_chord": None,
        "morphed_powers": [],
        "reward": 0.0,
        "energy": 350.0,
        "ether_harvested": 0,
        "structures_built": 0,
        "cells_morphed": 0,
        "steps_walked": 0,
        "confidence": 0.5,
        "friction": 0.5,
        "coherence": 1.0,
        "anatomy": [],
        "enn_metrics": {
            "neurons_born_total": 10,
            "synapses_active": 16,
            "synapses_pruned_total": 0,
            "aspiration_level": 0.5,
            "starvation_stress": 0.0,
            "meta_learning_rate": 0.01,
            "active_basin": "Primordial State",
            "trait_pulls": {}
        }
    }
    
    return {
        "step": 0,
        "sim_time": 0.0,
        "sun_intensity": 1.0,
        "weather": "clear",
        "cells": cells_data,
        "organisms": [alpha_genesis, beta_genesis],
        "fauna": [{"id": f.id, "type": f.fauna_type, "pos": f.pos.tolist()} for f in primordial_world.fauna],
        "is_genesis": True
    }

cached_genesis_payload = generate_genesis_snapshot()


class LiveUniverseHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_POST(self):
        global org_alpha, org_beta, world
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            req_json = json.loads(post_data.decode('utf-8'))
        except Exception:
            req_json = {}

        if self.path == "/api/spawn_humanoids":
            count = int(req_json.get("count", 1))
            count = max(1, min(count, 50))
            spawned_names = []
            for _ in range(count):
                new_org = spawn_additional_humanoid()
                spawned_names.append(new_org.agent_id)
            
            res_body = json.dumps({
                "status": "success",
                "spawned_count": len(spawned_names),
                "total_organisms": len(organisms),
                "names": spawned_names
            }).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(res_body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(res_body)

        elif self.path == "/api/telepathy":
            target = req_json.get("target", "Alpha")
            msg = req_json.get("message", "Hello")
            with organisms_lock:
                target_org = next((o for o in organisms if o.agent_id.lower() == target.lower()), organisms[0] if organisms else None)
            if target_org:
                target_org.ingest_telepathy(msg)
            
            res_body = json.dumps({"status": "delivered", "target": target, "message": msg}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(res_body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(res_body)

        elif self.path == "/api/imprint_knowledge":
            target = req_json.get("target", "Alpha")
            text = req_json.get("text", "")
            topic = req_json.get("topic", "Concept")
            with organisms_lock:
                target_org = next((o for o in organisms if o.agent_id.lower() == target.lower()), organisms[0] if organisms else None)
            
            res = imprinter.imprint_into_enn(target_org.system.world_field, text, topic) if target_org else {"status": "error"}
            res_body = json.dumps(res).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(res_body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(res_body)

        elif self.path == "/api/jarvis_chat":
            target = req_json.get("target", "Alpha")
            prompt = req_json.get("prompt", "")
            with organisms_lock:
                target_org = next((o for o in organisms if o.agent_id.lower() == target.lower()), organisms[0] if organisms else None)
            
            if not target_org:
                target_org = org_alpha
                
            # 4D Semantic Resonance Query over Memory Graph
            wf = target_org.system.world_field
            dom_id = imprinter._determine_domain_family(prompt)
            sem_vec = imprinter._text_to_4d_vector(prompt, domain_id=dom_id, depth=0)
            forces = wf.compute_resonance(sem_vec, sem_vec, np.zeros(4))
            
            top_memories = []
            if len(forces) > 0:
                top_indices = np.argsort(forces)[::-1][:6]
                for idx in top_indices:
                    if forces[idx] > 0.12 and wf.neurons[idx].text:
                        top_memories.append(wf.neurons[idx].text)
            
            winning_basin, conf, _ = target_org.system.trait_field.collapse_phase(sem_vec)
            trait_name = winning_basin.name if winning_basin else "INQUIRE"
            
            # Synthesize Companion Response
            if top_memories:
                resp = f"[{trait_name.upper()}] Resonating with '{top_memories[0]}'. My 4D brain connects your inquiry to {', '.join(top_memories[:3])}. We are expanding this living knowledge graph together!"
            else:
                resp = f"[{trait_name.upper()}] I have received '{prompt}' into my cognitive field. No prior memories matched this directly, so I have birthed an epistemic tension vector to learn it with you!"
                
            res_body = json.dumps({
                "response": resp,
                "trait": trait_name,
                "confidence": round(float(conf), 3),
                "resonant_memories": top_memories,
                "total_neurons": len(wf.neurons),
                "total_synapses": sum(len(n.synapses) for n in wf.neurons)
            }).encode()
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(res_body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(res_body)

        elif self.path == "/api/spawn_matter":
            x = float(req_json.get("x", 16.0))
            y = float(req_json.get("y", 16.0))
            meteor = world.spawn_celestial_meteor(x, y)
            res_body = json.dumps({"status": "spawned", "cell": meteor.to_dict()}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(res_body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(res_body)

        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        global latest_payload, chronicle_log, org_alpha, org_beta
        if self.path == "/api/live_state":
            with state_lock:
                data_str = json.dumps(latest_payload)
            body = data_str.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)

        elif self.path.startswith("/api/organism_brain"):
            query_id = "Alpha"
            if "?" in self.path:
                from urllib.parse import parse_qs, urlparse
                params = parse_qs(urlparse(self.path).query)
                query_id = params.get("id", ["Alpha"])[0]
                
            target_org = None
            with organisms_lock:
                for org in organisms:
                    if org.agent_id.lower() == query_id.lower():
                        target_org = org
                        break
                if target_org is None and organisms:
                    target_org = organisms[0]
            
            wf = target_org.system.world_field
            neurons_data = []
            for idx, n in enumerate(wf.neurons):
                neurons_data.append({
                    "id": idx,
                    "x": [round(float(v), 4) for v in n.x],
                    "y": [round(float(v), 4) for v in n.y],
                    "z": [round(float(v), 4) for v in n.z],
                    "w": int(n.w),
                    "text": str(n.text),
                    "role": str(n.role),
                    "energy": round(float(n.energy), 3),
                    "age": int(n.age),
                    "synapses": {str(k): round(float(v), 4) for k, v in n.synapses.items()}
                })
            
            prototypes = wf.get_all_family_prototypes()
            proto_data = {str(k): [round(float(v), 4) for v in val] for k, val in prototypes.items()}
            
            brain_payload = {
                "organism_id": target_org.agent_id,
                "neurons_count": len(neurons_data),
                "synapses_count": sum(len(n["synapses"]) for n in neurons_data),
                "neurons": neurons_data,
                "family_prototypes": proto_data
            }
            body = json.dumps(brain_payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)

        elif self.path == "/api/chronicle":
            with state_lock:
                data_str = json.dumps({"chronicle": chronicle_log})
            body = data_str.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)

        elif self.path == "/api/genesis_state":
            body = json.dumps(cached_genesis_payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)

        elif self.path in ["/", "/index.html"]:
            try:
                with open("live_dashboard.html", "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error loading dashboard: {e}".encode())
        else:
            self.send_response(404)
            self.end_headers()


def simulation_loop():
    global simulation_step, running_time, last_logged_minute, last_saved_time, latest_payload, chronicle_log
    dt = 0.01  # 100 Hz Simulation Frequency
    while True:
        t0 = time.time()
        try:
            with organisms_lock:
                current_orgs = list(organisms)
                
            num_orgs = len(current_orgs)
            org_states = []
            
            # Execute 20 substeps per frame for true 100 Hz physics
            for sub in range(20):
                frame_states = []
                for idx, org in enumerate(current_orgs):
                    other = current_orgs[(idx + 1) % num_orgs] if num_orgs > 1 else None
                    s = org.step(world, dt, other_organism=other)
                    frame_states.append(s)
                world.update_physics(dt)
                simulation_step += 1
                running_time += dt
                if sub == 3:
                    org_states = frame_states

            cur_min = int(running_time // 60)
            state_alpha = org_states[0] if len(org_states) > 0 else {}
            state_beta = org_states[1] if len(org_states) > 1 else {}
            
            is_novel_event = (state_alpha.get("outcome") != "walking") or (state_beta.get("outcome") != "walking")
            
            if cur_min > last_logged_minute or is_novel_event:
                last_logged_minute = cur_min
                time_str = time.strftime("%H:%M:%S")
                entry = {
                    "minute": cur_min,
                    "step": simulation_step,
                    "time_str": time_str,
                    "population": num_orgs,
                    "alpha": {
                        "action": state_alpha.get("outcome", "idle"),
                        "pos": state_alpha.get("pos", [0, 0, 0]),
                        "energy": state_alpha.get("energy", 0),
                        "ether": state_alpha.get("ether_harvested", 0),
                        "walls": state_alpha.get("structures_built", 0),
                        "chord": state_alpha.get("vocal_chord")
                    },
                    "beta": {
                        "action": state_beta.get("outcome", "idle"),
                        "pos": state_beta.get("pos", [0, 0, 0]),
                        "energy": state_beta.get("energy", 0),
                        "ether": state_beta.get("ether_harvested", 0),
                        "walls": state_beta.get("structures_built", 0),
                        "chord": state_beta.get("vocal_chord")
                    }
                }
                with state_lock:
                    chronicle_log.append(entry)
                    if len(chronicle_log) > 300:
                        chronicle_log.pop(0)

            with world.cells_lock:
                cells_data = [c.to_dict() for c in world.cells.values()]
                
            fauna_data = [f.to_dict() for f in world.fauna]
            payload = {
                "step": simulation_step,
                "running_time": round(running_time, 1),
                "sim_time": round(world.sim_time, 1),
                "sun_intensity": round(world.sun_intensity, 2),
                "weather": world.weather_type,
                "organisms": org_states,
                "organism": org_states[0] if org_states else {},
                "cells": cells_data,
                "fauna": fauna_data
            }

            with state_lock:
                latest_payload = payload

            # Continuous Auto-Save every 30 seconds
            if running_time - last_saved_time >= 30.0:
                last_saved_time = running_time
                try:
                    save_data = dict(payload)
                    save_data["full_organisms"] = [org_alpha.to_full_dict(), org_beta.to_full_dict()]
                    with open(CHECKPOINT_FILE, "w", encoding='utf-8') as f:
                        json.dump(save_data, f, indent=2)
                except Exception as ex:
                    print("Auto-save exception:", ex)

        except Exception as e:
            print("Recovered from simulation tick exception:", e)

        time.sleep(0.001)


def run_server():
    server_address = ("0.0.0.0", 8765)
    httpd = ThreadingHTTPServer(server_address, LiveUniverseHandler)
    print("Grand Living Universe Daemon running at http://127.0.0.1:8765 ...")
    httpd.serve_forever()


if __name__ == "__main__":
    sim_thread = threading.Thread(target=simulation_loop, daemon=True)
    sim_thread.start()
    run_server()
