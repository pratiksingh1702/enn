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

from hyper_cell_world import OrganicWorld3D
from hyper_organism import HumanoidENNOrganism

CHECKPOINT_FILE = "c:/Users/Dell/Downloads/enn/universe_master_checkpoint.json"
FALLBACK_FILE = "c:/Users/Dell/Downloads/enn/preserved_world_state.json"
RESTORE_FILE = CHECKPOINT_FILE if os.path.exists(CHECKPOINT_FILE) else FALLBACK_FILE

world = OrganicWorld3D(restore_file=RESTORE_FILE if os.path.exists(RESTORE_FILE) else None)

# Initialize Dual Autonomous Embodied Humanoids
org_alpha = HumanoidENNOrganism(agent_id="Alpha", initial_pos=(12.24, 21.98, 1.1))
org_beta = HumanoidENNOrganism(agent_id="Beta", initial_pos=(23.54, 21.42, 2.85))

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

simulation_step = 15320
running_time = 20830.0
last_logged_minute = int(running_time // 60)
last_saved_time = running_time
chronicle_log = []

state_lock = threading.Lock()
latest_payload = {}


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

        if self.path == "/api/telepathy":
            target = req_json.get("target", "Alpha")
            msg = req_json.get("message", "Hello")
            if target == "Alpha":
                org_alpha.ingest_telepathy(msg)
            else:
                org_beta.ingest_telepathy(msg)
            
            res_body = json.dumps({"status": "delivered", "target": target, "message": msg}).encode()
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
        global latest_payload, chronicle_log
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
    dt = 0.05  # 20 Hz
    while True:
        t0 = time.time()
        try:
            state_alpha = org_alpha.step(world, dt, other_organism=org_beta)
            state_beta = org_beta.step(world, dt, other_organism=org_alpha)
            world.update_physics(dt)
            
            simulation_step += 1
            running_time += dt

            cur_min = int(running_time // 60)
            is_novel_event = (state_alpha["outcome"] != "walking") or (state_beta["outcome"] != "walking") or (state_alpha.get("vocal_chord") is not None)
            
            if cur_min > last_logged_minute or is_novel_event:
                last_logged_minute = cur_min
                time_str = time.strftime("%H:%M:%S")
                entry = {
                    "minute": cur_min,
                    "step": simulation_step,
                    "time_str": time_str,
                    "alpha": {
                        "action": state_alpha["outcome"],
                        "pos": state_alpha["pos"],
                        "energy": state_alpha["energy"],
                        "ether": state_alpha["ether_harvested"],
                        "walls": state_alpha["structures_built"],
                        "chord": state_alpha.get("vocal_chord")
                    },
                    "beta": {
                        "action": state_beta["outcome"],
                        "pos": state_beta["pos"],
                        "energy": state_beta["energy"],
                        "ether": state_beta["ether_harvested"],
                        "walls": state_beta["structures_built"],
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
                "organisms": [state_alpha, state_beta],
                "organism": state_alpha,
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

        elapsed = time.time() - t0
        sleep_time = max(0.001, dt - elapsed)
        time.sleep(sleep_time)


def run_server():
    server_address = ("0.0.0.0", 8765)
    httpd = ThreadingHTTPServer(server_address, LiveUniverseHandler)
    print("Grand Living Universe Daemon running at http://127.0.0.1:8765 ...")
    httpd.serve_forever()


if __name__ == "__main__":
    sim_thread = threading.Thread(target=simulation_loop, daemon=True)
    sim_thread.start()
    run_server()
