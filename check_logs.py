import urllib.request
import json
import time
import sys

def fetch_and_print():
    sys.stdout.reconfigure(encoding='utf-8')
    try:
        req = urllib.request.urlopen("http://127.0.0.1:8765/api/live_state")
        state = json.loads(req.read().decode())
    except Exception as e:
        print(f"Error fetching live state: {e}")
        return

    print("=" * 80)
    print("👥 DUAL-HUMANOID LIVING UNIVERSE TELEMETRY REPORT")
    print("=" * 80)
    print(f"  • Simulation Step:      {state['step']} ({state.get('running_time', 0.0)} seconds running)")
    print(f"  • Daylight Intensity:   {int(state['sun_intensity'] * 100)}% (Solar Cycle)")
    
    # Organisms
    orgs = state.get("organisms", [state.get("organism")])
    for org in orgs:
        print("-" * 80)
        print(f"🚶‍♂️ ORGANISM: {org.get('id', 'Alpha').upper()} [Energy: {org['energy']:.1f} | Action: {org['outcome'].upper()}]")
        print(f"  • 3D Position:          {org['pos']} (Grounded: {org['is_grounded']})")
        print(f"  • Ground Velocity:      {org['velocity']} m/s")
        print(f"  • Steps Walked:         {org['steps_walked']} bipedal steps")
        print(f"  • Free Ether Harvested: {org['ether_harvested']} ether cells")
        print(f"  • Structures Built:     {org['structures_built']} architectural structures")
        print(f"  • Active Curiosity:     {org['curiosity_focus']}")
        print(f"  • Morphed Powers:       {org.get('morphed_powers', [])}")
        
        enn = org.get("enn_metrics", {})
        print(f"  • 4D Neurons Born:      {enn.get('neurons_born_total', 0)} Concept/Insight Neurons")
        print(f"  • Active Synapses:      {enn.get('synapses_active', 0)} Bridges")
        print(f"  • Inward Flow Conf:     {org['confidence']} / 1.000")

    # Architecture Census
    print("-" * 80)
    cells = state.get("cells", [])
    census = {}
    for c in cells:
        t = c["type"]
        census[t] = census.get(t, 0) + 1
    print(f"📦 ARCHITECTURE & HYPER-CELLS POPULATION ({len(cells)} Total Cells):")
    for t, cnt in census.items():
        print(f"  • {t.upper():<18}: {cnt:>4} cells")

    # Chronicle history
    try:
        req_c = urllib.request.urlopen("http://127.0.0.1:8765/api/chronicle")
        c_data = json.loads(req_c.read().decode())
        chronicle = c_data.get("chronicle", [])
        print("=" * 80)
        print(f"📜 MULTI-AGENT CHRONICLE HISTORY ({len(chronicle)} log entries)")
        print("=" * 80)
        for entry in chronicle[-8:]:
            alpha_info = entry.get("alpha", {})
            beta_info = entry.get("beta", {})
            print(f"  [Min {entry['minute']:02d} | {entry['time_str']} | Step {entry['step']:05d}] Alpha: {alpha_info.get('action', 'N/A'):<22} | Beta: {beta_info.get('action', 'N/A'):<22}")
        print("=" * 80)
    except Exception as e:
        print(f"Error fetching chronicle: {e}")

if __name__ == "__main__":
    fetch_and_print()
