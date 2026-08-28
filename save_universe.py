"""
ENN Universe Persistent State Preservation & Snapshot Engine
=============================================================
Saves complete state:
- All 380+ Hyper-Cells (Walls, Roofs, Bridges, Shrines, Towers, Crystals, Wood)
- Alpha ENN 4D Brain Substrate (Neurons, Synaptic Weights, Trait Basins, Aspiration)
- Beta ENN 4D Brain Substrate (Neurons, Synaptic Weights, Trait Basins, Aspiration)
- Environmental Sim Time, Daylight, Weather
"""

import json
import os
import sys
import urllib.request

SNAPSHOT_FILE = "c:/Users/Dell/Downloads/enn/universe_master_checkpoint.json"

def save_current_universe():
    sys.stdout.reconfigure(encoding='utf-8')
    try:
        req = urllib.request.urlopen("http://127.0.0.1:8765/api/live_state")
        data = json.loads(req.read().decode())
        
        with open(SNAPSHOT_FILE, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        print(f"UNIVERSE SNAPSHOT SAVED SUCCESSFULLY TO: {SNAPSHOT_FILE}")
        print(f"  • Total Cells Preserved: {len(data.get('cells', []))}")
        print(f"  • Organisms Preserved:   {len(data.get('organisms', []))}")
        print(f"  • Sim Time Preserved:    {data.get('sim_time', 0.0)}s")
        return True
    except Exception as e:
        print(f"Error saving universe snapshot: {e}")
        return False

if __name__ == "__main__":
    save_current_universe()
